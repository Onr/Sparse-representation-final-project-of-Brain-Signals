FISTADFT
========

:class:`.FISTADFT` specialises :class:`.FISTA` to solve problems of the form

.. math::
   \mathrm{argmin}_{\mathbf{x}} \;
    f(\mathbf{x}) + g(\mathbf{x}) \;\;,

where :math:`f, g` are convex functions and :math:`f` is smooth, and all the updates and gradients are computed in DFT domain.

Classes derived from :class:`.FISTADFT` should override/define the same
methods and attributes described in the :doc:`FISTA class documentation <fista>`.

See :class:`.fista.cbpdn.ConvBPDN` as an example of a class derived from
:class:`.FISTADFT`.
