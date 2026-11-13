from tkinter import *

from widgets import *
from settings import *

class header(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=primary, width=660, height=78)
        self.pack_propagate(False)
        logo(self, 64, primary).pack(side="left",padx=12)
        wordmark(self, logo_size).pack(side="left")