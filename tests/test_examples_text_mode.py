import os
import unittest
import pathlib

os.environ['EJUDGE_MODE'] = 'true'

example_modules = [
    f'drawzero.examples.{example.stem}'
    for example in (pathlib.Path(__file__).parent.parent / 'src' / 'drawzero' / 'drawzero.examples').glob('*.py')
]


# # Generate test code
# for module in example_modules:
#     print(f'''
#     def test_{module.replace(".", "_")}(self):
#         __import__('{module}')''')
# exit()


class RunExamples(unittest.TestCase):
    def test_examples_00_hello_world(self):
        __import__('drawzero.examples.00_hello_world')

    def test_examples_01_grid_and_coordinates(self):
        __import__('drawzero.examples.01_grid_and_coordinates')

    def test_examples_02_loops_and_rgb_colors(self):
        __import__('drawzero.examples.02_loops_and_rgb_colors')

    def test_examples_03_simple_objects(self):
        __import__('drawzero.examples.03_simple_objects')

    def test_examples_04_loops_sin_plot(self):
        __import__('drawzero.examples.04_loops_sin_plot')

    def test_examples_05_animation_circles(self):
        __import__('drawzero.examples.05_animation_circles')

    def test_examples_06_animation_traffic_light(self):
        __import__('drawzero.examples.06_animation_traffic_light')

    def test_examples_07_animation_planets(self):
        __import__('drawzero.examples.07_animation_planets')

    def test_examples_08_transparency_and_line_width(self):
        __import__('drawzero.examples.08_transparency_and_line_width')

    def test_examples_09_images(self):
        __import__('drawzero.examples.09_images')

    # def test_examples_10_animation_close_vertex(self):
    #     __import__('drawzero.examples.10_animation_close_vertex')

    # def test_examples_11_animation_firework(self):
    #     __import__('drawzero.examples.11_animation_firework')

    # def test_examples_12_keyboard_and_mouse(self):
    #     __import__('drawzero.examples.12_keyboard_and_mouse')

    # def test_examples_13_mouse_tube(self):
    #     __import__('drawzero.examples.13_mouse_tube')

    # def test_examples_14_game_stars(self):
    #     __import__('drawzero.examples.14_game_stars')

    # def test_examples_15_game_colors(self):
    #     __import__('drawzero.examples.15_game_colors')

    # def test_examples_16_game_racing(self):
    #     __import__('drawzero.examples.16_game_racing')


if __name__ == "__main__":
    unittest.main()
