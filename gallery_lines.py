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

def multi_linechart(df_lines, sett):
    """Creates a line chart of one or more lines.

    Number of lines to plot determined from columns in input dataframe.

    Args:
        df_lines (pandas dataframe): First column contains x-axis data, subsequent column(s) contain y-axis data.
        sett (dict): Styling and annotation specification for all visual elements (e.g. axes, grid, lines, legend, title, labels). If empty, defaults are used.
        sett['body'] (dict key, optional): Global style parameters for 'font-size', 'font-family', and 'fontfamily-list'. If empty, defaults are used.
        sett['body']['font-size'] (int, optional dict key): Global font size for plot. Default 12.
        sett['body']['font-family'] (str, optional dict key): Global font family for plot. Default 'sans-serif'.
        sett['body']['fontfamily-list'] (array, optional dict key): Array of fonts in font-family. The first font in the array that is installed in the system will be used. Default 'Libre Franklin'.
        sett['body']['stroke'] (hex str, optional dict key): Global colour for lines and text. Default '#000000'.
        sett['body']['stroke-width'] (num, optional dict key): Global linewidth. Default 2.
        sett['body']['border'] (str, optional dict key): Global border style for lines. Default 'solid'.

    Returns:
        fig (Matplotlib fig object)

        ax (Matplotlib ax object)
    """
    print("Hello world ")
    return


def lines3(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
