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

    def estimated_move_value(self,elo):
        #TODO
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
        self.mlt = 0
        self.mgt = 0

    def move_val(self, pos_before, pos_after):
        self.stock.set_fen_position(pos_before)
        SE = self.stock.get_evaluation()
        self.stock.set_fen_position(pos_after)
        return self.stock.get_evaluation().get('value')/100 - SE.get('value')/100



