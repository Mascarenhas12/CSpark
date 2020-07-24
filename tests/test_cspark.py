import unittest

import numpy as np
import numpy.random

from src.cspark import CSparkConfig, CSpark


class CSparkTest(unittest.TestCase):
    def setUp(self) -> None:
        a = np.random.random_sample(size=218)
        a /= sum(a)
        self.move_prob = {str(x): a[x] for x in range(len(a))}
        self.config = CSparkConfig("resources/2vincent2 vs docboss,1399394103794.pgn",
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
            0.47
        )
        self.assertGreaterEqual(self.spark.move_val(
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2q1P/PP3PP1/R3K2R w KQkq - 0 13',
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2P1P/PP3P2/R3K2R b KQkq - 0 13'),
            -0.24
        )

    def test_match_total_until_play_num(self):
        pass


if __name__ == '__main__':
    unittest.main()
