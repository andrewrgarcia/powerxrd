Welcome to powerxrd's documentation!
=======================================

The Python Toolkit That Might Finally Replace Origin — and Give FullProf a Headache
----------------------------------------------------------------------------------------

.. figure:: ../img/icon_xrd.png
  :width: 200
  :alt: Alternative text
  :target: https://github.com/andrewrgarcia/powerxrd

  `Check out powerxrd's open-source on GitHub <https://github.com/andrewrgarcia/powerxrd>`_

A Python package designed to manage data from powder XRD experiments.  
The sole open-source GitHub project with a working, stand-alone Rietveld refinement feature.  
It now includes a working Rietveld refinement engine (**MVR: Minimum Viable Rietveld**) for cubic systems.

In a nutshell, powerxrd is an open-source Python package for XRD data analysis.  
While Origin may still be preferred for more complex XRD workflows, the average Python user may find powerxrd easier and more flexible.

Check out the :doc:`usage` section for further information, including how to :ref:`installation` the project. 

Contributors Wanted: Develop Rietveld Refinement for PowerXRD's Vertical XRD Analysis Integration
............................................................................................................

We're seeking open-source contributors to help us develop a complete and efficient Rietveld refinement method for PowerXRD. 
This ambitious project has the potential to replace more complex refinement software, such as MAUD and Profex, by integrating
all XRD processing steps from data acquisition to crystal analysis and plotting.

If you're interested in getting involved in this exciting project, we would love to have your contributions.

Ways to contribute:
- Read up on Rietveld refinement via the :doc:`rietveld` section.
- Help develop the `CubicModel` and `RefinementWorkflow` in our `source code <https://github.com/andrewrgarcia/powerxrd/blob/main/powerxrd/model.py>`_.
- Join the discussion on the `enhancement issue <https://github.com/andrewrgarcia/powerxrd/issues/4>`_.
- Sponsor or star us on the `main GitHub repository <https://github.com/andrewrgarcia/powerxrd>`_.

Colab Notebook
..............................

If you prefer learning using a Jupyter notebook style, take a look at our Colab Notebook.

.. image:: ../img/colaboratory.png
  :width: 500
  :alt: Alternative text
  :target: https://colab.research.google.com/drive/1_Eq-cW6LSPPnaRjkbeHaC81Wfbd8mQS-?usp=sharing

.. note::

   This project is under active development.


Contents
--------

.. toctree::

   usage
   api


Rietveld Refinement 
----------------------------------

.. toctree::

   rietveld
