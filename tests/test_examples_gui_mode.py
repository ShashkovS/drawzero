import os
import unittest
import pathlib

import drawzero

example_modules = [
    f'drawzero.examples.{example.stem}'
    for example in (pathlib.Path(__file__).parent.parent / 'src' / 'drawzero' / 'examples').glob('*.py')
]


# # Generate test code
# for module in example_modules:
#     print(f'''
#     def test_{module.replace(".", "_")}(self):
#         __import__('{module}')''')
# exit()

@classmethod
def tearDownClass(cls):
    drawzero.quit()


class RunExamples(unittest.TestCase):

    def test_drawzero_examples_00_hello_world(self):
        __import__('drawzero.examples.00_hello_world')

    def test_drawzero_examples_01_grid_and_coordinates(self):
        __import__('drawzero.examples.01_grid_and_coordinates')

    def test_drawzero_examples_02_loops_and_rgb_colors(self):
        __import__('drawzero.examples.02_loops_and_rgb_colors')

    def test_drawzero_examples_03_simple_objects(self):
        __import__('drawzero.examples.03_simple_objects')

    def test_drawzero_examples_04_loops_sin_plot(self):
        __import__('drawzero.examples.04_loops_sin_plot')

    def test_drawzero_examples_05_turtle_style(self):
        __import__('drawzero.examples.05_turtle_style')

    def test_drawzero_examples_06_animation_circles(self):
        __import__('drawzero.examples.06_animation_circles')

    def test_drawzero_examples_07_animation_traffic_light(self):
        __import__('drawzero.examples.07_animation_traffic_light')

    def test_drawzero_examples_08_animation_rectangles(self):
        __import__('drawzero.examples.08_animation_rectangles')

    def test_drawzero_examples_09_animation_planets(self):
        __import__('drawzero.examples.09_animation_planets')

    def test_drawzero_examples_10_transparency_and_line_width(self):
        __import__('drawzero.examples.10_transparency_and_line_width')

    def test_drawzero_examples_11_images(self):
        __import__('drawzero.examples.11_images')

    def test_drawzero_examples_12_animation_close_vertex(self):
        __import__('drawzero.examples.12_animation_close_vertex')

    def test_drawzero_examples_13_animation_firework(self):
        __import__('drawzero.examples.13_animation_firework')

    # def test_drawzero_examples_14_keyboard_and_mouse(self):
    #     __import__('drawzero.examples.14_keyboard_and_mouse')
    #
    # def test_drawzero_examples_15_mouse_tube(self):
    #     __import__('drawzero.examples.15_mouse_tube')
    #
    # def test_drawzero_examples_16_game_stars(self):
    #     __import__('drawzero.examples.16_game_stars')
    #
    # def test_drawzero_examples_17_game_colors(self):
    #     __import__('drawzero.examples.17_game_colors')
    #
    # def test_drawzero_examples_18_game_racing(self):
    #     __import__('drawzero.examples.18_game_racing')


if __name__ == "__main__":
    unittest.main()
