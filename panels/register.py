from tkinter import *

from settings import *
from panels.ui import *

from patients import PRIORITIES as priority_choices

# ======================= CONDITIONS / OPTIONS (change these) =======================
name_required = True       # True = name must be filled in, False = optional
age_required = True        # True = age must be filled in, False = optional (label shows "(optional)")
max_age = 120              # highest age allowed
condition_required = False # True = condition must be filled in, False = optional
max_condition = 100        # most letters allowed in the condition
block_duplicates = True    # True = can't register the same name + age twice while still in the queue
max_in_queue = 50          # most patients allowed in the queue (None = no limit)
# =====================================================================================

error_color = "#B3121F"   # color of the error message (red)
ok_color = "#0E6B3A"      # color of the success message (green)

class register_card(RoundedBox):
    def __init__(self, parent, queue):
        # radius = roundness of the card, pad = space between the card edge and its content
        super().__init__(parent, card_bg, light_blue, radius=50, outline=card_outline, pad=8)   # <-- ADJUST radius
        self.queue = queue
        body = self.body

        # column widths: name, age, priority (priority covers the last 2 columns)   <-- ADJUST the numbers to change the width of each input
        # the three boxes together are as wide as the condition box
        for col, weight in enumerate((50, 18, 16, 16)):
            body.columnconfigure(col, weight=weight)

        # ---- title ----   padx = space from the left, pady = (space above, space below)
        card_title(body, "REGISTER NEW PATIENT").grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(14, 10))

        # ---- inputs ----
        self.name_entry = self._input(body, "PATIENT NAME:", "name", 0, name_required)
        self.age_entry = self._input(body, "AGE:", "age", 1, age_required)

        # ---- priority dropdown ----
        card_label(body, "PRIORITY:").grid(row=1, column=2, sticky="w", pady=(0, 3))
        box = RoundedBox(body, input_bg, card_bg, radius=30, pad=6)   # <-- ADJUST radius = roundness of the dropdown
        box.grid(row=2, column=2, columnspan=2, sticky="ew", padx=(0, 16))
        self.priority = StringVar(value=priority_choices[0])
        menu = OptionMenu(box.body, self.priority, *priority_choices)
        menu.config(font=(font_body, 12), bg=input_bg, fg=dark, activebackground=input_bg,
                    relief="flat", highlightthickness=0, bd=0, anchor="w")
        menu["menu"].config(font=(font_body, 12), bg=input_bg, fg=dark)
        menu.pack(fill="x", padx=4, pady=3)

        # ---- condition of the patient (2nd row, wide box) ----
        self.condition_entry = self._input(body, "CONDITION:", "ex: fever, cough", 0, condition_required, row=3, span=4, pady=(10, 3))

        # ---- message (error or success) ----
        self.message = Label(body, text="", font=(font_body, 12), bg=card_bg, fg=error_color)
        self.message.grid(row=5, column=0, columnspan=4, sticky="w", padx=18, pady=(10, 0))

        # ---- buttons ----
        buttons = Frame(body, bg=card_bg)
        buttons.grid(row=6, column=0, columnspan=4, sticky="e", padx=18, pady=(6, 14))
        # the numbers 110 and 170 = width of each button, padx = space between the buttons
        card_button(buttons, "Cancel", 110, self.clear).pack(side="left", padx=(0, 8))
        card_button(buttons, "Register Patient", 170, self.submit).pack(side="left")

    # one label + one rounded text box (with gray placeholder text)
    # row = row of the label (the box is right under it), span = how many columns the box covers
    def _input(self, body, label, placeholder, column, required, row=1, span=1, pady=(0, 3)):
        if not required:
            label = label[:-1] + " (optional):"
        card_label(body, label).grid(row=row, column=column, columnspan=span, sticky="w", padx=(18 if column == 0 else 0, 16), pady=pady)
        box, entry = input_box(body)
        box.grid(row=row + 1, column=column, columnspan=span, sticky="ew", padx=(18 if column == 0 else 0, 16))
        entry.bind("<Key>", lambda e: self.message.config(text=""))   # the old error goes away when you type again
        entry.placeholder = placeholder
        self._show_placeholder(entry)
        entry.bind("<FocusIn>", lambda e: self._hide_placeholder(entry))
        entry.bind("<FocusOut>", lambda e: self._show_placeholder(entry))
        return entry

    def _show_placeholder(self, entry):
        if entry.get() == "":
            entry.insert(0, entry.placeholder)
            entry.config(fg=muted)

    def _hide_placeholder(self, entry):
        if entry.get() == entry.placeholder and entry.cget("fg") == muted:
            entry.delete(0, END)
            entry.config(fg=dark)

    def value(self, entry):
        v = entry.get()
        return "" if (v == entry.placeholder and entry.cget("fg") == muted) else v

    def clear(self):
        for entry in (self.name_entry, self.age_entry, self.condition_entry):
            entry.delete(0, END)
            self._show_placeholder(entry)
        self.priority.set(priority_choices[0])
        self.message.config(text="")
        self.body.focus_set()

    # ---------- CONDITIONS: checks everything, returns the error message or None if all is ok ----------
    def check(self):
        name = self.value(self.name_entry).strip()
        age = self.value(self.age_entry).strip()
        condition = self.value(self.condition_entry).strip()

        if name_required and name == "":
            return "Please enter the patient's name."
        if name != "" and len(name) < 2:
            return "Name is too short."
        if name != "" and not all(c.isalpha() or c in " .'-" for c in name):
            return "Name can only have letters, spaces, . ' and -"

        if age_required and age == "":
            return "Please enter the patient's age."
        if age != "":
            if not age.isdigit():
                return "Age must be a number."
            if not 0 <= int(age) <= max_age:
                return "Age must be between 0 and " + str(max_age) + "."

        # condition (optional): not longer than max_condition
        if condition_required and condition == "":
            return "Please enter the patient's condition."
        if len(condition) > max_condition:
            return "Condition can only be " + str(max_condition) + " letters or less (now " + str(len(condition)) + ")."

        if self.priority.get() not in priority_choices:
            return "Please choose a priority."

        if max_in_queue is not None and len(self.queue) >= max_in_queue:
            return "The queue is full (" + str(max_in_queue) + " patients)."
        if block_duplicates and self.queue.has(name, age):
            return "This patient is already in the queue."
        return None

    # ---------- runs when you press Register Patient: checks, then adds the patient to the queue ----------
    def submit(self):
        error = self.check()
        if error:
            self.message.config(text=error, fg=error_color)
            return
        patient = self.queue.add(self.value(self.name_entry).strip(), self.value(self.age_entry).strip(), self.priority.get(),
                                 self.value(self.condition_entry).strip())
        self.clear()
        self.message.config(text="Registered " + patient["name"] + " (" + patient["id"] + ")", fg=ok_color)