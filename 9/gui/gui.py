from tkinter import *
from tkinter import ttk
import json
from dealer import Dealer

class Gui(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.tree = ttk.Treeview(master)

    def process_data(self, json, parent=""):
        for k, v in json:
            if hasattr(v, __iter__):
                ident = self.tree.insert(parent, "end", text=k)
                self.process_data(v, parent=ident)



if __name__ == "__main__":
    data = sys.stdin.read()
    configuration = json.loads(data)
    dealer = Dealer.deserialize(configuration)
    root = Tk()
    window = Gui(root)
    dealer.make_tree(window.tree, parent="")

    window.tree.pack()
    mainloop()
