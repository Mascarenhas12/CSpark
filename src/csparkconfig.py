import chess
import chess.pgn
from utils import extract_elo_from_pgn, estimated_move_value

DEFAULT_EMV = {
    "R14": 2,
    "R15": 1.5
    }
DEFAULT_MOVE_PROB = {}


class CSparkConfig:
    def __init__(self, pgn_path, colour: str, emv_dict: dict = DEFAULT_EMV, move_prob_dict: dict = DEFAULT_MOVE_PROB):
        self.pgn_path = pgn_path
        self.colour = colour
        self.elo_dict = extract_elo_from_pgn(pgn_path, colour)
        self.emv = estimated_move_value(emv_dict, self.elo_dict.get('elo'))
        self.opponent_emv = estimated_move_value(emv_dict, self.elo_dict.get('opponent_elo'))
        self.move_prob_dict = move_prob_dict

    def get_pgn(self):
        return self.pgn_path

    def get_colour(self):
        return self.colour

    def get_elo(self):
        return self.elo_dict.get('elo')

    def get_opponent_elo(self):
        return self.elo_dict.get('opponent_elo')

    def get_emv(self):
        return self.emv

    def get_opponent_emv(self):
        return self.opponent_emv

    def get_move_prob_dict(self):
        return self.move_prob_dict

    def get_fen_list_from_pgn(self):
        fen_list = []
        with open(self.pgn_path, 'r') as pgn:
            game = chess.pgn.read_game(pgn)

        board = game.board()
        fen_list.append(board.fen())

        for move in game.mainline_moves():
            board.push(move)
            fen_list.append(board.fen())

        return fen_list
