"""
RICK Grouped Bar Chart
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
#stacked_chart
#--------------------------
#
#This Section uses the revised stacked_chart function with a customized dataframe.

np.random.seed(42)
data = {
    'Location': ['Scarborough', 'Etobicoke York', 'North York', 'East York'],
    '2016': [4640, 7210, 9490, 43090],
    '2018': [13810, 20690, 24720, 93550]
}
df = pd.DataFrame(data)
##df = df.set_index('Category')

fig, ax = rick.charts.stacked_chart(df, xlab = 'Trips', lab1 = '2016', lab2 = '2018',  percent = True)
fig.tight_layout()
plt.show()
plt.savefig("sphinx/source/examples/grouped_bar/YZtest_stacked_chart.png")