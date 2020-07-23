import sys
import tkinter as tk
import pandas as pd
from tkinter import ttk, filedialog, StringVar, IntVar
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter
from pandastable import Table

class LineupOptimizerGui:
    def printSomeStuff(text):
        print(text)
