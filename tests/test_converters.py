import unittest

from drawzero.utils.screen_size import set_real_size
from drawzero.utils.errors import BadDrawParmsError
from drawzero.utils.colors import C
from drawzero.utils.converters import _to_color, _to_pos, _to_scaled_int, _to_line_width, _to_alpha, _to_flat, _to_rect, _to_points_list, _DFT_LINE_WIDTH


class ColorTest(unittest.TestCase):
    def test_color(self):
        error = BadDrawParmsError()
        self.assertEqual(_to_color('red', error), (255, 0, 0))
        self.assertEqual(_to_color(C.red, error), (255, 0, 0))
        self.assertEqual(_to_color('#FF0000', error), (255, 0, 0))
        self.assertEqual(_to_color('#f00', error), (255, 0, 0))
        self.assertEqual(_to_color((255, 0, 0), error), (255, 0, 0))
        self.assertEqual(_to_color([255, 0, 0], error), (255, 0, 0))

    def test_wrong_color(self):
        for bad in '#abcd', 'dummy', '#aabbZZ', '#aa bb cc', '# abc', (1,), (1, 1,), (1, 1, 1, 1, 1,), (-1, -1, -1), (300, 300, 300):
            error = BadDrawParmsError()
            color = _to_color(bad, error)
            self.assertIsNone(color)
            self.assertTrue(error.errors)

    def test_to_pos(self):
        error = BadDrawParmsError()
        set_real_size(1000, 1000)
        self.assertTupleEqual(_to_pos([1, 1], error), (1, 1))
        self.assertTupleEqual(_to_pos((1, 1), error), (1, 1))
        set_real_size(100, 100)
        self.assertTupleEqual(_to_pos([500, 604], error), (50, 60))
        set_real_size(1000, 1000)

    def test_wrong_pos(self):
        for bad in None, '1, 1', (1,), [None, 1], (1, 'foo'):
            error = BadDrawParmsError()
            pos = _to_pos(bad, error)
            self.assertIsNone(pos)
            self.assertTrue(error.errors)

    def test_to_flat(self):
        self.assertListEqual(_to_flat([1]), [1])
        self.assertListEqual(_to_flat([1, 2]), [1, 2])
        self.assertListEqual(_to_flat((1, 2)), [1, 2])
        self.assertListEqual(_to_flat((1, [2])), [1, 2])
        self.assertListEqual(_to_flat(([1], [2])), [1, 2])
        self.assertListEqual(_to_flat(([[1], [2]])), [1, 2])
        self.assertListEqual(_to_flat(([[1, 2], [3, 4]])), [1, 2, 3, 4])

    def test_to_scaled_int(self):
        error = BadDrawParmsError()
        set_real_size(1000, 1000)
        self.assertEqual(_to_scaled_int(127, error), 127)
        set_real_size(100, 100)
        self.assertEqual(_to_scaled_int(127, error), 13)
        set_real_size(1000, 1000)
        val = _to_scaled_int("val", error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)

    def test_to_line_width(self):
        error = BadDrawParmsError()
        set_real_size(1000, 1000)
        self.assertEqual(_to_line_width(None, error), _DFT_LINE_WIDTH)
        self.assertEqual(_to_line_width(127, error), 127)
        set_real_size(100, 100)
        self.assertEqual(_to_line_width(127, error), 13)
        set_real_size(1000, 1000)
        val = _to_line_width("val", error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)

    def test_to_alpha(self):
        error = BadDrawParmsError()
        self.assertEqual(_to_alpha(123, error), 123)
        self.assertEqual(_to_alpha(123.2, error), 123)
        val = _to_alpha(300, error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)

    def test_to_rect(self):
        error = BadDrawParmsError()
        set_real_size(1000, 1000)
        self.assertTupleEqual(_to_rect([1, 2, 3, 4], error), (1, 2, 3, 4))
        self.assertTupleEqual(_to_rect([(1, 2, 3, 4)], error), (1, 2, 3, 4))
        self.assertTupleEqual(_to_rect([(1, 2), (3, 4)], error), (1, 2, 3, 4))
        self.assertTupleEqual(_to_rect([(1, 2), 3, 4], error), (1, 2, 3, 4))
        set_real_size(100, 100)
        self.assertTupleEqual(_to_rect([(101, 201), 301, 401], error), (10, 20, 30, 40))
        set_real_size(1000, 1000)
        error = BadDrawParmsError()
        val = _to_rect([(101, 201), 301, "foo"], error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)
        error = BadDrawParmsError()
        val = _to_rect([(101, 201), 301, 401, 501], error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)

    def test_to_points_list(self):
        error = BadDrawParmsError()
        set_real_size(1000, 1000)
        self.assertListEqual(_to_points_list([1, 2, 3, 4], error), [(1, 2), (3, 4)])
        self.assertListEqual(_to_points_list([(1, 2, 3, 4)], error), [(1, 2), (3, 4)])
        self.assertListEqual(_to_points_list([(1, 2), (3, 4)], error), [(1, 2), (3, 4)])
        self.assertListEqual(_to_points_list([(1, 2), 3, 4, (5, 6), 7, 8], error), [(1, 2), (3, 4), (5, 6), (7, 8)])
        set_real_size(100, 100)
        self.assertListEqual(_to_points_list([(101, 201), 301, 401], error), [(10, 20), (30, 40)])
        set_real_size(1000, 1000)
        error = BadDrawParmsError()
        val = _to_points_list([1, 2, 3, "foo"], error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)
        error = BadDrawParmsError()
        val = _to_points_list([1, 2, 3], error)
        self.assertIsNone(val)
        self.assertTrue(error.errors)


################################################################################

if __name__ == "__main__":
    unittest.main()
