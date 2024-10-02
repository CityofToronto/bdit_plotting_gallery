"""
RICK Histogram Chart
=======================

Example of a histogram chart.
"""
import os
import os.path as osp
import sys
sys.path.append(osp.dirname(osp.dirname(osp.dirname(osp.dirname(osp.dirname(osp.abspath(__file__)))))))

from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd 
import configparser
from psycopg2 import connect
import psycopg2.sql as pg
import pandas.io.sql as pandasql
import numpy as np 
import datetime
import math
import rick
import geopandas as gpd
import os
import shapely
from shapely.geometry import Point
####os.environ["PROJ_LIB"]=r"C:\Users\rliu4\AppData\Local\Continuum\anaconda3\Library\share"
import importlib
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
import numpy as np

################################
#histogram_chart
#--------------------------
#
#This Section uses the histogram_chart function with a customized dataframe.

rng = np.random.default_rng()
numbers = rng.normal(size=10_000)

##plt.hist(numbers)
fig, ax = rick.charts.histogram_chart(numbers, ylab = 'hist', xlab = '', xmin=-3, nbin=100)
fig.tight_layout()
plt.show()