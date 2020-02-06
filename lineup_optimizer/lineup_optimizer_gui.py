import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, StringVar, IntVar 
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter 
from pandastable import Table

# Helper Methods
def LoadOptimizer(filename):
    global optimizer
    if (selected_sport.get() == 1):
        optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
    elif (selected_sport.get() == 2):
        optimizer = get_optimizer(Site.DRAFTKINGS, Sport.HOCKEY)
    try:
        optimizer.load_players_from_csv(filename)
    except: 
        sys.exit('Invalid csv file format')

def AddValueColumn(player_efficiency):
    players = optimizer.players
    for player in players:
        player_efficiency.append(player.efficiency*1000)

def DraftKingsRefromatting(filename):
    results_df = pd.DataFrame()
    try:
        results_df = pd.read_csv(filename)
    except:
        sys.exit('Failed to save %s' % filename)
    results_df = results_df[['QB','RB1', 'RB2', 'WR1', 'WR2', 'WR3','TE', 'FLEX', 'DST']]
    results_df.columns = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'DST']
    filename = filename.split('.')[0]
    results_df.to_csv(filename+'_DK_Format.csv', index=False)
    print('Saved: %s' % filename+'_DK_Format.csv')

def LockPlayers():
    for player_name in locked_player_list:
        player = optimizer.get_player_by_name(player_name)
        optimizer.add_player_to_lineup(player)

def ExcludePlayers():
    for player_name in excluded_player_list:
        player = optimizer.get_player_by_name(player_name)
        print(player)
        optimizer.remove_player(player)

def RestorePlayers():
    # Unlock Players
    for player_name in locked_player_list:
        player = optimizer.get_player_by_name(player_name)
        optimizer.remove_player_from_lineup(player)

    # Include Players back into the lineup
    for player_name in excluded_player_list:
        player = optimizer.get_player_by_name(player_name)
        optimizer.restore_player(player)

# Global Variables
player_file = ''
ffa_player_projections = pd.DataFrame()
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
locked_player_list=[]
excluded_player_list=[]

# Creating Main window object
main_window = tk.Tk()
main_window.title("Lineup Optimizer")

selected_sport = tk.IntVar(main_window, value=1)

ttk.Sizegrip(main_window).grid(column=999, row=999, sticky=('SE'))

# Menu
menubar = tk.Menu(main_window)

# TODO: Might want to remove borderwidth and relief for frames
# Frames
top_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
top_frame.grid(column=0, row=0, columnspan=2, sticky=('N', 'W', 'E', 'S'))

middle_left_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
middle_left_frame.grid(column=0, row=1, sticky=('N', 'W', 'E', 'S'))

middle_right_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
middle_right_frame.grid(column=1, row=1)

bottom_frame = ttk.Frame(main_window, borderwidth=4, relief='sunken')
bottom_frame.grid(column=0, row=2, columnspan=2, sticky=('N', 'W', 'E', 'S'))

locked_player_frame = ttk.Frame(middle_right_frame, borderwidth=4, relief='sunken')
locked_player_frame.grid(column=0, row=0)

excluded_player_frame = ttk.Frame(middle_right_frame, borderwidth=4, relief='sunken')
excluded_player_frame.grid(column=0, row=1)

# This just tells Tk that if the main window is resized the frame should expand with it
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(1, weight =1)

table = Table(middle_left_frame)

# Button Commands
def load_click():
    player_file = filedialog.askopenfilename(initialdir = "/home/pete/Documents/dk_player_exports/", title='Select Projections')
    load_label.configure(text=player_file, width=0)
    save_button.state(['disabled'])
    optimize_button.state(['!disabled'])
    try:
        global ffa_player_projections
        ffa_player_projections = pd.read_csv(player_file)
        LoadOptimizer(player_file)
        player_value = []
        AddValueColumn(player_value)
        ffa_player_projections = ffa_player_projections.assign(Value = player_value)
    except:
        sys.exit("Invalid file type")
    global table 
    table = Table(middle_left_frame, dataframe=ffa_player_projections)
    table.grid(column=0, row=0, rowspan=2)
    table.show()
    add_lock_button.state(['!disabled'])
    add_exclude_button.state(['!disabled'])
    remove_lock_button.state(['!disabled'])
    remove_exclude_button.state(['!disabled'])


def optimize_click():
    LockPlayers()
    ExcludePlayers()
    lineups = optimizer.optimize(int(num_lineups.get()))
    progress_bar['value'] = 0
    progress_bar['maximum'] = int(num_lineups.get())
    for lineup in lineups:
        print(lineup)
        progress_bar['value'] += 1
        main_window.update()
    save_button.state(['!disabled'])
    RestorePlayers()

def save_click():
    results = filedialog.asksaveasfilename(initialdir = '/home/pete/Documents/dk_lineups', title = 'Save File', initialfile = 'results.csv')
    LockPlayers()
    ExcludePlayers()
    exporter = CSVLineupExporter(optimizer.optimize(int(num_lineups.get())))
    exporter.export(results)
    DraftKingsRefromatting(results)
    save_button.state(['disabled'])

def add_locked_player_click():
    row = table.getSelectedRow()
    player = ffa_player_projections.iloc[row].Name
    if (player not in locked_player_list and player not in excluded_player_list):
        locked_player_list.append(player)

    locked_player_listbox.delete(0,'end')
    for item in locked_player_list:
        locked_player_listbox.insert('end', item)

def remove_locked_player_click():
    player = locked_player_listbox.get('active')
    if (player in locked_player_list):
        locked_player_list.remove(player)

    locked_player_listbox.delete(0,'end')
    for item in locked_player_list:
        locked_player_listbox.insert('end', item)

def add_excluded_player_click():
    row = table.getSelectedRow()
    player = ffa_player_projections.iloc[row].Name
    if (player not in excluded_player_list and player not in locked_player_list):
        excluded_player_list.append(player)

    excluded_player_listbox.delete(0,'end')
    for item in excluded_player_list:
        excluded_player_listbox.insert('end', item)

def remove_excluded_player_click():
    player = excluded_player_listbox.get('active')
    if (player in excluded_player_list):
        excluded_player_list.remove(player)

    excluded_player_listbox.delete(0,'end')
    for item in excluded_player_list:
        excluded_player_listbox.insert('end', item)

# Menubar
filemenu = tk.Menu(menubar, tearoff=0)
sportsmenu = tk.Menu(menubar, tearoff=0)
sportsmenu.add_radiobutton(label="NFL", value=1, variable=selected_sport)
sportsmenu.add_radiobutton(label="NHL", value=2, variable=selected_sport)

menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Select Sport', menu = sportsmenu)

# list box
locked_player_listbox = tk.Listbox(locked_player_frame, height=10)
locked_player_listbox.grid(column = 0, row = 1, columnspan=2, sticky=('N', 'W', 'E', 'S'))
excluded_player_listbox = tk.Listbox(excluded_player_frame)
excluded_player_listbox.grid(column=0, row=1, columnspan=2, sticky=('N', 'W', 'E', 'S'))

# Labels
load_label = ttk.Label(top_frame, text="empty", background='white', relief='groove', width=50)
load_label.grid(column=1, row=0, sticky='E')
num_lineup_label = ttk.Label(bottom_frame, text="Number of Lineups")
num_lineup_label.grid(column=3, row=0, sticky='W')
locked_player_label = ttk.Label(locked_player_frame, text='Locked Players', font='-weight bold')
locked_player_label.grid(column = 0, row = 0, columnspan=2, sticky=('N', 'W', 'E', 'S'))
excluded_player_label = ttk.Label(excluded_player_frame, text='Excluded Players', font='-weight bold')
excluded_player_label.grid(column=0, row=0, columnspan=2, sticky=('N', 'W', 'E', 'S'))

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

add_lock_button = ttk.Button(locked_player_frame, text='Add Player', command=add_locked_player_click, state='disabled')
add_lock_button.grid(column=0, row=2, sticky='W')

add_exclude_button = ttk.Button(excluded_player_frame, text='Add Player', command=add_excluded_player_click, state='disabled')
add_exclude_button.grid(column=0, row=2, sticky='W')

remove_lock_button = ttk.Button(locked_player_frame, text='Remove Player', command=remove_locked_player_click, state='disabled')
remove_lock_button.grid(column=1, row=2, sticky='E')

remove_exclude_button = ttk.Button(excluded_player_frame, text='Remove Player', command=remove_excluded_player_click, state='disabled')
remove_exclude_button.grid(column=1, row=2, sticky='E')

# Progressbar
progress_bar = ttk.Progressbar(bottom_frame, orient='horizontal', mode='determinate')
progress_bar.grid(column=4, row=0, padx=20, sticky='E')

# Calling mainloop
main_window.config(menu=menubar)
main_window.mainloop();
