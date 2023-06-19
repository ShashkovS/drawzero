from pathlib import Path
from shutil import copytree
import os

EXAMPLES_DIR = 'examples'


def copy_examples():
    """Create a pack of drawzero examples into current folder
    """
    src = Path(__file__).parent.parent.resolve() / EXAMPLES_DIR
    dst = Path.cwd() / EXAMPLES_DIR
    print(f'Copying examples to {dst}...')
    os.makedirs(dst, exist_ok=True)
    copytree(src, dst, dirs_exist_ok=True)
    print(f'Examples are ready!')
