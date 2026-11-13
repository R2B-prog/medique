from tkinter import *

from settings import *
from panels.ui import *

# ======================= OPTIONS (change these) =======================
rows_shown = 5     # how many patients you see at once in the card (scroll with the mouse wheel to see the rest)
# =====================================================================

# the table columns: (title, width)     <-- ADJUST the numbers to change the width of each column
columns = (("QUEUING NO", 14), ("PATIENT ID", 20), ("PATIENT NAME", 42), ("AGE", 10), ("PRIORITY", 17))


# ---------- the table (blue header that stays on top + rows that scroll) ----------
# max_rows       = how many rows are visible at once (None = fill all the space available)
# show_scrollbar = True shows the scroll bar, False hides it (you can still scroll with the mouse wheel)
# header text size: font_heading, 18      row text size: font_body, 12      row height: pady=6
class QueueTable(Frame):
    def __init__(self, parent, max_rows=None, show_scrollbar=True):
        super().__init__(parent, bg=border)
        self.max_rows = max_rows
        self.row_widgets = []

        # ---- header (stays on top) ----
        head = Frame(self, bg=border)
        head.pack(fill="x")
        head_cells = Frame(head, bg=border)
        head_cells.pack(side="left", fill="x", expand=True)
        for col, (title, weight) in enumerate(columns):
            head_cells.columnconfigure(col, weight=weight, uniform="cols")
            Label(head_cells, text=title, font=(font_heading, 18), bg=primary, fg=text, pady=4)\
                .grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 1, 0))

        # ---- shadow under the blue header (same shadow as the main header, smaller and softer) ----
        shadow(self, cell_bg, steps=(0.25, 0.14, 0.06), height=1)

        # ---- rows (scrollable) ----
        self.area = Frame(self, bg=border)
        self.area.pack(fill="both", expand=True)
        self.canvas = Canvas(self.area, bg=cell_bg, highlightthickness=0, bd=0, height=1, yscrollincrement=24)
        self.rows = Frame(self.canvas, bg=border)
        self.window = self.canvas.create_window(0, 0, window=self.rows, anchor="nw")
        for col, (title, weight) in enumerate(columns):
            self.rows.columnconfigure(col, weight=weight, uniform="cols")

        if show_scrollbar:
            bar = Scrollbar(self.area, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=bar.set)
            bar.pack(side="right", fill="y")
            # empty space in the header so the columns line up with the rows
            Frame(head, width=bar.winfo_reqwidth(), bg=border).pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        self.rows.bind("<Configure>", self._on_rows)

        # mouse wheel scrolling (only when the mouse is on the table)
        self.bind_all("<MouseWheel>", self._wheel, add="+")
        self.bind_all("<Button-4>", self._wheel, add="+")
        self.bind_all("<Button-5>", self._wheel, add="+")

    def _on_rows(self, event):
        self.canvas.configure(scrollregion=(0, 0, event.width, event.height))
        if self.max_rows is not None and self.row_widgets:
            row_height = self.row_widgets[0].winfo_reqheight() + 1
            self.canvas.configure(height=min(event.height, row_height * self.max_rows))

    # True when there are more rows than what fits (so the wheel scrolls this table instead of the page)
    def can_scroll(self):
        return self.rows.winfo_reqheight() > self.canvas.winfo_height()

    def _wheel(self, event):
        try:
            under = self.winfo_containing(event.x_root, event.y_root)
            if under is None or not str(under).startswith(str(self.area)) or not self.can_scroll():
                return
            up = event.num == 4 or getattr(event, "delta", 0) > 0
            self.canvas.yview_scroll(-1 if up else 1, "units")
        except TclError:
            pass

    # rows = list of (queuing no, patient id, name, age, priority)
    def set_rows(self, rows):
        for w in self.row_widgets:
            w.destroy()
        self.row_widgets = []
        if not rows:
            empty = Label(self.rows, text="No patients in the queue.", font=(font_body, 12), bg=cell_bg, fg=dark, pady=10)
            empty.grid(row=0, column=0, columnspan=len(columns), sticky="nsew", pady=(1, 0))
            self.row_widgets.append(empty)
            return
        for r, row in enumerate(rows):
            for col, value in enumerate(row):
                cell = Label(self.rows, text=value, font=(font_body, 12), bg=cell_bg, fg=dark, pady=6)
                cell.grid(row=r, column=col, sticky="nsew", padx=(0 if col == 0 else 1, 0), pady=(1, 0))
                self.row_widgets.append(cell)


class queue_card(RoundedBox):
    def __init__(self, parent, queue):
        # radius = roundness of the card, pad = space between the card edge and its content
        super().__init__(parent, card_bg, light_blue, radius=14, outline=card_outline, pad=6)   # <-- ADJUST radius
        self.queue = queue
        self.full_window = None
        self.full_table = None
        body = self.body

        # ---- title + View Full List button ----
        top = Frame(body, bg=card_bg)
        top.pack(fill="x", padx=18, pady=(14, 8))
        card_title(top, "QUEUING LIST").pack(side="left")
        card_button(top, "View Full List", 150, self.view_full).pack(side="right")   # 150 = width of the button

        # ---- table: shows rows_shown patients, scroll with the mouse wheel (scroll bar hidden) ----
        self.table = QueueTable(body, max_rows=rows_shown, show_scrollbar=False)
        self.table.pack(fill="x", padx=18, pady=(0, 6))

        # hint text when there are more patients than rows_shown
        self.more = Label(body, text="", font=(font_body, 12), bg=card_bg, fg=dark)
        self.more.pack(anchor="w", padx=18, pady=(0, 10))

        queue.subscribe(self.refresh)
        self.refresh()

    # ---------- updates the tables whenever the queue changes ----------
    def refresh(self):
        self.table.set_rows(self.queue.rows())
        total = len(self.queue)
        self.more.config(text=("Showing " + str(rows_shown) + " of " + str(total) + " patients. Scroll to see the rest.")
                         if total > rows_shown else "")
        if self.full_table is not None and self.full_window.winfo_exists():
            self.full_table.set_rows(self.queue.rows())

    # ---------- VIEW FULL LIST: opens a window with everyone in the queue (scroll with the mouse wheel) ----------
    def view_full(self):
        if self.full_window is not None and self.full_window.winfo_exists():
            self.full_window.lift()
            return
        win = Toplevel(self)
        win.title("Full queuing list")
        win.geometry("900x500")          # <-- ADJUST size of the window
        win.configure(bg=light_blue)
        table = QueueTable(win, max_rows=None, show_scrollbar=False)   # False = no scroll bar (mouse wheel still scrolls)
        table.pack(fill="both", expand=True, padx=16, pady=16)
        table.set_rows(self.queue.rows())
        self.full_window, self.full_table = win, table