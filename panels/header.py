from tkinter import *

from widgets import *
from settings import *

class header(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=primary, height=135)
        self.pack_propagate(False)
        logo(self, 110, primary).pack(side="left",padx=12)
        wordmark(self, 80, spacing=-3).pack(side="left")