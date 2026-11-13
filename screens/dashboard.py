from tkinter import *

from panels.header import header
from settings import *

class main_dashboard(Frame):
    def __init__(self, medique):
        super().__init__(medique.container, bg=light_blue)
        header(self).pack()