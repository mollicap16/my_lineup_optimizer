from pydfs_lineup_optimizer import get_optimizer, Site, Sport
import pandas

csv_player_path="/home/pete/projects/my_lineup_optimizer/data/draft_kings_players_template/DKSalaries_thr-mon_9_5_19_fan_pro_proj.csv"

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv(csv_player_path)
players = optimizer.players

most_efficient_players = sorted(players, key=lambda x: x.efficiency, reverse=True)
num_of_players_to_display = 300

for player in most_efficient_players[0:num_of_players_to_display]:
    print(player.first_name, " ", player.last_name, ": ", player.efficiency * 1000)

