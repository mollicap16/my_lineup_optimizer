import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, StringVar
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter 
from pandastable import Table

# Helper Methods
def LoadOptimizer(filename):
    try:
        optimizer.load_players_from_csv(filename)
    except: 
        sys.exit('Invalid csv file format')

def AddValueColumn(player_efficiency):
    players = optimizer.players
    for player in players:
        player_efficiency.append(player.efficiency*1000)

def DraftKingsRefromatting(filename):
    try:
        results_df = pd.read_csv(filename)
    except:
        sys.exit('Failed to save %s' % filename)
    print('Saved: %s' % filename )

# Global Variables
player_file = ''
ffa_player_projections = pd.DataFrame()
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL) 

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

# Button Commands
def load_click():
    player_file = filedialog.askopenfilename(initialdir = "/home/pete/Documents/dk_player_exports/", title='Select Projections')
    load_label.configure(text=player_file, width=0)
    save_button.state(['disabled'])
    optimize_button.state(['!disabled'])
    try:
        ffa_player_projections = pd.read_csv(player_file)
        LoadOptimizer(player_file)
        player_value = []
        AddValueColumn(player_value)
        ffa_player_projections = ffa_player_projections.assign(Value = player_value)
    except:
        sys.exit("Invalid file type")
    table = Table(middle_frame, dataframe=ffa_player_projections)
    table.grid(column=0, row=0)
    table.show()

def optimize_click():
    lineups = optimizer.optimize(int(num_lineups.get()))
    progress_bar['value'] = 0
    progress_bar['maximum'] = int(num_lineups.get())
    for lineup in lineups:
        print(lineup)
        progress_bar['value'] += 1
        main_window.update()
    save_button.state(['!disabled'])

def save_click():
    results = filedialog.asksaveasfilename(initialdir = '/home/pete/Documents/dk_lineups', title = 'Save File', initialfile = 'results.csv')
    exporter = CSVLineupExporter(optimizer.optimize(int(num_lineups.get())))
    exporter.export(results)
    DraftKingsRefromatting(results)
    save_button.state(['disabled'])

# Labels
load_label = ttk.Label(top_frame, text="empty", background='white', relief='groove', width=50)
load_label.grid(column=1, row=0, sticky='E')
num_lineup_label = ttk.Label(bottom_frame, text="Number of Lineups")
num_lineup_label.grid(column=3, row=0, sticky='W')

# Entries
num_lineups = tk.StringVar() 
num_lineups.set(20)
num_of_lineups_entry = ttk.Entry(bottom_frame, textvariable=num_lineups, justify='center', width=10)
num_of_lineups_entry.grid(column=2, row=0, sticky='W', padx=(25,5))

# Buttons
load_button = ttk.Button(top_frame, text="Load", command=load_click)
load_button.grid(column=0, row=0, sticky="W")

optimize_button = ttk.Button(bottom_frame, text="Optimize Lineups", command=optimize_click, state='disabled')
optimize_button.grid(column=1, row=0, sticky="E")

save_button = ttk.Button(bottom_frame, text="Save Lineups", command=save_click, state='disabled')
save_button.grid(column=0, row=0, sticky="W")

# Progressbar
progress_bar = ttk.Progressbar(bottom_frame, orient='horizontal', mode='determinate')
progress_bar.grid(column=5, row=0, padx=20)

# Calling mainloop
main_window.mainloop();
