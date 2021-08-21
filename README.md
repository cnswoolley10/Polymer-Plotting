# Polymer-Plotting
Plotting various models for polymers in python.

DISCLAIMER: This program was written by a student with < 1 year coding experience.
Some bits may not be best optimised, pls no hate, feedback always welcome :)

This is also the first time I've used GitHub and have absolutely no clue what I'm doing.

This code is available as a package on the Python Package Index (PyPI): https://pypi.org/project/PolymerPlotting/
Installation and running goes:
 - Make sure you have an up to date copy of python installed
 - In command line/powershell/commandprompt install the package and its dependencies with "pip install PolymerPlotting"
 - Enter the python environment and input (without the quotes):
        "from PolymerPlotting import PolymerPlottingGUI as PPG"
        "PPG.main()"
 - One can equivalently create and run a .py file containing the same lines for the same effect (such as "RunPolymerPlotting.py" included here)

In this GitHub Repo exists some code for plotting polymer chains.
The core is built around 'polymer_chains.py', which defines classes for various models of chain, if you've coded before then understanding this will be pretty easy.
You can use the objects defined in 'polymer_chains.py' to write your own code for maximum flexibility.
If you don't like coding then you can run 'PolymerPlottingGUI.py' to get a user interface version, with lots of pre-defined functionality, but less flexibility.

Python dependencies are: Numpy, Matplotlib and PySimpleGUI (GUI only).
