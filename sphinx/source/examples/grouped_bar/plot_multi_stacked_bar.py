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
data1 = {
    'Location': ['Scarborough', 'Etobicoke York', 'North York', 'East York'],
    '2016': [58640, 57210, 59490, 63090],
    '2018': [93810, 90690, 84720, 93550],
    '2020': [81538, 77456, 80235, 73692]
}

df = pd.DataFrame(data1)
##df = df.set_index('Category')

fig, ax = rick.charts.multi_stacked_bar_chart(df, xlab = 'Trips', lab1 = '2016', lab2 = '2018', lab3 = '2020', xmax= 250000)
fig.tight_layout()
plt.show()