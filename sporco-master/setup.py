#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import next
from builtins import filter

import os
from glob import glob
from setuptools import setup
import io
import os.path
from ast import parse


name = 'sporco'

# Get version number from sporco/__init__.py
# See http://stackoverflow.com/questions/2058802
with open(os.path.join(name, '__init__.py')) as f:
    version = parse(next(filter(
        lambda line: line.startswith('__version__'),
        f))).body[0].value.s

packages = ['sporco', 'sporco.admm', 'sporco.fista']

docdirbase  = 'share/doc/%s-%s' % (name, version)
data = [(os.path.join(docdirbase, 'examples/scripts'),
        ['examples/scripts/index.rst'])]
for d in glob('examples/scripts/*'):
    if os.path.isdir(d):
        data.append((os.path.join(docdirbase, d),
                    [os.path.join(d, 'index.rst')] +
                    glob(os.path.join(d, '*.py'))))


longdesc = \
"""
SPORCO is a Python package for solving optimisation problems with
sparsity-inducing regularisation. These consist primarily of sparse
coding and dictionary learning problems, including convolutional
sparse coding and dictionary learning, but there is also support for
other problems such as Total Variation regularisation and Robust
PCA. The optimisation algorithms in the current version are based
on the Alternating Direction Method of Multipliers (ADMM) or on
the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA).
"""

on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    print("Building on ReadTheDocs")
    install_requires = ['future', 'numpy', 'scipy', 'ipython']
else:
    install_requires = ['future', 'numpy', 'scipy', 'pyfftw', 'matplotlib']


setup(
    name             = name,
    version          = version,
    description      = 'Sparse Optimisation Research Code: A Python package ' \
                       'for sparse coding and dictionary learning',
    long_description = longdesc,
    keywords         = ['Sparse Representations', 'Sparse Coding',
                        'Dictionary Learning',
                        'Convolutional Sparse Representations',
                        'Convolutional Sparse Coding', 'Optimization',
                        'ADMM', 'FISTA'],
    platforms        = 'Any',
    license          = 'BSD',
    url              = 'http://bwohlberg.github.io/sporco',
    author           = 'Brendt Wohlberg',
    author_email     = 'brendt@ieee.org',
    packages         = packages,
    package_data     = {'sporco': ['data/*.png', 'data/*.jpg', 'data/*.npz']},
    data_files       = data,
    include_package_data = True,
    scripts          = ['bin/sporco_get_images'],
    setup_requires   = ['future', 'pytest-runner', 'numpy', 'scipy'],
    tests_require    = ['pytest'],
    install_requires = install_requires,
    extras_require = {
        'numexpr':  ['numexpr'],
        'datacursor': ['mpldatacursor'],
    },
    classifiers = [
    'License :: OSI Approved :: BSD License',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe = False
)
