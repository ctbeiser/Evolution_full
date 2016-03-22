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

    dealer_root = Tk()
    player_root = Tk()
    dealer_window = Gui(dealer_root)
    player_window = Gui(player_root)
    dealer.make_tree(dealer_window.tree, parent="")
    dealer.players[0].make_tree(player_window.tree, parent="")

    dealer_window.tree.pack()
    player_window.tree.pack()
    mainloop()
