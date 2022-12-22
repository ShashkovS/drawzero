import unittest
from drawzero.utils.draw import _to_color, _to_pos, renderer

class ColorTest(unittest.TestCase):
    def test_wrong_color(self):
        self.assertRaises(TypeError, _to_color, '#abcd')
        self.assertRaises(TypeError, _to_color, 'dummy')
        self.assertRaises(TypeError, _to_color, '#aabbZZ')
        self.assertRaises(TypeError, _to_color, '#aa bb cc')
        self.assertRaises(TypeError, _to_color, '# abc')

    def test_red(self):
        self.assertEqual(_to_color('red'), (255, 0, 0))
        self.assertEqual(_to_color('#FF0000'), (255, 0, 0))
        self.assertEqual(_to_color('#f00'), (255, 0, 0))
        self.assertEqual(_to_color((255, 0, 0)), (255, 0, 0))
        self.assertEqual(_to_color([255, 0, 0]), (255, 0, 0))

    def test_wrong_to_pos(self):
        self.assertRaises(TypeError, _to_pos, None)
        self.assertRaises(TypeError, _to_pos, 1)
        self.assertRaises(TypeError, _to_pos, '1', '1')
        self.assertRaises(TypeError, _to_pos, [1,1,1])

    def test_to_pos(self):
        saved_size = renderer.surface_size
        renderer.surface_size = 1000
        self.assertTupleEqual(_to_pos([1, 1]), (1, 1))
        self.assertTupleEqual(_to_pos((1, 1)), (1, 1))
        renderer.surface_size = 100
        self.assertTupleEqual(_to_pos([500, 604]), (50, 60))
        renderer.surface_size = saved_size


################################################################################

if __name__ == "__main__":
    unittest.main()
