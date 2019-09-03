from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter
import pandas

csv_player_path="/home/pete/projects/my_lineup_optimizer/data/draft_kings_players_template/DKSalaries.csv"
lineups_file="/home/pete/projects/my_lineup_optimizer/lineup_optimizer/lineups/results.csv"

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv(csv_player_path)
number_of_lineups = 20 
for lineup in optimizer.optimize(number_of_lineups):
    print(lineup)
#    print(lineup.players)
#    print(lineup.fantasy_points_projection)
#    print(lineup.salary_costs)

exporter = CSVLineupExporter(optimizer.optimize(number_of_lineups))
exporter.export(lineups_file)