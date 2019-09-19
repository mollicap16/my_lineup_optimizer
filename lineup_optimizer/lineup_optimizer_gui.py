import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pydfs_lineup_optimizer import get_optimizer, Site, Sport 
from modules.tables import createStandardTable as cst

# Global Variables
player_file = ''
ffa_player_projections = pd.DataFrame()

# Creating Main window object
main_window = tk.Tk()
main_window.title("Lineup Optimizer")

ttk.Sizegrip(main_window).grid(column=999, row=999, sticky=('SE'))

# TODO: Might want to remove borderwidth and relief for frames
# Frames
top_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
top_frame.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))

middle_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
middle_frame.grid(column=0, row=1, sticky=('N', 'W', 'E', 'S'))

bottom_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
bottom_frame.grid(column=0, row=2, sticky=('N', 'W', 'E', 'S'))

# This just tells Tk that if the main window is resized the frame should expand with it
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(1, weight =1)

# Labels
load_label = ttk.Label(top_frame, text="empty", background='white', relief='groove', width=50)
load_label.grid(column=1, row=0, sticky="E")
#test_label = ttk.Label(middle_frame, text="HELLO WORLD")
#test_label.grid(column=0, row=0, sticky='W')

# Button Commands
def load_click():
    player_file = filedialog.askopenfilename(initialdir = "/home/pete/Documents/dk_player_exports/")
    load_label.configure(text=player_file, width=0)
    save_button.state(['disabled'])
    optimize_button.state(['!disabled'])
    try:
        ffa_player_projections = pd.read_csv(player_file)
    except:
        sys.exit("Invalid file type")
    table = cst(player_file, middle_frame)
    table.grid(column=0, row=0)

def optimize_click():
    save_button.state(['!disabled'])
    print("Optimize")

def save_click():
    print("Save Lineups")
    save_button.state(['disabled'])

# Buttons
load_button = ttk.Button(top_frame, text="Load", command=load_click)
load_button.grid(column=0, row=0, sticky="W")

optimize_button = ttk.Button(bottom_frame, text="Optimize Lineups", command=optimize_click, state='disabled')
optimize_button.grid(column=2, row=0, sticky="E")

save_button = ttk.Button(bottom_frame, text="Save Lineups", command=save_click, state='disabled')
save_button.grid(column=0, row=0, sticky="W")

# Calling mainloop
main_window.mainloop();
