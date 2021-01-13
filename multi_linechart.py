# -*- coding: utf-8 -*-
"""
Version 0.8.0 


"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd 
import numpy as np 
import datetime
import math
import os
#os.environ["PROJ_LIB"]=r"C:\Users\rliu4\AppData\Local\Continuum\anaconda3\Library\share"
import importlib
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates
from matplotlib.lines import Line2D # for legend

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def multi_linechart(df_lines, sett):
    '''Creates a line chart based on the number of columns in the input dataframe.

    Parameters
    -----------
    df_orig : pandas dataframe
        First column contain the x-values, subsequent column(s) contain y-values.
    sett : dict
        Contains optional styling and annotation specification for all visual
        elements (axes, grid, lines, legend, title, labels). If empty, defaults
        will be used.
    ymax : int, optional, default is the max y value
        The max value of the y axis
    sett['body'] : dict key, optional
        The body section contains global style parameters. If empty, defaults
        will be used.
    sett['body']['font-size'] : int, optional
        Global font size for plot. Default 12.
    sett['body']['font-family'] : str, optional
        Global font family for plot. Default 'sans-serif'.
    sett['body']['sans-serif-list'] : array, optional
        An array of sans-serif fonts. The first font in the array that is installed
        in the system will be used. Default 'Libre Franklin'.
    
    Returns 
    --------
    fig
        Matplotlib fig object
    ax 
        Matplotlib ax object

    '''
    df=df_line.copy()

    # ----------------------------------------------
    # Setup the figure
    fig, ax =plt.subplots(1)
    fig.set_size_inches(18, 5)
    ax = plt.gca()

    return fig, ax

