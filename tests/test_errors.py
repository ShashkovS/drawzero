import os
import unittest
import traceback

os.environ['EJUDGE_MODE'] = 'true'
from drawzero import *


class ExceptionPrinter:
    def __init__(self):
        self.last_deep = 0
        self.last_raised = False

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        if exctb:
            traceback_deep = 0
            cur = exctb
            while cur:
                traceback_deep += 1
                cur = cur.tb_next
            print(f'Traceback is {traceback_deep} deep')
            print(''.join(traceback.format_tb(exctb)))
            self.last_deep = traceback_deep
            self.last_raised = True
        else:
            self.last_raised = False
        return True


MAX_TRACEBACK_DEEP = 2


# TODO
class RunExamples(unittest.TestCase):
    def test_bad_color(self):
        exception_printer = ExceptionPrinter()
        for bad_color in 'foo', '#zzz', 123, (1, 1), (1, 1, 1, 1, 1), []:
            # TODO filled_circle
            for func in fill, text, line, circle, filled_circle, rect, filled_rect, filled_rect_rotated, rect_rotated, filled_polygon, polygon, ellipse, filled_ellipse, arc:
                with exception_printer:
                    func(bad_color)
                msg = f'func={func.__name__}, {bad_color=}'
                self.assertTrue(exception_printer.last_raised, msg=msg)
                max_deep = MAX_TRACEBACK_DEEP
                if func.__name__.startswith('filled'):
                    max_deep += 2
                self.assertLessEqual(exception_printer.last_deep, max_deep, msg=msg)

    def test_bad_pos(self):
        exception_printer = ExceptionPrinter()
        for bad_coords in 'xxx', ['xxx'], ['xxx', 'yyy'], [1], [None], [1, 'xx']:
            # TODO filled_circle
            for func in text, line, circle, filled_circle, rect, filled_rect, filled_rect_rotated, rect_rotated, filled_polygon, polygon, ellipse, filled_ellipse, arc:
                with exception_printer:
                    if func is text:
                        text('red', 'text', bad_coords)
                    else:
                        func('red', bad_coords)
                msg = f'func={func.__name__}, {bad_coords=}'
                self.assertTrue(exception_printer.last_raised, msg=msg)
                max_deep = MAX_TRACEBACK_DEEP
                if func.__name__.startswith('filled'):
                    max_deep += 2
                self.assertLessEqual(exception_printer.last_deep, max_deep, msg=msg)


if __name__ == "__main__":
    unittest.main()
