#smjCoincidentGeometry.py
#SCRIPT - smjCoincidentGeometry.py

#PURPOSE
Creates Coincident Geometry Between Features.

#TYPICAL EXAMPLE
GPS Tracks captured in the field. Some post processing, geoprocessing is required to better align tracks to fixed (property) boundaries).

#LIMITATIONS
This tool has come about through some requirements by the SOuth African National Parks Board who are required to manage GPS Boundary tract along know given boundaries. 

#OWNERSHIP
Susan Jones
Spatial Logic Limited
Auckland, NEW ZEALAND
20 March 2013

#EMAIL
sjones@spatiallogic.co.nz
http://www.spatiallogic.co.nz

#INPUT PARAMETERS
1 - Line FeatureSet (can contain a selection)
2 - Coincident Feature Layer (can contain a selection)
3 - Working Geodatabase
4 - Tolerance

#OUTPUT PARAMETERS
1 - replacement adjusted polygon featurs
2 - alignment features

#DEPENDANCIES
arcgis desktop license (arceditor)

#ARCGIS SERVER
This tool is easily configured for ArcGIS Server but replacing the outWs with the scratch Geodatabase.