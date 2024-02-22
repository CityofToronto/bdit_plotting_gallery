"""
RICK Multi Stacked Bar Chart
=======================

Example of a horizontal grouped bar chart.
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


################################
#multi_stacked_bar_chart
#--------------------------
#
#This Section uses the revised multi_stacked_bar_chart function with a customized dataframe.

np.random.seed(42)
data = {
    'Year': [2015, 2016, 2017, 2018],
    'Group1': np.random.randint(10, 50, 4),
    'Group2': np.random.randint(20, 60, 4)
}
df = pd.DataFrame(data)
##df = df.set_index('Category')

fig, ax = rick.charts.bar_chart_stacked_on_top(df, xlab = 'Numbers', lab1 = 'Group1', lab2 = 'Group2')
fig.tight_layout()
plt.show()
plt.savefig("sphinx/source/examples/grouped_bar/YZtest_bar_chart_stacked_on_top.png")