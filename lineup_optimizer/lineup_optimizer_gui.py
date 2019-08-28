import tkinter as tk
from pydfs_lineup_optimizer import get_optimizer, Site, Sport 

# Creating Main window object
main_window = tk.Tk()

load_entry_text="";
load_entry = tk.Entry(main_window, text="empty", bg='white', relief='groove', state='disable')
load_entry.grid(column=1, row=0)

def load_click():
    load_entry_text = "Clicked"
    load_entry.configure(text=load_entry_text)

load_button = tk.Button(main_window, text="Load", command=load_click)
load_button.grid(column=0, row=0)

# Calling mainloop
main_window.mainloop();
