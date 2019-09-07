import pandas as pd
import numpy as np
import io

week_1_files = "/home/pete/projects/my_lineup_optimizer/data/projections/2019/week1/"
position_projections = ["FantasyPros_Fantasy_Football_Projections_DST.csv", "FantasyPros_Fantasy_Football_Projections_QB.csv",
        "FantasyPros_Fantasy_Football_Projections_RB.csv", "FantasyPros_Fantasy_Football_Projections_TE.csv",
        "FantasyPros_Fantasy_Football_Projections_WR.csv"]

dk_player_salaries = "/home/pete/projects/my_lineup_optimizer/data/draft_kings_players_template/DKSalaries_thr-mon_9_5_19.csv"

updated_dk_player_projections = "/home/pete/projects/my_lineup_optimizer/data/draft_kings_players_template/DKSalaries_thr-mon_9_5_19_fan_pro_proj.csv"

# Each projection file (QB, RB, WR, TE, and DST)
qb_file = week_1_files + position_projections[1]
wr_file = week_1_files + position_projections[4]
rb_file = week_1_files + position_projections[2]
te_file = week_1_files + position_projections[3]
dst_file = week_1_files + position_projections[0]

# Load file projections
qb_data = pd.read_csv(qb_file)
wr_data = pd.read_csv(wr_file)
rb_data = pd.read_csv(rb_file)
te_data = pd.read_csv(te_file)
dst_data = pd.read_csv(dst_file)
dk_salaries_data = pd.read_csv(dk_player_salaries)

all_projection_data_frames = [qb_data, wr_data, rb_data, te_data, dst_data]

players_fpts_data_frame = pd.DataFrame()

#Player is the first column and FPTS is the last column of each csv projection file
for data in all_projection_data_frames:
    column = data.columns
    column_size = len(column)
    players_fpts_data = data[[column[0],column[column_size - 1]]]
    players_fpts_data_frame = players_fpts_data_frame.append([players_fpts_data])

# Save complete list of players and their projected fantasy points
players_fpts_data_frame.to_csv(week_1_files+"complete_player_projection.csv", index=False, encoding='utf8')

# Replace "AvgPointsPerGame" in the draft kings template with the projected fantasy pro's "FPTS"
players_fpts_data_frame = players_fpts_data_frame[np.isfinite(players_fpts_data_frame['FPTS'])]
for player in players_fpts_data_frame.Player:
    print(player)
    player_fpts_value = players_fpts_data_frame.loc[players_fpts_data_frame.Player == player,'FPTS'].values[0]
    dk_avg_pts_player = dk_salaries_data.loc[dk_salaries_data.Name == player].AvgPointsPerGame.values[0]
    dk_player_index = dk_salaries_data.index[dk_salaries_data.Name == player].tolist()
    dk_salaries_data.at[dk_player_index , 'AvgPointsPerGame'] = player_fpts_value
#    print(player, ": ", player_fpts_value)
    print(player, ": ", dk_player_index)
    print(player, ": ", dk_avg_pts_player)
    print(player, ": ", dk_salaries_data.loc[dk_salaries_data.Name == player].AvgPointsPerGame.values[0])

dk_salaries_data.to_csv(updated_dk_player_projections, index=False, encoding='utf8')
