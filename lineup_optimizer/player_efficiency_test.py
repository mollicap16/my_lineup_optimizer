from pydfs_lineup_optimizer import get_optimizer, Site, Sport
import pandas

week = 'week4'
tournament = 'thur-mon'
csv_player_path = "/home/pete/Documents/dk_player_exports/WEEK/TOURNAMENT/DKSalaries_ffa.csv"
csv_player_path = csv_player_path.replace('WEEK', week).replace('TOURNAMENT',tournament)

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv(csv_player_path)
players = optimizer.players

most_efficient_players = sorted(players, key=lambda x: x.efficiency, reverse=True)
num_of_players_to_display = 300

for player in most_efficient_players[0:num_of_players_to_display]:
    print(player.first_name, " ", player.last_name, ": ", player.efficiency * 1000)

