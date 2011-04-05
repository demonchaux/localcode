"""
The following example shows how to import
geometry from PostGIS using this module:
>>> import sql
>>> import mayascripts as ms
>>> layers = sql.physLayers()
>>> sqlQuery = sql.getLayers( 56, layers )
>>> polys = ms.queryToPolygons( sqlQuery )
>>> print polys
[u'curve1', u'curve2', u'curve3', u'curve4', u'curve5', u'curve6', u'curve7', u'curve8', u'curve9']
"""

import db
import sql
from sql import sqlRootPath
import layers
import shapely
import shapely.wkt 
import pymel.core as pm

def zPt(coordTuple):
    c = coordTuple
    x = c[0]
    y = c[1]
    if len(c) == 3:
        z = c[2]
    else:
        z = 0.0
    point = (x,y,z)
    return (x,y,z)

def ptListToPolyline(ptList):
    """ This uses a list of points to create a
    polyline curve in Maya, and then returns
    the name of the created curve.
    """
    pts = []
    for pt in ptList:
        newPt = zPt(pt)
        pts.append(newPt)

    cv = pm.curve(p=pts, degree=1.0)
    return cv

def makePolygons(listOfPointLists):
    """ This takes a set of point lists
    and creates a polyline for each point
    list, returning the names of the new
    polylines."""
    curves = []
    for pointList in listOfPointLists:
        curves.append(ptListToPolyline(pointList))
    return curves
    
def polygonQuery(connection, sql):
    """This takes an SQL query, runs it,
    and creates polygons out of it. This function
    is still being fleshed out, and needs to filter
    out the necessary information for dealing with
    MultiPolygons, and the interior and exterior rings
    of Polygons."""
    data = db.runopen(connection, sql)
    geom = []
    for rowTuple in data:
        ewkt = rowTuple[0]
        cleaned_ewkt = db.removeSRID(ewkt)
        multiPolygon = shapely.wkt.loads(cleaned_ewkt)
        try:
            for polygon in multiPolygon:
                geom.append(polygon.exterior.coords)
        except:
            return 'error reading polygons in multipolygons'
    return geom

def queryToPolygons(connection, sql):
    return makePolygons(polygonQuery(connection, sql))

def moveToLayer(layerName, objectList=[]):
    
    if pm.objExists(layerName) == False: # the layer does not exist
        pm.select(objectList)
        pm.createDisplayLayer(name=layerName)
    else: # the layer already exists
        pm.editDisplayLayerMembers( layerName, objectList )

def baseModel(site_id):
    """Based on an input site ID, this function
    runs an sql query to the PostGIS database and
    collects the geometry for each layer, and then
    places that geometry on a designated layer in
    Maya and stores the attributes of the geometry
    in the maya geometry."""
    conn = db.connect()
    parcelSQL = sql.getParcel( site_id )
    parcel = queryToPolygons(conn, parcelSQL)
    moveToLayer('site', parcel)
    s = site_id
    otherParcelsSQL = sql.getOtherParcels(s)
    otherParcels = queryToPolygons(conn, otherParcelsSQL)
    moveToLayer('vacantparcels', otherParcels)
    for key in layers.sites:
        if key != 'vacantparcels':
            layerSQL = sql.oneLayer( site_id, layers.sites[key] ) + ';'
            layerPolys = queryToPolygons(conn, layerSQL )
            moveToLayer(key, layerPolys)
    for key in layers.physical:
        layerSQL = sql.oneLayer( site_id, layers.physical[key] ) + ';'
        layerPolys = queryToPolygons(conn, layerSQL )
        moveToLayer(key, layerPolys)
    conn.close()
    
def deleteEverything():
    """deletes all layers and objects in the maya scene."""
    everything = pm.ls()
    undeleteables = pm.ls(ud=True)
    try:
        pm.delete(everything)    
    except:
        pass



    
