from tkinter import *

from widgets import *
from settings import *

# Welcome Screen
class landing(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg=primary)
        centered_frame = Frame(self, bg=primary)
        centered_frame.place(relx=0.5,rely=0.46,anchor="center")

        logo(self, heading_size, primary).place(relx=0.493,rely=0.375,anchor="center")
        wordmark(centered_frame, 64).pack()
        RoundedSurface(self, 150, 30, radius_button, 2, secondary, primary, command=lambda: medique.page("dashboard"), txt="Get Started!", hover=card).place(relx=0.5,rely=0.57,anchor="center")