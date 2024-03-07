"""
RICK Vertical Grouped Bar Chart
=======================

Example of a vertical grouped bar chart.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import rick

################################
#Data Collection
#----------------
#
#This Section grabs and formats the data.
np.random.seed(42)
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Group1': np.random.randint(10, 50, 4),
    'Group2': np.random.randint(20, 60, 4)
}
df = pd.DataFrame(data)
df = df.set_index('Category')

################################
#Vertical Grouped Bar Chart
#--------------------------
#
#This Section uses the new vertical grouped bar chart function.

# Setting a custom plot_size to prevent cropping during sphinx autogeneration.
plot_size = (len(df)*1.5*0.9, 6.1*0.9)
fig, ax = rick.charts.vertical_grouped_bar_chart(
    data=df,
    precision=1,
    xlab='Group',
    ylab='Category',
    percent=True,
    legend=['Group1', 'Group2'])
plt.show()