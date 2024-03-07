"""
RICK Horizontal Grouped Bar Chart
=======================

Example of a horizontal grouped bar chart.
"""
import matplotlib.pyplot as plt
import pandas as pd 
import rick

################################
#Data Collection
#----------------
#
#This Section grabs and formats the data.
data = [["Scarborough",	4645.87, 13813.73],
        ["Etobicoke York", 7212.29, 20690.60],
        ["North York",	9494.93, 24715.76],
        ["Toronto and East York", 43089.61, 93547.43]]
district_cond = pd.DataFrame(data, columns=['area_name', 'count1', 'count2']).set_index('area_name')

################################
#Horizontal Grouped Bar Chart 
#----------------------------
#
#This Section uses the rewritten horizontal grouped bar chart function.

# Setting a custom plot_size to prevent cropping during sphinx autogeneration.
plot_size = (6.1*0.9, len(district_cond)*1.5*0.9)
fig, ax = rick.charts.horizontal_grouped_bar_chart(
    data=district_cond,
    xlab = 'Trips',
    legend=['2016', '2018'],
    percent = True)
plt.show()
