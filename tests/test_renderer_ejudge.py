import os
import unittest
import json
from io import StringIO
import sys

os.environ['EJUDGE_MODE'] = 'true'
# We need to reload drawzero to apply EJUDGE_MODE
if 'drawzero' in sys.modules:
    import importlib
    importlib.reload(sys.modules['drawzero.utils.draw'])
    importlib.reload(sys.modules['drawzero'])
from drawzero import *

class EjudgeRendererTest(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.held

    def test_line(self):
        line('red', (10, 20), (30, 40), alpha=128, line_width=2)
        output = sys.stdout.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data['figure'], 'line')
        self.assertEqual(data['color'], [255, 0, 0])
        self.assertEqual(data['start'], [10, 20])
        self.assertEqual(data['end'], [30, 40])
        self.assertEqual(data['alpha'], 128)
        self.assertEqual(data['line_width'], 2)

    def test_circle(self):
        circle('blue', (50, 60), 10, alpha=200, line_width=4)
        output = sys.stdout.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data['figure'], 'circle')
        self.assertEqual(data['color'], [0, 0, 255])
        self.assertEqual(data['pos'], [50, 60])
        self.assertEqual(data['radius'], 10)
        self.assertEqual(data['alpha'], 200)
        self.assertEqual(data['line_width'], 4)

    def test_rect(self):
        rect('green', (10, 20, 30, 40), alpha=100, line_width=1)
        output = sys.stdout.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data['figure'], 'rect')
        self.assertEqual(data['color'], [0, 255, 0])
        self.assertEqual(data['rect'], [10, 20, 30, 40])
        self.assertEqual(data['alpha'], 100)
        self.assertEqual(data['line_width'], 1)

    def test_text(self):
        text('yellow', 'Hello', (10, 20), fontsize=12, align='..')
        output = sys.stdout.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data['figure'], 'text')
        self.assertEqual(data['color'], [255, 255, 0])
        self.assertEqual(data['text'], 'Hello')
        self.assertEqual(data['pos'], [10, 20])
        self.assertEqual(data['fontsize'], 12)
        self.assertEqual(data['align'], '..')

    def test_fill(self):
        fill('black', alpha=50)
        output = sys.stdout.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data['figure'], 'fill')
        self.assertEqual(data['color'], [0, 0, 0])
        self.assertEqual(data['alpha'], 50)

    def test_clear(self):
        clear()
        output = sys.stdout.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data['figure'], 'clear')

if __name__ == "__main__":
    unittest.main()
