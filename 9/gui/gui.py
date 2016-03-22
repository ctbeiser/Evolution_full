from tkinter import *
from tkinter import ttk
import json
from dealer import Dealer


class Gui(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.tree = ttk.Treeview(master)

if __name__ == "__main__":
    data = sys.stdin.read()
    configuration = json.loads(data)
    dealer = Dealer.deserialize(configuration)

    for p in [dealer, dealer.players[0]]:
        root = Tk()
        window = Gui(root)
        p.make_tree(window.tree, parent="")
        window.tree.pack()
    mainloop()