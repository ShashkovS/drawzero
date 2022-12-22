#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

# build and upload
# pip install wheel

# python setup.py sdist bdist_wheel
# twine check dist/*
# twine upload dist/*


import io
import os
import re
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = 'drawzero'
DESCRIPTION = 'A zero-boilerplate canvas drawing framework for Python 3, based on Pygame.'
URL = 'https://github.com/ShashkovS/drawzero'
EMAIL = 'sh57@yandex.ru'
AUTHOR = 'Sergey Shashkov'

# Current version
with io.open(os.path.join(here, 'src', NAME, f'__about__.py'), encoding='utf-8') as f:
    VERSION = re.search(r'\d+\.\d+\.\d+', f.read()).group()

# What packages are required for this module to be executed?
with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    REQUIRED = [row.strip() for row in f.readlines() if row.strip() and not row.strip().startswith('#')]

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = '\n' + f.read()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [],
    },
    install_requires=REQUIRED,
    # include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.in'],
    },
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia :: Graphics',
    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)
