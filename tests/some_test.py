import unittest
import drawzero


class ColorTest(unittest.TestCase):
    def test_wrong_color(self):
        self.assertRaises(TypeError, drawzero._make_color, '#abcd')
        self.assertRaises(TypeError, drawzero._make_color, 'dummy')
        self.assertRaises(TypeError, drawzero._make_color, '#aabbZZ')
        self.assertRaises(TypeError, drawzero._make_color, '#aa bb cc')
        self.assertRaises(TypeError, drawzero._make_color, '# abc')

    def test_red(self):
        self.assertEqual(drawzero._make_color('red'), (255, 0, 0))
        self.assertEqual(drawzero._make_color('#FF0000'), (255, 0, 0))
        self.assertEqual(drawzero._make_color('#f00'), (255, 0, 0))
        self.assertEqual(drawzero._make_color((255, 0, 0)), (255, 0, 0))
        self.assertEqual(drawzero._make_color([255, 0, 0]), (255, 0, 0))


################################################################################

if __name__ == "__main__":
    unittest.main()
