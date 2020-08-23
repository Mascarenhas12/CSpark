import sys
from src.results import create_move_prob_data_csv as move_prob
from src.csv_parsing import csv_extract_ranked_move_prob_data as ranked_move_prob

[game_dir] = sys.argv[1:]

move_prob(game_dir)
for i in range(0, 31):
    ranked_move_prob('../results/move_prob_data.csv', "R" + str(i))
