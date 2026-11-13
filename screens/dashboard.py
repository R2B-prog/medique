from tkinter import *

from panels.header import header
from settings import *

# mixes two hex colors, t = how much of color b (0 to 1)
def blend(a, b, t):
    a = [int(a[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))

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

        # shadow under the header
        for t in (0.30, 0.20, 0.12, 0.06, 0.03):
            Frame(self.panel, bg=blend(light_blue, "#0B2A4D", t), height=2).pack(fill="x")

        self.bind("<Configure>", self._resize)

    def _resize(self, event):
        if dashboard_max_width is None:
            width = event.width
        else:
            width = min(event.width, dashboard_max_width)
        self.panel.place_configure(relwidth=0, width=width)