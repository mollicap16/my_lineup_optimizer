import tkinter as tk
from tkinter import filedialog
from pydfs_lineup_optimizer import get_optimizer, Site, Sport 

# Creating Main window object
main_window = tk.Tk()

load_label_text="";
load_label = tk.Label(main_window, text="empty", bg='white', relief='groove', width=50)
load_label.grid(column=1, row=0)

def load_click():
    file_load = filedialog.askopenfilename()
    load_label.configure(text=file_load, width=0)

load_button = tk.Button(main_window, text="Load", command=load_click)
load_button.grid(column=0, row=0)

# Calling mainloop
main_window.mainloop();
