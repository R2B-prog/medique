from tkinter import *

from settings import *
from screens.landing import landing
from screens.dashboard import main_dashboard
from screens.full_list import full_list
from patients import PatientQueue


#-------------------------- Medique --------------------------#
class Medique(Tk):
    def __init__(self):
        super().__init__()
        self.title("Medique!")
        self.geometry("1440x967")
        self.resizable(False, False)
        self.container = Frame(self, bg=background)
        self.container.pack(fill="both", expand=True)
        
        self.queue = PatientQueue()    # one list of patients shared by the dashboard and the full list screen
        self.screens = {"landing": landing(self), "dashboard": main_dashboard(self), "full_list": full_list(self)}
        for s in self.screens.values():
            s.place(relwidth=1, relheight=1)
        self.page("landing")

    def page(self, name):
        s = self.screens[name]
        if hasattr(s, "refresh"):
            s.refresh()
        s.tkraise()



if __name__ == "__main__":
    Medique().mainloop()