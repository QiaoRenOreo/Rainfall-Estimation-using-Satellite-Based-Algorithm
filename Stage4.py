import ilwis
ilwis.Engine.setWorkingCatalog ("file:///D:/chapter11/chapter11_Qiao_ilwis4")

rc1=ilwis.RasterCoverage("hydroestimator_025.mpr")
print (rc1.name())
rc2=ilwis.RasterCoverage("gauges_20110103_025.mpr")
print (rc2.name())
rc3=ilwis.RasterCoverage("prcp_20110103_025.mpr")
print (rc3.name())

#____________step1. cross two maps_________________________________________
'''
rc100=ilwis.RasterCoverage("Cuencas.mpr")
rc33=ilwis.RasterCoverage("cosch.mpr")
print(rc100.size().xsize, rc100.size().ysize)
print(rc33.size().xsize, rc33.size().ysize)
table_cross = ilwis.Engine.do( "cross", rc100 , rc33, "ignoreundef")# syntax is correct
table_cross.store("cross_table_DoubleCheck", "table", "ilwis3")# the resulting table does not have columns: Cuencas, NPix, area, and cosch
# after executing cross, the Cuencas is changed to only one domain. but it should has 12 domains
# when I run the same code after one day, the resulting table can not be produced.
# The error says "Failed to execute command "cross(_ILWISOBJECT_1004821,_ILWISOBJECT_1004824,ignoreundef)"; Please check the parameters provided."
'''
#__________step2. add a new column to the table_cross:  value domain
tableCross=ilwis.Table("Rain_basin_cross_forPython.tbt") 
print(tableCross.columnCount(), tableCross.recordCount())
print(tableCross.columns())
tableCross=ilwis.Engine.do("tabcalc",'"iff(@1>=1,@1,?)"',tableCross,"coschGE1mm","cosch",False)
print(tableCross.columnCount(), tableCross.recordCount())
print(tableCross.columns())

# __________step3. aggregrate by weighted average
totalRows = tableCross.recordCount()
print(totalRows)
columnCuencas = tableCross.column("Cuencas")
print(columnCuencas)
columnCosch = tableCross.column("cosch")
columnNPix = tableCross.column("NPix")

#i want to create a new empty table. There are three ways.
# way 1) use 'groupby'
# tableStatistics=ilwis.Engine.do('groupby', tableCross, "Cuencas", min)
# fail. error: Please check the parameters provided.

# way 2) create a table by domain names
# i was told that ilwis4 does not support this function. but normally, this function should be able to work

# way 3)
tableStatistics=ilwis.Table("statisticsPython.tbt")#create a new table
print(tableStatistics.columnCount())
print(tableStatistics.name())
tableStatistics.addColumn("Cuencas", "String")


basinList=('Amazonas', 'Del Plata', 'Orinoco', 'Tocantins','San Francisco','Colorado','Uruguay','Parnaiba',
'Salado','Chubut','Negro','Magdalena')
basinTotalNumber=len(basinList)
print(basinList)
print(basinList[1])
print(basinTotalNumber)

for basinIndex in range (basinTotalNumber):#put the basin names into the Cuencas column of the table
    tableStatistics.setCell("Cuencas", basinIndex, basinList[1])
print(tableStatistics.columns())

# to calculate Mean (weighted average precipitation or each basin)
tableStatistics.addColumn("mean", "value")
Sum=0
for basinIndex in range (basinTotalNumber): # basinIndex goes from the first basin name to the last basin name
    for rowIndex in range (totalRows): # rowIndex goes from the first row to the last row of the table
        iff(columnCuencas[rowIndex]==basinList[basinIndex])
        # fail: the correct syntax is unknown. this is a basic operation. I also need it for the other steps
        Sum=Sum+columnCuencas[rowIndex]*cosch[rowIndex]
        totalWeight=totalWeight+cosch[rowIndex]
    meanForBasin = Sum/totalWeight
    tableStatistics.setCell("mean", basinIndex, meanForBasin)    

#tableStatistics.store("tableStatistics", "table", "ilwis3")

# to calculate Area_GE_1mm (The percentage of the area which has precipitation >=1mm among the total area, for each basin )
#_______________step 6  tabcalc rain_basin_cross.tbt NPix_GE_1mm:=iff(cosch ge 1,NPix,0)
tableCross.addColumn("NPixGE1mm", "value")
tableCross=ilwis.Engine.do("tabcalc",'"iff(@1>=1,@2,0)"',tableCross,"NPixGE1mm","cosch","NPix",False)
tableCross.store("tableCross_aaaaaaaaa", "table", "ilwis3")
# this command works. but the orginal column "Cuencas" is missing. Secondly, the first column should be "basin name * value", instead of row number. 


#_______________step 9 and 8
#I have not created a tableTablaTemp yet
tableTablaTemp.addColumn("SumNPixGE1mm", "value")
tableTablaTemp.addColumn("SumNPix", "value")

#_______________step 10
tableCross.addColumn("areaGE1mm", "value")
tableCross=ilwis.Engine.do("tabcalc",'"(@1*100)/@2"',tableTablaTemp,"areaGE1mm","SumNPixGE1mm","SumNPix",False)
