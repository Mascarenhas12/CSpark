import chess
import chess.pgn
import os


def create_raw_points_csv():
    with open('../results/points.csv') as result:
        for filename in os.listdir('../games/pgn/init_sample'):
            with open(filename, 'r') as pgn:
                game = chess.pgn.read_game(pgn)
