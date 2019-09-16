from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter
import pandas

week = 'week2'
tournament = 'sun-1pm'
csv_player_path="/home/pete/Documents/dk_player_exports/WEEK/TOURNAMENT/DKSalaries_ffa.csv"
lineups_file="/home/pete/Documents/dk_lineups/WEEK/TOURNAMENT/results.csv"

csv_player_path = csv_player_path.replace("WEEK", week).replace("TOURNAMENT", tournament)
lineups_file = lineups_file.replace("WEEK", week).replace("TOURNAMENT", tournament)

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv(csv_player_path)
number_of_lineups = 15 
for lineup in optimizer.optimize(number_of_lineups):
    print(lineup)
#    print(lineup.players)
#    print(lineup.fantasy_points_projection)
#    print(lineup.salary_costs)

exporter = CSVLineupExporter(optimizer.optimize(number_of_lineups))
exporter.export(lineups_file)
# TODO: reformat the headers to match the approriate upload order for Draft Kings (QB, RB, RB, WR, WR, WR, TE, FLEX, DST)
