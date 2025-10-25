# Установка

В окне терминала введите:
```shell
pip install drawzero --upgrade --user
```


Или запустите следующую программу:

```python
import os, sys
python = sys.executable
user = '--user' if 'venv' not in python and 'virtualenvs' not in python else ''
cmd = f'"{python}" -m pip install drawzero --upgrade {user}'
os.system(cmd)
from drawzero import *
```
