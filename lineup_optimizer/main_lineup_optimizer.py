import lineup_optimizer_gui as OG
from tkinter import Tk, Label, Button

def main():
    root = Tk()
    lineup_optimizer = OG.LineupOptimizerGui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
