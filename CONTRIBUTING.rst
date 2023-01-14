Contributions
=============

Contributions are welcome and are greatly appreciated! Every little bit helps,
and credit will always be given.


Report Bugs
-----------

Report bugs through `GitHub <https://github.com/ShashkovS/drawzero/issues>`__.


Improve Documentation
---------------------

Drawzero could always use better documentation, whether as part of the docs, in docstrings, ``docs/*.rst`` or even on the web as blog posts or
articles.



Configure Your Environment
==========================

First you need to create virtual environment and make an editable install of the package (`ref <https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout>`_)::

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


Run tests
---------
::

    python -m pytest -vvs tests/
    # or
    python -m coverage run -m pytest -vvs tests/
