import unittest
import pathlib
import shutil
import re

from drawzero import copy_examples

example_file_mask = re.compile(r'\b\d\d_\w+\.py|\b\w+\.png|\b__\w+__\b')


class CopyExamplesTest(unittest.TestCase):
    def test_copy_examples(self):
        copy_examples()
        examples = []
        examples_dir = pathlib.Path('./examples')
        for obj in examples_dir.rglob('*'):
            examples.append(str(obj))
            print(obj)
        self.assertGreater(len(examples), 10, 'There must be at least 10 example files...')
        self.assertTrue(all(example_file_mask.search(name) for name in examples))
        if all(example_file_mask.search(name) for name in examples):
            shutil.rmtree(examples_dir)


if __name__ == "__main__":
    unittest.main()
