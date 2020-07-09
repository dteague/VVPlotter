.. VVPlotter documentation master file, created by
   sphinx-quickstart on Wed Jul  8 12:53:41 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Installation Guide
==================

This package has removed ROOT dependencies so one can use python3 (suggested!). For ease, this guide with assume one is using a virtual environment. Below shows how to set that up

Python3 
*******

.. code-block:: python

   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt

**Note:** if you are new to virtual environments, to exit it, simply type ``deactivate``. You will need to make sure virtual environment is activated every time you want to run the code

Quick Start
===========

The two main scripts in this repo are for making plots and for setting up combine. The structures for both are fairly similar, especially since they both take the same input (``VVAnalysis`` output files)

To run the plotting and combine code, simply type

.. code-block:: bash

   ./make_hist.py -i <infile> -a <Analysis>  # Plotting code
   ./setup_combinepy -i <infile> -a <Analysis> -o <outdir>  # Combine code

Or if you need more information, just run using the ``--help`` option

MVA_studies' documentation
==========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   self
   running_plotting
   running_combine
   code_basics
   code_plothelps
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
