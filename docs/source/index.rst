Welcome to powerxrd's documentation!
=======================================

The Open-Source Python Package That'll Make You Want to Say 'Origin Who?'
----------------------------------------------------------------------------

.. figure:: ../img/icon_xrd.png
  :width: 200
  :alt: Alternative text
  :target: https://github.com/andrewrgarcia/powerxrd

  `Check out powerxrd's open-source on GitHub <https://github.com/andrewrgarcia/powerxrd>`_


A Python package designed to manage data from powder XRD experiments. The sole open-source Github project that is known to be developing a Rietveld refining method. 
In a nutshell, powerxrd is an open-source Python package for XRD data analysis. While Origin may still be preferred for more complex XRD analysis, the average Python user may find powerxrd to be more user-friendly than Origin for this type of analysis. 

Check out the :doc:`usage` section for further information, including how to :ref:`installation` the project. 

Contributors Wanted: Develop Rietveld Refinement for PowerXRD's Vertical XRD Analysis Integration
............................................................................................................

We're seeking open-source contributors to help us develop a complete and efficient Rietveld refinement method for PowerXRD. 
This ambitious project has the potential to replace more complex refinement software, such as MAUD and Profex, by integrating
all XRD processing steps from data acquisition to crystal analysis and plotting. While this will be a significant undertaking,
we believe the potential benefits are substantial. 

If you are interested in getting involved in this exciting project, we would love to have your contributions.
There are several ways you can contribute, including familiarizing yourself with Rietveld refinement by checking the :doc:`rietveld`
section, helping develop the Rietveld class in the `source file <https://github.com/andrewrgarcia/powerxrd/blob/main/powerxrd/main.py>`_,
contributing to the enhancement issue on our `Issue page <https://github.com/andrewrgarcia/powerxrd/issues/4>`_, 
or sponsoring our project on the `main Github repository page <https://github.com/andrewrgarcia/powerxrd>`_.


.. autoclass:: powerxrd.Rietveld
   :members: 


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