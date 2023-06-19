import unittest

from drawzero.utils.gradient import Gradient


class ColorGradient(unittest.TestCase):
    def test_2_steps(self):
        scale = Gradient([(200, 0, 0), (0, 0, 0)], 200, 300)
        self.assertTupleEqual(scale(150), (200, 0, 0))
        self.assertTupleEqual(scale(200), (200, 0, 0))
        self.assertTupleEqual(scale(350), (0, 0, 0))
        self.assertTupleEqual(scale(300), (0, 0, 0))
        for i in range(100):
            self.assertTupleEqual(scale(200 + i), (200 - 2 * i, 0, 0))

    def test_4_steps(self):
        scale = Gradient([(200, 0, 0), (0, 0, 0), (0, 200, 0), (0, 0, 200), (100, 0, 100)], 0, 400)
        for i in range(100):
            self.assertTupleEqual(scale(i), (200 - 2 * i, 0, 0))
            self.assertTupleEqual(scale(100 + i), (0, 2 * i, 0))
            self.assertTupleEqual(scale(200 + i), (0, 200 - 2 * i, 2 * i))
            self.assertTupleEqual(scale(300 + i), (i, 0, 200 - i))

        scale = Gradient([(200, 0, 0), (0, 0, 0), (0, 200, 0), (0, 0, 200), (100, 0, 100)], 0, 100, 200, 300, 600)
        for i in range(100):
            self.assertTupleEqual(scale(i), (200 - 2 * i, 0, 0))
            self.assertTupleEqual(scale(100 + i), (0, 2 * i, 0))
            self.assertTupleEqual(scale(200 + i), (0, 200 - 2 * i, 2 * i))
            self.assertTupleEqual(scale(300 + i * 3), (i, 0, 200 - i))


################################################################################

if __name__ == "__main__":
    unittest.main()
