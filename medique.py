from tkinter import *

# Colors
primary, secondary, background, card, light_blue, text, accent, border = "#1664B0", "#7CA9DF", "#1E1E1E", "#A5C0DF", "#95BAEB", "#EFE8DE", "#D21624", "#6A8CB7"

#Typography
font_heading, font_body = "Bebas Neue", "Roboto Condensed"
logo_size, heading_size, body_size, label_size = 44, 18, 12, 10

#Border Radius
radius_panel, radius_card, radius_input, radius_button = 12, 12, 8, 7

#Spacing
space_xs, space_sm, space_md, space_lg, space_xl, space_2xl = 4, 8, 12, 16, 24, 32

#Layout
sidebar_width, content_padding = 240, 24

#----------------------------------------------------------------------------------#



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
def wordmark(parent, font_size):
    wordframe = Frame(parent)
    Label(wordframe, text="Medique", font=(font_heading, font_size), bg=primary, fg=text).pack(side="left",padx=0)
    Label(wordframe, text="!", font=(font_heading, font_size), bg=primary, fg=accent).pack(side="left",padx=0)
    return wordframe
    
#Creates rounded rectangles, can be used to create buttons by inputting command=function_name (ex: command=test) when calling this class, text can also be placed inside it using txt=""
class RoundedSurface(Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None, txt=None):
        Canvas.__init__(self, parent, borderwidth=0, relief="flat", highlightthickness=0, bg=bg)

        rad = 2*cornerradius
        if rad > width:
            print("Error: cornerradius is greater than width.")
            return None
        if rad > height:
            print("Error: cornerradius is greater than height.")
            return None
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)

        id = shape()
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)

        if txt != None:
            label = Label(self, text=txt, font=(font_heading, label_size), bg=secondary, fg=text)
            label.place(relx=0.5,rely=0.5, anchor="center")

        if command != None:
            self.command = command
            self.bind("<ButtonPress-1>", self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)
            self.config(cursor="hand2")
            if txt != None:
                label.config(cursor="hand2")
                label.bind("<ButtonPress-1>", self._on_press)
                label.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()

#Creates the header
class header(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=primary, width=660, height=78)
        self.pack_propagate(False)
        logo(self, 64, primary).pack(side="left",padx=12)
        wordmark(self, logo_size).pack(side="left")

#-------------------------- Pages --------------------------#
# Welcome Page
class landing(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg=primary)
        centered_frame = Frame(self, bg=primary)
        centered_frame.place(relx=0.5,rely=0.46,anchor="center")

        logo(self, heading_size, primary).place(relx=0.493,rely=0.375,anchor="center")
        wordmark(centered_frame, 64).pack()
        get_started = RoundedSurface(self, 150, 30, radius_button, 2, secondary, primary, command=lambda: medique.page("dashboard"), txt="Get Started!")
        get_started.place(relx=0.5,rely=0.57,anchor="center")


class main_dashboard(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg=light_blue)
        header(self).pack()


#-------------------------- Medique --------------------------#
class Medique(Tk):
    def __init__(self):
        super().__init__()
        self.title("Medique!")
        self.geometry("660x489")
        self.resizable(False,False)
        self.container = Frame(self, bg=background)
        self.container.pack(fill="both", expand=True)
        
        self.screens = {"landing": landing(self), "dashboard": main_dashboard(self)}
        for s in self.screens.values():
            s.place(relwidth=1, relheight=1)
        self.page("landing")

    def page(self, name):
        s = self.screens[name]
        if hasattr(s, "refresh"):
            s.refresh()
        s.tkraise()



# Should we make the program resizable?

if __name__ == "__main__":
    Medique().mainloop()