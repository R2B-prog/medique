from tkinter import *

from panels.header import header
from panels.register import register_card
from panels.next_patient import next_patient_card
from panels.queue_list import queue_card, QueueTable
from panels.ui import shadow
from patients import PatientQueue
from settings import *

# Max width of the dashboard panel. When the window is wider than this
# (ex: full screen), the extra space on the left and right turns black.
# Set to None to make the panel fill the whole screen (no black sides).
dashboard_max_width = None

class main_dashboard(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg="black")
        self.panel = Frame(self, bg=light_blue)
        self.panel.place(relx=0.5, rely=0, anchor="n", relheight=1, relwidth=1)
        header(self.panel).pack(fill="x")

        # shadow under the header (the function is in panels/ui.py)
        shadow(self.panel, light_blue)

        # ---- scrollable page: scroll with the mouse wheel (no scroll bar shown) ----
        area = Frame(self.panel, bg=light_blue)
        area.pack(fill="both", expand=True)
        self.canvas = Canvas(area, bg=light_blue, highlightthickness=0, bd=0, yscrollincrement=24)
        self.canvas.pack(side="left", fill="both", expand=True)
        content = Frame(self.canvas, bg=light_blue)
        self.window = self.canvas.create_window(0, 0, window=content, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas)
        content.bind("<Configure>", self._on_content)
        self.content_height = 0
        self.bind_all("<MouseWheel>", self._wheel, add="+")
        self.bind_all("<Button-4>", self._wheel, add="+")
        self.bind_all("<Button-5>", self._wheel, add="+")

        # the three cards     pady=(space above, space below) = space between the cards,  padx = space on the left and right
        self.queue = PatientQueue()    # the list of patients, shared by the three cards
        register_card(content, self.queue).pack(fill="x", padx=16, pady=(16, 0))
        next_patient_card(content, self.queue).pack(fill="x", padx=16, pady=(12, 0))
        queue_card(content, self.queue).pack(fill="x", padx=16, pady=(12, 16))

        self.bind("<Configure>", self._resize)

    # the cards follow the width of the window
    def _on_canvas(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)
        self._update_scroll()

    def _on_content(self, event):
        self.content_height = event.height
        self.canvas.configure(scrollregion=(0, 0, event.width, event.height))
        self._update_scroll()

    # if everything fits in the window, go back to the top (nothing to scroll)
    def _update_scroll(self):
        if self.content_height <= self.canvas.winfo_height():
            self.canvas.yview_moveto(0)

    # mouse wheel scrolls the page (but a long queuing list table scrolls itself first)
    def _wheel(self, event):
        try:
            under = self.winfo_containing(event.x_root, event.y_root)
            if under is None or not str(under).startswith(str(self.canvas)):
                return
            w = under
            while w is not None:
                if isinstance(w, QueueTable) and w.can_scroll():
                    return
                w = w.master
            if self.content_height <= self.canvas.winfo_height():
                return
            up = event.num == 4 or getattr(event, "delta", 0) > 0
            self.canvas.yview_scroll(-1 if up else 1, "units")
        except TclError:
            pass

    def _resize(self, event):
        if dashboard_max_width is None:
            width = event.width
        else:
            width = min(event.width, dashboard_max_width)
        self.panel.place_configure(relwidth=0, width=width)