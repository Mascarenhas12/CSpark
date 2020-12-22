import unittest
import os
import numpy as np
import numpy.random
from src.csparkconfig import CSparkConfig
from src.cspark import CSpark


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
        result = self.spark.move_val(
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2q1P/PP3PP1/R3K2R w KQkq - 0 13',
            'rn2k2r/ppp1bpp1/3p3p/8/2BBP3/2P2P1P/PP3P2/R3K2R b KQkq - 0 13')
        print(result)

        self.assertLessEqual(result, 0.48)
        self.assertGreaterEqual(result, 0.15)

    def test_match_average_until_play_num(self):
        result = self.spark.match_average_until_play_num(10)
        print(result)

        self.assertLessEqual(result.get('MLA'), 0.89)
        self.assertLessEqual(result.get('MGA'), 0.83)
        self.assertGreaterEqual(result.get('MLA'), 0.39)
        self.assertGreaterEqual(result.get('MGA'), 0.33)


if __name__ == '__main__':
    unittest.main()
