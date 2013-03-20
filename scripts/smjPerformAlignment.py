#smjPerformAlignment.py

#PURPOSE
#Performs alignment of polygon features with line features using a specified Cluster Tolerance (10 default)

#PROCESS
#Capture Input Feature Classes and tolerance
#Get the Working File Geodatabase
#Get the Spatial Reference of the Input Datasets
#Create a Feature Dataset Using the Spatial Reference
#Copy Input Features Across into Feature Dataset
#Create a Topology Rule
#Add the 2 Feature Classes to The Rule
#Define the Rule Action
#Validate

#AUTHOR
#Susan Jones
#Spatial Logic Limited

#REVISION
#20 March 2013

#import Modules
import arcpy, os, datetime

startTime=datetime.datetime.now()

#banner
arcpy.AddMessage("***\nPerform Alignment Between Feature Classes\n***")

#get Parameters
arcpy.AddMessage("\n***getParameters")
Cluster_Tolerance=arcpy.GetParameterAsText(3)
LandPortion=arcpy.GetParameterAsText(0)
RoadSections=arcpy.GetParameterAsText(1)
gdb=arcpy.GetParameterAsText(2)
editRank="5"
fixRank="1"

#settings
arcpy.env.overwriteOutput=1

#spatial Reference
arcpy.AddMessage("\n***get The Spatial reference")
sr=arcpy.Describe(LandPortion).spatialReference
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#create Feature Dataset
arcpy.AddMessage("\n***create Feature Dataset")
arcpy.CreateFeatureDataset_management(gdb, "topo", sr)
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#copy The Input Features
arcpy.AddMessage("\n***copy The Input Features")
polyTopo=arcpy.CopyFeatures_management(LandPortion,gdb+os.path.sep+"topo"+os.path.sep+"polyTopo")
lineTopo=arcpy.CopyFeatures_management(LandPortion,gdb+os.path.sep+"topo"+os.path.sep+"lineTopo")
arcpy.CopyFeatures_management(LandPortion,polyTopo)
arcpy.CopyFeatures_management(RoadSections,lineTopo)
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#create Topology
arcpy.AddMessage("\n***create Topology")
arcpy.CreateTopology_management(gdb+os.path.sep+"topo", "coincidentBoundaries", Cluster_Tolerance)
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

###add Feature Class To Topology
arcpy.AddMessage("\n***add Feature Class To Topology")
arcpy.AddFeatureClassToTopology_management(gdb+os.path.sep+"topo"+os.path.sep+"coincidentBoundaries", lineTopo, fixRank, "1")
arcpy.AddFeatureClassToTopology_management(gdb+os.path.sep+"topo"+os.path.sep+"coincidentBoundaries", polyTopo, editRank, "1")
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#add Rule To Topology
arcpy.AddMessage("\n***add Rule Topology")
arcpy.AddRuleToTopology_management(gdb+os.path.sep+"topo"+os.path.sep+"coincidentBoundaries", "Boundary Must Be Covered By (Area-Line)", polyTopo, "", lineTopo, "")
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#validate Topology
arcpy.AddMessage("\n***validate Topology")
arcpy.ValidateTopology_management(gdb+os.path.sep+"topo"+os.path.sep+"coincidentBoundaries", "VISIBLE_EXTENT")
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#copy Features Back
arcpy.AddMessage("\n***copy Features Back")
arcpy.Delete_management(LandPortion)
arcpy.CopyFeatures_management(polyTopo,LandPortion)
arcpy.Delete_management(RoadSections)
arcpy.CopyFeatures_management(lineTopo,RoadSections)
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))

#set Parameters
print("***set Output Parameters")
arcpy.SetParameter(4,LandPortion)
arcpy.SetParameter(5,RoadSections)

#completed
arcpy.AddMessage("\ncompleted")
arcpy.AddMessage("elapsed:\t"+str(datetime.datetime.now()-startTime))
arcpy.RefreshActiveView()

