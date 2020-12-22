from stockfish import Stockfish
import chess
import chess.pgn
from csparkconfig import CSparkConfig
from utils import convert_dict_to_pawn_value


class CSpark:
    def __init__(self, config: CSparkConfig):
        self.stock = Stockfish("/usr/games/stockfish")
        self.config = config
        self.pos_list = config.get_fen_list_from_pgn()
        self.mlt = []
        self.mgt = []

    def get_position(self, pos: int) -> str:
        if 0 <= pos <= len(self.pos_list):
            self.stock.set_fen_position(self.pos_list[pos])
            return self.stock.get_board_visual()
        return "Position outside of scope"

    def move_val(self, pos_before, pos_after) -> float:
        self.stock.set_fen_position(pos_before)
        se = self.stock.get_evaluation()
        self.stock.set_fen_position(pos_after)
        return abs(convert_dict_to_pawn_value(self.stock.get_evaluation()) - convert_dict_to_pawn_value(se))

    def match_total_until_play_num(self, play_num: int, start: int) -> None:
        """
        :param play_num: number of the current play
        :param start:
        :return:
        """
        turn = "white"
        limit = (2 * play_num - 1, 2 * play_num)[self.config.get_colour() == "white"]

        for i in range(start, limit):
            se = self.move_val(self.pos_list[i], self.pos_list[i + 1])

            if turn == "white":
                self.mlt.append(se)
            else:
                self.mgt.append(se)

            turn = ("white", "black")[turn == "white"]

    def match_average_until_play_num(self, play_num: int) -> dict:
        """
        #TODO: *OPTIMIZATION* method when asked to get match averages of a previous play
        :param play_num: number of the current play
        :return: dictionary of Match Loss Average and Match Gain Average
        """

        self.match_total_until_play_num(play_num, len(self.mlt) + len(self.mgt))
        print(self.mlt)
        print(self.mgt)
        return dict(MLA=sum(self.mlt) / len(self.mlt), MGA=sum(self.mgt) / len(self.mgt))

    def sorted_value_list(self, fen_position):
        board = chess.Board()
        board.set_fen(fen_position)
        legal = board.legal_moves
        val_list = []

        for move in legal:
            board.set_fen(fen_position)
            board.push(move)
            self.stock.set_fen_position(board.fen())
            val_list.append(convert_dict_to_pawn_value(self.stock.get_evaluation()))

        board.set_fen(fen_position)
        val_list.sort()
        if self.config.get_colour() == "white":
            val_list.reverse()
        return val_list

    def conditional_position_evaluation(self, fen_position):
        cpe = 0
        val_list = self.sorted_value_list(fen_position)

        for i in range(len(val_list)):
            cpe += self.config.get_move_prob_dict().get(str(i)) * val_list[i]

        return cpe

    def cspark_estimation(self, play_num: int, estimate_play_num: int = 1) -> float:
        """
        :param play_num: number of the current play
        :param estimate_play_num: number of plays (for each player) ahead to which estimate
        :return: cspark estimation in pawn value
        """
        match_averages = self.match_average_until_play_num(play_num)
        cpe = self.conditional_position_evaluation(self.pos_list[play_num])
        return cpe \
               - match_averages.get('MLA') * pow(self.config.get_emv(), estimate_play_num) \
               + match_averages.get('MGA') * pow(self.config.get_opponent_emv(), estimate_play_num)

    def guess_next_move(self, play_num: int):
        cse = self.cspark_estimation(play_num)
        fen_position = self.pos_list[play_num]
        board = chess.Board()
        board.set_fen(fen_position)
        legal = board.legal_moves
        difference = 0
        guess = None

        for move in legal:
            board.set_fen(fen_position)
            board.push(move)
            self.stock.set_fen_position(board.fen())
            if difference > abs(convert_dict_to_pawn_value(self.stock.get_evaluation()) - cse):
                difference = abs(convert_dict_to_pawn_value(self.stock.get_evaluation()) - cse)
                guess = move.__str__()

        return guess

    def __del__(self):
        self.stock.stockfish.kill()
        self.stock.stockfish.wait()
