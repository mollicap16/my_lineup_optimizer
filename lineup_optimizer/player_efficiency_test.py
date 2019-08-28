from pydfs_lineup_optimizer import get_optimizer, Site, Sport
import pandas

csv_player_path="/home/pete/projects/my_lineup_optimizer/data/draft_kings_players_template/DKSalaries.csv"

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv(csv_player_path)
for player in optimizer.players:
    print(player.first_name, " ", player.last_name, ": ", player.efficiency * 100)

