"""
RICK Time-of-Week Line Chart
============================

Example time-of-week line chart.
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


CONFIG = configparser.ConfigParser()
# CONFIG.read(r'C:\Users\rliu4\Documents\Python\config.cfg')
CONFIG.read(r'/home/cnangini/db.cfg')
dbset = CONFIG['DBSETTINGS']
con = connect(**dbset)
################################
#Data Collection
#----------------
#
#This Section grabs and formats the data.
query = '''

WITH sum AS (

SELECT pickup_datetime, hr, sum(count) as count, extract(month from pickup_datetime) as mon, extract(year from pickup_datetime) as yr,
extract(dow from pickup_datetime) as dow FROM ptc.trip_data_agg_ward_25


WHERE pickup_datetime > '2018-08-31'
GROUP BY pickup_datetime, hr

)
, collect AS (
SELECT  avg(count) as count, hr, dow from sum
group by hr, dow)

SELECT period_name, period_uid, count, hr, CASE WHEN dow = 0 THEN 7 ELSE dow END AS dow, 
CASE WHEN swatch IS NULL THEN '#999999' ELSE swatch END AS swatch
FROM collect
LEFT JOIN ptc.period_lookup_simple ON dow=period_dow AND hr=period_hr
LEFT JOIN ptc.periods_simple USING (period_uid)
ORDER BY dow, hr

'''
count_18 = pandasql.read_sql(query,con)

fig, ax, prop = rick.charts.tow_chart(data = count_18['count'], ylab='Trips', ymax = 14000, yinc= 3500)
