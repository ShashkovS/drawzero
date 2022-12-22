import unittest
import drawzero
import utils


class ColorTest(unittest.TestCase):
    def test_wrong_color(self):
        self.assertRaises(TypeError, drawzero._to_color, '#abcd')
        self.assertRaises(TypeError, drawzero._to_color, 'dummy')
        self.assertRaises(TypeError, drawzero._to_color, '#aabbZZ')
        self.assertRaises(TypeError, drawzero._to_color, '#aa bb cc')
        self.assertRaises(TypeError, drawzero._to_color, '# abc')

    def test_red(self):
        self.assertEqual(drawzero._to_color('red'), (255, 0, 0))
        self.assertEqual(drawzero._to_color('#FF0000'), (255, 0, 0))
        self.assertEqual(drawzero._to_color('#f00'), (255, 0, 0))
        self.assertEqual(drawzero._to_color((255, 0, 0)), (255, 0, 0))
        self.assertEqual(drawzero._to_color([255, 0, 0]), (255, 0, 0))

    def test_wrong_to_pos(self):
        self.assertRaises(TypeError, drawzero._to_pos, None)
        self.assertRaises(TypeError, drawzero._to_pos, 1)
        self.assertRaises(TypeError, drawzero._to_pos, '1', '1')
        self.assertRaises(TypeError, drawzero._to_pos, [1,1,1])

    def test_to_pos(self):
        saved_size = drawzero.renderer.surface_size
        drawzero.renderer.surface_size = 1000
        self.assertTupleEqual(drawzero._to_pos([1, 1]), (1, 1))
        self.assertTupleEqual(drawzero._to_pos((1, 1)), (1, 1))
        drawzero.renderer.surface_size = 100
        self.assertTupleEqual(drawzero._to_pos([500, 604]), (50, 60))
        drawzero.renderer.surface_size = saved_size


################################################################################

if __name__ == "__main__":
    unittest.main()
