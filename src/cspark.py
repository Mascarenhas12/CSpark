from stockfish import Stockfish


class CSparkConfig:
    def __init__(self, pgn, colour, elo, opponent_elo):
        self.pgn = pgn
        self.colour = colour
        self.elo = elo
        self.opponent_elo = opponent_elo
        self.emv = self.estimated_move_value(elo)
        self.opponent_emv = self.estimated_move_value(opponent_elo)

    def get_pgn(self):
        return self.pgn

    def get_colour(self):
        return self.colour

    def get_elo(self):
        return self.elo

    def get_opponent_elo(self):
        return self.opponent_elo

    def get_emv(self):
        return self.emv

    def get_opponent_emv(self):
        return self.opponent_emv

    def estimated_move_value(self, elo):
        # TODO
        """
        Returns emv in table of emvs (external file) for the elo given
        :param elo:
        :return emv:
        """
        return 1


class CSpark:
    def __init__(self, config: CSparkConfig):
        self.stock = Stockfish("/usr/games/stockfish")
        self.config = config
        self.mlt = []
        self.mgt = []

    def move_val(self, pos_before, pos_after) -> float:
        self.stock.set_fen_position(pos_before)
        SE = self.stock.get_evaluation()
        self.stock.set_fen_position(pos_after)
        return self.convert_dict_to_pawn_value(self.stock.get_evaluation()) - self.convert_dict_to_pawn_value(SE)

    def is_player_turn(self, turn):
        return self.config.get_colour() == turn

    def convert_dict_to_pawn_value(self, evaluation: dict) -> float:
        return float(evaluation.get('value')) / 100

    def match_total_until_play_num(self, pos_list: list[str], play_num: int, start: int) -> None:
        turn = "white"
        limit = (2 * play_num - 1, 2 * play_num)[self.config.get_colour() == "white"]

        for i in range(start, limit - 1):
            SE = self.move_val(pos_list[i], pos_list[i + 1])

            if self.is_player_turn(turn):
                self.mlt.append(SE)
            else:
                self.mgt.append(SE)

            turn = ("white", "black")[turn == "white"]

    def match_average_until_play_num(self, pos_list: list[str], play_num: int) -> dict[float, float]:
        """
        :param pos_list:
        :param play_num:
        :return: dictionary of Match Loss Average and Match Gain Average
        """

        self.match_total_until_play_num(pos_list, play_num, len(self.mlt) + len(self.mgt))

        return dict(MLA=sum(self.mlt) / len(self.mlt), MGA=sum(self.mgt) / len(self.mgt))

    def raw_cspark_estimation(self, pos_list: list[str], play_num: int) -> float:
        match_averages = self.match_average_until_play_num(pos_list, play_num)
        self.stock.set_fen_position(pos_list[play_num])
        return self.convert_dict_to_pawn_value(self.stock.get_evaluation()) \
               + match_averages.get('MLA') \
               + match_averages.get('MGA')

    def cspark_estimation(self, pos_list: list[str], play_num: int, estimate_play_num: int = 1) -> float:
        match_averages = self.match_average_until_play_num(pos_list, play_num)
        self.stock.set_fen_position(pos_list[play_num])
        return self.convert_dict_to_pawn_value(self.stock.get_evaluation()) \
               + match_averages.get('MLA') * pow(self.config.get_emv(), estimate_play_num) \
               + match_averages.get('MGA') * pow(self.config.get_opponent_emv(), estimate_play_num)
