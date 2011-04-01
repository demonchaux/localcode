"""
This module is used to construct sql statements,
sometimes using templates that are written out
in text files in a local folder.
"""

import layers


def renderSQL(sqlFilePath, variableDict):
    """
    Returns a string based on reading some template,
    as designated by the file path, and then replacing
    each key in the variableDict with the value in 
    variableDict associated with that key.
    """
    sql = open(sqlFilePath, 'r').read()
    for key in variableDict:
        sql = sql.replace(key, variableDict[key])
    return sql

def justGeom(site_id):
    """
    returns an sql statement string that would retrieve
    all geometry from the layers of physical data
    where that geometry touches the bounding box of
    vacant parcel with the given id.
    """
    template = 'justGeometry.sql'
    tables = layers.physical['all']
    varD = {
        '$tables':tables,
        '$site_id':str(site_id)
        }
    return renderSQL(template, varD)
        
        


