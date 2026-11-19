# The queue of patients. Shared by the Register, Next Patient and Queuing List cards.
# (Not named "queue.py" because Python already has a module called queue.)
import json
import heapq

PRIORITIES = ["regular", "priority", "emergency"]
RANK = {"emergency": 1, "priority": 2, "regular": 3}      # who goes first (0 = first)
PREFIX = {"emergency": "E", "priority": "P", "regular": "R"}   # E-0001, P-0001, R-0001

class PatientQueue:
    def __init__(self):
        self.patients = []
        self.counters = {p: 0 for p in PRIORITIES}
        self.ticket = 0
        self.listeners = []
        self.archive = []
        try:
            with open("data/patient_list.json", "r", encoding="utf-8") as patient_list:
                data = json.load(patient_list)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
                print("Could not read file")
        else:
            if len(data) != 3:
                self.savefile()
            else:
                self.ticket = data[0]
                self.counters = data[1]
                self.patients = [tuple(x) for x in data[2]]

        try:
            with open("data/patient_archive.json", "r", encoding="utf-8") as patient_archive:
                data2 = json.load(patient_archive)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            print("Could not read file")
        else:
            self.archive = data2
        self.subscribe(self.savefile)
        heapq.heapify(self.patients)

    # the cards call subscribe(function) so they refresh when the queue changes
    def subscribe(self, function):
        self.listeners.append(function)

    def _notify(self):
        for function in self.listeners:
            function()

    def enqueue(self, name, age, priority, condition=""):
        self.counters[priority] += 1
        self.ticket += 1
        patient = {"id": "%s-%04d" % (PREFIX[priority], self.counters[priority]),
                   "name": name, "age": age, "priority": priority, "condition": condition}
        heapq.heappush(self.patients, (RANK[priority], self.ticket, patient)) # emergency first, then priority, then regular. Same priority = first come first served
        self._notify()
        return patient

    def dequeue(self):
        self.archive_patient()
        heapq.heappop(self.patients)
        self._notify()

    def peek(self):
        return self.patients[0][2] if self.patients else None

    def isEmpty(self):
        return len(self.patients) == 0

    def size(self):
        return len(self.patients)

    def __len__(self):
        return len(self.patients)
    
    def has(self, name, age):
        return any(p["name"].lower() == name.lower() and p["age"] == age for p in [sublist[2] for sublist in self.patients])

    # rows for the table: (queuing no, patient id, name, age, priority)
    def rows(self, limit=None):
        temp = self.patients.copy()
        patients = []
        while temp:
            pid = heapq.heappop(temp)[2]
            patients.append(pid)
        return [(str(i + 1), p["id"], p["name"], p["age"] or "-", p["priority"].capitalize())
                for i, p in enumerate(patients)]

    # rows for the table: (queuing no, patient id, name, age, priority, consulted
    def archive_rows(self, limit=None):
        patients = self.archive if limit is None else self.archive[:limit]
        return [(str(i + 1), p["id"], p["name"], p["age"] or "-", p["priority"].capitalize(), p["consulted"])
                for i, p in enumerate(patients)]

    # saves current queue of patients into patient_list.json file in the data folder
    def savefile(self):
        try:
            with open("data/patient_list.json", "w") as final:
                json.dump([self.ticket,self.counters,self.patients], final, indent=4)
        except OSError as e:
            print("Could not save records:", e)

    # archives the patient that'll be removed from the queue
    def archive_patient(self):
        self.archive.append(self.peek())

        # saves current archive list into patient_archive.json file in the data folder
        try:
            with open("data/patient_archive.json", "w") as final:
                json.dump(self.archive, final, indent=4)
        except OSError as e:
            print("Could not save records:", e)