import chess
import chess.pgn
from stockfish import Stockfish
from src.cspark import convert_dict_to_pawn_value as value
import os


def create_move_prob_dict_csv():
    """
               Go through every pgn and setup game DONE
               Go through all positions DONE
               Get all legal moves' evaluation inside list DONE
               Sort list based on evaluation DONE
               Get index of previous move played (ie determine rank of move) DONE
               put in csv elo_rank, move_rank
   """

    with open('../results/move_prob_data.csv', 'w') as result:
        for filename in os.listdir('../tests/resources'):
            with open("../tests/resources/" + filename, 'r') as pgn:
                game = chess.pgn.read_game(pgn)
                stock = Stockfish("/usr/games/stockfish")
                board = game.board()

                for move in game.mainline_moves():
                    base_fen = board.fen()
                    move_ev = []

                    for legal in board.legal_moves:
                        board.push_uci(legal.uci())
                        stock.set_fen_position(board.fen())
                        move_ev.append(value(stock.get_evaluation()))
                        board.set_fen(base_fen)

                    move_ev.sort()
                    move_ev.reverse()
                    board.push(move)
                    stock.set_fen_position(board.fen())
                    ev = value(stock.get_evaluation())
                    # NOT GOING TO WORK BECAUSE STOCKFISH GIVES DIFFERENT EVALUATIONS
                    move_rank = move_ev.index(list(filter(lambda x: x <= ev, move_ev))[0]) - 1
                    elo = (game.headers['WhiteElo'], game.headers['BlackElo'])[board.turn]
                    elo_rank = "R" + str(int(elo) // 100)
                    result.write("" + elo_rank + "," + str(move_rank))


create_move_prob_dict_csv()