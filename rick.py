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
import pandas as pd
import copy

class font:
    """
    Class defining the global font variables for all functions.
    
    """
    
    leg_font = font_manager.FontProperties(family='DejaVu Sans',size=9)
    normal = 'DejaVu Sans'
    semibold = 'DejaVu Sans SemiBold'


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

    colours_map = {
        1: purple,
        2: grey,
        3: orange,
        4: blue,
        5: green,
        6: light_grey
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
        mpl.rc('font',family='DejaVu Sans')

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
                ax.annotate(str(format(round(i,precision), ',')), xy=(i+0.015*upper, j-0.05), ha = 'left', color = 'k', fontname = font.normal, fontsize=10)
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
    
    def stacked_chart_quad(data_in, xlab, lab1, lab2, lab3, lab4, **kwargs):
        """Creates a stacked bar chart comparing 4 sets of data
        
        Parameters
        -----------
        data : dataframe
            Data for the stacked bar chart. The dataframe must have 5 columns, the first representing the y ticks, the second representing the baseline, and the third representing the next series of data.
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
        
        data.columns = ['name', 'values1', 'values2', 'values3', 'values4']
        
        xmin = kwargs.get('xmin', 0)
        xmax = kwargs.get('xmax', None)
        precision = kwargs.get('precision', -1)
        percent = kwargs.get('percent', False)
        
        xmax_flag = True
        if xmax == None:
            xmax = int(max(data[['values1', 'values2', 'values3', 'values4']].max()))
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
        fig.set_size_inches(6.1, len(data)*1.5)
        ax.grid(color='k', linestyle='-', linewidth=0.25)

        p1 = ax.barh(ind+0.6, data['values1'], 0.2, align='center', color = colour.green)
        p2 = ax.barh(ind+0.4, data['values2'], 0.2, align='center', color = colour.blue)
        p3 = ax.barh(ind+0.2, data['values3'], 0.2, align='center', color = colour.grey)
        p4 = ax.barh(ind, data['values4'], 0.2, align='center', color=colour.purple)
        ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        ax.xaxis.grid(True)
        ax.yaxis.grid(False)
        ax.set_yticks(ind+0.6/2)
        ax.set_xlim(0,upper)
        ax.set_yticklabels(data['name'])
        ax.set_xlabel(xlab,  horizontalalignment='left', x=0, labelpad=10, fontname = font.normal, fontsize=10, fontweight = 'bold')

        ax.set_facecolor('xkcd:white')
        
        
        if precision < 1:
            data[['values1', 'values2', 'values3', 'values4']] = data[['values1', 'values2', 'values3', 'values4']].astype(int)
        
        j = 0.0
        for k in range(4,0,-1):

            for i in data[f'values{k}']:
                if i < 0.1*upper:
                    ax.annotate(str(format(round(i,precision), ',')), xy=(i+0.015*upper, j-0.05), ha = 'left', color = 'k', fontname = font.normal, fontsize=10)
                else:
                    ax.annotate(str(format(round(i,precision), ',')), xy=(i-0.015*upper, j-0.05), ha = 'right', color = 'w', fontname = font.normal, fontsize=10)
                j=j+1
            j = j-len(data[f'values{k}']) + 0.2
            

        ax.legend((p1[0], p2[0], p3[0], p4[0]), (lab1, lab2, lab3, lab4), loc=4, frameon=False, prop=font.leg_font)
        plt.xticks(range(xmin,upper+int(0.1*xinc), xinc), fontname = font.normal, fontsize =10)
        plt.yticks( fontname = font.normal, fontsize =10)
        
        if percent == True:
            j = 0.15 
            data_yoy = data
            for k in range(3,0,-1):
                data_yoy[f'percent{k}'] = (data['values4']-data[f'values{k}'])*100/data[f'values{k}']
                
                for index, row in data_yoy.iterrows():
                    ax.annotate(('+' if row[f'percent{k}'] > 0 else '')+str(format(int(round(row[f'percent{k}'],0)), ','))+'%', 
                                xy=(max(row[['values1', 'values2', 'values3', 'values4']]) + (0.12 if row['values4'] < 0.1*upper else 0.03)*upper, j), color = 'k', fontname = font.normal, fontsize=10)
                    j+=1
                j = j-len(data_yoy) + 0.2
                    

        return fig, ax
    
    def horizontal_grouped_bar_chart(data: pd.DataFrame, **kwargs: dict) -> (plt.figure, plt.axes):

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


    def multi_linechart(df_line, sett):
        '''Creates a line chart of one or more lines.
    
        Number of lines to plot determined from columns in input dataframe.
    
    
        '''
        df=df_line.copy()
    
        # ----------------------------------------------
        # Setup the figure
        fig, ax =plt.subplots(1)
        fig.set_size_inches(18, 5)
        ax = plt.gca()
    
        # ----------------------------------------------
        # Default styling params if not defined in sett
        if 'body' in sett:
            dflt={
                'font-size':(12 if 'font-size' not in sett['body']
                             else sett['body']['font-size']),
                'font-family':('sans-serif' if 'font-family' not in sett['body']
                             else sett['body']['font-family']),
                'fontfamily-list':(['Libre Franklin', 'DejaVu Sans'] if 'fontfamily-list'
                              not in sett['body']
                              else sett['body']['fontfamily-list']),
                'stroke':('#000000' if 'stroke' not in sett['body']
                             else sett['body']['stroke']),
                'stroke-width':(2 if 'stroke-width' not in sett['body']
                             else sett['body']['stroke-width']),
                'border':('solid' if 'border' not in sett['body']
                             else sett['body']['border'])
            }
        else:
            dflt={
                'font-size':12, 'font-family':'sans-serif',
                'fontfamily-list':['Libre Franklin', 'DejaVu Sans'],
                'stroke':'#000000', 'stroke-width':2, 'border':'solid'
            }
    
        mpl.rcParams['font.family'] = dflt['font-family']
        if dflt['font-family']=='sans-serif':
            mpl.rcParams['font.sans-serif']=dflt['fontfamily-list']
    
    #     mpl.rcParams.update({
    #         'font.size': dflt['font-size'],
    #         'font.family': dflt['font-family']
    #     })
        # ----------------------------------------------------------------
        # WEIRD HACK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # For some reason, mpl.rcParams needs to be run TWICE before it
        # actually gets set. So just before calling the function,
        # make sure you set it again...
        # ----------------------------------------------------------------
    
        # ----------------------------------------------
        # Define line-number-dependent params
        num_lines=df.shape[1] - 1
    
        col_names=['xcol']
        ymax_array=[]
        for n in range(num_lines):
            col_names.append('ycol_' + str(n))
            ymax_array.append(df.iloc[:,n+1].max())
    
        df.columns=col_names
    
        # ----------------------------------------------
        # title
        if 'title' in sett:
            if 'title_params' in sett:
                title_size=(
                    dflt['font-size'] if 'font-size' not in
                    sett['title_params']
                    else sett['title_params']['font-size'])
                loc=('center' if 'loc' not in sett['title_params']
                     else sett['title_params']['loc'])
            ax.set_title(sett['title'], fontsize=title_size,  loc=loc)
    
        # ----------------------------------------------
        # grid
        if 'major_grid_on' in sett and sett['major_grid_on']==True:
            if 'major_grid' in sett:
                c=('gray' if 'stroke' not in sett['major_grid']
                   else sett['major_grid']['stroke'])
                b=('-' if 'border' not in sett['major_grid']
                   else sett['major_grid']['border'])
            else:
                c='gray'
                b='-'
            plt.grid(b=True, which='major', color=c, linestyle=b)
        if 'minor_grid_on' in sett and sett['minor_grid_on']==True:
            if 'minor_grid' in sett:
                c=('gray' if 'stroke' not in sett['minor_grid']
                   else sett['minor_grid']['stroke'])
                b=('-' if 'border' not in sett['minor_grid']
                   else sett['minor_grid']['border'])
            else:
                c='gray'
                b='-'
            plt.grid(b=True, which='minor', color=c, linestyle=b)
    
        # ----------------------------------------------
        # axes (both)
        mpl.rcParams['axes.linewidth'] = 0.3
        ticklength=2 if 'ticklength' not in sett else sett['ticklength']
        tickwidth=1 if 'tickwidth' not in sett else sett['tickwidth']
        ax.tick_params(width=tickwidth, length=ticklength)
    
        # y-axis
        if 'yaxis' in sett:
            ymin=(0 if 'ymin' not in sett['yaxis']
                  else sett['yaxis']['ymin'])
            ymax=(np.max(ymax_array)*(1 + 0.1) if 'ymax'
                  not in sett['yaxis']
                  else sett['yaxis']['ymax'])
    
            # y-axis label
            label=('' if 'label' not in sett['yaxis']
                   else sett['yaxis']['label'])
            labelsize=(dflt['font-size'] if 'labelsize'
                       not in sett['yaxis']
                       else sett['yaxis']['labelsize'])
            plt.ylabel(label, fontsize=labelsize)
    
            # Format y-axis tick labels
            ticklabelsize=(dflt['font-size'] if 'ticklabelsize'
                      not in sett['yaxis']
                      else sett['yaxis']['ticklabelsize'])
            ax.tick_params(axis='y', labelsize=ticklabelsize)
    
            # comma format
            precision=('.0f' if 'precision'
                       not in sett['yaxis']
                       else sett['yaxis']['precision'])
            ax.yaxis.set_major_formatter(
                mpl.ticker.StrMethodFormatter('{x:,' + precision + '}')
            )
        else:
            ymin=0
            ymax=np.max(ymax_array)*(1 + 0.1)
    
        delta = (ymax - ymin)/4
        i = 0
        while True:
            delta /= 10
            i += 1
            if delta < 10:
                break
        if 'yinc' in sett:
            yinc=sett['yinc']
        else:
            yinc = int(round(delta+1)*pow(10,i))
    
        plt.ylim(top=ymax, bottom=ymin)
    
        # ----------------------------------------------
        # x-axis
        if 'xaxis' in sett:
            # x-axis label
            label=('' if 'label' not in sett['xaxis']
                   else sett['xaxis']['label'])
            labelsize=(dflt['font-size'] if 'labelsize'
                       not in sett['xaxis']
                       else sett['xaxis']['labelsize'])
            plt.xlabel(label, fontsize=labelsize)
    
            # x-axis tick labels
            if 'major_loc' in sett['xaxis']: # x-values are dates
                date_form_mjr = sett['xaxis']['major_loc']['date_form']
                ax.xaxis.set_major_formatter(date_form_mjr)
            if 'minor_loc' in sett['xaxis']:
                date_form_mnr = sett['xaxis']['minor_loc']['date_form']
                ax.xaxis.set_minor_locator(date_form_mnr)
    
            # x-axis tick label size
            ticklabelsize=(dflt['font-size'] if 'ticklabelsize'
                      not in sett['xaxis']
                      else sett['xaxis']['ticklabelsize'])
            ax.tick_params(axis='x', labelsize=ticklabelsize,
                           labelbottom=True)
        else:
            # Default x-axis tick lines
            ax.tick_params(axis='x', labelsize=dflt['font-size'],
                           labelbottom=True)
    
        # ----------------------------------------------
        # Plot data and legend
        if 'legend' in sett:
            legend_loc=('upper left' if 'loc' not in sett['legend']
                        else sett['legend']['loc'])
            leg_array=[]
            custom_lines=[]
    
        for n in range(num_lines):
            if 'lines' in sett:
                line_colour=(dflt['stroke'] if 'stroke' not in
                             sett['lines'][n]
                             else sett['lines'][n]['stroke'])
                line_width=(dflt['stroke-width'] if 'stroke-width'
                            not in sett['lines'][n]
                            else sett['lines'][n]['stroke-width'])
                border_style=(dflt['border'] if 'border-style' not in
                              sett['lines'][n]
                              else sett['lines'][n]['border-style'])
            else:
                line_colour=dflt['stroke']
                line_width=dflt['stroke-width']
                border_style=dflt['border']
    
            ax.plot(df['xcol'], df['ycol_' + str(n)], linewidth=line_width,
                    color = line_colour, linestyle=border_style)
    
            # Legend
            if 'legend' in sett:
                leg_array.append(sett['lines'][n]['label'])
                custom_lines.append(Line2D([0], [0],
                                           color=line_colour,
                                           lw=line_width,
                                           linestyle=border_style)
                                   )
    
        if 'legend' in sett:
            ax.legend(custom_lines, leg_array, loc=legend_loc,
                      prop={"size": dflt['font-size']},
                      ncol=len(df.columns))
    
        # ----------------------------------------------
        # Plot shaded areas
        if 'shaded' in sett:
            num_a=len(sett['shaded'].keys())
    
            for area in range(num_a):
                idx=sett['shaded'][area]['lims']
                facecolour=sett['shaded'][area]['fill']
                zorder=(0 if 'zorder' not in sett['shaded'][area]
                        else sett['shaded'][area]['zorder'])
                alpha=(1 if 'alpha' not in sett['shaded'][area]
                       else sett['shaded'][area]['alpha'])
    
                # Shaded area left and right bds
                for i in range(len(idx)):
                    bd1=idx[i][0]
                    bd2=idx[i][1]
    
                    ax.axvspan(bd1, bd2, facecolor=facecolour,
                               edgecolor='none', alpha=alpha,
                               zorder=zorder)
    
                # Shaded area label
                if 'label' in sett['shaded'][area]:
                    rot=(0 if 'rotation' not in
                         sett['shaded'][area]['label']
                         else sett['shaded'][area]['label']['rotation'])
                    label_colour=(dflt['stroke'] if 'colour' not in
                                  sett['shaded'][area]['label']
                                  else sett['shaded'][area]['label']['colour'])
                    label_size=(dflt['font-size'] if 'font-size' not in
                                sett['shaded'][area]['label']
                                else sett['shaded'][area]['label']['font-size'])
                    plt.text(
                        sett['shaded'][area]['label']['x'], # x posn of label
                        sett['shaded'][area]['label']['y'], # y posn of label
                        sett['shaded'][area]['label']['text'],
                        rotation=rot,
                        color=label_colour,
                        fontsize=label_size
                    )
    
        return fig, ax
 
    def multi_linechart_test(data:pd.DataFrame, ylab:str, xlab:str, **kwargs:dict) -> (plt.figure, plt.axes):
        '''
        Creates a line chart of one or more lines.
        Number of lines to plot determined from columns in input dataframe.
        
        Parameters
        ----------

        Required: 
        data : Data for the line chart.
        ylab : Label for the y axis.
        xlab : Label for the x axis.

        Optional:
        ymax : The max value of the y axis.
        ymin : The min value of the y axis. Should include this if ymin < 0.
        yinc : The increment of ticks on the y axis.
        ax : The axis that the plot will be located on. 
        plot_size : The dimensions of the plot if given a custom size.

        Returns 
        --------
        fig : Matplotlib fig object
        ax  : Matplotlib ax object
        ''' 
        
        func() 

        ymax, ymin, yinc, upper = calculate_params(
            df=data,
            param_axis ='y',
            **kwargs
            )

        fig, ax = plot_line_data(
            df=data,
            axis=kwargs.get('ax',None)
            )
        
        set_plot_style(
            fig=fig,
            ax=ax,
            plot_size=kwargs.get('plot_size', (6.1, 4.1)), 
            grid_x=True,
            grid_y=True,
            min_value=ymin,
            max_value=ymax, 
            param_axis='y'
            )

        set_ticks(
            ax=ax,
            df=data,
            min_value=ymin, 
            max_value=ymax, 
            inc=yinc
            )

        set_labels(
            ax=ax,
            xlab=xlab,
            ylab=ylab
            )

        return fig, ax

def calculate_params(df:pd.DataFrame, param_axis:str, **kwargs:dict) -> (float, float, float, float): 
    '''
    Checks if minimum, maximum and increment values are passed into the plotting function 
    for the specified axis, and returns these. Otherwise, calculates them.

    Parameters
    ----------

    Required: 
    data :  Data for the line chart.
    param_axis : Axis along which max, min, upper, inc values should be calculated. 

    Optional: 
    xmin : Minimum value of x axis. 
    xmax : Maximum value of x axis.
    xinc : The increment of ticks on the x axis.
    ymin : Minimum value of y axis
    ymax : Maximum value of y axis.
    yinc : The increment of ticks on the y axis.

    Returns 
    -------

    max_value : Maximum value along param_axis 
    min_value  : Minimum value along param_axis 
    inc : Increment of ticks along param_axis
    upper : Value used for placing of annotations. 

    TODO: check whether the calculation of inc can be improved, at what value does it fail,
    maybe print a warning if the user should specify it.
    '''

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
    '''

    delta = (max_value - min_value)/4
    i = 0
    while True:
        delta /= 10
        i += 1
        if delta < 10:
            break
    return delta, i

def plot_line_data(df:pd.DataFrame, axis:plt.axes) -> (plt.figure, plt.axes):
    '''
    Plots all columns in the input dataframe as lines in one graph 
    on the specified axis object.

    Parameters 
    ---------- 
    df : Data to be plotted 
    axis : Prespecified axis to be used for the plot. 

    Returns 
    ------- 
    fig : Matplotlib fig object
    ax  : Matplotlib ax object
    '''

    fig, ax = init_fig(axis)
    colour_instance = colour()
    for i, col in enumerate(df.columns):
        hex_code = colour_instance.get_colour_from_index(i+1)
        ax.plot(df[col], linewidth=3, color=hex_code)
        
    return fig, ax

def plot_grouped_bar_data(df:pd.DataFrame, ax:plt.axes, horizontal:bool) -> (plt.figure, plt.axes):
    '''
    Plots all columns in the input dataframe as bars in a grouped bar graph.
    '''

    fig, ax = init_fig(ax)
    bar_width = 1/(len(df.columns)+1)
    adjustment = 0
    colour_instance = colour()
    ind = np.arange(len(df))
    
    for i, col in enumerate((reversed(df.columns)) if horizontal else (df.columns)):
        hex_code = colour_instance.get_colour_from_index(i+1)
        getattr(ax, 'barh' if horizontal else 'bar')(ind+adjustment, df[col], bar_width, align='center', color = hex_code)
        adjustment += bar_width

    return fig, ax 

def init_fig(axis:plt.axes) -> (plt.figure, plt.axes):
    '''
    Sets the plot fig and axes objects to be the ones specified by the user or 
    creates new ones.
    '''

    if axis != None:
        ax = axis
        fig = ax.get_figure()
    else:
        fig, ax = plt.subplots()    

    return fig, ax

def set_plot_style(fig:plt.figure, ax:plt.axes, plot_size:(int, int), grid_x:bool, grid_y:bool, min_value:float, max_value:float, param_axis:str) -> None:
    '''
    Sets size, background and grid for plot.

    Parameters 
    ---------- 
    fig : Matplotlib fig object.
    ax  : Matplotlib ax object.
    plot_size : The dimensions of the plot in inches. 
    grid_x : Whether there is a grid parallel to x ticks. 
    grid_y : Whether there is a grid parallel to y ticks. 
    min_value : Minimum value of param_axis.
    max_value : Maximum value of param_axis.
    param_axis : Axis opposite to index axis. 
    '''

    fig.set_size_inches(plot_size)
    getattr(ax, 'set_ylim' if param_axis == 'y' else 'set_xlim')([min_value, max_value])
    ax.set_facecolor('xkcd:white')
    set_grid(ax, grid_x, grid_y)

def set_grid(ax:plt.axes, grid_x:bool, grid_y:bool) -> None:
    '''
    Sets the grid for plot. 
    '''
    ax.grid(color='k', linestyle='-', linewidth=0.2)
    ax.xaxis.grid(grid_x)
    ax.yaxis.grid(grid_y)

def set_ticks(ax:plt.axes, df:pd.DataFrame, min_value:float, max_value:float, inc:float, index_axis:str='x', offset:float=0.0) -> None: 
    '''
    Sets x and y axis tick locations and tick labels.
    
    Parameters 
    ----------
    ax : Matplotlib axes object.
    df : Dataset being plotted.
    min_value : Minimum value along non index axis.
    max_value : Maximum value along non index axis. 
    inc : Incrementation of ticks along non index axis. 
    index_axis : The index of the DataFrame object, 
                 e.g. the x axis for a line chart. 
    offset : Offset in the placement of ticks. 
             Used for grouped bar charts to center labels. 
    '''
    height, width = ax.figure.get_size_inches()
    NUM_SLICES = int(width) + 1

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

    # Set the locations for the ticks of the two axes 
    getattr(ax, 'yaxis' if index_axis == 'y' else 'xaxis').set_major_locator(mpl.ticker.FixedLocator(locs))
    getattr(ax, 'set_xticks' if index_axis == 'y' else 'set_yticks')(range(min_value, max_value + inc, inc), 
                                                                    labels=range(min_value, max_value + inc, inc), 
                                                                    fontsize = 9, fontname = font.normal)
    # Set the formatting of the labels
    getattr(ax, 'xaxis' if index_axis == 'y' else 'yaxis').set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    getattr(ax, 'set_yticklabels' if index_axis == 'y' else 'set_xticklabels')(labels=index_labels, 
                                                                               rotation=label_rotation,
                                                                               fontsize = 9)


def set_labels(ax:plt.axes, xlab:str, ylab:str) -> None:
    '''
    Set the labels of the y and x axes.

    Parameters
    ----------
    ax : Matplotlib axes object. 
    xlab : Label of x axis. 
    ylab : Label of y axis. 
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
    ax : Matplotlib axes object. 
    df : Dataset being plotted.
    upper : Bar value used for determining placement of annotation. 
    precision : Decimal points in the annotations. 
    percent : Flag determining whether to show percentage change between 
                baseline column (assumed to be the first column) and 
                remaining columns.
    horizontal : Flag to indicate if this is a horizontal bar graph.
    additional_annotations : Dictionary with keys of type (int, int) and values 
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
    '''
    HORIZONTAL_CUTOFF = 0.1 * upper
    ANNOTATION_OFFSET = 0.015 * upper
    PERCENT_OFFSET = 0.03
    
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
                    xy = (row[col] + (4*PERCENT_OFFSET if row[col] < HORIZONTAL_CUTOFF else PERCENT_OFFSET) * upper, j),  # Placement of percentage annotation 
                    color = 'k',
                    fontname = font.normal,
                    fontsize=10
                    )
                j += 1
        
def vertical_bar_annotations(df:pd.DataFrame, ax:plt.axes, bar_width:float, upper:float, precision:int, percent:bool) -> None:
    '''
    Adds value annotations to vertical grouped or regular bar charts. 
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

def general_grouped_bar_chart(data:pd.DataFrame, param_axis:str, index_axis:str, standard_plot_size:(int, int), horizontal:bool, grid_x:bool=True, grid_y:bool=True, **kwargs:dict) -> (plt.figure, plt.axes):
        '''
        Creates a horizontal or vertical grouped bar chart. Number of
        bars in each group to plot is determined from the number of
        columns in input dataframe, while the number of groups is
        determined by the number of rows.

        Parameters
        -----------

        Required: 
        data : Data for the line chart.
        param_axis : Axis along which bars are plotted.
        index_axis : Axis containing labels for bars. 
        standard_plot_size : The standard size depending on the type of graph (horizontal or vertical).
        horizontal : Flag indicating whether plot is horizontal. 
        
        
        Optional: 
        ylab : Label for the y axis.
        xlab : Label for the x axis.

        xmax or ymax : The max value of the x axis.
        xmin or ymin : The minimum value of the x axis
                        Should include this if minimum < 0.
        xinc or yinc : The increment of ticks on the y axis.
        ax : The axis that the plot will be located on.
        plot_size : Custom plot dimensions. 
        precision : Decimal points in the annotations. 
        percent : Flag determining whether to show percentage change between 
                    baseline column (assumed to be the first column) and 
                    remaining columns.
        additional_annotations : Dictionary with keys of type (int, int) and values 
                                    of type (str), indicating the coordinates and 
                                    annotation to be added. 

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
            **kwargs)

        fig, ax = plot_grouped_bar_data(
            df=data,
            ax=kwargs.get('ax', None), 
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