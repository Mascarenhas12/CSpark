import unittest

import numpy as np
import numpy.random

from src.cspark import CSparkConfig, CSpark


class CSparkTest(unittest.TestCase):
    def setUp(self) -> None:
        a = np.random.random_sample(size=218)
        a /= sum(a)
        self.move_prob = {str(x): a[x] for x in range(len(a))}
        self.config = CSparkConfig("tests/resources/2vincent2 vs docboss,1399394103794.pgn",
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
        pass


if __name__ == '__main__':
    unittest.main()
