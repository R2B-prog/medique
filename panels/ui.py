from tkinter import *

from widgets import *
from settings import *

# shared colors / helpers for the dashboard cards
# ======================= COLORS (change these to recolor ALL the cards) =======================
card_bg = secondary          # color of the cards
card_outline = "#A9C6EA"     # thin line around the cards
input_bg = "#93B5DE"         # color of the input boxes
cell_bg = "#A5C0DF"          # color of the table cells
dark = "#0B2A4D"             # color of titles / labels
muted = "#5C7FAA"            # color of the placeholder text (name, age)
button_fill = "#8FB1DA"      # color INSIDE the buttons (a little grayer than the card, like the design)
button_outline = "#C3D8F0"   # color of the thin white-ish line around the buttons (None = no line)

# ================================================================================================


# ---------- SHADOW (used under the header and under the blue header of the queuing list) ----------
# mixes two hex colors, t = how much of color b (0 to 1)
def blend(a, b, t):
    a = [int(a[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))

# puts a soft shadow right under whatever you pack before it.
# bg      = color of what is under the shadow (the shadow fades into this color)
# steps   = how dark each strip is (more numbers = longer shadow, bigger numbers = darker)
# height  = thickness of each strip in pixels
def shadow(parent, bg, steps=(0.30, 0.20, 0.12, 0.06, 0.03), height=2, dark="#0B2A4D"):
    for t in steps:
        Frame(parent, bg=blend(bg, dark, t), height=height).pack(fill="x")


# ---------- RoundedBox: the rounded rectangle used for the cards and the input boxes ----------
# Put your widgets inside  box.body
# radius = how round the corners are (bigger = rounder)
# pad    = space between the edge and the content (if radius is big, make pad bigger too)
# The height follows whatever is inside it, the width follows the window.
class RoundedBox(Canvas):
    def __init__(self, parent, fill, bg, radius=14, outline=None, pad=6):
        Canvas.__init__(self, parent, bg=bg, highlightthickness=0, bd=0, height=10)
        self.fill, self.outline, self.radius, self.pad = fill, outline, radius, pad
        self.body = Frame(self, bg=fill)
        self.win = self.create_window(pad, pad, window=self.body, anchor="nw")
        self.bind("<Configure>", self._on_canvas)
        self.body.bind("<Configure>", self._on_body)

    def _on_body(self, event):
        self.configure(height=event.height + 2 * self.pad)

    def _on_canvas(self, event):
        self.itemconfigure(self.win, width=max(1, event.width - 2 * self.pad))
        self.delete("bg")
        x0, y0, x1, y1, r = 1, 1, event.width - 1, event.height - 1, self.radius
        points = [x0+r,y0, x1-r,y0, x1,y0, x1,y0+r, x1,y1-r, x1,y1, x1-r,y1, x0+r,y1,
                  x0,y1, x0,y1-r, x0,y0+r, x0,y0]
        self.create_polygon(points, smooth=True, fill=self.fill,
                            outline=self.outline or self.fill, tags="bg")
        self.tag_lower("bg")


# ---------- FillBox: same as RoundedBox, but it STRETCHES to fill all the space it is given ----------
# (RoundedBox follows the height of its content, FillBox makes its content follow the box instead.)
# Use pack(fill="both", expand=True) on it. Used by the full queuing list screen.
class FillBox(RoundedBox):
    def _on_body(self, event):
        pass   # do not follow the height of the content

    def _on_canvas(self, event):
        RoundedBox._on_canvas(self, event)
        self.itemconfigure(self.win, height=max(1, event.height - 2 * self.pad))


# small label above the inputs (PATIENT NAME:, AGE: ...)   <-- ADJUST the size: font_body, 12
def card_label(parent, txt):
    return Label(parent, text=txt, font=(font_body, 12), bg=card_bg, fg=dark)

# big title of each card (REGISTER NEW PATIENT ...)   <-- ADJUST the size: font_heading, 22
def card_title(parent, txt):
    return Label(parent, text=txt, font=(font_heading, 22), bg= secondary, fg=dark,
                 padx=6, pady=1)   # padx/pady = laki ng kahon sa paligid ng text

# rounded input box, returns (box, entry). Grid/pack the box, not the entry.
# radius = roundness of the box (each card can give its own number)
def input_box(parent, readonly=False, radius=10):
    box = RoundedBox(parent, input_bg, card_bg, radius=radius, pad=3)
    entry = Entry(box.body, font=(font_body, 12), bg=input_bg, fg=dark, relief="flat", bd=0,
                  highlightthickness=0, insertbackground=dark, readonlybackground=input_bg)
    entry.pack(fill="x", padx=10, pady=7)   # <-- ADJUST pady = height of the input box, padx = space before the text
    if readonly:
        entry.config(state="readonly")
    return box, entry

def set_text(entry, value):
    state = entry.cget("state")
    entry.config(state="normal")
    entry.delete(0, END)
    entry.insert(0, value)
    entry.config(state=state)

# rounded button with dark text, used by ALL the buttons in the cards
# width = given when you call it, 36 = height of the button, radius_button = roundness (from settings.py)
# bg = color behind the button (use light_blue when the button sits on the page, not inside a card)
def card_button(parent, txt, width, command, bg=card_bg):
    font = (font_heading, 16)   # <-- ADJUST 16 = text size inside the buttons
    try:
        # newest RoundedSurface: the text is drawn directly on the button (no background box behind it)
        return RoundedSurface(parent, width, 36, radius_button, 2, button_fill, bg, command=command, txt=txt,
                              outline=button_outline, fg=dark, font=font)   # <-- ADJUST 36 = button height
    except TypeError:
        pass
    try:
        # RoundedSurface that only has the outline option
        b = RoundedSurface(parent, width, 36, radius_button, 2, button_fill, bg, command=command, txt=txt, outline=button_outline)
    except TypeError:
        b = RoundedSurface(parent, width, 36, radius_button, 2, button_fill, bg, command=command, txt=txt)
    for child in b.winfo_children():
        child.config(fg=dark, font=font)
    return b