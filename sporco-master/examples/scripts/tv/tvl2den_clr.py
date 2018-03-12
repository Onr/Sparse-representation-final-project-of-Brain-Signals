#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""
Colour ℓ2-TV Denoising
======================

This example demonstrates the use of class :class:`.tvl2.TVL2Denoise` for removing Gaussian white noise from a colour image using Total Variation regularization with an ℓ2 data fidelity term (ℓ2-TV denoising).
"""


from __future__ import print_function
from builtins import input
from builtins import range

import numpy as np

from sporco.admm import tvl2
from sporco import util
from sporco import metric
from sporco import plot


"""
Load reference image.
"""

img = util.ExampleImages().image('monarch.png', scaled=True,
                                 idxexp=np.s_[:,160:672])


"""
Construct test image corrupted by Gaussian white noise with a 0.05 standard deviation.
"""

np.random.seed(12345)
imgn = img + np.random.normal(0.0, 0.05, img.shape)


"""
Set regularization parameter and options for ℓ2-TV denoising solver. The regularization parameter used here has been manually selected for good performance.
"""

lmbda = 0.04
opt = tvl2.TVL2Denoise.Options({'Verbose': True, 'MaxMainIter': 200,
                'gEvalY': False, 'AutoRho': {'Enabled': True}})


"""
Create solver object and solve, returning the the denoised image ``imgr``.
"""

b = tvl2.TVL2Denoise(imgn, lmbda, opt)
imgr = b.solve()


"""
Display solve time and denoising performance.
"""

print("TVL2Denoise solve time: %5.2f s" % b.timer.elapsed('solve'))
print("Noisy image PSNR:    %5.2f dB" % metric.psnr(img, imgn))
print("Denoised image PSNR: %5.2f dB" % metric.psnr(img, imgr))


"""
Display reference, corrupted, and denoised images.
"""

fig = plot.figure(figsize=(20, 5))
plot.subplot(1, 3, 1)
plot.imview(img, fig=fig, title='Reference')
plot.subplot(1, 3, 2)
plot.imview(imgn, fig=fig, title='Corrupted')
plot.subplot(1, 3, 3)
plot.imview(imgr, fig=fig, title=r'Restored ($\ell_2$-TV)')
fig.show()


"""
Get iterations statistics from solver object and plot functional value, ADMM primary and dual residuals, and automatically adjusted ADMM penalty parameter against the iteration number.
"""

its = b.getitstat()
fig = plot.figure(figsize=(20, 5))
plot.subplot(1, 3, 1)
plot.plot(its.ObjFun, fig=fig, xlbl='Iterations', ylbl='Functional')
plot.subplot(1, 3, 2)
plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T, fig=fig,
          ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
          lgnd=['Primal', 'Dual'])
plot.subplot(1, 3, 3)
plot.plot(its.Rho, fig=fig, xlbl='Iterations', ylbl='Penalty Parameter')
fig.show()


# Wait for enter on keyboard
input()
