# Sphinx Module

## Introduction

Sphinx is a python module that autogenerates python documentation for a python package using predefined CSS templates. The output would be in the form of an html page that can eventually be hosted on Github. Many python modules uses sphinx to generate their documentation. 

[Official Website](http://www.sphinx-doc.org/en/master/)

## Installation and Setup

1. Install Sphinx with `pip install sphinx`
2. Run `sphinx-quickstart` on the command line on your root folder. 
3. Sphinx will give you a bunch of options to setup in the `conf.py` folder. For the most part, the default options will be fine, however you should select the following options, which are different from the default options.

Select `y` to different directory for source and build. This is not as essential as the next options, but it will declutter your project directory.

Select `y` to automatically insert docstring from module.

Select `y` to including links to the source code.

Select `n` to creating windows command file only if you're working on linux instead of windows. 


4. Change the settings in `conf.py` file. 

4a. Add the following line under the `import sys, os` line. This line tells sphinx where to look for your index files when building the html

` sys.path.insert(0, os.path.abspath('.'))`

4b. Under the extensions table, add the following extensions, so the code looks something like this:

```python
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'sphinx_gallery.gen_gallery']

sphinx_gallery_conf = {
     'examples_dirs': 'examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path where to save gallery generated examples
}
```

4c. If you want to change the theme of the docs, select a different theme. The default line of code is `html_theme = 'alabaster`

## Documenting the Code

In order for Sphinx to auto generate the documentation, the code should be documented in a numpy style doc string. An example can be found [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html)

Additionally, this was done for the `rick.py` module.

```python
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

        ttc['geom']=ttc['geom'].apply(lambda x: shapely.affinity.rotate(x, angle=-17, origin = Point(0, 0)))
        
        return ttc
```

Ensure this is done this throughout the code, including all classes, functions, and at the start of the code, so that the code is documented properly and sphinx catches everything. 

## Graph Gallery

[Official Website](https://sphinx-gallery.github.io/)

As mentioned, you can also create a gallery of examples. The above module is the tool to create it. Recall that we previously enabled graph gallerys in the `conf.py` file:
```python
sphinx_gallery_conf = {
     'examples_dirs': 'examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path where to save gallery generated examples
}
```

Create a folder named `examples` in your project directory (i.e. same name as specified in `example_dirs` in `conf.py`), and fill it with python files that generate your examples. In this case, the project directory is `charts/sphinx`. Each python file must start with `plot_xxxxxx.py`.

To create cells in the downloadable jupyter notebook, or create breaks in the code for the html page, you'll need to format a comment like this

```python
################################
#Data Collection
#----------------
#
#This Section grabs and formats the data.
```

Make sure in your `examples` folder to include a Readme. It would only need to include a title and body.

```python
Gallery of Charts
==================

Below is a gallery of example charts for each charting function in rick.charts. 
```

### Graph Gallery - Sub-galleries
You might want to organize the Gallery into sub-sections. In this case, we want to group examples of the same type of chart into its own sub-gallery. To do this, go to the `charts/sphinx/examples` directory, and make a new sub-directory for each sub-gallery you want to have. Here, we have made the directories `bar`, `grouped_bar`, `line` and `map`. Inside each sub-directory, move the python file pertaining to that chart type. For example, in `line/`, we have two types of line charts: `plot_line_rick.py` and `plot_tow_line_rick.py`. These are both from the RICK module.

**Important**: There must be a README.txt in **each sub-directory** otherwise `make html` will fail. You can format the README title to be html class `h2` so that they will be displayed as sub-headings of the main Gallery page. For example, the README.txt file in the `line` directory starts like:

```python
***********
Line Charts
***********

Below is a gallery of line charts. 

``` 

An observation: I noticed that the `auto_examples` directory in `bdit_python_utilities/charts/sphinx` that is automatically generated from the `examples` directory will not update perfectly when changes are made in `examples`, like moving files into sub-directories. Just check the `auto_examples` folder manually after any structural changes in the `examples` folder to make sure it is correct. 

## Formatting the `rst` File

Sphinx will be looking at the autocreated `index.rst` file (in `bdit_python_utilities/charts/sphinx`) when you're building the html. This file also serves as the homepage for your documentation.

You can change the title and body of the file to add more information, and add a link to your autogenerated documentation/graph gallery by including your directory in the file as so:

```python

Title
==========================================

Body

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   code #folder containing documentation
   auto_examples/index #folder conatining graph gallery. 



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

## Building the Code

Make sure your build folder is clean, by navigating to your directory where your sphinx documents are, and then running `make clean` on the command line. You can skip this step if you manually deleted everything, or if this is your first time building the html.

Then, run `make html`.

If you encounter an error with make, ensure that `sphinx-gallery` is installed:
`pip install --user sphinx-gallery`

If you're developing in a virutual environment:
`pipenv install sphinx-gallery` 
(If you encounter errors with locks, you can skip the locks `pipenv install --skip-lock sphinx-gallery`)
Then, to activate the project's virtual environment, type `pipenv shell`. 
This brings you to the environment root directory, so `cd` to the project directory `bdit_python_utilities/charts/sphinx`.

Now try running `make clean` and then `make html`.



## Helpful Videos

[Simple tutorial](https://www.youtube.com/watch?v=LQ6pFgQXQ0Q)

[Another Tutorial](https://www.youtube.com/watch?v=qrcj7sVuvUA)

[Numpy Style Docstring](https://numpydoc.readthedocs.io/en/latest/format.html)

[Sphinx-Gallery Demo](https://youtu.be/ikT_xnTFHC0?t=5662)

