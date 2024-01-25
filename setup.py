from setuptools import setup, find_packages

setup(
    name='rick',
    version='0.8',
    description='Standardized matplotlib charts and graphs',
    packages=['rick'],
    install_requires=[
        'matplotlib',
        'psycopg2',
        'geopandas',
        'pandas',
        'shapely',
        'seaborn'
    ],
    python_requires='>=3'
)
