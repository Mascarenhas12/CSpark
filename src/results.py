import chess
import chess.pgn
from stockfish import Stockfish
from src.cspark import convert_dict_to_pawn_value as value
import os


def create_move_prob_data_csv(game_dir):
    # TODO: OPTIMIZATION use threading for files in directory
    """
               Go through every pgn and setup game DONE
               Go through all positions DONE
               Get all legal moves' evaluation inside list DONE
               Sort list based on evaluation DONE
               Get index of previous move played (ie determine rank of move) DONE
               put in csv elo_rank, move_rank
   """

    with open('../results/move_prob_data.csv', 'w') as result:
        result.write("elo_rank,move_rank\n")
        for filename in os.listdir(game_dir):
            with open(game_dir + filename, 'r') as pgn:
                game = chess.pgn.read_game(pgn)
                stock = Stockfish("/usr/games/stockfish")
                board = game.board()

                for move in game.mainline_moves():
                    base_fen = board.fen()
                    move_ev = []

                    for legal in board.legal_moves:
                        board.push_uci(legal.uci())
                        stock.set_fen_position(board.fen())
                        move_ev.append({"move": legal.uci(), "val": value(stock.get_evaluation())})
                        board.set_fen(base_fen)

                    new = sorted(move_ev, key=lambda m: m['val'], reverse=board.turn)
                    move_rank = next((index for (index, d) in enumerate(new) if d["move"] == move.uci()), None) + 1

                    elo = (game.headers['BlackElo'], game.headers['WhiteElo'])[board.turn]
                    elo_rank = "R" + str(int(elo) // 100)
                    result.write("" + elo_rank + "," + str(move_rank) + "\n")
                    board.push(move)
