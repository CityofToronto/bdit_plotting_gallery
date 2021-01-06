# -*- coding: utf-8 -*-
"""
Version 0.8.0 


"""
from psycopg2 import connect
import psycopg2.sql as pg
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

class font:
    """
    Class defining the global font variables for all functions.
    
    """
    
    leg_font = font_manager.FontProperties(family='Libre Franklin',size=9)
    normal = 'Libre Franklin'
    semibold = 'Libre Franklin SemiBold'
    
    
class colour:
    """
    Class defining the global colour variables for all functions.
    
    """
    purple = '#660159'
    grey = '#7f7e7e'
    light_grey = '#777777'
    cmap = 'YlOrRd'
    
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
        # ttc = ttc.to_crs({'init' :'epsg:3857'})
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

        fig, ax = plt.subplots()
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
        
        fig, ax =plt.subplots()
        ax.plot(data, linewidth = 2.5, color = colour.purple)

        plt.grid()
        ax.set_facecolor('xkcd:white')

        plt.xlabel('Time of week', fontname = font.normal, fontsize=9, horizontalalignment='left', x=0, labelpad=3, fontweight = 'bold')
        ax.set_ylim([ymin,upper])

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
                ax.annotate(str(format(round(i,precision), ',')), xy=(i-0.015*upper, j-0.05), ha = 'right', color = 'w', fontname = font.normal, fontsize=10)
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
                ax.annotate('+'+str(format(int(round(row['percent'],0)), ','))+'%', xy=(max(row[['values1', 'values2']]) + 0.03*upper, j), 
                                                                                           color = 'k', fontname = font.normal, fontsize=10)
                j=j+1
                

        return fig, ax
    
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
