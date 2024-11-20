# -*- coding: utf-8 -*-
"""
Version 0.9.0
"""
from psycopg import connect
import psycopg.sql as pg
import pandas.io.sql as pandasql
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import geopandas as gpd
import os
import shapely
import seaborn as sns
from shapely.geometry import Point
import matplotlib.font_manager as font_manager
import numpy as np
import pandas as pd
import copy
import datetime
import importlib

class font:
    """
    Class defining the global font variables for all functions.
    
    """
    
    leg_font = font_manager.FontProperties(family='Libre Franklin',size=9)
    normal = 'Libre Franklin'
    semibold = 'Libre Franklin SemiBold'


class colour():
    """
    Class defining the global colour variables for all functions.
    
    """
    purple = '#660159'
    grey = '#7f7e7e'
    orange = '#d95f02'
    green = '#0D9F73' 
    blue = '#253494'
    light_grey = '#777777'
    cmap = 'YlOrRd'
    teal = '#23a87f' 
    blue_grey = '#1b5872'
    wisteria = '#beaed4'
    brown ='#a6761d'
    vivid_pink = '#f0027f'

    # Purple shades
    purple_0 = '#440436'
    purple_1 = '#550347'
    purple_2 = '#660159'
    purple_3 = '#9c7b94'
    purple_4 = '#c0abbb'

    colours_map = {
        1: purple,
        2: orange,
        3: grey,
        4: green,
        5: wisteria,
        6: brown,
        7: blue,
        8: vivid_pink
    }
    def get_colour_from_index(self, index):
        return self.colours_map[index]

class geo:
    """
    Class for additional gis layers needed for the cloropleth map.
    
    """
    
    def ttc(con):
        """Function to return the TTC subway layer.
        
        Parameters
        ------------
        con : SQL connection object
            Connection object needed to connect to the RDS
        
        Returns
        --------
        gdf
            Geopandas Dataframe of the Subway Layer
        
        """
        query = '''
        
        SELECT * FROM gis.subway_to
        
        '''
        ttc = gpd.GeoDataFrame.from_postgis(query, con, geom_col='geom')
        ttc = ttc.to_crs(epsg=3857)
        
        # Below can be replaced by an apply lambda
        # in case one row is of a different type (e.g. MULTIPOLYGON vs POLYGON)
        #for index, row in ttc.iterrows():
        #    rotated = shapely.affinity.rotate(row['geom'], angle=-17, origin = Point(0, 0))
        #    ttc.loc[index, 'geom'] = rotated  
        ttc['geom']=ttc['geom'].apply(lambda x: shapely.affinity.rotate(x, angle=-17, origin = Point(0, 0)))
        
        return ttc
    
    def island(con):
        
        """Function to return a layer of the Toronto island. Since the island is classified in the same neighbourhood as the waterfront, in some cases its not completely accurate to show the island shares the same data as the waterfront. 
        
        Parameters
        ------------
        con : SQL connection object
            Connection object needed to connect to the RDS
        
        Returns
        --------
        gdf
            Geopandas Dataframe of the Toronto island.
        
        """
        
        query = '''

        SELECT 
        geom
        FROM tts.zones_tts06
        WHERE gta06 = 81

        '''

        island =  gpd.GeoDataFrame.from_postgis(query, con, geom_col='geom')
        # island  = island.to_crs({'init' :'epsg:3857'})
        island  = island.to_crs(epsg=3857)

        # Below can be replaced by an apply lambda
        # in case one row is of a different type (e.g. MULTIPOLYGON vs POLYGON)
        #for index, row in island.iterrows():
        #    rotated = shapely.affinity.rotate(row['geom'], angle=-17, origin = Point(0, 0)) 
        #    island.loc[index, 'geom'] = rotated
        island['geom']=island['geom'].apply(lambda x: shapely.affinity.rotate(x, angle=-17, origin = Point(0, 0)))

        return island

class charts:
    """
    Class defining all the charting functions.
    
    """
    
    global func
    def func():
        
        """Function to set global settings for the charts class. 
        
        """
        
        sns.set(font_scale=1.5) 
        mpl.rc('font',family='Libre Franklin')
    
    def chloro_map(con, df, lower, upper, title, **kwargs):
        """Creates a chloropleth map
        
        Parameters
        -----------
        con : SQL connection object
            Connection object needed to connect to the RDS
        df : GeoPandas Dataframe
            Data for the chloropleth map. The data must only contain 2 columns; the first column has to be the geom column and the second has to be the data that needs to be mapped.
        lower : int
            Lower bound for colourmap
        upper : int
            Upper bound for the colourmap
        title : str
            Legend label
        subway : boolean, optional, default: False
            True to display subway on the map
        island : boolean, optional, defailt: True
            False to grey out the Toronto island
        cmap : str, optional, default: YlOrRd
            Matplotlib colourmap to use for the map
        unit : str, optional
            Unit to append to the end of the legend tick
        nbins : int, optional, defualt: 2
            Number of ticks in the colourmap
            
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object
            
        """
        
        func()
        subway = kwargs.get('subway', False)
        island = kwargs.get('island', True)
        cmap = kwargs.get('cmap', colour.cmap)
        unit = kwargs.get('unit', None)
        nbins = kwargs.get('nbins', 2)
        
        df.columns = ['geom', 'values']
        light = '#d9d9d9'

        fig, ax = plt.subplots(dpi=450.0, figsize=(12,12))
        fig.set_size_inches(6.69,3.345)
        
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_axis_off()
    
        mpd = df.plot(column='values', ax=ax, vmin=lower, vmax=upper,  cmap = cmap, edgecolor = 'w', linewidth = 0.5)
        
        if island == False:
            island_grey = geo.island(con)
            island_grey.plot(ax=ax, edgecolor = 'w', linewidth = 4,  color = light)
            island_grey.plot(ax=ax, edgecolor = 'w', linewidth = 0,  color = light)
         
        if subway == True:
            ttc_df = geo.ttc(con)
            line = ttc_df.plot( ax=ax, linewidth =4, color = 'w', alpha =0.6) # ttc subway layer
            line = ttc_df.plot( ax=ax, linewidth =2, color = 'k', alpha =0.4) # ttc subway layer
    
         
        props = dict(boxstyle='round', facecolor='w', alpha=0)
        plt.text(0.775, 0.37, title, transform=ax.transAxes, wrap = True, fontsize=7, fontname = font.semibold,
                verticalalignment='bottom', bbox=props, fontweight = 'bold') # Adding the Legend Title
         
        
        cax = fig.add_axes([0.718, 0.16, 0.01, 0.22]) # Size of colorbar
         
        rect = patches.Rectangle((0.76, 0.01),0.235,0.43,linewidth=0.5, transform=ax.transAxes, edgecolor=light,facecolor='none')
        ax.add_patch(rect)
        
        ax.margins(0.1)
         
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=lower, vmax=upper))
        sm._A = []
        cbr = fig.colorbar(sm, cax=cax)
        cbr.outline.set_linewidth(0)
        tick_locator = ticker.MaxNLocator(nbins=nbins)
        cbr.locator = tick_locator
        cbr.update_ticks()
        cbr.ax.yaxis.set_tick_params(width=0.5)
        cbr.ax.tick_params(labelsize=6)  # Formatting for Colorbar Text
        for l in cbr.ax.yaxis.get_ticklabels():
            l.set_family(font.normal)
        
        if unit is not None:
            if 0 < upper < 10:
                ax.text(0.829, 0.32, unit, transform=ax.transAxes, wrap = True, fontsize=6, fontname = font.normal, verticalalignment='bottom', ha = 'left') 
            elif 10 <= upper < 100:
                ax.text(0.839, 0.32, unit, transform=ax.transAxes, wrap = True, fontsize=6, fontname = font.normal, verticalalignment='bottom', ha = 'left')
            elif 100 <= upper < 1000:
                ax.text(0.851, 0.32, unit, transform=ax.transAxes, wrap = True, fontsize=6, fontname = font.normal, verticalalignment='bottom', ha = 'left')
            elif 1000 <= upper < 100000:
                ax.text(0.862, 0.32, unit, transform=ax.transAxes, wrap = True, fontsize=6, fontname = font.normal, verticalalignment='bottom', ha = 'left')
            else:
                pass
            
        
        return fig, ax

    def histogram_chart(data, ylab, xlab, nbin, **kwargs):
        """Creates a histogram chart with specified nbin (nbin data)
        
        Parameters
        -----------
        data : array like or scalar
            Data for the line chart.
        ylab : str
            Label for the y axis.
        xlab : str
            Label for the x axis.
        xmax : int, optional, default is the max x value
            The max value of the x axis
        xmin : int, optional, default is the min x value
            The minimum value of the x axis
        nbin : int, optional, default is none
            The number of bins for the two dimensions
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object

        """

        func()
        xmax = kwargs.get('xmax', None)
        xmin = kwargs.get('xmin', 0)

        if (xmax is None):
            xmax = int(max(data))

        if (nbin is None):
            nbin = 10

        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(1,1, dpi=450.0)
        fig.set_size_inches(6.1, 4.2)
        ax.hist(data, bins=nbin, alpha=1.0, color=colour.purple)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_xlim(xmin, xmax)

        return fig, ax
        
    def line_chart(data, ylab, xlab, **kwargs):
        """Creates a line chart. x axis must be modified manually
        
        Parameters
        -----------
        data : array like or scalar
            Data for the line chart.
        ylab : str
            Label for the y axis.
        xlab : str
            Label for the x axis.
        ymax : int, optional, default is the max y value
            The max value of the y axis
        ymin : int, optional, default is 0
            The minimum value of the y axis
        baseline : array like or scalar, optional, default is None
            Data for another line representing the baseline.
        yinc : int, optional
            The increment of ticks on the y axis.
        
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object
        props
            Dictionary of the text annotation properties
            
        """
        
        func()
        ymax = kwargs.get('ymax', int(data.max()))
        ymin = kwargs.get('ymin', 0)
        baseline = kwargs.get('baseline', None)
        
        delta = (ymax - ymin)/4
        i = 0
        while True:
            delta /= 10
            i += 1
            if delta < 10:
                break
        yinc = kwargs.get('yinc', int(round(delta+1)*pow(10,i)))
        
        fig, ax =plt.subplots()
        ax.plot(data ,linewidth=3, color = colour.purple)
        if baseline is not None:
            ax.plot(baseline ,linewidth=3, color = colour.grey)

        plt.grid()
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        ax.set_facecolor('xkcd:white')

        plt.xlabel(xlab, fontsize=9, fontweight = 'bold', horizontalalignment='right', x=0, labelpad=10, 
                   fontname = font.normal)
        ax.grid(color='k', linestyle='-', linewidth=0.2)
        plt.ylabel(ylab, fontsize=9, fontweight = 'bold',
                   horizontalalignment='right', y=1.0, 
                   labelpad=10, fontname = font.normal)
        fig.set_size_inches(6.1, 4.1)
        plt.xticks(fontsize=9, fontname = font.normal)
        plt.yticks(range(ymin, ymax + yinc, yinc), fontsize =9,
                   fontname = font.normal)

        props = dict(boxstyle='round, pad=0.4',edgecolor=colour.purple,
                     linewidth = 2, facecolor = 'w', alpha=1)

        ax.set_ylim([ymin, ymax])
        fig.patch.set_facecolor('w')
        
        return fig, ax, props
    
    def tow_chart(data, ylab, **kwargs):
        """Creates a 7 day time of week line chart. Each data point represents 1 hour out of 168 hours.
        
        Parameters
        -----------
        data : array like or scalar
            Data for the tow chart. Data must only have 168 entries, with row 0 representing Monday at midnight.
        ylab : str
            Label for the y axis.
        ymax : int, optional, default is the max y value
            The max value of the y axis
        ymin : int, optional, default is 0
            The minimum value of the y axis
        yinc : int, optional
            The increment of ticks on the y axis.
        
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object
        props
            Dictionary of the text annotation properties
            
        """

        func()
        ymax = kwargs.get('ymax', None)
        ymin = kwargs.get('ymin', 0)
        
        
        ymax_flag = True
        if ymax == None:
            ymax = int(data.max())
            ymax_flag = False
        
        delta = (ymax - ymin)/3
        i = 0
        while True:
            delta /= 10
            i += 1
            if delta < 10:
                break
        yinc = kwargs.get('yinc', int(round(delta+1)*pow(10,i)))
        
        if ymax_flag == True:
            upper = ymax
        else:
            upper = int(3*yinc+ymin)
        
        fig, ax = plt.subplots(dpi=450.0)
        ax.plot(data, linewidth = 2.5, color = colour.purple)

        plt.grid()
        ax.set_xlim(0, 168)
        ax.set_facecolor('xkcd:white')

        plt.xlabel('Time of week', fontname = font.normal, fontsize=9, horizontalalignment='left', x=0, labelpad=3, fontweight = 'bold')
        ax.set_ylim([ymin, upper])

        ax.grid(color='k', linestyle='-', linewidth=0.2)
        plt.ylabel(ylab, fontname = font.normal, fontsize=9, horizontalalignment='right', y=1, labelpad=7, fontweight = 'bold')
        fig.set_size_inches(6.1, 1.8)


        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
        plt.yticks(range(ymin,upper+int(0.1*yinc), yinc), fontsize =9, fontname = font.normal)
        ax.set_xticks(range(0,180,12))
        ax.set_xticklabels(['0','12','0','12',
                                                            '0','12','0','12',
                                         '0','12','0','12','0','12'], fontname = font.normal, fontsize = 7, color = colour.light_grey)

        ax.xaxis.set_minor_locator(ticker.FixedLocator(list(range(12,180,24))))
        ax.xaxis.set_minor_formatter(ticker.FixedFormatter(['Monday','Tuesday',
                                                            'Wednesday','Thursday',
                                         'Friday','Saturday','Sunday']))
        ax.tick_params(axis='x', which='minor', colors = 'k', labelsize=9, pad =14)

        props = dict(boxstyle='round, pad=0.3',edgecolor=colour.purple, linewidth = 1.5, facecolor = 'w', alpha=1)

        ax.set_xlim([0,167])
        return fig, ax, props

    def stacked_chart(data_in, xlab, lab1, lab2, **kwargs):
        """Creates a stacked bar chart comparing 2 sets of data
        
        Parameters
        -----------
        data : dataframe
            Data for the stacked bar chart. The dataframe must have 3 columns, the first representing the y ticks, the second representing the baseline, and the third representing the next series of data.
        xlab : str
            Label for the x axis.
        lab1 : str
            Label in the legend for the baseline
        lab2 : str
            Label in the legend fot the next data series
        xmax : int, optional, default is the max s value
            The max value of the y axis
        xmin : int, optional, default is 0
            The minimum value of the x axis
        precision : int, optional, default is -1
            Decimal places in the annotations
        percent : boolean, optional, default is False
            Whether the annotations should be formatted as percentages
            
        xinc : int, optional
            The increment of ticks on the x axis.
        
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object
            
        """
        
        func()
        data = data_in.copy(deep=True)
        
        data.columns = ['name', 'values1', 'values2']
        
        xmin = kwargs.get('xmin', 0)
        xmax = kwargs.get('xmax', None)
        precision = kwargs.get('precision', -1)
        percent = kwargs.get('percent', False)
        
        xmax_flag = True
        if xmax == None:
            xmax = int(max(data[['values1', 'values2']].max()))
            xmax_flag = False
        
        delta = (xmax - xmin)/4
        i = 0
        while True:
            delta /= 10
            i += 1
            if delta < 10:
                break
        xinc = kwargs.get('xinc', int(round(delta+1)*pow(10,i)))

        if xmax_flag == True:
            upper = xmax
        else:
            upper = int(4*xinc+xmin)
        
        ind = np.arange(len(data))

        fig, ax = plt.subplots()
        fig.set_size_inches(6.1, len(data))
        ax.grid(color='k', linestyle='-', linewidth=0.25)

        p1 = ax.barh(ind+0.4, data['values1'], 0.4, align='center', color = colour.grey)
        p2 = ax.barh(ind, data['values2'], 0.4, align='center', color = colour.purple)
        ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        ax.xaxis.grid(True)
        ax.yaxis.grid(False)
        ax.set_yticks(ind+0.4/2)
        ax.set_xlim(0,upper)
        ax.set_yticklabels(data['name'])
        ax.set_xlabel(xlab,  horizontalalignment='left', x=0, labelpad=10, fontname = font.normal, fontsize=10, fontweight = 'bold')

        ax.set_facecolor('xkcd:white')
        j=0
        
        if precision < 1:
            data[['values1', 'values2']] = data[['values1', 'values2']].astype(int)
        for i in data['values2']:
            if i < 0.1*upper:
                ax.annotate(str(format(round(i,precision), ',')), xy=(i-0.015*upper, j-0.05), ha = 'right', color = 'k', fontname = font.normal, fontsize=10)
            else:
                ax.annotate(str(format(round(i,precision), ',')), xy=(i-0.015*upper, j-0.05), ha = 'right', color = 'w', fontname = font.normal, fontsize=10)
            j=j+1
        j=0.4
        for i in data['values1']:
            if i < 0.1*upper:
                ax.annotate(str(format(round(i,precision), ',')), xy=(i+0.015*upper, j-0.05), ha = 'left', color = 'k', fontname = font.normal, fontsize=10)
            else:
                ax.annotate(str(format(round(i,precision), ',')), xy=(i-0.015*upper, j-0.05), ha = 'right', color = 'w', fontname = font.normal, fontsize=10)
            j=j+1

        
        ax.legend((p1[0], p2[0]), (lab1, lab2), loc=4, frameon=False, prop=font.leg_font)
        plt.xticks(range(xmin,upper+int(0.1*xinc), xinc), fontname = font.normal, fontsize =10)
        plt.yticks( fontname = font.normal, fontsize =10)
        
        if percent == True:
            data_yoy = data
            data_yoy['percent'] = (data['values2']-data['values1'])*100/data['values1']
            j=0.15
            for index, row in data_yoy.iterrows():
                ax.annotate(('+' if row['percent'] > 0 else '')+str(format(int(round(row['percent'],0)), ','))+'%', 
                            xy=(max(row[['values1', 'values2']]) + (0.12 if row['values2'] < 0.1*upper else 0.03)*upper, j), color = 'k', fontname = font.normal, fontsize=10)
                j=j+1              

        return fig, ax
    
    def multi_stacked_bar_chart(data, xlab, lab1, lab2, lab3, **kwargs):
        """Creates a stacked bar chart comparing 3 sets of data
        
        Parameters
        -----------
        data : array like or scalar
            Data for the stacked bar chart.
        xlab : str
            Label for the x axis.
        lab1 : str
            Label in the legend for the baseline
        lab2 : str
            Label in the legend fot the next data series
        lab3 : str
            Label in the legend fot the next data series    
        xmax : int, optional, default is the max s value
            The max value of the y axis
        xmin : int, optional, default is 0
            The minimum value of the x axis
        precision : int, optional, default is 1
            Decimal places in the annotations
        xinc : int, optional
            The increment of ticks on the x axis.
        
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object
            
        """
        
        func()
        data = data.copy(deep=True)
        
        data.columns = ['name', 'values1', 'values2', 'values3']
        
        xmin = kwargs.get('xmin', 0)
        xmax = kwargs.get('xmax', None)
        precision = kwargs.get('precision', 1)
        percent = kwargs.get('percent', False)
        
        xmax_flag = True
        if xmax == None:
            xmax = int(max(data[['values1', 'values2', 'values3']].max()))
            xmax_flag = False
        
        delta = (xmax - xmin)/4
        i = 0
        while True:
            delta /= 10
            i += 1
            if delta < 10:
                break
        xinc = kwargs.get('xinc', int(round(delta+1)*pow(10,i)))

        if xmax_flag == True:
            upper = xmax
        else:
            upper = int(4*xinc+xmin)
        
        ind = np.arange(len(data))

        fig, ax = plt.subplots()
        fig.set_size_inches(6.1, len(data))
        ax.grid(color='k', linestyle='-', linewidth=0.25)
        p1 = ax.barh(ind, data['values1'], 0.4, align='center', color = colour.grey)
        p2 = ax.barh(ind, data['values2'], 0.4, align='center', color = colour.purple, left = data['values1'])
        p3 = ax.barh(ind, data['values3'], 0.4, align='center', color = colour.teal, left = (data['values1'] + data['values2']))
        ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        ax.xaxis.grid(True)
        ax.yaxis.grid(False)
        ax.set_yticks(ind)
        ax.set_xlim(0,upper)
        ax.set_yticklabels(data['name'])
        ax.set_xlabel(xlab,  horizontalalignment='left', x=0, labelpad=10, fontname = font.normal, fontsize=10, fontweight = 'bold')
        ax.set_facecolor('xkcd:white')

        # if precision < 1:   # removed this so it does not round or cast to int prematurely. Also, casting to int truncates the decimal WITHOUT rounding.
        #     data[['values1', 'values2','values3']] = data[['values1', 'values2','values3']].astype(int)
        horiz_nudge = 0.2
        for index, i in enumerate(data['values3']):
            offset = data['values3'][index]+ data['values2'][index] + data['values1'][index]
            # if value is less  than 0.5%, do not show data label, if less than 4%, show data label above the bar, else show label on the bar
            if i < 0.5:
                continue
            if i < 4:
                ax.annotate(str(format(round(i,precision), ',')), xy=((offset+offset-i)/2+horiz_nudge, index+0.3), ha = 'center', color = 'k', fontname = font.normal, fontsize=10)
            else:
                ax.annotate(str(format(round(i,precision), ',')), xy=((offset+offset-i)/2+horiz_nudge, index-0.07), ha = 'center', color = 'w', fontname = font.normal, fontsize=10)
        for index, i in enumerate(data['values2']):
            offset = data['values2'][index] + data['values1'][index]
            if i < 0.5:
                continue
            if i < 4:
                ax.annotate(str(format(round(i,precision), ',')), xy=((offset+offset-i)/2+horiz_nudge, index+0.3), ha = 'center', color = 'k', fontname = font.normal, fontsize=10)
            else:
                ax.annotate(str(format(round(i,precision), ',')), xy=((offset+offset-i)/2+horiz_nudge, index-0.07), ha = 'center', color = 'w', fontname = font.normal, fontsize=10)
        for index, i in enumerate(data['values1']):
            offset = data['values1'][index]
            if i < 0.5:
                continue
            if i < 4:
                ax.annotate(str(format(round(i,precision), ',')), xy=((offset+offset-i)/2+horiz_nudge, index+0.3), ha = 'center', color = 'k', fontname = font.normal, fontsize=10)
            else:
                ax.annotate(str(format(round(i,precision), ',')), xy=((offset+offset-i)/2+horiz_nudge, index-0.07), ha = 'center', color = 'w', fontname = font.normal, fontsize=10)
        
        ax.legend((p1[0], p2[0], p3[0]), (lab1, lab2, lab3), bbox_to_anchor=(1.05, 1.0), loc='upper left', frameon=False, prop=font.leg_font)
        # ax.legend((p1[0], p2[0], p3[0]), (lab1, lab2, lab3), bbox_to_anchor=(0.5, 1.15), loc='upper center', ncol=3, frameon=False, prop=font.leg_font)
        # plt.subplots_adjust(bottom=0.2) # Adjust layout to make room for the legend above the plot
        plt.xticks(range(xmin,upper+int(0.1*xinc), xinc), fontname = font.normal, fontsize =10)
        plt.yticks( fontname = font.normal, fontsize =10)
        
        return fig, ax
    
    def horizontal_grouped_bar_chart(data: pd.DataFrame, **kwargs: dict) -> (plt.figure, plt.axes):
        '''
        Creates a horizontal grouped bar chart. Number of bars in
        each group to plot is determined from the number of
        columns in input dataframe, while the number of groups is
        determined by the number of rows.

        Parameters
        -----------

        Required:
        data : pd.DataFrame
            Data for the grouped bar chart.

        Optional:
        ylab : str
            Label for the y axis.
        xlab : str
            Label for the x axis.
        xmax : float 
            The max value of the x axis.
        xmin : float
            The minimum value of the x axis
            Should include this if minimum < 0.
        xinc : float
            The increment of ticks on the x axis.
        ax : plt.axes
            The axis that the plot will be located on.
        plot_size : (int, int)
            Custom plot dimensions.
        precision : int
            Decimal points in the annotations.
        percent : bool 
            Flag determining whether to show percentage change between
            baseline column (assumed to be the first column) and
            remaining columns.
        additional_annotations : dict
            Dictionary with keys of type (int, int) and values
            of type (str), indicating the coordinates and
            annotation to be added.
        legend : list[str]
            A list of labels to be used for the legend.

        Returns
        --------
        fig 
            Matplotlib fig object
        ax
            Matplotlib ax object
        '''
        return general_grouped_bar_chart(
            data=data,
            param_axis='x',
            index_axis='y',
            horizontal=True,
            standard_plot_size=(6.1, len(data)*1.5),
            grid_y=False,
            **kwargs
            )

    def vertical_grouped_bar_chart(data: pd.DataFrame, **kwargs: dict) -> (plt.figure, plt.axes):
        '''
        Creates a vertical grouped bar chart. Number of bars in
        each group to plot is determined from the number of
        columns in input dataframe, while the number of groups is
        determined by the number of rows.

        Parameters
        -----------

        Required:
        data : pd.DataFrame
            Data for the grouped bar chart.

        Optional:
        ylab : str 
            Label for the y axis.
        xlab : str 
            Label for the x axis.
        ymax : float 
            The max value of the y axis.
        ymin : float  
            The minimum value of the y axis
            Should include this if minimum < 0.
        yinc : float 
            The increment of ticks on the y axis.
        ax : plt.axes 
            The axis that the plot will be located on.
        plot_size : (int, int)
            Custom plot dimensions.
        precision : int
            Decimal points in the annotations.
        percent : int
            Flag determining whether to show percentage change between
            baseline column (assumed to be the first column) and
            remaining columns.
        additional_annotations : dict
            Dictionary with keys of type (int, int) and values
            of type (str), indicating the coordinates and
            annotation to be added.
        legend : list[str]
            A list of string objects to be used for the legend.

        Returns
        --------
        fig
            Matplotlib fig object
        ax
            Matplotlib ax object
        '''
        return general_grouped_bar_chart(
            data=data,
            param_axis='y',
            index_axis='x',
            horizontal=False,
            standard_plot_size=(len(data)*1.5, 6.1),
            grid_x=False,
            **kwargs
            )

    def bar_chart(data_in, xlab,**kwargs):
        """Creates a bar chart
        
        Parameters
        -----------
        data : dataframe
            Data for the bar chart. The dataframe must have 2 columns, the first representing the y ticks, and the second representing the data
        xlab : str
            Label for the x axis.
        xmax : int, optional, default is the max s value
            The max value of the y axis
        xmin : int, optional, default is 0
            The minimum value of the x axis
        precision : int, optional, default is -1
            Decimal places in the annotations
            
        xinc : int, optional
            The increment of ticks on the x axis.
        
        Returns 
        --------
        fig
            Matplotlib fig object
        ax 
            Matplotlib ax object
            
        """
        func()
        data = data_in.copy(deep=True)
        
        data.columns = ['name', 'values1']
        
        xmin = kwargs.get('xmin', 0)
        xmax = kwargs.get('xmax', None)
        precision = kwargs.get('precision', 0)
        
        xmax_flag = True
        if xmax == None:
            xmax = data['values1'].max()
            xmax_flag = False

        delta = (xmax - xmin)/4
        i = 0
        while True:
            if delta < 10:
                break
            delta /= 10
            i += 1
        xinc = kwargs.get('xinc', int(round(delta+1)*pow(10,i)))

        if xmax_flag == True:
            upper = xmax
        else:
            upper = int(4*xinc+xmin)
        
        ind = np.arange(len(data))

        fig, ax = plt.subplots()
        fig.set_size_inches(6.1, len(data)*0.7)
        ax.grid(color='k', linestyle='-', linewidth=0.25)
        p2 = ax.barh(ind, data['values1'], 0.75, align='center', color = colour.purple)
        ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        ax.xaxis.grid(True)
        ax.yaxis.grid(False)
        ax.set_yticks(ind)
        ax.set_xlim(0,upper)
        ax.set_yticklabels(data['name'])
        ax.set_xlabel(xlab,  horizontalalignment='left', x=0, labelpad=10, fontname = font.normal, fontsize=10, fontweight = 'bold')

        ax.set_facecolor('xkcd:white')
        j=0
        
        if precision < 1:
            data['values1'] = data['values1'].astype(int)

        j=0
        for i in data['values1']:
            if i < 0.1*upper:
                ax.annotate(str(format(round(i,precision), ',')), xy=(i+0.015*upper, j-0.05), ha = 'left', color = 'k', fontname = font.normal, fontsize=10)
            else:
                ax.annotate(str(format(round(i,precision), ',')), xy=(i-0.015*upper, j-0.05), ha = 'right', color = 'w', fontname = font.normal, fontsize=10)
            j=j+1

        
        plt.xticks(range(xmin,upper+int(0.1*xinc), xinc), fontname = font.normal, fontsize =10)
        plt.yticks( fontname = font.normal, fontsize =10)
        
        return fig, ax


    def multi_linechart(data:pd.DataFrame, ylab:str, xlab:str, **kwargs:dict) -> (plt.figure, plt.axes):
        '''
        Creates a line chart of one or more lines.
        Number of lines to plot determined from columns in input dataframe.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data for the line chart.
        ylab : str
            Label for the y axis.
        xlab : str
            Label for the x axis.
        ymax : float, optional
            The max value of the y axis.
        ymin : float, optional
            The min value of the y axis. Should include this if ymin < 0.
        yinc : float, optional
            The increment of ticks on the y axis.
        ax : plt.axes, optional
            The axis that the plot will be located on. 
        plot_size : (int, int), optional
            The dimensions of the plot if given a custom size.
        minor_x : bool, optional 
            When set to True, a minor grid is added to the plot along x axis. 
        minor_y : bool, optional 
            When set to True, a minor grid is added to the plot along y axis. 
        num_minor_x: int, optional
            The number of minor ticks between major ticks along the x axis. 
        num_minor_y: int, optional
            The number of minor ticks between major ticks along the y axis. 
        shaded_areas : dict[(str, str): (Any, Any)], optional 
            Start and end x coordinates indicate range of shaded region
            and must be specified.
            Label can be specified or left as None. 
            Colour can be specified or left as None in which case light 
            grey is used by default.
            
        Returns 
        --------
        fig 
            Matplotlib fig object
        ax
            Matplotlib ax object
        ''' 
        
        func() 

        ymax, ymin, yinc, upper = calculate_params(
            df=data,
            param_axis ='y',
            **kwargs
            )

        fig, ax = plot_line_data(
            df=data,
            axis=kwargs.get('ax',None),
            legend=kwargs.get('legend',None)
            )
        
        set_plot_style(
            fig=fig,
            ax=ax,
            plot_size=kwargs.get('plot_size', (6.1, 4.1)), 
            grid_x=True,
            grid_y=True,
            grid_minor_x=kwargs.get('minor_x',False),
            grid_minor_y=kwargs.get('minor_y',False),
            min_value=ymin,
            max_value=ymax, 
            param_axis='y'
            )

        set_ticks(
            ax=ax,
            df=data,
            min_value=ymin, 
            max_value=ymax, 
            inc=yinc,
            minor_x=kwargs.get('minor_x',False),
            minor_y=kwargs.get('minor_y',False),
            num_minor_x=kwargs.get('num_minor_x',None),
            num_minor_y=kwargs.get('num_minor_y',None)
            )

        set_labels(
            ax=ax,
            xlab=xlab,
            ylab=ylab
            )

        add_shaded_areas(
            ax=ax,
            df=data,
            shaded_areas=kwargs.get('shaded_areas', None)
            )

        return fig, ax

def calculate_params(df:pd.DataFrame, param_axis:str, **kwargs:dict) -> (float, float, float, float): 
    '''
    Checks if minimum, maximum and increment values are passed into the plotting function 
    for the specified axis, and returns these. Otherwise, calculates them.

    Parameters
    ----------
    df :  pd.DataFrame
        Data for the line chart.
    param_axis : str
        Axis along which max, min, upper, inc values should be calculated. 
    xmin : float, optional
        Minimum value of x axis. 
    xmax : float, optional
        Maximum value of x axis.
    xinc : float, optional
        The increment of ticks on the x axis.
    ymin : float, optional
        Minimum value of y axis
    ymax : float, optional
        Maximum value of y axis.
    yinc : float, optional
        The increment of ticks on the y axis.

    Returns 
    -------
        max_value : float
            Maximum value along param_axis 
        min_value : float
            Minimum value along param_axis 
        inc : float
            Increment of ticks along param_axis
        upper : float
            Value used for placing of annotations. 
    '''
    # TODO: check whether the calculation of inc can be improved, at what value does it fail,
    # maybe print a warning if the user should specify it.

    max_value = kwargs.get(f'{param_axis}max', int(df.max(axis=1).max(axis=0)))
    min_value = kwargs.get(f'{param_axis}min', 0)
    delta, i = calculate_delta(max_value, min_value)
    inc = kwargs.get(f'{param_axis}inc', int(round(delta+1)*pow(10,i)))
    if kwargs.get(f'{param_axis}max',None)==None:
        upper=max_value 
    else: 
        upper=int(min_value+4*inc)
    return max_value, min_value, inc, upper 

def calculate_delta(max_value:float, min_value:float) -> (float, float):
    '''
    Returns parameters used to find the size of the y or x axis increments.

    Parameters
    ----------
    max_value : float 
        Maximum value of data being plotted in non-index axis. 
    min_value : float 
        Minimum value of data being plotted in non-index axis. 

    Returns
    -------
    float 
        The spacing between ticks in non-index axis.
    float 
        Order of magnitude of spacing. 
    '''

    delta = (max_value - min_value)/4
    i = 0
    while True:
        delta /= 10
        i += 1
        if delta < 10:
            break
    return delta, i

def plot_line_data(df:pd.DataFrame, axis:plt.axes, legend:list[str]) -> (plt.figure, plt.axes):
    '''
    Plots all columns in the input dataframe as lines in one graph 
    on the specified axis object.

    Parameters 
    ---------- 
    df : pd.DataFrame
        Data to be plotted.
    axis : plt.axes
        Prespecified axis to be used for the plot. 
    legend : list[str]
        List of labels to be used for the legend.
    Returns 
    ------- 
    fig 
        Matplotlib fig object
    ax
        Matplotlib ax object
    '''

    fig, ax = init_fig(axis)
    colour_instance = colour()
    lines = []

    for i, col in enumerate(df.columns):
        hex_code = colour_instance.get_colour_from_index(i+1)
        lines.extend(ax.plot(df[col], linewidth=3, color=hex_code))

    if legend != None:
        ax.legend(handles=lines,
                  labels=legend, 
                  loc='upper left',
                  bbox_to_anchor=(1.04, 1),
                  frameon=False, 
                  prop=font.leg_font,
                  borderpad=0
        )
    return fig, ax

def plot_grouped_bar_data(df:pd.DataFrame, ax:plt.axes, legend:list[str], horizontal:bool) -> (plt.figure, plt.axes):
    '''
    Plots all columns in the input dataframe as bars in a grouped bar graph.
    Also adds a legend if a list of strings is provided.

    Parameters 
    ----------
    df : pd.DataFrame 
        Input dataframe being plotted.
    ax : plt.axes 
        Axis object to be used for the plot if specified by user.
    legend : list[str]
        List of labels to be used for the legend.
    horizontal : bool 
        Flag indicating whether this is a horizontal plot.

    Returns
    -------
    fig 
        Matplotlib figure object.
    ax
        Matplotlib axis object.
    '''

    fig, ax = init_fig(ax)
    bar_width = 1/(len(df.columns)+1)
    adjustment = 0
    colour_instance = colour()
    ind = np.arange(len(df))
    bars = []

    for i, col in enumerate((reversed(df.columns)) if horizontal else (df.columns)):
        hex_code = colour_instance.get_colour_from_index(i+1)
        bars.append(getattr(ax, 'barh' if horizontal else 'bar')(ind+adjustment, df[col], bar_width, align='center', color = hex_code))
        adjustment += bar_width

    if legend != None:
        ax.legend(handles=bars[::-1] if horizontal else bars,
                  labels=legend , 
                  loc='upper left',
                  bbox_to_anchor=(1.04, 1),
                  frameon=False, 
                  prop=font.leg_font,
                  borderpad=2
        )
        
    return fig, ax 

def init_fig(axis:plt.axes) -> (plt.figure, plt.axes):
    '''
    Sets the plot fig and axes objects to be the ones specified by the user or 
    creates new ones.

    Parameters
    ----------
    axis : plt.axes 
        Axis object for the plot prespecified by the user.

    Returns
    -------
    fig 
        Matplotlib figure object.
    ax 
        Matplotlib axis object.
    '''

    if axis != None:
        ax = axis
        fig = ax.get_figure()
    else:
        fig, ax = plt.subplots()    

    return fig, ax

def set_plot_style(fig:plt.figure, 
                   ax:plt.axes, 
                   plot_size:(int, int), 
                   grid_x:bool, 
                   grid_y:bool, 
                   min_value:float, 
                   max_value:float, 
                   param_axis:str,
                   grid_minor_x:bool = False,
                   grid_minor_y:bool = False
                   )-> None:
    '''
    Sets size, background and grid for plot.

    Parameters 
    ---------- 
    fig : plt.figure
        Figure object corresponding to plot.
    ax : plt.axes
        Axis object corresponding to plot.
    plot_size : (int, int)
        The dimensions of the plot in inches. 
    grid_x : bool 
        Whether there is a grid parallel to x ticks. 
    grid_y : bool
        Whether there is a grid parallel to y ticks. 
    min_value : float
        Minimum value of param_axis.
    max_value : float
        Maximum value of param_axis.
    param_axis : str
        Axis opposite to index axis.
    grid_minor_x : bool, optional 
        When set to True, a minor grid is added to the plot along x axis. 
    grid_minor_y : bool, optional 
        When set to True, a minor grid is added to the plot along y axis. 
    '''

    fig.set_size_inches(plot_size)
    getattr(ax, 'set_ylim' if param_axis == 'y' else 'set_xlim')([min_value, max_value])
    ax.set_facecolor('xkcd:white')
    set_grid(ax, grid_x, grid_y, grid_minor_x, grid_minor_y)

def set_grid(ax:plt.axes,
             grid_x:bool,
             grid_y:bool, 
             grid_minor_x:bool, 
             grid_minor_y:bool)-> None:
    '''
    Sets the grid for plot. 

    Parameters
    ----------
    ax : plt.axes 
        Axis object corresponding to plot.
    grid_x : bool
        Flag indicating whether to add a grid along the x axis. 
    grid_y : bool
        Flag indicating whether to add a grid along the y axis.
    grid_minor_x : bool, optional 
        When set to True, a minor grid is added to the plot along x axis. 
    grid_minor_y : bool, optional 
        When set to True, a minor grid is added to the plot along y axis. 
    '''
    # Minor ticks 
    if grid_minor_x: 
        ax.xaxis.grid(grid_minor_x,
                      which='minor',
                      color='k',
                      linestyle='-',
                      linewidth=0.05)
    if grid_minor_y:
        ax.yaxis.grid(grid_minor_y,
                      which='minor',
                      color='k',
                      linestyle='-',
                      linewidth=0.05)
    # Major ticks
    if grid_x: 
        ax.xaxis.grid(grid_x,
                      which='major',
                      color='k',
                      linestyle='-',
                      linewidth=0.2)
    if grid_y: 
        ax.yaxis.grid(grid_y,
                      which='major',
                      color='k',
                      linestyle='-',
                      linewidth=0.2)


def set_ticks(ax:plt.axes,
              df:pd.DataFrame,
              min_value:float,
              max_value:float,
              inc:float,
              index_axis:str='x',
              offset:float=0.0,
              minor_x:bool=False,
              minor_y:bool=False,
              num_minor_x:int=None, 
              num_minor_y:int=None) -> None: 
    '''
    Sets x and y axis tick locations and tick labels.
    
    Parameters 
    ----------
    ax : plt.axes 
        Matplotlib axes object.
    df : pd.DataFrame 
        Dataset being plotted.
    min_value : float 
        Minimum value along non index axis.
    max_value : float 
        Maximum value along non index axis. 
    inc : float  
        Incrementation of ticks along non index axis. 
    index_axis : str 
        The index of the DataFrame object, 
        e.g. the x axis for a line chart. 
        Defaults to 'x'.
    offset : float 
        Offset in the placement of ticks. 
        Used for grouped bar charts to center labels. 
        Defaults to 0.0. 
    minor_x : bool, optional 
        When set to True, a minor grid is added to the plot along x axis. 
    minor_y : bool, optional 
        When set to True, a minor grid is added to the plot along y axis. 
    num_minor_x: int, optional
        The number of minor ticks between major ticks along the x axis. 
    num_minor_y: int, optional
        The number of minor ticks between major ticks along the y axis. 
    '''
    NUM_SLICES = int(len(df)/8) # makes it so that there is 8 date labels along x axis
    
    # Checking if data being plotted is indexed by date 
    # Assumption: dates are plotted on x axis 
    if type(df.index) == pd.core.indexes.datetimes.DatetimeIndex:
        locs = mpl.dates.date2num(df.index)[::NUM_SLICES]
        label_rotation = 45
        index_labels = df.index.strftime('%Y-%m-%d')[::NUM_SLICES]

    else: 
        locs = [x+offset for x in np.arange(len(df.index))]
        label_rotation = 0
        index_labels = df.index
        
    ####################### Minor ticks #########################
    if minor_x:
        if num_minor_x!=None:
            ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(num_minor_x))
        else: 
            ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
            
    if minor_y: 
        if num_minor_y!=None:
            ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(num_minor_y))
        else: 
            ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())

    ####################### Major ticks ######################### 
    # Set the locations for the ticks of the two axes 
    getattr(ax, 'yaxis' if index_axis == 'y' else 'xaxis').set_major_locator(mpl.ticker.FixedLocator(locs))
    getattr(ax, 'xaxis' if index_axis == 'y' else 'yaxis').set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

    # Set the formatting of the labels
    getattr(ax, 'set_xticks' if index_axis == 'y' else 'set_yticks')(range(min_value, max_value + inc, inc), 
                                                                    labels=range(min_value, max_value + inc, inc), 
                                                                    fontsize = 10, 
                                                                    fontname = font.normal)
    getattr(ax, 'set_yticklabels' if index_axis == 'y' else 'set_xticklabels')(labels=index_labels, 
                                                                               rotation=label_rotation,
                                                                               fontsize=10)

def set_labels(ax:plt.axes, xlab:str, ylab:str) -> None:
    '''
    Set the labels of the y and x axes.

    Parameters
    ----------
    ax : plt.axes
        Matplotlib axes object. 
    xlab : str
        Label of x axis. 
    ylab : str
        Label of y axis. 
    '''

    if xlab != None:
        ax.set_xlabel(xlab, fontsize=9, fontweight='bold',
                      horizontalalignment='right', x=0, 
                      labelpad=10,
                      fontname = font.normal)
    if ylab != None:
        ax.set_ylabel(ylab, fontsize=9, fontweight='bold',
                      horizontalalignment='right', y=1.0, 
                      labelpad=10, fontname = font.normal)

def add_bar_annotations(ax:plt.axes, df:pd.DataFrame, upper:float, precision:int, percent:bool, horizontal:bool, additional_annotations:dict) -> None:
    '''
    Adds bar annotations to bar charts, and other annotations if specified. 

    Parameters 
    ----------
    ax : plt.axes
        Matplotlib axes object corresponding to plot. 
    df : pd.DataFrame 
        Dataset being plotted.
    upper : float
        Bar value used for determining placement of annotation. 
    precision : int 
        Decimal points in the annotations. 
    percent : bool
        Flag determining whether to show percentage change between 
        baseline column (assumed to be the first column) and 
        remaining columns.
    horizontal : bool  
        Flag to indicate if this is a horizontal bar graph.
    additional_annotations : dict
        Dictionary with keys of type (int, int) and values 
        of type (str), indicating the coordinates and 
        annotation to be added. 
    '''
    bar_width = 1/(len(df.columns)+1)

    if precision < 1:
        df[df.columns] = df[df.columns].astype(int)

    if horizontal:
        horizontal_bar_annotations(df, ax, bar_width, upper, precision, percent)
    else:
        vertical_bar_annotations(df, ax, bar_width, upper, precision, percent)

    # TODO: make this more customizable - add another function possibly?
    if additional_annotations != None:
        for xy, text in additional_annotations.items():
            ax.annotate(text=text, xy=xy, ha = 'left', color = 'k', fontname = font.normal, fontsize=10)

def horizontal_bar_annotations(df:pd.DataFrame, ax:plt.axes, bar_width:float, upper:float, precision:int, percent:bool) -> None:
    '''
    Adds value annotations to horizontal grouped or regular bar charts. 

    Parameters 
    ----------
    df : pd.DataFrame 
        Input dataframe being plotted. 
    ax : plt.axes 
        Axis object corresponding to the plot.
    bar_width : float 
        The width of each bar. 
    upper : float 
        Bar value used for determining placement of annotation. 
    precision : int 
        Decimal points in the annotations. 
    percent : bool
        Flag determining whether to show percentage change between 
        baseline column (assumed to be the first column) and 
        remaining columns.
    '''
    HORIZONTAL_CUTOFF = 0.2 * upper
    ANNOTATION_OFFSET = 0.015 * upper
    PERCENT_HRZNTL_OFFSET = 0.04
    PERCENT_VRTCL_OFFSET =  (0.15) if len(df.columns) == 2 else (-0.05) 

    # Adding annotations for values of each bar 
    for k in range(len(df.columns)):
        j = bar_width*(len(df.columns)-1-k)
        for i in df[df.columns[k]]:
            xy = (i + ANNOTATION_OFFSET, j-0.05) if i < HORIZONTAL_CUTOFF else (i - ANNOTATION_OFFSET, j-0.05) 
            ha = 'left' if i < HORIZONTAL_CUTOFF else 'right'
            color = 'k' if i < HORIZONTAL_CUTOFF else 'w'
            ax.annotate(str(format(round(i,precision), ',')), xy=xy, ha=ha, color=color, fontname=font.normal, fontsize=10)
            j+=1

    # Adding percentage difference between 'baseline' bar and all other bars (optional)
    if percent: 
        df_percent = copy.deepcopy(df)
        for k, col in enumerate(reversed(df.columns[1:])):
            df_percent[f'percent{k}'] = 100 * (df[col] - df[df.columns[0]]) / df[df.columns[0]]  # percent change = 100*(col-baseline)/baseline
            j = bar_width*k
            for index, row in df_percent.iterrows():
                ax.annotate(
                    ('+' if row[f'percent{k}'] > 0 else '') + str(format(int(round(row[f'percent{k}'])), ',')) + '%', # Rounds percentage to closest integer
                    xy = (row[col] + (4*PERCENT_HRZNTL_OFFSET if row[col] < HORIZONTAL_CUTOFF else PERCENT_HRZNTL_OFFSET) * upper, j + PERCENT_VRTCL_OFFSET),  # Placement of percentage annotation 
                    color = 'k',
                    fontname = font.normal,
                    fontsize=10
                    )
                j += 1
        
def vertical_bar_annotations(df:pd.DataFrame, ax:plt.axes, bar_width:float, upper:float, precision:int, percent:bool) -> None:
    '''
    Adds value annotations to vertical grouped or regular bar charts. 

    Parameters 
    ----------

    df : pd.DataFrame 
        Input dataframe being plotted. 
    ax : plt.axes 
        Axis object corresponding to the plot.
    bar_width : float 
        The width of each bar. 
    upper : float 
        Bar value used for determining placement of annotation. 
    precision : int 
        Decimal points in the annotations. 
    percent : bool
        Flag determining whether to show percentage change between 
        baseline column (assumed to be the first column) and 
        remaining columns.
    '''
    VERTICAL_CUTOFF = 0.1 * upper
    ANNOTATION_OFFSET = 0.015 * upper
    PERCENT_OFFSET = 0.03

    # Adding annotations for values of each bar 
    for k in range(len(df.columns)):
        j = bar_width*k
        for i in df[df.columns[k]]:
            xy = (j, i + ANNOTATION_OFFSET) if i < VERTICAL_CUTOFF else (j, i - ANNOTATION_OFFSET)
            va = 'top' if i >= VERTICAL_CUTOFF else 'center'
            color = 'w' if i >= VERTICAL_CUTOFF else 'k'
            ax.annotate(str(format(round(i, precision), ',')), xy=xy, ha='center', va=va, color=color, fontname=font.normal, fontsize=10)
            j += 1

    # Adding percentage difference between 'baseline' bar and all other bars (optional)
    if percent: 
        df_percent = copy.deepcopy(df)
        for k, col in enumerate(df.columns[1:]):
            df_percent[f'percent{k}'] = 100 * (df[col] - df[df.columns[0]]) / df[df.columns[0]]  # percent change = 100*(col-baseline)/baseline
            j = bar_width * (k + 1)
            for index, row in df_percent.iterrows():
                ax.annotate(
                    ('+' if row[f'percent{k}'] > 0 else '') + str(format(int(round(row[f'percent{k}'])), ',')) + '%', # Rounds percentage to closest integer
                    xy = (j, row[col] + (4*PERCENT_OFFSET if row[col] < VERTICAL_CUTOFF else PERCENT_OFFSET) * upper),  # Placement of percentage annotation 
                    ha='center',
                    color = 'k',
                    fontname = font.normal,
                    fontsize=10
                    )
                j += 1
                
def add_shaded_areas(ax:plt.axes, df:pd.DataFrame, shaded_areas: dict) -> None:
    '''
    Adds shaded areas to plot if specified by user. 

    Paramaters 
    ----------
    df : pd.DataFrame
        Data for the grouped bar chart.
    ax : plt.axes 
        Axis object being used. 
    shaded_areas : dict 
        Dictionary with the following format:
        {(label, colour): (x_start, x_end)}. 
        Start and end x coordinates indicate range of shaded region
        and must be specified.
        Label can be specified or left as None. 
        Colour can be specified or left as None in which case light 
        grey is used by default.
    '''
    if shaded_areas==None:
        return 
    colour_instance = colour()
    for (label, color), location in shaded_areas.items():
        color=colour_instance.light_grey if color==None else color
        ax.axvspan(location[0], 
                   location[1], 
                   alpha=0.2, 
                   color=color)
        # Show the label if it is not empty 
        if label != None:
            ax.text(s=label,
                    x=location[0],
                    y=ax.get_ylim()[1],
                    ha='left',
                    va='top',
                    rotation=90,
                    fontname=font.normal,
                    fontsize=9
                   )
        
def general_grouped_bar_chart(data:pd.DataFrame, param_axis:str, index_axis:str, standard_plot_size:(int, int), horizontal:bool, grid_x:bool=True, grid_y:bool=True, **kwargs:dict) -> (plt.figure, plt.axes):
        '''
        Creates a horizontal or vertical grouped bar chart. Number of
        bars in each group to plot is determined from the number of
        columns in input dataframe, while the number of groups is
        determined by the number of rows.

        Parameters
        -----------
        data : pd.DataFrame
            Data for the grouped bar chart.
        param_axis : str
            Axis along which bars are plotted.
        index_axis : str
            Axis containing labels for bars. 
        standard_plot_size :  (int, int) 
            The standard size depending on the type of graph (horizontal or vertical).
        horizontal : bool
            Flag indicating whether plot is horizontal. 
        ylab : str, optional
            Label for the y axis.
        xlab : str, optional
            Label for the x axis.
        xmax or ymax : float, optional
            The max value of the x or y axis.
        xmin or ymin : float, optional
            The minimum value of the x or y axis
            Should include this if minimum < 0.
        xinc or yinc : float, optional
            The increment of ticks on the x or y axis.
        ax : plt.axes, optional
            The axis that the plot will be located on.
        plot_size : (int, int), optional
            Custom plot dimensions. 
        precision : int, optional
            Decimal points in the annotations. 
        percent : bool, optional
            Flag determining whether to show percentage change between 
            baseline column (assumed to be the first column) and 
            remaining columns.
        additional_annotations : dict, optional
            Dictionary with keys of type (int, int) and values 
            of type (str), indicating the coordinates and 
            annotation to be added. 
        legend : list[str], optional
            A list of labels to be used for the legend.

        Returns
        --------
        fig
            Matplotlib fig object
        ax
            Matplotlib ax object
        '''

        BAR_WIDTH = 1/(len(data.columns)+1)
        TICK_OFFSET = (len(data.columns)-1) * BAR_WIDTH/2

        func()

        max_value, min_value, inc, upper = calculate_params(
            df=data,
            param_axis=param_axis,
            **kwargs
        )

        fig, ax = plot_grouped_bar_data(
            df=data,
            ax=kwargs.get('ax', None), 
            legend=kwargs.get('legend', None),
            horizontal=horizontal
        )

        set_plot_style(
            fig=fig,
            ax=ax,
            min_value=min_value,
            max_value=max_value,
            param_axis=param_axis,
            plot_size=kwargs.get('plot_size', standard_plot_size),
            grid_x=grid_x,
            grid_y=grid_y
        )

        set_ticks(
            ax=ax,
            min_value=min_value,
            max_value=max_value,
            inc=inc,
            index_axis=index_axis,
            df=data,
            offset=TICK_OFFSET
        )

        set_labels(
            ax=ax,
            xlab=kwargs.get('xlab', None),
            ylab=kwargs.get('ylab', None)
        )

        add_bar_annotations(
            ax=ax,
            df=data,
            upper=upper,
            horizontal=horizontal,
            precision=kwargs.get('precision', -1),
            percent=kwargs.get('percent', False),
            additional_annotations=kwargs.get('annotations', None)
        )


        return fig, ax
