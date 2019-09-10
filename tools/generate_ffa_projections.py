'''
TODO: (Still a little more work to do:)
       1) Handle multiple entries of the same player (e.g. Sterling Shepard & Russel Shepard)
       2) Also refactor, break code up into functions and eventually into a single/multiple
          class object(s).
       3) Handle File locations - so we dont need to change it everytime week to week 
          (possibly providing arguments to provide specific week and tournament data)
'''
import pandas as pd
import numpy as np
import io
import sys

# Define file locations
ffa_projections = '/home/pete/Documents/projection_downloads/ff_analytics/ffa_customrankings2019-1.csv'
dk_salaries_template = '/home/pete/Documents/dk_player_exports/week1/sun_12_teams/DKSalaries.csv'
update_dk_template = '/home/pete/Documents/dk_player_exports/week1/sun_12_teams/DKSalaries_ffa.csv'

'''
Preprocess data so projections are not thrown off. In order for the projection to be correctly updated, 
The names of the players in the projection and the Draft Kings template need to make up exactly. In order for 
this to happen we need search the DK template file based off of the last name inside the projection file. Then
Update the ffa_projections with the exact name in the DK template. 
'''
ffa_data_frame = pd.read_csv(ffa_projections)
dk_data_frame = pd.read_csv(dk_salaries_template)

# filter projections to remove any players whos projected points is less than the specified value
value_threshold = 2.0
index_cutoffs = ffa_data_frame[ffa_data_frame['points'] <= value_threshold].index

# drop frames
ffa_data_frame.drop(index_cutoffs, inplace=True)

# Filter last names to remove ' from last names
excluded_character = '\''
last_names = list()
list_index = 0
dk_frame_index = 0
for names in dk_data_frame.Name:
    if (len(names.split()) > 1):
        last_names.append(names.split()[1])
        if (last_names[list_index].find(excluded_character) >= 0):
#            print(last_names[list_index])
#            print(last_names[list_index].replace(excluded_character, ''))
            dk_data_frame.at[dk_frame_index, 'Name'] = names.replace(excluded_character,'')
#            print(dk_data_frame.iloc[dk_frame_index])
        list_index += 1
    dk_frame_index += 1

# Change team names to match DK Templates
data_frame_index = 0
for team in ffa_data_frame.team:
    if (team == 'JAC'):
        ffa_data_frame.at[data_frame_index, 'team'] = 'JAX'
    data_frame_index += 1

players = ffa_data_frame['player'].tolist()
last_names = list()
for player in players:
    if (len(player.split()) == 1):
        last_names.append(player.split()[0])
    elif (len(player.split()) > 1):
        last_names.append(player.split()[1])

if (len(last_names) != len(players)):
    sys.exit('ERROR: last name and players dont match.') 

# Finding last name in DK templates
new_dk_data_frame = pd.DataFrame()
index = 0
for name in last_names:
#    print(name)
#    print(dk_data_frame['Name'].str.count(name).sum())
    name_count = dk_data_frame['Name'].str.count(name).sum()
    # If name_count == 0 they dont have a game in the dk_template
    if (name_count > 1 ):
        pos = ffa_data_frame.iloc[index].position 
        team = ffa_data_frame.iloc[index].team
        matched_names = dk_data_frame[dk_data_frame['Name'].str.contains(name)]
        matched_names = matched_names[matched_names['Position'].str.contains(pos)]
        matched_names = matched_names[matched_names['TeamAbbrev'].str.contains(team)]
#        print("name_count = ",name_count, ", Matched names = ",matched_names.shape[0])

        # Same last name at the same position on the same team. Which means we now need
        # to cross reference it to the ffa_data_frame
        if (matched_names.shape[0] > 1):
            dk_names = matched_names['Name'].tolist()
            for dk_name in dk_names:
                if(ffa_data_frame['player'].str.count(dk_name).sum() == 1):
                    matched_dk_data_frame = dk_data_frame[dk_data_frame['Name'].str.contains(dk_name)]
                    updated_value = ffa_data_frame.loc[ffa_data_frame.player == dk_name, 'points'].values[0]
                    matched_dk_index = matched_dk_data_frame.index[matched_dk_data_frame.Name == dk_name].tolist()
                    dk_data_frame.at[matched_dk_index, 'AvgPointsPerGame'] = updated_value
                    # TODO: Only append if they are not in the new_dk_data_frame
                    new_dk_data_frame = new_dk_data_frame.append([dk_data_frame.iloc[matched_dk_index]])

                # TODO: Add a else to handle potential errors (means the names may not match up 
                # Mavin Jones vs. Marvin Jones Jr.)
                else:
                    print("WARNING: Not in FFA projections list: ", dk_name, "Possible points = ", ffa_data_frame.iloc[index].points)
                    matched_dk_index = dk_data_frame.index[dk_data_frame.Name == dk_name].tolist()
                    first_name = dk_data_frame.iloc[matched_dk_index].Name.tolist()[0].split()[0]
                    first_name_ffa = ffa_data_frame.iloc[index].player.split()[0]
                    print(first_name, " : ", first_name_ffa, " = ", ffa_data_frame.iloc[index].points)
                    if (first_name_ffa == first_name):
                        dk_data_frame.at[matched_dk_index, 'AvgPointsPerGame'] = ffa_data_frame.iloc[index].points 
                    else:
                        dk_data_frame.at[matched_dk_index, 'AvgPointsPerGame'] = 0.0
                    new_dk_data_frame = new_dk_data_frame.append([dk_data_frame.iloc[matched_dk_index]])
        elif (matched_names.shape[0] == 1):
            updated_value = ffa_data_frame.iloc[index].points
            dk_name = matched_names.Name.tolist()[0]
            dk_index = matched_names.index[matched_names.Name == dk_name].tolist()
            dk_data_frame.at[dk_index, 'AvgPointsPerGame'] = updated_value
            new_dk_data_frame = new_dk_data_frame.append([dk_data_frame.iloc[dk_index]])

    elif (name_count == 1):
        updated_value = ffa_data_frame.iloc[index].points
        pos = ffa_data_frame.iloc[index].position
        team = ffa_data_frame.iloc[index].team
        matched_names = dk_data_frame[dk_data_frame['Name'].str.contains(name)]
        matched_names = matched_names[matched_names['Position'].str.contains(pos)]
        matched_names = matched_names[matched_names['TeamAbbrev'].str.contains(team)]

        if (matched_names.shape[0] == 1):
            dk_index = dk_data_frame.index[dk_data_frame['Name'].str.contains(name)].tolist()
            dk_data_frame.at[dk_index, 'AvgPointsPerGame'] = updated_value
            new_dk_data_frame = new_dk_data_frame.append([dk_data_frame.iloc[dk_index]])


    index += 1

#print(new_dk_data_frame)
new_dk_data_frame.to_csv(update_dk_template, index = False, encoding='utf8')
