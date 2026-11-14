from tkinter import *
from tkinter import messagebox

from settings import *
from panels.ui import *

# ======================= OPTIONS (change these) =======================
confirm_cancel = True       # True = ask "Are you sure?" before removing the patient
confirm_complete = False    # True = ask "Are you sure?" before completing the consultation
# =====================================================================

error_color = "#B3121F"   # color of the error message (red)
ok_color = "#0E6B3A"      # color of the success message (green)

class next_patient_card(RoundedBox):
    def __init__(self, parent, queue):
        # radius = roundness of the card, pad = space between the card edge and its content
        super().__init__(parent, card_bg, light_blue, radius=45, outline=card_outline, pad=6)   # <-- ADJUST radius
        self.queue = queue
        body = self.body

        # column widths: name, age, queuing id, priority     <-- ADJUST the numbers to change the width of each box
        for col, weight in enumerate((48, 14, 14, 10)):
            body.columnconfigure(col, weight=weight)

        card_title(body, "NEXT PATIENT TO BE ATTENDED").grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(14, 10))

        # key, label, column, row of the label, how many columns it covers
        self.fields = {}
        for key, label, col, row, span in (("name", "PATIENT NAME:", 0, 1, 1), ("age", "AGE:", 1, 1, 1),
                                           ("id", "QUEUING ID:", 2, 1, 1), ("priority", "PRIORITY:", 3, 1, 1),
                                           ("condition", "CONDITION:", 0, 3, 4)):
            card_label(body, label).grid(row=row, column=col, columnspan=span, sticky="w", padx=(18 if col == 0 else 0, 16),
                                         pady=(10 if row == 3 else 0, 3))
            box, entry = input_box(body, readonly=True)
            box.grid(row=row + 1, column=col, columnspan=span, sticky="ew", padx=(18 if col == 0 else 0, 16))
            self.fields[key] = entry

        # message (error or success)
        self.message = Label(body, text="", font=(font_body, 12), bg=card_bg, fg=ok_color)
        self.message.grid(row=5, column=0, columnspan=4, sticky="w", padx=18, pady=(10, 0))

        # ---- buttons ----  (110 and 220 = width of each button)
        buttons = Frame(body, bg=card_bg)
        buttons.grid(row=6, column=0, columnspan=4, sticky="e", padx=18, pady=(6, 14))
        card_button(buttons, "Cancel", 110, self.cancel).pack(side="left", padx=(0, 8))
        card_button(buttons, "Complete Consultation", 220, self.complete).pack(side="left")

        queue.subscribe(self.refresh)
        self.refresh()

    # ---------- fills the boxes with the first patient in the queue (dashes if the queue is empty) ----------
    def refresh(self):
        patient = self.queue.next()
        if patient is None:
            values = ("-",) * 5
        else:
            values = (patient["name"], patient["age"] or "-", patient["id"], patient["priority"].capitalize(),
                      patient["condition"] or "-")
        for key, value in zip(("name", "age", "id", "priority", "condition"), values):
            set_text(self.fields[key], value)

    def show(self, msg, ok=True):
        self.message.config(text=msg, fg=ok_color if ok else error_color)

    # ---------- CANCEL = the patient left / did not show up, remove them from the queue ----------
    def cancel(self):
        patient = self.queue.next()
        if patient is None:
            self.show("There is no patient to cancel.", ok=False)
            return
        if confirm_cancel and not messagebox.askyesno("Cancel patient", "Remove " + patient["name"] + " from the queue?"):
            return
        self.queue.remove(patient)
        self.show(patient["name"] + " was removed from the queue.")

    # ---------- COMPLETE CONSULTATION = done with this patient, the next one comes up ----------
    def complete(self):
        patient = self.queue.next()
        if patient is None:
            self.show("There is no patient to attend.", ok=False)
            return
        if confirm_complete and not messagebox.askyesno("Complete consultation", "Complete the consultation of " + patient["name"] + "?"):
            return
        self.queue.remove(patient)
        self.show("Consultation of " + patient["name"] + " completed.")