# Installation

In a Terminal window, type:
```shell
pip install drawzero --upgrade --user
```


Or run the following program:

```python
import os, sys
python = sys.executable
user = '--user' if 'venv' not in python and 'virtualenvs' not in python else ''
cmd = f'"{python}" -m pip install drawzero --upgrade {user}'
os.system(cmd)
from drawzero import *
```
