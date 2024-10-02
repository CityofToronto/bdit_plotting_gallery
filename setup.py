from setuptools import setup, find_packages

setup(
    name='rick',
    version='0.9.0',
    description='Standardized matplotlib charts and graphs',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'psycopg[binary]',
        'geopandas',
        'pandas',
        'shapely',
        'seaborn'
    ],
    python_requires='>=3'
)