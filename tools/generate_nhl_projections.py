import pandas as pd
import numpy as np
import io
import sys

# Define file locations
date = '2020-08-02'
nhl_projections = '/home/pete/Documents/nhl/projection_downloads/DFF_NHL_cheatsheet_DATE.csv'
dk_salaries_template = '/home/pete/Documents/nhl/dk_player_exports/DATE/DKSalaries.csv'
update_dk_template = '/home/pete/Documents/nhl/dk_player_exports/DATE/DKSalaries_dff.csv'

nhl_projections = nhl_projections.replace("DATE", date)
dk_salaries_template = dk_salaries_template.replace("DATE", date)
update_dk_template = update_dk_template.replace("DATE", date)

nhl_data_frame = pd.read_csv(nhl_projections)
dk_data_frame = pd.read_csv(dk_salaries_template)

# filter projections to remove any players whos projected points is less than the specified value
value_threshold = 2.0
index_cutoffs = nhl_data_frame[nhl_data_frame['ppg_projection'] <= value_threshold].index

# drop frames
nhl_data_frame.drop(index_cutoffs, inplace=True)

# Change team names to match DK Templates
data_frame_index = 0
for team in nhl_data_frame.team:
    if (team == 'CBJ'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'CLS'
    if (team == 'MTL'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'MON'
    if (team == 'WSH'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'WAS'
    if (team == 'SJS'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'SJ'
    if (team == 'NJD'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'NJ'
    if (team == 'LAK'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'LA'
    if (team == 'TBL'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'TB'
    if (team == 'ANA'):
        nhl_data_frame.at[data_frame_index, 'team'] = 'ANH'
    data_frame_index += 1

print(dk_data_frame.TeamAbbrev.unique(), "\n")
print(nhl_data_frame.team.unique())

names = list()
for index, row in nhl_data_frame.iterrows():
    full_name = row.first_name + " " + row.last_name
    names.append(full_name)

# Finding last name in DK templates
new_dk_data_frame = pd.DataFrame()
index = 0
for name in names:
    name_count = dk_data_frame['Name'].str.count(name).sum()
    if (name_count > 1):
        print("Warning: More than one player with the same name", name)
        projected_points = nhl_data_frame.iloc[index].ppg_projection
        team = nhl_data_frame.iloc[index].team
        pos = nhl_data_frame.iloc[index].position
        matched_players = dk_data_frame[dk_data_frame['Name'].str.contains(name)]
        matched_players = matched_players[matched_players['TeamAbbrev'].str.contains(team)]
        matched_players = matched_players[matched_players['Position'].str.contains(pos)]

        if (matched_players.shape[0] > 1):
            print("ERROR: Multiple Players with the same name (", name,")")
            sys.exit()
        else:
            dk_index = matched_players[matched_players['Name'].str.contains(name)].index.values[0]
            new_dk_data_frame = new_dk_data_frame.append(matched_players[matched_players['Name'].str.contains(name)])
            new_dk_data_frame.at[dk_index,'AvgPointsPerGame'] = projected_points
    else:
        projected_points = nhl_data_frame.iloc[index].ppg_projection
        dk_index = dk_data_frame[dk_data_frame['Name'].str.contains(name)].index.values[0]
        new_dk_data_frame = new_dk_data_frame.append(dk_data_frame[dk_data_frame['Name'].str.contains(name)])
        new_dk_data_frame.at[dk_index,'AvgPointsPerGame'] = projected_points
    index +=1

new_dk_data_frame.to_csv(update_dk_template, index = False, encoding='utf8')
