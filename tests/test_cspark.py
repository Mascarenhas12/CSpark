import unittest
import os

import numpy as np
import numpy.random

from src.cspark import CSparkConfig, CSpark


class CSparkTest(unittest.TestCase):
    def setUp(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        a = np.random.random_sample(size=218)
        a /= sum(a)
        self.move_prob = {str(x): a[x] for x in range(len(a))}
        self.config = CSparkConfig(dir_path + "/resources/2vincent2 vs docboss,1399394103794.pgn",
                                   "white",
                                   {
                                       "R14": 2,
                                       "R15": 1.5
                                   },
                                   self.move_prob
                                   )
        self.spark = CSpark(self.config)

    def tearDown(self) -> None:
        del self.spark

    def test_move_val(self):
        self.assertLessEqual(self.spark.move_val(
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2q1P/PP3PP1/R3K2R w KQkq - 0 13',
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2P1P/PP3P2/R3K2R b KQkq - 0 13'),
            0.48
        )
        self.assertGreaterEqual(self.spark.move_val(
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2q1P/PP3PP1/R3K2R w KQkq - 0 13',
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2P1P/PP3P2/R3K2R b KQkq - 0 13'),
            0.15
        )

    def test_match_average_until_play_num(self):
        self.assertLessEqual(self.spark.match_average_until_play_num(10)
                             .get('MLA'), 0.85)
        self.assertLessEqual(self.spark.match_average_until_play_num(10)
                             .get('MGA'), 0.72)
        self.assertGreaterEqual(self.spark.match_average_until_play_num(10)
                             .get('MLA'), 0.58)
        self.assertGreaterEqual(self.spark.match_average_until_play_num(10)
                             .get('MGA'), 0.6)


if __name__ == '__main__':
    unittest.main()
