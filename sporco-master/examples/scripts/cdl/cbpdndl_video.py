#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""
Convolutional Dictionary Learning
=================================

This example demonstrates the use of :class:`.admm.cbpdndl.ConvBPDNDictLearn` for learning a 3D convolutional dictionary from video data. The dictionary learning algorithm is based on the ADMM consensus dictionary update.
"""


from __future__ import print_function
from builtins import input
from builtins import range

import os.path
import tempfile
import sys

import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
import numpy as np

try:
    import skvideo.datasets
    import skvideo.io
except ImportError:
    print('Package sk-video is required by this demo script', file=sys.stderr)
    raise

from sporco.admm import cbpdndl
from sporco import util
from sporco import plot


"""
Construct 3D training array from video data
"""

vid = skvideo.io.vread(skvideo.datasets.fullreferencepair()[0],
                outputdict={"-pix_fmt": "gray"})[..., 0]
vid = np.moveaxis(vid, 0, -1)
vid = vid[0:106,40:136, 10:42].astype(np.float32)/255.0

"""
Highpass filter video frames.
"""

npd = 16
fltlmbd = 10
vl, vh = util.tikhonov_filter(vid, fltlmbd, npd)


"""
Construct initial dictionary.
"""

np.random.seed(12345)
D0 = np.random.randn(5, 5, 3, 25)


"""
Set regularization parameter and options for dictionary learning solver.
"""

lmbda = 0.1
opt = cbpdndl.ConvBPDNDictLearn.Options({'Verbose': True, 'MaxMainIter': 200,
                'CBPDN': {'rho': 5e1*lmbda, 'AutoRho': {'Enabled': True}},
                'CCMOD': {'rho': 1e2, 'AutoRho': {'Enabled': True}}})


"""
Create solver object and solve.
"""

d = cbpdndl.ConvBPDNDictLearn(D0, vh, lmbda, opt, dimK=0, dimN=3)
D1 = d.solve()
print("ConvBPDNDictLearn solve time: %.2fs" % d.timer.elapsed('solve'))


"""
Display initial and final dictionaries: central temporal slice
"""

D1 = D1.squeeze()
fig = plot.figure(figsize=(14,7))
plot.subplot(1, 2, 1)
plot.imview(util.tiledict(D0[...,2,:]), fig=fig, title='D0')
plot.subplot(1, 2, 2)
plot.imview(util.tiledict(D1[...,2,:]), fig=fig, title='D1')
fig.show()


"""
Display initial and final dictionaries: central spatial vertical slice
"""

D1 = D1.squeeze()
fig = plot.figure(figsize=(14, 7))
plot.subplot(1, 2, 1)
plot.imview(util.tiledict(D0[2]), fig=fig, title='D0')
plot.subplot(1, 2, 2)
plot.imview(util.tiledict(D1[2]), fig=fig, title='D1')
fig.show()


"""
Get iterations statistics from solver object and plot functional value, ADMM primary and dual residuals, and automatically adjusted ADMM penalty parameter against the iteration number.
"""

its = d.getitstat()
fig = plot.figure(figsize=(20, 5))
plot.subplot(1, 3, 1)
plot.plot(its.ObjFun, fig=fig, xlbl='Iterations', ylbl='Functional')
plot.subplot(1, 3, 2)
plot.plot(np.vstack((its.XPrRsdl, its.XDlRsdl, its.DPrRsdl, its.DDlRsdl)).T,
          fig=fig, ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
          lgnd=['X Primal', 'X Dual', 'D Primal', 'D Dual'])
plot.subplot(1, 3, 3)
plot.plot(np.vstack((its.XRho, its.DRho)).T, fig=fig, xlbl='Iterations',
          ylbl='Penalty Parameter', ptyp='semilogy',
          lgnd=['$\\rho_X$', '$\\rho_D$'])
fig.show()


# Wait for enter on keyboard
input()
