import heapq
import json
import time
import csv
import statistics
import tracemalloc
import os


# ==========================================
# MEDIQUE PATIENT QUEUE
# Standalone version for algorithm analysis
# ==========================================

class PatientQueue:
    PRIORITIES = ["regular", "priority", "emergency"]

    RANK = {
        "emergency": 1,
        "priority": 2,
        "regular": 3
    }

    PREFIX = {
        "emergency": "E",
        "priority": "P",
        "regular": "R"
    }

    def __init__(self):
        self.patients = []
        self.archive = []
        self.counters = {
            "regular": 0,
            "priority": 0,
            "emergency": 0
        }
        self.ticket = 0

    def enqueue(self, name, age, priority, condition=""):
        self.counters[priority] += 1
        self.ticket += 1

        patient = {
            "id": f"{self.PREFIX[priority]}-{self.counters[priority]:03d}",
            "name": name,
            "age": age,
            "priority": priority,
            "condition": condition
        }

        heapq.heappush(
            self.patients,
            (self.RANK[priority], self.ticket, patient)
        )

        return patient

    def dequeue(self):
        if not self.patients:
            return None

        patient = heapq.heappop(self.patients)[2]
        self.archive.append(patient)
        return patient

    def peek(self):
        if self.patients:
            return self.patients[0][2]
        return None

    def isEmpty(self):
        return len(self.patients) == 0

    def size(self):
        return len(self.patients)

    def has(self, name, age):
        return any(
            p[2]["name"].lower() == name.lower()
            and p[2]["age"] == age
            for p in self.patients
        )

    def rows(self):
        temp = self.patients.copy()
        heapq.heapify(temp)

        result = []

        while temp:
            result.append(heapq.heappop(temp)[2])

        return result

    def archive_rows(self):
        return self.archive.copy()

    def savefile(self):
        return json.dumps({
            "ticket": self.ticket,
            "counters": self.counters,
            "patients": self.patients
        })

    def heapify_data(self, data):
        self.patients = data.copy()
        heapq.heapify(self.patients)


# ==========================================
# BENCHMARK FUNCTIONS
# ==========================================

def create_queue(n):
    queue = PatientQueue()

    for i in range(n):
        priority = PatientQueue.PRIORITIES[i % 3]
        queue.enqueue(f"Patient {i}", 20 + (i % 50), priority)

    return queue


def measure(operation, repetitions=5):
    times = []

    for _ in range(repetitions):
        start = time.perf_counter()
        operation()
        end = time.perf_counter()

        times.append(end - start)

    return statistics.median(times)


def benchmark_enqueue(n):
    def operation():
        queue = PatientQueue()

        for i in range(n):
            priority = PatientQueue.PRIORITIES[i % 3]
            queue.enqueue(f"Patient {i}", 20, priority)

    return measure(operation)


def benchmark_dequeue(n):
    queue = create_queue(n)

    def operation():
        temp = queue.patients.copy()
        heapq.heapify(temp)

        while temp:
            heapq.heappop(temp)

    return measure(operation)


def benchmark_peek(n):
    queue = create_queue(n)

    return measure(
        lambda: [queue.peek() for _ in range(1000)]
    ) / 1000


def benchmark_has(n):
    queue = create_queue(n)

    return measure(
        lambda: [queue.has("Patient 0", 20) for _ in range(100)]
    ) / 100


def benchmark_rows(n):
    queue = create_queue(n)
    return measure(queue.rows)


def benchmark_heapify(n):
    queue = create_queue(n)
    data = queue.patients.copy()

    return measure(
        lambda: heapq.heapify(data.copy())
    )


def benchmark_archive_rows(n):
    queue = create_queue(n)
    queue.archive = [
        {"name": f"Archived {i}", "age": 20}
        for i in range(n)
    ]

    return measure(queue.archive_rows)


def benchmark_size(n):
    queue = create_queue(n)

    return measure(
        lambda: [queue.size() for _ in range(1000)]
    ) / 1000


def benchmark_isempty(n):
    queue = create_queue(n)

    return measure(
        lambda: [queue.isEmpty() for _ in range(1000)]
    ) / 1000


def benchmark_savefile(n):
    queue = create_queue(n)

    return measure(queue.savefile)


def benchmark_has_memory(n):
    tracemalloc.start()

    queue = create_queue(n)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return peak / 1024


# ==========================================
# RUN ALGORITHM ANALYSIS
# ==========================================

def run_analysis():
    sizes = [100, 500, 1000, 2000, 5000, 10000]

    results = []

    print("\nMEDIQUE - ALGORITHM PERFORMANCE ANALYSIS")
    print("=" * 90)

    for n in sizes:
        print(f"\nTesting with {n} patients...")

        tests = {
            "Enqueue": benchmark_enqueue(n),
            "Dequeue All": benchmark_dequeue(n),
            "Peek": benchmark_peek(n),
            "Search": benchmark_has(n),
            "Display Rows": benchmark_rows(n),
            "Heapify": benchmark_heapify(n),
            "Archive Rows": benchmark_archive_rows(n),
            "Size": benchmark_size(n),
            "Is Empty": benchmark_isempty(n),
            "Save Serialization": benchmark_savefile(n),
            "Memory (KB)": benchmark_has_memory(n)
        }

        for operation, duration in tests.items():
            results.append({
                "Patients": n,
                "Operation": operation,
                "Execution Time (seconds)": duration
                if operation != "Memory (KB)" else "",
                "Memory Usage (KB)": duration
                if operation == "Memory (KB)" else ""
            })

            if operation == "Memory (KB)":
                print(f"{operation}: {duration:.2f} KB")
            else:
                print(f"{operation}: {duration:.8f} seconds")

    # Save results to CSV
    filename = "medique_algorithm_analysis.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Patients",
                "Operation",
                "Execution Time (seconds)",
                "Memory Usage (KB)"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 90)
    print("ANALYSIS COMPLETED")
    print(f"Results saved to: {filename}")


# ==========================================
# CORRECTNESS TESTS
# ==========================================

def run_correctness_tests():
    queue = PatientQueue()

    queue.enqueue("Regular Patient", 25, "regular")
    queue.enqueue("Emergency Patient", 30, "emergency")
    queue.enqueue("Priority Patient", 22, "priority")
    queue.enqueue("Second Emergency", 40, "emergency")

    assert queue.size() == 4
    assert queue.peek()["name"] == "Emergency Patient"
    assert queue.has("Regular Patient", 25)

    assert queue.dequeue()["name"] == "Emergency Patient"
    assert queue.dequeue()["name"] == "Second Emergency"
    assert queue.dequeue()["name"] == "Priority Patient"
    assert queue.dequeue()["name"] == "Regular Patient"

    assert queue.isEmpty()
    assert queue.dequeue() is None

    print("\nAll correctness tests passed!")


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":
    run_correctness_tests()
    run_analysis()
