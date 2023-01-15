from pathlib import Path
from drawzero import *

this_file_dir = Path(__file__).parent.absolute()

image(this_file_dir / 'cat.png', (0, 0))
image(this_file_dir / 'cat.png', (500, 500), width=500)

image(this_file_dir / 'cat.png', (100, 600), width=200, alpha=128)
image(this_file_dir / 'cat.png', (200, 700), width=200, alpha=128)
image(this_file_dir / 'cat.png', (300, 800), width=200, alpha=128)
