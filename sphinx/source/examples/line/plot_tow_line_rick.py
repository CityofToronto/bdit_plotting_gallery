"""
RICK Time-of-Week Line Chart
============================

Example time-of-week line chart.
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
dt= list(range(168))

# y-axis
# line 1
y1= [np.cos(d/10)*50+np.random.randint(60, 200)+d/2 for d in dt]

# Create dataframe to be plotted
data = {'dt':dt, 'y1':y1}
df_multi = pd.DataFrame(data) 

df_multi_dt = df_multi.set_index('dt')

fig, ax, props = rick.charts.tow_chart(df_multi_dt , ylab='Trips', ymax = 350)
fig.tight_layout()
plt.show()
plt.savefig("sphinx/source/examples/line/YZtest_tow_line.png")