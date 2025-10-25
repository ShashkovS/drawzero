import os
import unittest
import pathlib

import drawzero

example_modules = sorted([
    f'drawzero.examples.{example.stem}'
    for example in (pathlib.Path(__file__).parent.parent / 'src' / 'drawzero' / 'examples').glob('*.py')
    if example.stem != '__init__'
])


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

    def test_drawzero_examples_05_points(self):
        __import__('drawzero.examples.05_points')

    def test_drawzero_examples_06_turtle_style(self):
        __import__('drawzero.examples.06_turtle_style')

    def test_drawzero_examples_07_animation_circles(self):
        __import__('drawzero.examples.07_animation_circles')

    def test_drawzero_examples_08_animation_traffic_light(self):
        __import__('drawzero.examples.08_animation_traffic_light')

    def test_drawzero_examples_09_animation_rectangles(self):
        __import__('drawzero.examples.09_animation_rectangles')

    def test_drawzero_examples_10_animation_planets(self):
        __import__('drawzero.examples.10_animation_planets')

    def test_drawzero_examples_11_transparency_and_line_width(self):
        __import__('drawzero.examples.11_transparency_and_line_width')

    def test_drawzero_examples_12_images(self):
        __import__('drawzero.examples.12_images')

    def test_drawzero_examples_13_gradients(self):
        __import__('drawzero.examples.13_gradients')

    def test_drawzero_examples_14_animation_close_vertex(self):
        __import__('drawzero.examples.14_animation_close_vertex')

    def test_drawzero_examples_15_animation_firework(self):
        __import__('drawzero.examples.15_animation_firework')

    # def test_drawzero_examples_16_keyboard_and_mouse(self):
    #     __import__('drawzero.examples.16_keyboard_and_mouse')
    #
    # def test_drawzero_examples_17_mouse_tube(self):
    #     __import__('drawzero.examples.17_mouse_tube')
    #
    # def test_drawzero_examples_18_game_stars(self):
    #     __import__('drawzero.examples.18_game_stars')
    #
    # def test_drawzero_examples_19_game_colors(self):
    #     __import__('drawzero.examples.19_game_colors')
    #
    # def test_drawzero_examples_20_game_racing(self):
    #     __import__('drawzero.examples.20_game_racing')

    def test_drawzero_examples_99_errors(self):
        __import__('drawzero.examples.99_errors')


if __name__ == "__main__":
    unittest.main()