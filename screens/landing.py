from tkinter import *

from widgets import *
from settings import *

# Welcome Screen
class landing(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg=primary)
        centered_frame = Frame(self, bg=primary)
        centered_frame.place(relx=0.5,rely=0.46,anchor="center")

        logo(self, 50, primary).place(in_=centered_frame,relx=0.5,rely=0,x=-5,y=30,anchor="center")
        wordmark(centered_frame, 180, spacing=-7).pack()
        RoundedSurface(self, 280, 50, radius_button, 2, "#4A82BD", primary, command=lambda: medique.page("dashboard"), txt="Get Started!", outline="#86AEDB", hover=card).place(in_=centered_frame,relx=0.5,rely=1,y=-30,anchor="center")
