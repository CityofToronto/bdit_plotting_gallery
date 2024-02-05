"""
Multi-Line Chart
================

Examples of multi-line chart function `multi_linechart()`. The number
of lines to be plotted is automatically determined from the columns
in the input dataframe. Also includes the option to display one or
more shaded regions with labels.
"""
import rick
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import datetime
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates
from matplotlib.lines import Line2D # for legend

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

################################
#Source Code
#-----------
#
#Source code for multi-line function.

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

################################
#Data Collection
#----------------
#
#This Section creates example data.

# x-axis
dt=[datetime.date(2020, 10, 27), datetime.date(2020, 10, 28), datetime.date(2020, 10, 29), 
    datetime.date(2020, 10, 30), datetime.date(2020, 10, 31), datetime.date(2020, 11, 1), 
    datetime.date(2020, 11, 2), datetime.date(2020, 11, 3), datetime.date(2020, 11, 4), 
    datetime.date(2020, 11, 5), datetime.date(2020, 11, 6), datetime.date(2020, 11, 7), 
    datetime.date(2020, 11, 8), datetime.date(2020, 11, 9), datetime.date(2020, 11, 10), 
    datetime.date(2020, 11, 11), datetime.date(2020, 11, 12), datetime.date(2020, 11, 13), 
    datetime.date(2020, 11, 14), datetime.date(2020, 11, 15), datetime.date(2020, 11, 16), 
    datetime.date(2020, 11, 17), datetime.date(2020, 11, 18), datetime.date(2020, 11, 19), 
    datetime.date(2020, 11, 20), datetime.date(2020, 11, 21), datetime.date(2020, 11, 22), 
    datetime.date(2020, 11, 23), datetime.date(2020, 11, 24), datetime.date(2020, 11, 25), 
    datetime.date(2020, 11, 26), datetime.date(2020, 11, 27), datetime.date(2020, 11, 28), 
    datetime.date(2020, 11, 29), datetime.date(2020, 11, 30), datetime.date(2020, 12, 1), 
    datetime.date(2020, 12, 2), datetime.date(2020, 12, 3), datetime.date(2020, 12, 4), 
    datetime.date(2020, 12, 5), datetime.date(2020, 12, 6), datetime.date(2020, 12, 7), 
    datetime.date(2020, 12, 8), datetime.date(2020, 12, 9), datetime.date(2020, 12, 10), 
    datetime.date(2020, 12, 11), datetime.date(2020, 12, 12), datetime.date(2020, 12, 13)]

# y-axis
# line 1
y1=[32512.0, 34852.0, 35136.0, 38154.0, 35551.0, 27617.0, 33677.0, 34163.0, 34606.0, 35106.0, 38034.0, 36077.0, 30372.0, 34616.0, 34264.0, 34162.0, 34891.0, 36871.0, 34465.0, 25836.0, 41818.0, 42943.0, 42199.0, 44307.0, 49460.0, 47071.0, 31263.0, 38039.0, 39162.0, 29431.0, 42445.0, 45586.0, 42333.0, 35198.0, 39244.0, 38740.0, 41345.0, 43083.0, 43299.0, 41210.0, 32797.0, 40363.0, 41577.0, 38094.0, 43813.0, 46515.0, 38156.0, 28232.0]

# line 2
y2=[38781.0, 41387.0, 40545.0, 42473.0, 35726.0, 28066.0, 36873.0, 38191.0, 39432.0, 40123.0, 42199.0, 37404.0, 32564.0, 38425.0, 40460.0, 39506.0, 39780.0, 40666.0, 34904.0, 25290.0, 35852.0, 37037.0, 36880.0, 38007.0, 40274.0, 35163.0, 23323.0, 33689.0, 35129.0, 12352.0, 36524.0, 38759.0, 32995.0, 29132.0, 33974.0, 32964.0, 35851.0, 37296.0, 36458.0, 31332.0, 26148.0, 34649.0, 35588.0, 34950.0, 36615.0, 38317.0, 29245.0, 21929.0]

# line 3
y3=[21713.0, 23644.0, 22949.0, 24473.0, 21201.0, 16189.0, 21592.0, 21946.0, 23200.0, 23324.0, 25188.0, 23107.0, 20544.0, 23035.0, 24334.0, 23354.0, 23144.0, 23411.0, 20691.0, 14232.0, 20965.0, 21615.0, 20784.0, 21851.0, 24003.0, 20617.0, 13727.0, 19809.0, 20124.0, 8755.0, 20952.0, 22788.0, 20327.0, 17183.0, 19609.0, 19223.0, 20557.0, 21295.0, 20377.0, 17362.0, 14867.0, 19576.0, 20172.0, 19520.0, 20884.0, 22209.0, 16241.0, 12449.0]

# Create dataframe to be plotted
data = {'dt':dt, 'y1':y1, 'y2':y2, 'y3':y3}
df_multi = pd.DataFrame(data) 


################################
#Example: plot data with no options
#----------------------------------
#
#This Section plots dataframe using default settings.

sett_empty={
    
}

multi_linechart(df_multi, sett_empty)

################################
#Example: plot data with new multiline function
#----------------------------------------------
#
#This section plots the `df_multi` dataframe using the rewrite of the multiline function.

df_multi_dt = df_multi.set_index('dt')
df_multi_dt.index = pd.to_datetime(df_multi_dt.index)
fig, ax = rick.charts.multi_linechart_test(df_multi_dt, ylab='Values', xlab='Dates', legend=['Vol 1', 'Vol 2', 'Vol 3'])
fig.tight_layout()
plt.show()

#####################################
#Example: one shaded area with legend
#------------------------------------
#
#This Section plots dataframe with legend and one shaded area.

sett = {
    'body': {
        'font-size': 16,
        'font-family': 'sans-serif'
    },
    
    # Axes labels and limits
    'yaxis': {
        'label': 'Daily Volume',
        'labelsize': 18
    },
    'xaxis': {
        'major_loc': {
            'loc': mdates.DayLocator(),
            'date_form': mdates.DateFormatter('%Y-%m-%d')
        },
        'minor_loc': {
            'date_form': mdates.DayLocator(interval=1),  # every other day
        }
    },
    
    # grid
    'major_grid_on': True,
    'minor_grid_on': True,
    'minor_grid': {
        'stroke': '#D3D3D3',
        'border': '--'
    },
    
    # legend
    'legend': {
        'loc': 'lower left'
    },

    'lines': {
        0: {
            'stroke': '#1A75B5',
            'border-style': 'solid',
            'label': 'Vol 1'
            },
        1: {
            'stroke': '#FF7F00',
            'border-style': 'solid',
            'label': 'Vol 2'
            },
        2: {
            'stroke': '#28A026',
            'border-style': 'dashed',
            'label': 'Vol 3'
            }
    },
    
    'shaded': {
        0: {
            'lims':[[pd.to_datetime('2020-11-23'), pd.to_datetime('2020-12-22')]],
            'fill': 'magenta',
            'zorder':-100,
            'alpha': 0.3,
            'label': {
                'x': pd.to_datetime('2020-11-23') + datetime.timedelta(days=.5),
                'y': 51000,
                'text': 'Lockdown 2',
                'font-size': 14, 
                'colour': 'k',
                'rotation': 0
            }
        }
    }
}

# ----------------------------------------------------------------
# WEIRD HACK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# For some reason, you need to run mpl.rcParams TWICE before it 
# actually gets set. The mpl.rcParams is already specified in 
# multi_linechart() but here we run it for the second time otherwise
# the font.family will not be updated
if 'body' in sett:
    if 'font-family' in sett['body']:
        mpl.rcParams['font.family'] = sett['body']['font-family']
        print(mpl.rcParams['font.family'])

#multi_linechart(df_multi, sett)

#####################################
#Example: two shaded area blocks  
#------------------------------------
#
#This Section plots dataframe with legend, one shaded 
#block, and shaded blocks for weekends.

def find_weekend_indices(df):
    '''Outputs a 2D list of weekend date pairs given date column
    in df. Assumes first column of df is the date column. 
    Datetime pairs output in `datetime.date()` format.
    '''
    xcol=list(df)[0]
    datetime_array=df[xcol]
    
    s = []
    for i in range(len(datetime_array) - 1):
        if datetime_array[i].weekday() >= 5:
            s.append([df[xcol][i], df[xcol][i + 1]])

    return s

sett = {
    'body': {
        'font-size': 16,
        'font-family': 'sans-serif'
#         'font-family': 'monospace'
#         'fontfamily-list': ['Libre Franklin', 'DejaVu Sans'],
    },
    
    # Axes labels and limits
    'yaxis': {
        'label': 'Daily Volume'
    },
   'xaxis': {
        'major_loc': {
            'loc': mdates.DayLocator(),
            'date_form': mdates.DateFormatter('%Y-%m-%d')
        },
        'minor_loc': {
            'date_form': mdates.DayLocator(interval=1),  # every other day
        }
   },
    
    # grid
    'major_grid_on': True,
    'minor_grid_on': True,
    'minor_grid': {
        'stroke': '#D3D3D3',
        'border': '--'
    },
    
    # legend
    'legend': {
        'loc': 'lower left'
    },

    'lines': {
        0: {
            'stroke': '#1A75B5',
            'border-style': 'solid',
            'label': 'Vol 1'
            },
        1: {
            'stroke': '#FF7F00',
            'border-style': 'solid',
            'label': 'Vol 2'
            },
        2: {
            'stroke': '#28A026',
            'border-style': 'dashed',
            'label': 'Vol 3'
            }
    },
    
    'shaded': {
        0: {
            'lims':[[pd.to_datetime('2020-11-23'), pd.to_datetime('2020-12-22')]],
            'fill': 'magenta',
            'zorder':-100,
            'alpha': 0.3,
            'label': {
                'x': pd.to_datetime('2020-11-23') + datetime.timedelta(days=.5),
                'y': 51000,
                'text': 'Lockdown 2',
                'font-size': 12, 
                'colour': 'k',
                'rotation': 0
            }
        },
        1:{
            'lims':find_weekend_indices(df_multi),
            'fill': '#ccffff',
            'alpha': 0.9 
        }
    }
}

if 'body' in sett:
    if 'font-family' in sett['body']:
        mpl.rcParams['font.family'] = sett['body']['font-family']
        print(mpl.rcParams['font.family'])

#multi_linechart(df_multi, sett)
