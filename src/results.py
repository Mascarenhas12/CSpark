import chess
import chess.pgn
from stockfish import Stockfish
import os

stock = Stockfish("/usr/games/stockfish")


def create_move_prob_dict_csv():
    with open('../results/move_prob_data.csv') as result:
        for filename in os.listdir('../games/pgn/init_sample'):
            with open(filename, 'r') as pgn:
                game = chess.pgn.read_game(pgn)
                # TODO
                """
                Go through every pgn and setup game
                Go through all positions
                Get all legal moves' evaluation in dict inside list
                Sort list based on evaluation
                Get index of next move played (ie determine rank of move)
                put in csv elo_rank, move_rank
                """
