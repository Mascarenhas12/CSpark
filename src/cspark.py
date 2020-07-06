from stockfish import Stockfish
import chess
import chess.pgn


def extract_elo_from_pgn(pgn, colour):
    elo_dict = dict()

    game = chess.pgn.read_game(pgn)

    if colour == "white":
        elo_dict['elo'] = game.headers.get('WhiteElo')
        elo_dict['opponent_elo'] = game.headers.get('BlackElo')
    else:
        elo_dict['elo'] = game.headers.get('BlackElo')
        elo_dict['opponent_elo'] = game.headers.get('WhiteElo')

    return elo_dict


def estimated_move_value(emv_dict: dict, elo):
    # 1400-1499 elo is R14
    rank = "R" + str(elo / 100)
    return emv_dict.get(rank)


class CSparkConfig:
    def __init__(self, pgn, colour, emv_dict):
        self.pgn = pgn
        self.colour = colour
        self.elo_dict = extract_elo_from_pgn(pgn, colour)
        self.emv = estimated_move_value(emv_dict, self.elo_dict.get('elo'))
        self.opponent_emv = estimated_move_value(emv_dict, self.elo_dict.get('opponent_elo'))

    def get_pgn(self):
        return self.pgn

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

    def get_fen_list_from_pgn(self):
        fen_list = []
        game = chess.pgn.read_game(self.pgn)
        board = game.board()

        for move in game.mainline_moves():
            board.push(move)
            fen_list.append(board.fen())

        return fen_list


def convert_dict_to_pawn_value(evaluation: dict) -> float:
    return float(evaluation.get('value')) / 100


class CSpark:
    def __init__(self, config: CSparkConfig):
        self.stock = Stockfish("/usr/games/stockfish")
        self.config = config
        self.pos_list = config.get_fen_list_from_pgn()
        self.mlt = []
        self.mgt = []

    def move_val(self, pos_before, pos_after) -> float:
        self.stock.set_fen_position(pos_before)
        se = self.stock.get_evaluation()
        self.stock.set_fen_position(pos_after)
        return convert_dict_to_pawn_value(self.stock.get_evaluation()) - convert_dict_to_pawn_value(se)

    def match_total_until_play_num(self, play_num: int, start: int) -> None:
        """
        :param play_num: number of the current play
        :param start:
        :return:
        """
        turn = "white"
        limit = (2 * play_num - 1, 2 * play_num)[self.config.get_colour() == "white"]

        for i in range(start, limit - 1):
            se = self.move_val(self.pos_list[i], self.pos_list[i + 1])

            if turn == "white":
                self.mlt.append(se)
            else:
                self.mgt.append(se)

            turn = ("white", "black")[turn == "white"]

    def match_average_until_play_num(self, play_num: int) -> dict[float, float]:
        """
        #TODO : method when asked to get match averages of a previous play
        :param play_num: number of the current play
        :return: dictionary of Match Loss Average and Match Gain Average
        """

        self.match_total_until_play_num(play_num, len(self.mlt) + len(self.mgt))

        return dict(MLA=sum(self.mlt) / len(self.mlt), MGA=sum(self.mgt) / len(self.mgt))

    def raw_cspark_estimation(self, play_num: int) -> float:
        match_averages = self.match_average_until_play_num(play_num)
        self.stock.set_fen_position(self.pos_list[play_num])
        return convert_dict_to_pawn_value(self.stock.get_evaluation()) \
               + match_averages.get('MLA') \
               + match_averages.get('MGA')

    def average_position_evaluation(self, position):
        se_total = 0
        board = chess.Board()
        board.set_fen(position)
        legal = board.legal_moves

        for move in legal:
            board.set_fen(position)
            board.push(move)
            self.stock.set_fen_position(board.fen())
            se_total += convert_dict_to_pawn_value(self.stock.get_evaluation())

        board.set_fen(position)
        return se_total / board.legal_moves.count()

    def cspark_estimation(self, play_num: int, estimate_play_num: int = 1) -> float:
        """
        :param play_num: number of the current play
        :param estimate_play_num: number of plays (for each player) ahead to which estimate
        :return: cspark estimation in pawn value
        """
        match_averages = self.match_average_until_play_num(play_num)
        se_avg = self.average_position_evaluation(self.pos_list[play_num])
        return se_avg \
               + match_averages.get('MLA') * pow(self.config.get_emv(), estimate_play_num) \
               + match_averages.get('MGA') * pow(self.config.get_opponent_emv(), estimate_play_num)
