"""
RICK Bar Chart
==================

Example bar chart from the RICK module.
"""

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
os.environ["PROJ_LIB"]=r"C:\Users\rliu4\AppData\Local\Continuum\anaconda3\Library\share"
import importlib
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager

################################
#Data Collection
#----------------
#
#This creates a test dataframe to use
pass_data = {'cat': ['PTC','Taxi',  'Trip Making Population'],
        'TTC Pass': [22,16,16],
        }

transit_pass = pd.DataFrame(pass_data,columns= ['cat', 'TTC Pass'])
transit_pass  = transit_pass .reindex(index=transit_pass .index[::-1])

fig, ax = rick.charts.bar_chart(transit_pass, xlab='Trips')
