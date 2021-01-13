# Sphinx Module

## Introduction

Sphinx is a python module that autogenerates python documentation for a python package using predefined CSS templates. The output would be in the form of an html page that can eventually be hosted on Github. Many python modules uses sphinx to generate their documentation. 

[Official Website](http://www.sphinx-doc.org/en/master/)

## Installation and Setup

0. Make directory `sphinx` in the root folder (`bdit_plotting_gallery/`)
1. Install Sphinx with `pip install sphinx` *update: this is now done, no need to re-do*
2. Run `sphinx-quickstart` on the command line on your root folder. 
3. Sphinx will give you a bunch of options to setup in the `conf.py` folder. For the most part, the default options will be fine, however you should select the following options, which are different from the default options.

Select `y` to different directory for source and build. This is not as essential as the next options, but it will declutter your project directory.

Select `y` to automatically insert docstring from module. *update: this note no longer appears*

Select `y` to including links to the source code. *update: this note no longer appears*

Select `n` to creating windows command file only if you're working on linux instead of windows.  *update: this note no longer appears*


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
You can also follow [this formatting style](https://pythonhosted.org/an_example_pypi_project/sphinx.html) for the docstring, e.g.:

```
def public_fn_with_googley_docstring(name, state=None):
    """This function does something.

    Args:
       name (str):  The name to use.

    Kwargs:
       state (bool): Current state to be in.

    Returns:
       int.  The return code::

          0 -- Success!
          1 -- No good.
          2 -- Try again.

    Raises:
       AttributeError, KeyError

    A really great idea.  A way you might use me is

    >>> print public_fn_with_googley_docstring(name='foo', state=None)
    0

    BTW, this always returns 0.  **NEVER** use with :class:`MyPublicClass`.

    """
    return 0
```


## Graph Gallery

[Official Website](https://sphinx-gallery.github.io/)

As mentioned, you can also create a gallery of examples. The above module is the tool to create it. Recall that we previously enabled graph gallerys in the `conf.py` file:
```python
sphinx_gallery_conf = {
     'examples_dirs': 'examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path where to save gallery generated examples
}
```

Create a folder named `examples` (i.e. same name as specified in `example_dirs` in `conf.py`) in your project directory.
If you opted for separate directories for source and build in the `conf.py` setup, then create the `examples/` folder in `source/`. Add to `examples/` the python files that generate your examples. **NB**: Each python file must start with `plot_xxxxxx.py`.

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
You might want to organize the Gallery into sub-sections. In this case, we want to group examples of the same type of chart into its own sub-gallery. To do this, go to the `charts/sphinx/source/examples` directory, and make a new sub-directory for each sub-gallery you want to have. Here, we have made the directories `bar`, `grouped_bar`, `line` and `map`. Inside each sub-directory, move the python file pertaining to that chart type. For example, in `line/`, we have two types of line charts: `plot_line_rick.py` and `plot_tow_line_rick.py`. These are both from the RICK module.

**Important**: There must be a README.txt in **each sub-directory** otherwise `make html` will fail. You can format the README title to be html class `h2` so that they will be displayed as sub-headings of the main Gallery page. For example, the README.txt file in the `line` directory starts like:

```python
***********
Line Charts
***********

Below is a gallery of line charts. 

``` 

An observation: I noticed that the `auto_examples` directory in `bdit_python_utilities/charts/sphinx/source/` that is automatically generated from the `examples` directory will not update perfectly when changes are made in `examples`, like moving files into sub-directories. Just check the `auto_examples` folder manually after any structural changes in the `examples` folder to make sure it is correct. 

## Formatting the `rst` File

Sphinx will be looking at the autocreated `index.rst` file (in `bdit_python_utilities/charts/sphinx/source`) when you're building the html. This file also serves as the homepage for your documentation.

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

The code is built from the directory where `Makefile` is. In this case, `bdit_plotting_gallery/sphinx`.  

Make sure your build folder is clean by running `make clean` on the command line. You can skip this step if you manually deleted everything, or if this is your first time building the html.

Then, run `make html`.

If you encounter an error with make, ensure that `sphinx-gallery` is installed:
`pip install --user sphinx-gallery`

If you're developing in a virutual environment:
`pipenv install sphinx-gallery` 
(If you encounter errors with locks, you can skip the locks `pipenv install --skip-lock sphinx-gallery`)
Then, to activate the project's virtual environment, type `pipenv shell`. 
This brings you to the environment root directory, so `cd` to the project directory `bdit_python_utilities/charts/sphinx`.

Now try running `make clean && make html`.


## Adding new functions and configure for autogenerated docs

If you would like to add your own chart function to the Gallery _and_ have the docstring automatically generated in the webpage, you need to configure the function as a module (or inside a module). If it is not a module, the docstring will not be autogenerated in the webpage (and as a result, will not be searchable and will not appear in the Index listings).  Here, we will use as an example a new type of line chart, `multi_linechart()`, which plots one or more lines based on the number of columns in the input data.

1. Put the source code in the project directory, which in this case is `bdit_plotting_gallery/`. Since we may in future have many varieties of line charts, we can create a general module called `gallery_lines.py` and in it put all the new line chart functions (you can define them one after the other). For now, there is only one new function, `multi_linechart()`. Create and format the docstring for the new function as described above.

2. In the project directory, there is already a file called `__init__.py`. This file contains all the modules of the project. We can add our new module `gallery_lines` and import all functions defined inside it:

```
from rick import *
from gallery_lines import *
```

3. Lastly, you must instruct the build script to include the new module when it builds. Go to `sphinx/source/`. The `index.rst` file already contains `code`, which directs it to `code.rst` that is also in the `source` directory. Edit `code.rst` so that it includes the new module and all its members:
```
Auto Generated Documentation
============================

.. automodule:: rick
        :members:

.. automodule:: gallery_lines
        :members: 
```

4. Final check: make sure `conf.py` knows where to find your new module. If using `abspath`, then define the location of the module relative to the directory containing `conf.py`. In this case, `gallery_lines.py` is 2 directories up from `sphinx/source/`:

```
sys.path.insert(0, os.path.abspath('../../'))
```

5. Build the script. Go to the `sphinx` directory (i.e. the directory containing the `Makefile`), clean and build the code:

`make clean && make html`

On the webpage, you should now see the functions defined in `gallery_lines` listed in Index, Module Index, and also that they can be searched for in the search bar.

## Adding new functions with no autogenerated docs
If you do not need any autogenerated documentation, you do not need to go through the steps above. You can simply define an example in `sphinx/source/examples` as explained above, and this example will appear in the Gallery of Charts. The function in the example will not be found in the search bar of the webpage nor listed in the Index or Module Index.

## Helpful Videos

[Simple tutorial](https://www.youtube.com/watch?v=LQ6pFgQXQ0Q)

[Another Tutorial](https://www.youtube.com/watch?v=qrcj7sVuvUA)

[Numpy Style Docstring](https://numpydoc.readthedocs.io/en/latest/format.html)

[Sphinx-Gallery Demo](https://youtu.be/ikT_xnTFHC0?t=5662)

