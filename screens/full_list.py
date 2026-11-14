from tkinter import *

from panels.header import header
from panels.queue_list import QueueTable
from panels.ui import *
from settings import *

# ======================= OPTIONS (change these) =======================
show_scrollbar = False   # True = show a scroll bar on the right (the mouse wheel works either way)
# =====================================================================

# Full queuing list screen (opens when you click "View Full List" in the dashboard)
# Same header as the dashboard. The blue column names (QUEUING NO, PATIENT ID, ...) stay on top while the rows scroll.
class full_list(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg=light_blue)

        # ---- same header + shadow as the dashboard ----
        header(self).pack(fill="x")
        shadow(self, light_blue)

        # ---- GO BACK button ----
        top = Frame(self, bg=light_blue)
        top.pack(fill="x", padx=16, pady=(12, 8))
        card_button(top, "GO BACK", 110, lambda: medique.page("dashboard"), bg=light_blue).pack(side="left")   # 110 = width of the button

        # ---- card with the title + the table (the card fills all the space left in the window) ----
        card = FillBox(self, card_bg, light_blue, radius=14, outline=card_outline, pad=6)
        card.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        card_title(card.body, "QUEUING LIST").pack(anchor="w", padx=18, pady=(14, 8))

        self.table = QueueTable(card.body, max_rows=None, show_scrollbar=show_scrollbar, fill_blank=True)
        self.table.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        # same queue as the dashboard, so new patients show up here too
        self.queue = medique.queue
        self.queue.subscribe(self.refresh)
        self.refresh()

    def refresh(self):
        self.table.set_rows(self.queue.rows())