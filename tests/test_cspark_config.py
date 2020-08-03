import unittest
import os
from src.cspark import CSparkConfig
from src.cspark import estimated_move_value
from src.cspark import convert_dict_to_pawn_value


class CSparkConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config = CSparkConfig(dir_path+ "/resources/2vincent2 vs docboss,1399394103794.pgn",
                                   "white",
                                   {
                                       "R14": 2,
                                       "R15": 1.5
                                   },
                                   None
                                   )

    def tearDown(self) -> None:
        del self.config

    def test_estimated_move_value(self):
        emv_dict = {"R14": 2, "R15": 1.5}
        self.assertEqual(estimated_move_value(emv_dict, 1400), 2)
        self.assertEqual(estimated_move_value(emv_dict, 1499), 2)
        self.assertEqual(estimated_move_value(emv_dict, 1500), 1.5)
        self.assertEqual(estimated_move_value(emv_dict, 1538), 1.5)

    def test_convert_dict_to_pawn_value(self):
        self.assertEqual(convert_dict_to_pawn_value({"type": "cp", "value": 100}), 1)
        self.assertEqual(convert_dict_to_pawn_value({"type": "cp", "value": 0}), 0)
        self.assertEqual(convert_dict_to_pawn_value({"type": "cp", "value": -100}), -1)
        self.assertEqual(convert_dict_to_pawn_value({"type": "mate", "value": 1}), 317.65)
        self.assertEqual(convert_dict_to_pawn_value({"type": "mate", "value": 6}), 267.65)
        self.assertEqual(convert_dict_to_pawn_value({"type": "mate", "value": -1}), -317.65)

    def test_extract_elo_from_pgn(self):
        self.assertEqual(self.config.get_elo(), "1486")
        self.assertEqual(self.config.get_opponent_elo(), "1539")

    def test_get_fen_list_from_pgn(self):
        self.assertEqual(self.config.get_fen_list_from_pgn(),
                         ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                          'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1',
                          'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2',
                          'rnbqkbnr/pppp1ppp/8/4p3/4P3/2P5/PP1P1PPP/RNBQKBNR b KQkq - 0 2',
                          'rnbqkbnr/pppp1pp1/7p/4p3/4P3/2P5/PP1P1PPP/RNBQKBNR w KQkq - 0 3',
                          'rnbqkbnr/pppp1pp1/7p/4p3/4P3/2P2N2/PP1P1PPP/RNBQKB1R b KQkq - 1 3',
                          'rnb1kbnr/pppp1pp1/5q1p/4p3/4P3/2P2N2/PP1P1PPP/RNBQKB1R w KQkq - 2 4',
                          'rnb1kbnr/pppp1pp1/5q1p/4p3/3PP3/2P2N2/PP3PPP/RNBQKB1R b KQkq - 0 4',
                          'rnb1kbnr/ppp2pp1/3p1q1p/4p3/3PP3/2P2N2/PP3PPP/RNBQKB1R w KQkq - 0 5',
                          'rnb1kbnr/ppp2pp1/3p1q1p/4p3/2BPP3/2P2N2/PP3PPP/RNBQK2R b KQkq - 1 5',
                          'rnb1kb1r/ppp1npp1/3p1q1p/4p3/2BPP3/2P2N2/PP3PPP/RNBQK2R w KQkq - 2 6',
                          'rnb1kb1r/ppp1npp1/3p1q1p/4p3/2BPP3/2P1BN2/PP3PPP/RN1QK2R b KQkq - 3 6',
                          'rnb1kb1r/ppp2pp1/3p1qnp/4p3/2BPP3/2P1BN2/PP3PPP/RN1QK2R w KQkq - 4 7',
                          'rnb1kb1r/ppp2pp1/3p1qnp/4p3/2BPP3/2P1BN2/PP1N1PPP/R2QK2R b KQkq - 5 7',
                          'rnb1k2r/ppp1bpp1/3p1qnp/4p3/2BPP3/2P1BN2/PP1N1PPP/R2QK2R w KQkq - 6 8',
                          'rnb1k2r/ppp1bpp1/3p1qnp/4P3/2B1P3/2P1BN2/PP1N1PPP/R2QK2R b KQkq - 0 8',
                          'rnb1k2r/ppp1bpp1/3p1q1p/4n3/2B1P3/2P1BN2/PP1N1PPP/R2QK2R w KQkq - 0 9',
                          'rnb1k2r/ppp1bpp1/3p1q1p/4n3/2BBP3/2P2N2/PP1N1PPP/R2QK2R b KQkq - 1 9',
                          'rn2k2r/ppp1bpp1/3p1q1p/4n3/2BBP1b1/2P2N2/PP1N1PPP/R2QK2R w KQkq - 2 10',
                          'rn2k2r/ppp1bpp1/3p1q1p/4n3/2BBP1b1/2P2N1P/PP1N1PP1/R2QK2R b KQkq - 0 10',
                          'rn2k2r/ppp1bpp1/3p1q1p/4n3/2BBP3/2P2b1P/PP1N1PP1/R2QK2R w KQkq - 0 11',
                          'rn2k2r/ppp1bpp1/3p1q1p/4n3/2BBP3/2P2N1P/PP3PP1/R2QK2R b KQkq - 0 11',
                          'rn2k2r/ppp1bpp1/3p1q1p/8/2BBP3/2P2n1P/PP3PP1/R2QK2R w KQkq - 0 12',
                          'rn2k2r/ppp1bpp1/3p1q1p/8/2BBP3/2P2Q1P/PP3PP1/R3K2R b KQkq - 0 12',
                          'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2q1P/PP3PP1/R3K2R w KQkq - 0 13',
                          'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2P1P/PP3P2/R3K2R b KQkq - 0 13',
                          'rn2k2r/ppp1b1p1/3p1p1p/8/2BBP3/2P2P1P/PP3P2/R3K2R w KQkq - 0 14',
                          'rn2k2r/ppp1b1p1/3p1p1p/8/2BBPP2/2P4P/PP3P2/R3K2R b KQkq - 0 14',
                          'r3k2r/pppnb1p1/3p1p1p/8/2BBPP2/2P4P/PP3P2/R3K2R w KQkq - 1 15',
                          'r3k2r/pppnb1p1/3p1p1p/8/2BBPP2/2P4P/PP3P2/2KR3R b kq - 2 15',
                          'r3k2r/pp1nb1p1/3p1p1p/2p5/2BBPP2/2P4P/PP3P2/2KR3R w kq - 0 16',
                          'r3k2r/pp1nb1p1/3p1p1p/2p5/2B1PP2/2P1B2P/PP3P2/2KR3R b kq - 1 16',
                          '2kr3r/pp1nb1p1/3p1p1p/2p5/2B1PP2/2P1B2P/PP3P2/2KR3R w - - 2 17',
                          '2kr3r/pp1nb1p1/3p1p1p/2p5/2B1PP2/2P1B2P/PP3P2/2KRR3 b - - 3 17',
                          '2kr3r/pp2b1p1/1n1p1p1p/2p5/2B1PP2/2P1B2P/PP3P2/2KRR3 w - - 4 18',
                          '2kr3r/pp2b1p1/1n1p1p1p/2p5/4PP2/1BP1B2P/PP3P2/2KRR3 b - - 5 18',
                          '2kr3r/pp2b1p1/1n1p1p1p/8/2p1PP2/1BP1B2P/PP3P2/2KRR3 w - - 0 19',
                          '2kr3r/pp2b1p1/1n1p1p1p/8/2p1PP2/2P1B2P/PPB2P2/2KRR3 b - - 1 19',
                          '3r3r/ppk1b1p1/1n1p1p1p/8/2p1PP2/2P1B2P/PPB2P2/2KRR3 w - - 2 20',
                          '3r3r/ppk1b1p1/1n1p1p1p/8/2p1PP2/1PP1B2P/P1B2P2/2KRR3 b - - 0 20',
                          '3r3r/1pk1b1p1/pn1p1p1p/8/2p1PP2/1PP1B2P/P1B2P2/2KRR3 w - - 0 21',
                          '3r3r/1pk1b1p1/pn1p1p1p/8/2p1PP2/1PP1B2P/PKB2P2/3RR3 b - - 1 21',
                          '3r3r/1pk1b1p1/pn3p1p/3p4/2p1PP2/1PP1B2P/PKB2P2/3RR3 w - - 0 22',
                          '3r3r/1pk1b1p1/pn3p1p/3p4/P1p1PP2/1PP1B2P/1KB2P2/3RR3 b - - 0 22',
                          '3r3r/1pk1b1p1/pn3p1p/3p4/P3PP2/1pP1B2P/1KB2P2/3RR3 w - - 0 23',
                          '3r3r/1pk1b1p1/pn3p1p/3p4/P3PP2/1BP1B2P/1K3P2/3RR3 b - - 0 23',
                          '3r3r/1p2b1p1/pnk2p1p/3p4/P3PP2/1BP1B2P/1K3P2/3RR3 w - - 1 24',
                          '3r3r/1p2b1p1/pnk2p1p/3P4/P4P2/1BP1B2P/1K3P2/3RR3 b - - 0 24',
                          '3r3r/1p2b1p1/p1k2p1p/3n4/P4P2/1BP1B2P/1K3P2/3RR3 w - - 0 25',
                          '3r3r/1p2b1p1/p1k2p1p/3B4/P4P2/2P1B2P/1K3P2/3RR3 b - - 0 25',
                          '7r/1p2b1p1/p1k2p1p/3r4/P4P2/2P1B2P/1K3P2/3RR3 w - - 0 26',
                          '7r/1p2b1p1/p1k2p1p/3R4/P4P2/2P1B2P/1K3P2/4R3 b - - 0 26',
                          '7r/1p2b1p1/p4p1p/3k4/P4P2/2P1B2P/1K3P2/4R3 w - - 0 27',
                          '7r/1p2b1p1/p4p1p/3k4/P4P2/2P1B2P/1K3P2/3R4 b - - 1 27',
                          '7r/1p2b1p1/p1k2p1p/8/P4P2/2P1B2P/1K3P2/3R4 w - - 2 28',
                          '7r/1p2b1p1/p1k2p1p/8/P4P2/1KP1B2P/5P2/3R4 b - - 3 28',
                          '7r/1p2b1p1/2k2p1p/p7/P4P2/1KP1B2P/5P2/3R4 w - - 0 29',
                          '7r/1p2b1p1/2k2p1p/p7/P1P2P2/1K2B2P/5P2/3R4 b - - 0 29',
                          '7r/4b1p1/1pk2p1p/p7/P1P2P2/1K2B2P/5P2/3R4 w - - 0 30',
                          '7r/4b1p1/1pk2p1p/p1P5/P4P2/1K2B2P/5P2/3R4 b - - 0 30',
                          '7r/6p1/1pk2p1p/p1b5/P4P2/1K2B2P/5P2/3R4 w - - 0 31',
                          '7r/6p1/1pk2p1p/p1B5/P4P2/1K5P/5P2/3R4 b - - 0 31',
                          '7r/6p1/2k2p1p/p1p5/P4P2/1K5P/5P2/3R4 w - - 0 32',
                          '7r/6p1/2k2p1p/p1p5/P1K2P2/7P/5P2/3R4 b - - 1 32',
                          '1r6/6p1/2k2p1p/p1p5/P1K2P2/7P/5P2/3R4 w - - 2 33',
                          '1r6/6p1/2k2p1p/p1pR4/P1K2P2/7P/5P2/8 b - - 3 33',
                          '8/6p1/2k2p1p/p1pR4/PrK2P2/7P/5P2/8 w - - 4 34',
                          '8/6p1/2k2p1p/p1pR4/Pr3P2/2K4P/5P2/8 b - - 5 34',
                          '8/6p1/5p1p/p1pk4/Pr3P2/2K4P/5P2/8 w - - 0 35',
                          '8/6p1/5p1p/p1pk4/Pr3P2/3K3P/5P2/8 b - - 1 35',
                          '8/6p1/5p1p/p1pk4/P4r2/3K3P/5P2/8 w - - 0 36',
                          '8/6p1/5p1p/p1pk4/P4r2/4K2P/5P2/8 b - - 1 36',
                          '8/6p1/5p1p/p1pk4/P6r/4K2P/5P2/8 w - - 2 37',
                          '8/6p1/5p1p/p1pk4/P4P1r/4K2P/8/8 b - - 0 37',
                          '8/6p1/5p1p/p1pk4/P4P2/4K2r/8/8 w - - 0 38',
                          '8/6p1/5p1p/p1pk4/P4P2/7r/5K2/8 b - - 1 38',
                          '8/6p1/5p1p/p1pk4/P4P2/r7/5K2/8 w - - 2 39',
                          '8/6p1/5p1p/p1pk1P2/P7/r7/5K2/8 b - - 0 39',
                          '8/6p1/5p1p/p2k1P2/P1p5/r7/5K2/8 w - - 0 40',
                          '8/6p1/5p1p/p2k1P2/P1p5/r7/4K3/8 b - - 1 40',
                          '8/6p1/5p1p/p3kP2/P1p5/r7/4K3/8 w - - 2 41',
                          '8/6p1/5p1p/p3kP2/P1p5/r7/3K4/8 b - - 3 41',
                          '8/6p1/5p1p/p4k2/P1p5/r7/3K4/8 w - - 0 42',
                          '8/6p1/5p1p/p4k2/P1p5/r7/2K5/8 b - - 1 42',
                          '8/6p1/5p2/p4k1p/P1p5/r7/2K5/8 w - - 0 43',
                          '8/6p1/5p2/p4k1p/P1p5/r7/1K6/8 b - - 1 43',
                          '8/6p1/5p2/p4k1p/r1p5/8/1K6/8 w - - 0 44',
                          '8/6p1/5p2/p4k1p/r1p5/8/8/1K6 b - - 1 44',
                          '8/6p1/5p2/p4k2/r1p4p/8/8/1K6 w - - 0 45',
                          '8/6p1/5p2/p4k2/r1p4p/8/1K6/8 b - - 1 45',
                          '8/6p1/5p2/p4k2/r1p5/7p/1K6/8 w - - 0 46',
                          '8/6p1/5p2/p4k2/r1p5/7p/8/1K6 b - - 1 46',
                          '8/6p1/5p2/p7/r1p1k3/7p/8/1K6 w - - 2 47',
                          '8/6p1/5p2/p7/r1p1k3/7p/8/2K5 b - - 3 47',
                          '8/6p1/5p2/p7/r1p5/4k2p/8/2K5 w - - 4 48',
                          '8/6p1/5p2/p7/r1p5/4k2p/8/1K6 b - - 5 48',
                          '8/6p1/5p2/p7/r1p5/7p/3k4/1K6 w - - 6 49',
                          '8/6p1/5p2/p7/r1p5/7p/1K1k4/8 b - - 7 49',
                          '8/6p1/5p2/p7/1rp5/7p/1K1k4/8 w - - 8 50',
                          '8/6p1/5p2/p7/1rp5/7p/K2k4/8 b - - 9 50',
                          '8/6p1/5p2/p7/1r6/2p4p/K2k4/8 w - - 0 51',
                          '8/6p1/5p2/p7/1r6/K1p4p/3k4/8 b - - 1 51',
                          '8/6p1/5p2/p7/1r6/K6p/2pk4/8 w - - 0 52',
                          '8/6p1/5p2/p7/1r6/7p/K1pk4/8 b - - 1 52',
                          '8/6p1/5p2/p7/r7/7p/K1pk4/8 w - - 2 53',
                          '8/6p1/5p2/p7/r7/1K5p/2pk4/8 b - - 3 53',
                          '8/6p1/5p2/p7/r7/1K5p/3k4/2q5 w - - 0 54',
                          '8/6p1/5p2/p7/K7/7p/3k4/2q5 b - - 0 54',
                          '8/6p1/5p2/p7/K1q5/7p/3k4/8 w - - 1 55',
                          '8/6p1/5p2/K7/2q5/7p/3k4/8 b - - 0 55',
                          '8/6p1/5p2/K7/8/1q5p/3k4/8 w - - 1 56',
                          '8/6p1/K4p2/8/8/1q5p/3k4/8 b - - 2 56',
                          '8/6p1/K4p2/8/8/1qk4p/8/8 w - - 3 57',
                          '8/K5p1/5p2/8/8/1qk4p/8/8 b - - 4 57',
                          '8/K5p1/5p2/8/2k5/1q5p/8/8 w - - 5 58',
                          'K7/6p1/5p2/8/2k5/1q5p/8/8 b - - 6 58',
                          'K7/6p1/5p2/2k5/8/1q5p/8/8 w - - 7 59',
                          '8/K5p1/5p2/2k5/8/1q5p/8/8 b - - 8 59',
                          '8/K5p1/5p2/1qk5/8/7p/8/8 w - - 9 60',
                          'K7/6p1/5p2/1qk5/8/7p/8/8 b - - 10 60',
                          'K7/6p1/2k2p2/1q6/8/7p/8/8 w - - 11 61',
                          '8/K5p1/2k2p2/1q6/8/7p/8/8 b - - 12 61',
                          '8/K1k3p1/5p2/1q6/8/7p/8/8 w - - 13 62',
                          'K7/2k3p1/5p2/1q6/8/7p/8/8 b - - 14 62',
                          'K7/1qk3p1/5p2/8/8/7p/8/8 w - - 15 63']
                         )


if __name__ == '__main__':
    unittest.main()
