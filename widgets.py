from tkinter import *

from settings import *
#-------------------------- Custom UI Widgets --------------------------#
# creates the asterisk logo
# I might change this to where it'll just use the actual asterisk * symbol if we decide to use place() instead of pack() 
def logo(parent, size, bg):
    c = Canvas(parent, width=size, height=size, bg=bg, highlightthickness=0)
    import math
    cx = cy = size / 2
    r, w = size * 0.48, size * 0.26
    for deg in (90, 30, 150):
        a = math.radians(deg)
        c.create_line(cx - r * math.cos(a), cy - r * math.sin(a),
                      cx + r * math.cos(a), cy + r * math.sin(a),
                      fill=accent, width=w, capstyle="butt")
    return c

#For creating a label for the wordmark/logotype (needed since the exclamation mark is red)
from tkinter import font as tkfont

def wordmark(parent, font_size, spacing=0):
    f = tkfont.Font(family=font_heading, size=font_size)
    letters = [(ch, text) for ch in "Medique"] + [("!", accent)]
    total = sum(f.measure(ch) for ch, _ in letters) + spacing * (len(letters) - 1)
    c = Canvas(parent, width=total, height=f.metrics("linespace"), bg=primary, highlightthickness=0)
    x = 0
    for ch, color in letters:
        c.create_text(x, 0, text=ch, font=f, fill=color, anchor="nw")
        x += f.measure(ch) + spacing
    return c
    
#Creates rounded rectangles, can be used to create buttons by inputting command=function_name (ex: command=test) when calling this class, text can also be placed inside it using txt=""
class RoundedSurface(Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None, txt=None, outline=None, hover=None, fg=None, font=None):
        Canvas.__init__(self, parent, borderwidth=0, relief="flat", highlightthickness=0, bg=bg)

        if 2*cornerradius > width:
            print("Error: cornerradius is greater than width.")
            return None
        if 2*cornerradius > height:
            print("Error: cornerradius is greater than height.")
            return None

        def shape(pad, cr, fill, tag=""):
            rad = 2*cr
            self.create_polygon((pad,height-cr-pad,pad,cr+pad,pad+cr,pad,width-pad-cr,pad,width-pad,cr+pad,width-pad,height-cr-pad,width-pad-cr,height-pad,pad+cr,height-pad), fill=fill, outline=fill, tags=tag)
            self.create_arc((pad,pad+rad,pad+rad,pad), start=90, extent=90, fill=fill, outline=fill, tags=tag)
            self.create_arc((width-pad-rad,pad,width-pad,pad+rad), start=0, extent=90, fill=fill, outline=fill, tags=tag)
            self.create_arc((width-pad,height-rad-pad,width-pad-rad,height-pad), start=270, extent=90, fill=fill, outline=fill, tags=tag)
            self.create_arc((pad,height-pad-rad,pad+rad,height-pad), start=180, extent=90, fill=fill, outline=fill, tags=tag)

        if outline != None:
            shape(padding, cornerradius, outline)                       # outer layer = the outline
            shape(padding+1, max(cornerradius-1, 1), color, "body")     # inner layer = the fill (+1 = thickness of the outline)
        else:
            shape(padding, cornerradius, color, "body")

        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)

        # the text is drawn right on the button (no Label, so no background box behind it)
        if txt != None:
            self.create_text(width/2, height/2, text=txt, font=font or (font_heading, label_size), fill=fg or text)

        # hover = the color the button changes to when the mouse is on it
        if hover != None:
            self.bind("<Enter>", lambda e: self.itemconfig("body", fill=hover, outline=hover))
            self.bind("<Leave>", lambda e: self.itemconfig("body", fill=color, outline=color))

        if command != None:
            self.command = command
            self.bind("<ButtonPress-1>", self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)
            self.config(cursor="hand2")

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()