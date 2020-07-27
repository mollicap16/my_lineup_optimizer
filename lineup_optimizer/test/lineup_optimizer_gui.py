import sys
import tkinter as tk
import pandas as pd
from tkinter import ttk, filedialog, StringVar, IntVar
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter
from pandastable import Table

# TODO: Remove after debugging
class MyFirstGui:
    def __init__(self, master):
        self.master = master
        master.title("A simple Gui")

        self.label = tk.Label(master, text="This is our first example GUI class")
        self.label.pack()

        self.greet_button = tk.Button(master, text="Greet", command = self.greet)
        self.greet_button.pack()

        self.close_button = tk.Button(master, text="Close", command = master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings all!")

class LineupOptimizerGui():
    def __init__(self, master):
        self.player_file=""
        self.optimizer=get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
        self.locked_player_list=[]
        self.excluded_player_list=[]
        self.player_value=[]
        self.ffa_player_projections = pd.DataFrame()

        self.master = master 
        master.title("Lineup Optimizer")

        self.selected_sport=tk.IntVar(master, value=1)

        ttk.Sizegrip(master).grid(column=999, row=999, sticky=('SE'))

        # Setting up Frames on master window
        self.top_frame = ttk.Frame(master, borderwidth=4, relief='sunken')
        self.top_frame.grid(column=0, row=0, columnspan=2, sticky=('N', 'W', 'E', 'S'))

        self.middle_left_frame = ttk.Frame(master, borderwidth=4, relief='sunken')
        self.middle_left_frame.grid(column=0, row=1, sticky=('N', 'W', 'E', 'S'))

        self.middle_right_frame = ttk.Frame(master, borderwidth=4, relief='sunken')
        self.middle_right_frame.grid(column=1, row=1)

        self.bottom_frame = ttk.Frame(master, borderwidth=4, relief='sunken')
        self.bottom_frame.grid(column=0, row=2, columnspan=2, sticky=('N', 'W', 'E', 'S'))
        
        self.locked_player_frame = ttk.Frame(self.middle_right_frame, borderwidth=4, relief='sunken')
        self.locked_player_frame.grid(column=0, row=0)

        self.excluded_player_frame = ttk.Frame(self.middle_right_frame, borderwidth=4, relief='sunken')
        self.excluded_player_frame.grid(column=0, row=1)
        
        # Menu 
        self.menubar = tk.Menu(master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.sportsmenu = tk.Menu(self.menubar, tearoff=0)
        self.sportsmenu.add_radiobutton(label="NFL", value=1, variable=self.selected_sport)
        self.sportsmenu.add_radiobutton(label="NHL", value=2, variable=self.selected_sport)

        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Select Sport', menu = self.sportsmenu)

        # List box
        self.locked_player_listbox = tk.Listbox(self.locked_player_frame, height=10)
        self.locked_player_listbox.grid(column = 0, row = 1, columnspan=2, sticky=('N', 'W', 'E', 'S'))
        self.excluded_player_listbox = tk.Listbox(self.excluded_player_frame)
        self.excluded_player_listbox.grid(column=0, row=1, columnspan=2, sticky=('N', 'W', 'E', 'S'))

        # Labels
        self.load_label = ttk.Label(self.top_frame, text="Empty", background='white', relief='groove', width=50)
        self.load_label.grid(column=1, row=0, sticky='E')
        self.num_lineup_label = ttk.Label(self.bottom_frame, text="Number of Lineups")
        self.num_lineup_label.grid(column=3, row=0, sticky='W')
        self.locked_player_label = ttk.Label(self.locked_player_frame, text='Locked Players', font='-weight bold')
        self.locked_player_label.grid(column=0, row=0, columnspan=2, sticky=('N', 'W', 'E', 'S'))
        self.excluded_player_label = ttk.Label(self.excluded_player_frame, text='Excluded Players', font='-weight bold')
        self.excluded_player_label.grid(column=0, row=0, columnspan=2, sticky=('N', 'W', 'E', 'S'))

        # Entries
        self.num_lineups=tk.StringVar()
        self.num_lineups.set(20)
        self.num_of_lineups_entry = ttk.Entry(self.bottom_frame, textvariable=self.num_lineups, justify='center', width=10)
        self.num_of_lineups_entry.grid(column=2, row=0, sticky='W', padx=(25,5))

        # Buttons
        self.load_button = ttk.Button(self.top_frame, text="Load", command=self.load_click)
        self.load_button.grid(column=0, row=0, sticky="W")
        self.optimize_button = ttk.Button(self.bottom_frame, text="Optimize Lineups", command=self.optimize_click, state='disabled')
        self.optimize_button.grid(column=1, row=0, sticky="E")
        self.save_button = ttk.Button(self.bottom_frame, text="Save Lineups", command=self.save_click, state='disabled')
        self.save_button.grid(column=0, row=0, sticky="W")
        self.add_lock_button = ttk.Button(self.locked_player_frame, text="Add Player", command=self.add_locked_player_click, state='disabled')
        self.add_lock_button.grid(column=0, row=2, sticky='W')
        self.add_exclude_button = ttk.Button(self.excluded_player_frame, text="Add Player", command=self.add_excluded_player_click, state='disabled')
        self.add_exclude_button.grid(column=0, row=2, sticky='W')
        self.remove_lock_button = ttk.Button(self.locked_player_frame, text="Remove Player", command=self.remove_locked_player_click, state='disabled')
        self.remove_lock_button.grid(column=1, row=2, sticky='E')
        self.remove_exclude_button = ttk.Button(self.excluded_player_frame, text="Remove player", command=self.remove_excluded_player_click, state='disabled')
        self.remove_exclude_button.grid(column=1, row=2, sticky='E')

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.bottom_frame, orient='horizontal', mode='determinate')
        self.progress_bar.grid(column=4, row=0, padx=20, sticky='E')

        #This just tells Tk that if the master window is resized the frame should expand with it
        master.columnconfigure(0, weight =1)
        master.rowconfigure(1, weight =1)

        self.table = Table(self.middle_left_frame)

        master.config(menu=self.menubar)

    # Command Functions
    def load_click(self):
        init_dir = ""
        if (self.selected_sport.get() == 1):
            init_dir = "/home/pete/Documents/dk_player_exports/"
        elif (self.selected_sport.get() == 2):
            init_dir = "/home/pete/Documents/nhl/dk_player_exports/"
        else: 
            sys.exit("INVALID SPORT SELECTED")
        self.player_file = filedialog.askopenfilename(initialdir=init_dir, title="Selected Projections")
        self.load_label.configure(text=self.player_file, width=0)
        self.save_button.state(['disabled'])
        self.optimize_button.state(['!disabled'])
        try:
            self.ffa_player_projections = pd.read_csv (self.player_file)
            self.load_optimizer()
            self.add_value_column()
            self.ffa_player_projections = self.ffa_player_projections.assign(Value = self.player_value)
        except:
            sys.exit("Invalid file type")
        self.table = Table(self.middle_left_frame, dataframe=self.ffa_player_projections)
        self.table.show()
        self.add_lock_button.state(['!disabled'])
        self.add_exclude_button.state(['!disabled'])
        self.remove_lock_button.state(['!disabled'])
        self.remove_exclude_button.state(['!disabled'])

    def optimize_click(self):
        self.lock_players()
        self.exclude_players()
        lineups = self.optimizer.optimize(int(self.num_lineups.get()))
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = int(self.num_lineups.get())
        print("Clicked Optimize")

    def save_click(self):
        print("Clicked Save")
    
    def add_locked_player_click(self):
        row = self.table.getSelectedRow()
        player = self.ffa_player_projections.iloc[row].Name
        if (player not in self.locked_player_list and player not in self.excluded_player_list):
            self.locked_player_list.append(player)
        print(player)
        print("Add Locked Player")
        print(self.locked_player_list)

        self.locked_player_listbox.delete(0, 'end')
        for item in self.locked_player_list:
            self.locked_player_listbox.insert('end', item)

    def remove_locked_player_click(self):
        player = self.locked_player_listbox.get('active')
        if (player in self.locked_player_list):
            self.locked_player_list.remove(player)

        self.locked_player_listbox.delete(0, 'end')
        for item in self.locked_player_list:
            self.locked_player_listbox.insert('end', item)
        print(self.locked_player_list)
        print("Remove locked Player")

    def add_excluded_player_click(self):
        row = self.table.getSelectedRow()
        player = self.ffa_player_projections.iloc[row].Name
        if (player not in self.excluded_player_list and player not in self.locked_player_list):
            self.excluded_player_list.append(player)

        self.excluded_player_listbox.delete(0, 'end')
        for item in self.excluded_player_list:
            self.excluded_player_listbox.insert('end', item)
        print(self.excluded_player_list)
        print("Add Excluded Player")


    def remove_excluded_player_click(self):
        player = self.excluded_player_listbox.get('active')
        if (player in self.excluded_player_list):
            self.excluded_player_list.remove(player)

        self.excluded_player_listbox.delete(0, 'end')
        for item in self.excluded_player_list:
            self.excluded_player_listbox.insert('end', item)
        print("Removed Excluded Player")

    # Helper Functions
    def load_optimizer(self):
        if (self.selected_sport.get() == 1):
            self.optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
        elif (self.selected_sport.get() == 2):
            self.optimizer = get_optimizer(Site.DRAFTKINGS, Sport.HOCKEY)
        try:
            self.optimizer.load_players_from_csv(self.player_file)
        except:
            sys.exit("Invalid csv file format")

    def add_value_column(self):
        self.player_value = []
        players = self.optimizer.players
        for player in players:
            self.player_value.append(player.efficiency*1000)
    
    def lock_players(self):
        for player_name in self.locked_player_list:
            player = self.optimizer.get_player_by_name(player_name)
            self.optimizer.add_player_to_lineup(player)
            print(player)
        print("lock_players()")

    def exclude_players(self):
        for player_name in self.excluded_player_list:
            player = self.optimizer.get_player_by_name(player_name)
            self.optimizer.remove_player(player)
            print(player)
        print("exclude_players")
