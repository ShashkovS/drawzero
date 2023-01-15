# Contributions

Contributions are welcome and are greatly appreciated! Every little bit helps,
and credit will always be given.


# Report Bugs

Report bugs through [GitHub issues](https://github.com/ShashkovS/drawzero/issues).


# Improve Documentation

Drawzero could always use better documentation, whether as part of the docs, in docstrings, ``docs/*.md`` or even on the web as blog posts or
articles.

# Install the last version from GitHub 

```shell
pip uninstall drawzero
pip install --upgrade git+https://github.com/ShashkovS/drawzero.git
```

# Configure Your Environment

First you need clone repo, create virtual environment and make an editable install of the package ([ref](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout)):

```shell
# Clone
git clone https://github.com/ShashkovS/drawzero.git
# Get into
cd drawzero
# Create virtual environment
python -m venv venv

# Activate (bash)
source venv/bin/activate
# Activate (Windows)
. venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Install dev-dependencies
pip install -r requirements-dev.txt

# Make an editable install of the package
python -m pip install --editable . --upgrade
```




# Run tests

```shell
python -m pytest -vvs tests/
# or
python -m coverage run -m pytest -vvs tests/
```
