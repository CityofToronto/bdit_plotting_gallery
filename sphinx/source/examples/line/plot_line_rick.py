"""
RICK Line Chart
==================

Example line chart from the RICK package, with an additional baseline plot and custom formatted x axis.
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
#Data Collection
#----------------
#
#This Section creates example data.

# x-axis
dt=[2015, 2016, 2017, 2018, 2019, 2020]

# y-axis
# line 1
y1=[100, 120, 115, 135, 150, 120]

# Create dataframe to be plotted
data = {'dt':dt, 'y1':y1}
df_multi = pd.DataFrame(data) 

df_multi_dt = df_multi.set_index('dt')

fig, ax, props = rick.charts.line_chart(df_multi_dt, xlab='Dates', ylab= "Values", ymin =50, ymax=200)
fig.tight_layout()
plt.show()
plt.savefig("sphinx/source/examples/line/YZtest_line.png")


