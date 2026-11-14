# The queue of patients. Shared by the Register, Next Patient and Queuing List cards.
# (Not named "queue.py" because Python already has a module called queue.)

PRIORITIES = ["regular", "priority", "emergency"]
RANK = {"emergency": 0, "priority": 1, "regular": 2}      # who goes first (0 = first)
PREFIX = {"emergency": "E", "priority": "P", "regular": "R"}   # E-0001, P-0001, R-0001

class PatientQueue:
    def __init__(self):
        self.patients = []
        self.counters = {p: 0 for p in PRIORITIES}
        self.ticket = 0
        self.listeners = []

    # the cards call subscribe(function) so they refresh when the queue changes
    def subscribe(self, function):
        self.listeners.append(function)

    def _notify(self):
        for function in self.listeners:
            function()

    def add(self, name, age, priority, condition=""):
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

    def next(self):
        return self.patients[0] if self.patients else None

    def remove(self, patient):
        if patient in self.patients:
            self.patients.remove(patient)
            self._notify()

    def has(self, name, age):
        return any(p["name"].lower() == name.lower() and p["age"] == age for p in self.patients)

    def __len__(self):
        return len(self.patients)

    # rows for the table: (queuing no, patient id, name, age, priority)
    def rows(self, limit=None):
        patients = self.patients if limit is None else self.patients[:limit]
        return [(str(i + 1), p["id"], p["name"], p["age"] or "-", p["priority"].capitalize())
                for i, p in enumerate(patients)]