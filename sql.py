"""
This module is used to construct sql statements,
sometimes using templates that are written out
in text files in a local folder.

Usage Example:
>>> import sql, db
>>> layers = sql.physLayers()
>>> print layers
['doitt_building_01_28jul2009', 'doitt_hydrography_01_282009', 'doitt_median_01_28jul2009', 'doitt_hydrography_structure_01_28jul2009', 'doitt_sidewalk_01_28jul2009', 'doitt_transportation_structure_01_28jul2009']
>>> siteID = 59
>>> sqlRequest = sql.getLayers(siteID, layers)
>>> data = db.run(sqlRequest)
>>> len(data)
5
"""

import layers
sqlRootPath = 'C:\\Users\\gallery\\LocalCodeNY\\PythonScripts'

def physLayers():
    layList = []
    for key in layers.physical:
        layList.append(layers.physical[key])
    return layList

def amenityLayers():
    layList = []
    for key in layers.amenities:
        layList.append(layers.amenities[key])
    return layList

def siteLayers():
    layList = []
    for key in layers.sites:
        layList.append(layers.sites[key])
    return layList

def healthLayers():
    layList = []
    for key in layers.health:
        layList.append(layers.health[key])
    return layList

def render(filePath, variableDict):
    """
    Returns a string based on reading some template,
    as designated by the file path, and then replacing
    each key in the variableDict with the value in 
    variableDict associated with that key.
    """
    sql = open(filePath, 'r').read()
    for key in variableDict:
        sql = sql.replace(key, variableDict[key])
    return sql

def oneLayer( site_id, layer, columns=[]):
    """returns the sql statement to get the geometry and
    other optional columns (as a list of strings) of 
    information based on which features touch the bounding 
    box of the parcel with the given id.
    Usage Example:
    >>> sId = 72
    >>> layer = 'roads'
    >>> cols = ['length', 'azimuth']
    >>> sqlStatement = oneLayer(sId, layer, cols)
    """
    template = '%s\\one_layer.sql' % sqlRootPath
    colString = ''
    for col in columns:
        colString += ', %s' % col
    varD = {
        '$table':layer,
        '$columns':colString,
        '$site_id':str(site_id)
        }
    return render(template, varD)

def getLayers(site_id, layerList, columnsDict={}):
    """
    returns an sql statement to get the geometry and
    any optional columns for a set of layers, by finding
    which features in each layer overlap the bounding box
    of the parcel with the input site id. Each key in the
    columnsDict should precisely match one of the layer
    names, and the value that corresponds to each key should
    be a list of column name strings.
    Usage Example:
    >>> sId = 34
    >>> layers = ['roads', 'parking_lots', 'trees']
    >>> colsDict = {'roads':['length'], 'parking_lots':['area', 'rate']}
    >>> sqlStatement = getLayers( sId, layers, colsDict )
    """
    union = 'UNION ALL\n'
    lay1 = layerList[0]
    if lay1 in columnsDict:
        cols = columnsDict[lay1]
        sqlString = oneLayer(site_id, lay1, cols)
    else:
        sqlString = oneLayer(site_id, lay1)
    for layer in layerList[1:]:
        sqlString += union
        if layer in columnsDict:
            cols = columnsDict[layer]
            sqlString += oneLayer(site_id, layer, cols)
        else:
            sqlString += oneLayer(site_id, layer)
    sqlString += ';'
    return sqlString
    
        
        
    
        


    
        


