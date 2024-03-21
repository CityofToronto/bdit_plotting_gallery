# Welcome to the BDITTO Plotting Gallery !

Are you tired of re-inventing the matplotlib wheel every time you need a chart for a new project?
Did you forget where to find the right colour palette for those bars?
Do you need a total rewrite just to include one more line in a line chart?
If you said yes to any of the above, this Gallery is for you!

This repo contains a collection of reusable chart functions that strive to conform to standardized formats and designs based on output the BDITTO team has already created for various projects.

The Gallery collection includes:

- a built-in module called Repeatable Information Charts Kit (RICK) that already contains many chart types for use out-of-the-box. Some customization is possible. The source code for all RICK charts is found in `rick.py`.
- stand-alone examples beyond the scope of RICK  with source code up-front to allow easy customization as you desire

All charts were developed with proper python documentation to allow the documentation for each chart to be auto-generated using [sphinx](http://www.sphinx-doc.org/en/master/).

## Contribute to the Gallery

This is a work in progress and we need YOU to add to the collective knowledge! Please go to the README in the `sphinx` directory for a step-by-step guide to adding your own example to the Gallery.

## Browse the Gallery

Please visit [this page](https://cityoftoronto.github.io/bdit_plotting_gallery) to browse the Gallery and associated (auto-generated) documentation. There you can also download the scripts and example notebooks for your own use.

A quick summary of the charts currently available in the Gallery is listed below:

### Charts in the Repeatable Information Charts Kit (RICK) module

This module was inspired by charts created for the VFH Bylaw Review Report. There was a need to develop a standardized brand and design language for everything BDITTO produces, so this module aims to produce a regularized set of charts and maps that are consistent with previous charts we create. All of the chart/map producing functions returns a matplotlib `fig` and `ax` object so that the figure can be furthere modified using matplotlib functions.

#### `geo.ttc(con)`

Returns a geopandas dataframe of the TTC subway network.

#### `geo.island(con)`

Returns a geopandas dataframe of the Toronto Island.

#### `charts.chloro_map(con, df, lower, upper, title, **kwargs)`

This function creates a chloropleth map.

The following arguments must be passed in order for the function to run.

| argument | variable type         | description                                                                                                                                                                   |
| -------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| con      | SQL Connection Object | Used to additional layers from the SQL database.                                                                                                                              |
| df       | GeoPandas DataFrame   | Data for the chloropleth map. The data must only contain 2 columns; the first column has to be the `geom` column and the second has to be the data that needs to be mapped. |
| lower    | int                   | Lower bound for the colourmap                                                                                                                                                 |
| upper    | int                   | Upper bound for the colourmap                                                                                                                                                 |
| title    | str                   | Text string for the title text                                                                                                                                                |

Additionally, there are optional arguments that can be passed to the function

| argument | variable type | default    | description                                                                                                                                    |
| -------- | ------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| subway   | boolean       | `False`  | Flag to plot the subway network on the map. False indicates the subway network does not show up.                                               |
| island   | boolean       | `True`   | Flag to plot the Toronto Islands as having no data. True indicates the islands are coloured the same as the Waterfront neighbourhood.          |
| cmap     | str           | `YlOrRd` | String to specify colourmap for the map.                                                                                                       |
| unit     | str           | `None`   | Specifies if a unit should be added to the legend box. The automatic placement of the unit only works if the upper or lower are whole numbers. |
| nbins    | int           | `2`      | Number of ticks in the colourmap                                                                                                               |

#### `charts.line_chart(data, ylab, xlab, **kwargs)`

Produces a simple line chart. The xaxis is not formatted by this function and requires further manipulation with matplotlib. In addition, annotation boxes must be added on manually with a something like this:

```python
fig.text(0.94, 0.96, '176,000', transform=ax.transAxes, wrap = True, fontsize=9, fontname = 'Libre Franklin',
         verticalalignment='top', ha = 'center', bbox=props, color = purple)
```

The function defines the styling with the `props` variable, so the only manipulations needed is the positioning and the text itself.

The following arguments must be passed in order for the function to run.

| argument | variable type  | description         |
| -------- | -------------- | ------------------- |
| data     | Series or list | Data for the chart  |
| ylab     | str            | Label for the yaxis |
| xlab     | str            | Label for the xaxis |

Additionally, there are optional arguments that can be passed to the function

| argument | variable type | default                            | description                  |
| -------- | ------------- | ---------------------------------- | ---------------------------- |
| ymin     | int           | 0                                  | Lower bound for the yaxis    |
| ymax     | int           | The maximum value of the dataset   | Upper bound for the yaxis    |
| yinc     | int           | One-third of the range of the data | Interval for the yaxis ticks |

#### `charts.tow_chart(data, ylab, **kwargs)`

Produces a 7-Day time of week chart that shows data points for each hour during one week. The xaxis is fixed to the 168 hours that produces the week, and the data must be ordered so that the first entry represents Monday at midnight.

The following arguments must be passed in order for the function to run.

| argument | variable type  | description         |
| -------- | -------------- | ------------------- |
| data     | Series or list | Data for the chart  |
| ylab     | str            | Label for the yaxis |

Additionally, there are optional arguments that can be passed to the function

| argument | variable type | default                            | description                  |
| -------- | ------------- | ---------------------------------- | ---------------------------- |
| ymin     | int           | 0                                  | Lower bound for the yaxis    |
| ymax     | int           | The maximum value of the dataset   | Upper bound for the yaxis    |
| yinc     | int           | One-third of the range of the data | Interval for the yaxis ticks |

#### Helper functions

| function                         | purpose                                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `calculate_params()`           | Finds minimum, maximum and incremental values used to determine the limits and ticks of the dependent axis. |
| `calculate_delta()`            | Required for `calculate_params()`.                                                                        |
| `init_fig()`                   | Initializes the figure object corresponding to the plot being made.                                         |
| `set_plot_style()`             | Sets size, background and grid for plot.                                                                    |
| `set_grid()`                   | Sets the grid for plot. Called by `set_plot_style()`.                                                     |
| `set_ticks()`                  | Sets x and y axis ticks. Format depends on type of index being used.                                        |
| `set_labels()`                 | Set the labels of the y and x axes.                                                                         |
| `add_bar_annotations()`        | Adds annotations to charts including bars, such as the height of bars or percent changes.                   |
| `horizontal_bar_annotations()` | Called by `add_bar_annotations()` in the case of horizontal graphs.                                       |
| `vertical_bar_annotations()`   | Called by `add_bar_annotations()` in the case of vertical graphs.                                         |
| `plot_line_data()`             | Used for line-type plots.                                                                                   |
| `plot_grouped_bar_data()`      | Used for bar charts.                                                                                        |

### Stand-alone examples

WIP.....

### Adding to / modifying the Charts class

If you would like to add a new plotting function to the `Charts` class:

1. Check through the [autogenerated documentation](https://cityoftoronto.github.io/bdit_plotting_gallery/code.html) and `rick.py` to see if there is a similar pre-existing function to avoid duplication.
2. Try to make use of the helper functions available. If there is functionality that you would like to add that is not covered by the available helper functions, consider updating them or creating new ones. Ideally, we want to avoid repetition of code throughout `rick.py` to make it easier to debug and add features later on.
3. Make sure to include docstrings formatted according to the Sphinx gallery requirements (check [here](./sphinx/README.md#documenting-the-code)) so that they can automatically be added to the autogenerated documentation.
4. Create some examples that can be added to the online Gallery following the instructions [here](./sphinx/README.md#graph-gallery). Ideally, do not create new examples that depend on database connections so that they are always reproducible. 
5. Create a PR in this repo and make sure to include your new examples. Prior to merging, make sure to manually move the autogenerated contents of `sphnix/build/html` under `docs/`.

If you are updating an existing function:

1. Recreate the corresponding example from the Sphinx gallery and make sure that it still works.
2. Include this in your PR.
