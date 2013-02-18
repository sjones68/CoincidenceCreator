#smjCoincidentGeometry.py

#PURPOSE
#creates Coincident Geometry Between Features.

#TYPICAL EXAMPLE
#GPS Tracks captured in the field. Some post processing, geoprocessing is required
#to better align tracks to fixed (property) boundaries).

#LIMITATIONS
#This tool has come about through some requirements by the SOuth African National Parks Board
#who are required to manage GPS Boundary tract along know given boundaries. 

#OWNERSHIP
#Susan Jones
#Spatial Logic Limited
#Auckland, NEW ZEALAND
#30 January 2013

#EMAIL
#sjones@spatiallogic.co.nz
#http://www.spatiallogic.co.nz

#INPUT PARAMETERS
#1 - Line FeatureSet (can contain a selection)
#2 - Coincident Feature Layer (can contain a selection)
#3 - Working Geodatabase
#4 - Tolerance

#OUTPUT PARAMETERS
#1 - featureSet called MewRoutes in the Geodatabase

#DEPENDANCIES
#arcgis desktop license (arcview)

#ARCGIS SERVER
#This tool is easily configured for ArcGIS Server but replacing the outWs with the scratch Geodatabase.

#import Modules
import arcpy, os, datetime

#timings
start=datetime.datetime.now()

#banner
arcpy.AddMessage("***\nCREATE COINCIDENT GEOMETRY\n***")
arcpy.AddMessage("Susan Jones\nSpatial Logic Ltd\n30 January 2013\n")

#get Parameters
arcpy.AddMessage("fetching Parameters...")
lineFc=arcpy.GetParameterAsText(0)
polygonFc=arcpy.GetParameterAsText(1)
tolerance=arcpy.GetParameter(3)
outWsp=arcpy.GetParameterAsText(2)

#print Details
arcpy.AddMessage("-> Line Featureset:"+lineFc)
arcpy.AddMessage("-> Coincident Features:"+polygonFc)
arcpy.AddMessage("-> Output Geodatabase:"+outWsp)
arcpy.AddMessage("-> Tolerance:"+str(tolerance))

#set Environment
arcpy.AddMessage("\nsetting Environment...")
arcpy.env.overwriteOutput=1
arcpy.env.workspace=outWsp

#layer Management
arcpy.AddMessage("\nmaking Layers")
arcpy.MakeFeatureLayer_management(lineFc,"lines1")

#copy To Geodatabase
arcpy.AddMessage("copying Coincient Features To "+outWsp+"...")
arcpy.CopyFeatures_management(polygonFc, "poly")
arcpy.MakeFeatureLayer_management("poly", "poly1")

#analysis
arcpy.AddMessage("buffering features...")
if arcpy.Exists("buffer_"+str(tolerance)):
    arcpy.Delete_management("buffer_"+str(tolerance))
arcpy.Buffer_analysis ("lines1", "buffer_"+str(tolerance), tolerance)
##arcpy.Buffer_analysis ("lines1", "buffer_"+str(tolerance), tolerance, "FULL", "ROUND", "ALL")
arcpy.MakeFeatureLayer_management("buffer_"+str(tolerance),"buff1")

#intersect
arcpy.AddMessage("intersecting intersectArea...")
if arcpy.Exists("intersectArea"):
    arcpy.Delete_management("intersectArea")
arcpy.Intersect_analysis(["buffer_"+str(tolerance), polygonFc], "intersectArea", "ONLY_FID", 0.05) 

#create Featureclasa
arcpy.AddMessage("creating intersectLine...")
if arcpy.Exists("intersectLine.shp"):
    arcpy.Delete_management("intersectLine")
descFc=arcpy.Describe("intersectArea")
sr=descFc.spatialReference
arcpy.CreateFeatureclass_management(outWsp, "intersectLine", "POLYLINE", "intersectArea", "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", sr)

#insert Cursor
irecs=arcpy.InsertCursor("intersectLine")
recs=arcpy.SearchCursor("intersectArea")
rec=recs.next()
while rec:
    irec=irecs.newRow()
    irec.shape=rec.shape.getPart(0)
    irecs.insertRow(irec)
    #next rec
    rec=recs.next()
del irec
del irecs
del recs

#select Coincident Features
arcpy.AddMessage("selecting Coincident Features...")
arcpy.MakeFeatureLayer_management("intersectLine", "intersectLine1")
arcpy.AddMessage("intersecting...")
if arcpy.Exists("intersectLine2"):
    arcpy.Delete_management("intersectLine2")
arcpy.Intersect_analysis(["intersectLine1"], "intersectLine2", "ONLY_FID", 0.001)

#rename
arcpy.AddMessage("renaming intersectLine...")
arcpy.Delete_management("intersectLine1")
arcpy.Delete_management("intersectLine")
arcpy.Rename_management("intersectLine2", "intersectLine")

#integrating
arcpy.AddMessage("integrating Coincident Geometry...")
if arcpy.Exists("NewRoutes"):
    arcpy.Delete_management("NewRoutes")
arcpy.CopyFeatures_management(lineFc, outWsp+os.path.sep+"NewRoutes")
arcpy.MakeFeatureLayer_management("NewRoutes", "NewRoutes1")
arcpy.MakeFeatureLayer_management("intersectLine", "intersectLine1")
lstFeatures="\"intersectLine1\" 1;\"NewRoutes1\" "+str(50)
arcpy.AddMessage(lstFeatures)
arcpy.Integrate_management(lstFeatures, tolerance)

#smoothing
arcpy.AddMessage("smoothing NewRoutes...")
if arcpy.Exists("smoothingFc"):
    arcpy.Delete_management("smoothingFc")
arcpy.SmoothLine_cartography ("NewRoutes1", "smoothingFc", "BEZIER_INTERPOLATION")
arcpy.Delete_management("NewRoutes1")

#rename
arcpy.AddMessage("renaming To NewRoutes...")
arcpy.Delete_management("NewRoutes")
arcpy.Rename_management("smoothingFc", "NewRoutes")

#set Output
arcpy.AddMessage("\nassigning Output...")
arcpy.SetParameter(4, "NewRoutes")
arcpy.MakeFeatureLayer_management("NewRoutes", "NewRoutes1")
arcpy.SetParameter(4, "NewRoutes1")

#cleanUp
arcpy.AddMessage("\ncleaning Up")
arcpy.Delete_management("lines1")
arcpy.Delete_management("poly1")
arcpy.Delete_management("poly")
arcpy.Delete_management("buff1")
arcpy.Delete_management("intersectArea")
arcpy.Delete_management("intersectLine")
arcpy.Delete_management("buffer_"+str(tolerance))
arcpy.Delete_management("intersectLine1")

#refreshView
arcpy.RefreshActiveView()

#completed
arcpy.AddMessage("completed")
arcpy.AddMessage("elapsed "+str(datetime.datetime.now()-start)+"\n")