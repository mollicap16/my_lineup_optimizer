#import pandas as pd
import csv
import operator

csv_player_data_file="/home/pete/projects/my_lineup_optimizer/data/draft_kings_players_template/DKSalaries.csv"

player_data = csv.reader(open(csv_player_data_file), delimiter=',')

print(player_data(0))

#for player in player_data:
#    print(player)

