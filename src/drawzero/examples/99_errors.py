import os
import traceback
import sys

os.environ['EJUDGE_MODE'] = 'true'

from drawzero import *

filled_circle('boo')
# line('nocolor', (100, 100), ('asdf',))
circle('red', (100, 100), 'asd', line_width=0)


class ExceptionPrinter:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_traceback:
            traceback_len = 0
            cur = exc_traceback
            while cur:
                traceback_len += 1
                cur = cur.tb_next
            print(f'Traceback is {traceback_len} deep')
            print(''.join(traceback.format_tb(exc_traceback)), end='')
            print(exc_value)
        return True


# import drawzero
# print(help(drawzero))
# exit()
#
#
s = ExceptionPrinter()

with s: line('nocolor', (100, 100), (200, 200))
with s: line(C.red, (100, 200), (200, 'baz'))
with s: rect('violet', (100, 200, 300, 'baz'))
