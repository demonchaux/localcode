## Local Code ##

- - -

<!--This is a repository of scripts being used on the [Local Code Project](http://nicholas.demonchaux.com) which is currently in residency at the [Autodesk Idea Studio](http://usa.autodesk.com/ideastudio).-->
<!--These scripts are new, messy, and in development. Feel free to browse them, but don't expect them to work well or safely on your computer.  -->



####So far the scripts include:  
- shpPopulate.py: used for loading a large quantity of shapefiles into a PostGIS/PostgreSQL database.
- db.py: some scripts for running queries and retrieving gis data
- sql.py: scripts for composing specific sql queries.
- mayascripts.py: a set of functions used in Autodesk Maya to retrieve and render animations of gis data based on SQL queries

### Development

1. Install a good text editor or IDE
2. Get a GitHub account.
2. [Install Git and set it up.](http://help.github.com/win-set-up-git/)

### Installation and Setup - Windows

The software for local code is a set of Python modules. These modules use other
tools to manage gis data and build 3d models. Here is an overview of the steps:

1. Install the database and GIS tools.
2. Make sure that the GIS tools can be found by Python
3. Install the code libraries.

After that, you can begin loading and exporting data.

#### 1. Install the database and GIS tools.

1. Install PostgreSQL (9.0.4) (you can just install it on the default
2. Install PostGIS (Use the stackbuilder program that pops up at the end of
   installing PostgreSQL).
4. Install OSGeo4W (Use the Express Desktop Install)

#### 2. Make sure that the GIS tools can be found by python

1. Make sure that the PostgreSQL/bin folder (where PostgreSQL keeps it's
   scripts) is on the PATH.
2. find the bin folder for OSGeo4W that contains `ogr2ogr` and `ogrinfo`. Make sure
   it is on the PATH.

#### 3. Install the code libraries

1. Install [Python](http://www.python.org/download/releases/2.6.6/) (Windows x86 MSI 2.6.6) and make sure it is on the PATH
2. Install [setuptools](http://pypi.python.org/pypi/setuptools#files) (setuptools-0.6c11.win32-py2.6.exe)
1. Install pip 

