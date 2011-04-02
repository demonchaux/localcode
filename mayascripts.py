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
import shapely
import shapely.wkt 
import maya.cmds as cmds

def getAllCmds(outputFilePath):
    f = open(outputFilePath, 'w')
    for cmd in dir(cmds):
        f.write('%s\n' % cmd)
    f.close()
    print 'done'

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

    cv = cmds.curve(p=pts, degree=1.0)
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
    
def polygonQuery(sql):
    """This takes an SQL query, runs it,
    and creates polygons out of it. This function
    is still being fleshed out, and needs to filter
    out the necessary information for dealing with
    MultiPolygons, and the interior and exterior rings
    of Polygons."""
    data = db.run(sql)
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

def queryToPolygons(sql):
    return makePolygons(polygonQuery(sql))



    
