# The queue of patients. Shared by the Register, Next Patient and Queuing List cards.
# (Not named "queue.py" because Python already has a module called queue.)
import json

PRIORITIES = ["regular", "priority", "emergency"]
RANK = {"emergency": 0, "priority": 1, "regular": 2}      # who goes first (0 = first)
PREFIX = {"emergency": "E", "priority": "P", "regular": "R"}   # E-0001, P-0001, R-0001

class PatientQueue:
    def __init__(self):
        self.patients = []
        self.counters = {p: 0 for p in PRIORITIES}
        self.ticket = 0
        self.listeners = []

        try:
            with open("data/patient_list.json", "r", encoding="utf-8") as patient_list:
                data = json.load(patient_list)
        except FileNotFoundError:
            self.savefile()
        except json.JSONDecodeError:
            self.savefile()
        else:
            if len(data) != 3:
                self.savefile()
            else:
                self.ticket = data[0]
                self.counters = data[1]
                self.patients = data[2]
        self.subscribe(self.savefile)

    # the cards call subscribe(function) so they refresh when the queue changes
    def subscribe(self, function):
        self.listeners.append(function)

    def _notify(self):
        print(self.counters)
        for function in self.listeners:
            function()
        

    def enqueue(self, name, age, priority, condition=""):
        self.counters[priority] += 1
        self.ticket += 1
        patient = {"id": "%s-%04d" % (PREFIX[priority], self.counters[priority]),
                   "name": name, "age": age, "priority": priority, "condition": condition,
                   "ticket": self.ticket}
        self.patients.append(patient)
        # emergency first, then priority, then regular. Same priority = first come first served
        self.patients.sort(key=lambda p: (RANK[p["priority"]], p["ticket"]))
        self._notify()
        return patient

    def dequeue(self, patient):
        self.patients.pop(0)
        self._notify()

    def peek(self):
        return self.patients[0] if self.patients else None

    def isEmpty(self):
        return len(self.patients) == 0

    def size(self):
        return len(self.patients)

    def __len__(self):
        return len(self.patients)
    
    def has(self, name, age):
        return any(p["name"].lower() == name.lower() and p["age"] == age for p in self.patients)

    # rows for the table: (queuing no, patient id, name, age, priority)
    def rows(self, limit=None):
        patients = self.patients if limit is None else self.patients[:limit]
        return [(str(i + 1), p["id"], p["name"], p["age"] or "-", p["priority"].capitalize())
                for i, p in enumerate(patients)]

    def savefile(self):
        with open("data/patient_list.json", "w") as final:
            json.dump([self.ticket,self.counters,self.patients], final)