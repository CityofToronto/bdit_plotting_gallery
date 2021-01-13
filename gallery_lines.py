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

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def lines1(df_lines, sett):
    '''Creates a line chart based on the number of columns in the input.
    '''
    print("Hello world ")
    return

def lines2(df_lines, sett):
    '''Creates another line chart.
    Parameters
    -----------
    df_orig : pandas dataframe
        Data for the chloropleth map. The data must only contain 2 columns; the first column has to be the geom column and the second has to be the data that needs to be mapped.
    '''
    print("Hello lines2")
    return
