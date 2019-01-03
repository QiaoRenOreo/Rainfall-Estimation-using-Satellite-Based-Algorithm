import ilwis
ilwis.Engine.setWorkingCatalog ("file:///D:/chapter11/chapter11_Qiao_ilwis4")
#-----------------resample the map "hydro_20110103.mpr"
rcSatellite=ilwis.RasterCoverage("hydro_20110103.mpr")
print(rcSatellite.name())
print(rcSatellite.geoReference().name())
georef025 = ilwis.GeoReference("sudamerica_0_25.grf")
rc1 = ilwis.Engine.do("resample", rcSatellite, georef025, "nearestneighbour")
rc1.store("hydroestimator_025Copy", "map", "ilwis3")
print(rc1.size().xsize, rc1.size().ysize )#succeed

#-------------------read gauge based map (cpc_temp1 and cpc_temp2)-------------------------
rc101=ilwis.RasterCoverage("cpc_temp1.mpr")
print(rc101.name())
print(rc101.size().xsize, rc101.size().ysize)

rc102=ilwis.RasterCoverage("cpc_temp2.mpr")
print(rc102.name())
print(rc102.size().xsize, rc101.size().ysize)

initialGeoref = ilwis.GeoReference("code=georef:type=corners,csy=epsg:4326,envelope= 0.0 -90.0 360.0 90.0,  gridsize=720 360, cornerofcorners=yes, name=initialGeoref")
rc101.setGeoReference(initialGeoref)
rc102.setGeoReference(initialGeoref)

#---------------------------------------mirror rotate-------------------------
rc104 = ilwis.Engine.do("mirrorrotateraster", rc101, "mirrhor")
rc104.setGeoReference(initialGeoref)
rc104.store("cpc_temp1_mirror", "map", "ilwis3")
print(rc104.name())
print(rc104.size().xsize, rc104.size().ysize)
print(rc104.geoReference().name())


rc105 = ilwis.Engine.do("mirrorrotateraster", rc102, "mirrhor")
rc105.setGeoReference(initialGeoref)
rc105.store("cpc_temp2_mirror", "map", "ilwis3")
print(rc105.name())
print(rc105.size().xsize, rc105.size().ysize)
print(rc105.geoReference().name())

#--------------------------------create georeference: east
georefEast = ilwis.GeoReference("code=georef:type=corners,csy=epsg:4618,envelope= 0.0 90.0 180.0 90.0,  gridsize=360 360, cornerofcorners=yes, name=east")
# about the georeference definition, normally, epsg:4326 should be able to include the envelope. it does not make sense to define epsg and envelope at the same time
georefEast.store("east", "georeference", "stream") 
print(georefEast.name())#succeed
print(georefEast.pixelSize())
print(georefEast.size().xsize, georefEast.size().ysize)

#--------------------------------create georeference: west
georefWest = ilwis.GeoReference("code=georef:type=corners,csy=epsg:4618,envelope= 180.0 90.0 0.0 90.0,  gridsize=360 360, cornerofcorners=yes, name=west")
georefWest.store("west", "georeference", "stream") 
print(georefWest.name())#succeed
print(georefWest.pixelSize())
print(georefWest.size().xsize, georefWest.size().ysize)

#------------ test setting georeference---------test map: hydro_20110103.mpr
rc200=ilwis.RasterCoverage("hydro_20110103.mpr")
print(rc200.name())#succeed
print(rc200.size().xsize, rc200.size().ysize)#succeed
print(rc200.geoReference().name())

georefEast = ilwis.GeoReference("code=georef:type=corners,csy=epsg:4618,envelope= 0.0 90.0 180.0 90.0,  gridsize=360 360, cornerofcorners=yes, name=east")
rc200.setGeoReference(georefEast)# set succeed, store fail
print(rc200.name())
print(rc200.geoReference().name())# succceed. print: east

rc200.store("aaaaa" ,  "map" , "ilwis3" )
#fail storing of this map. error: ILWIS ErrorObject: format coordsystem or data object is readonly



#--------------------------------split one map to two submaps
#-------------------------raster selection-----------------------------------
# I made 3 tries.
# the syntax is (min x, min y, max x, max y). in a global map, does x goes from -180 to 180? or from 0 to 360? Or this is not fixed and I can define this in my own way?
# east to the Greenwich is negative, and south to the equator is negative. This is not written in the github tutorial
# the example from github is the following. It does not solve this problem:
#      create a new georeference
#      the following georeference is for a 1800x1380 grid, and the provided lat/lon bounds are assigned to the corners of this grid
#      georef = ilwis.GeoReference("code=georef:type=corners,csy=epsg:4326,envelope=32.991677775048 14.900003906339 47.991678557359 3.400003306568,gridsize=1800 1380,cornerofcorners=yes,name=ethnew")


# first try:
#rc_cpc_temp1_SelectedForEast = ilwis.Engine.do("selection", rc104, "boundingbox(361,-90,720,90)")
#rc_cpc_temp1_SelectedForWest = ilwis.Engine.do("selection", rc104, "boundingbox(0,-90,360,90)")
# both of the above two commands have the error: obj = Engine__do(str(out),str(operation),str(arg1),str(arg2),str(arg3),str(arg4),str(arg5),str(arg6),str(arg7)) Please check the parameters provided.

# second try:
# rc_cpc_temp1_SelectedForEast = ilwis.Engine.do("selection", rc104, "boundingbox(0,-90,180,90)")
# rc_cpc_temp1_SelectedForWest = ilwis.Engine.do("selection", rc104, "boundingbox(-180,-90,0,90)")
# both of the above two commands have the error: obj = Engine__do(str(out),str(operation),str(arg1),str(arg2),str(arg3),str(arg4),str(arg5),str(arg6),str(arg7)) Please check the parameters provided.

# third try:
# rc_cpc_temp1_SelectedForEast = ilwis.Engine.do("selection", rc104, "boundingbox(180,-90,360,90)")
# rc_cpc_temp1_SelectedForWest = ilwis.Engine.do("selection", rc104, "boundingbox(0,-90,180,90)")
# both of the above two commands have the error: obj = Engine__do(str(out),str(operation),str(arg1),str(arg2),str(arg3),str(arg4),str(arg5),str(arg6),str(arg7)) Please check the parameters provided.


#read a map-----------------------------split cpc_temp1_mirror into two submaps
rc106=ilwis.RasterCoverage("cpc_temp1_mirror.mpr")#question: fail. after a new raster is generated, reading the new map fails
print(rc106.name())#suceed
print(rc106.size().xsize, rc106.size().ysize)#succeed


rc_cpc_temp1_SelectedForEast.setGeoReference(georefEast)
rc_cpc_temp1_SelectedForEast.store("cpc_temp1_mirror_prepareForEast", "map", "ilwis3") #fail: readonly
print(rc_cpc_temp1_SelectedForEast.name())
print(rc_cpc_temp1_SelectedForEast.size().xsize, rc_cpc_temp1_SelectedForEast.size().ysize)
print(rc104.geoReference().name())


rc_cpc_temp1_SelectedForWest.setGeoReference(georefWest)
rc_cpc_temp1_SelectedForWest.store("cpc_temp1_mirror_prepareForWest", "map", "ilwis3")
print(rc_cpc_temp1_SelectedForWest.name())
print(rc_cpc_temp1_SelectedForWest.size().xsize, rc_cpc_temp1_SelectedForWest.size().ysize)
print(rc_cpc_temp1_SelectedForWest.geoReference().name())

#set geo reference east
#rc104.setGeoReference(georefEast)#succceed
#print(rc104.name())
#print(rc104.geoReference().name())#succceed. print: east
#store the geo-referenced  map
#rc104.store("cpc_temp1_east" ,  "map" , "ilwis3" )#fail
#print(rc104.name())
#print(rc104.size().xsize, rc104.size().ysize)

#set geo reference west
#rc106.setGeoReference(georefWest)#succceed
#print(rc106.name())
#print(rc106.geoReference().name())#succceed. print: west
#store the geo-referenced  map
#rc106.store("cpc_temp1_west" ,  "map" , "ilwis3" )#fail
#print(rc106.name())
#print(rc106.size().xsize, rc106.size().ysize)



#read a map-----------------------------split cpc_temp2_mirror into two submaps
rc107=ilwis.RasterCoverage("cpc_temp2_mirror.mpr")
print(rc107.name())#succeed
print(rc107.size().xsize, rc107.size().ysize)#succeed

#set geo reference east
rc107.setGeoReference(georefEast)
print(rc107.geoReference().name())# succceed. print: east
#set geo reference west
rc107.setGeoReference(georefWest)
print(rc107.geoReference().name())# succceed. print: west

#store the geo-referenced  map
#rc107.store("aaaaa" ,  "map" , "ilwis3" )#fail cpc_temp2_west
#fail because "format coord system or data object is read only"
#print(rc107.name())

#------------set full georeference and resample
# read the existing georefference "full_WtoE.grf" 
georefFullWtoE = ilwis.GeoReference("full_WtoE.grf")
# Set the full geo-refference on the mean precipitation value of gauges: 
glued_gauge_rainfall.setGeoReference(georefFullWtoE)
# resample the mean precipitation value of gauges:
rc3 = ilwis.Engine.do("resample", glued_gauge_rainfall, georef025, "nearestneighbour")

# Set the full geo-refference on the gauge-distribution image
glued_gauge_distribution.setGeoReference(georefFullWtoE)
# resample the gauge-distribution image
rc2 = ilwis.Engine.do("resample", glued_gauge_distribution, georef025, "nearestneighbour")

