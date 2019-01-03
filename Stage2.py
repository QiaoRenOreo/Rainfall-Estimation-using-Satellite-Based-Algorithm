import ilwis
ilwis.Engine.setWorkingCatalog ("file:///D:/chapter11/chapter11_Qiao_ilwis4")

rc1=ilwis.RasterCoverage("hydroestimator_025.mpr")
print (rc1.name())

rc2=ilwis.RasterCoverage("gauges_20110103_025.mpr")
print (rc2.name())

rc3=ilwis.RasterCoverage("prcp_20110103_025.mpr")
print (rc3.name())

#Mask the location of gauges (gauge_boolean)
rc2_1=ilwis.Engine.do("mapcalc",'"iff(@1>=1,1,?)"',rc2)
#first problem:  fail in ilwis 4, invalid syntax. only works in python
#second problem: when I open the resulting map, the result is totally black.
#it shows both 0 and 1 as black. in its attribute table, the column "value" is missing.
#the undefined value should be shown as "?". But in the resulting map, it shows undefined value as 0

rc2_1.store("gauge_boolean","map","ilwis3")
print (rc2_1.name())

#Clean the precipitation value: set the negative precipitation value as undefined (prcp_temp)
rc3_1=ilwis.Engine.do("mapcalc",'"iff(@1>=0,@1,?)"',rc3)
rc3_1.store("prcp_temp", "map", "ilwis3")
print (rc3_1.name())


#--------------------------question!!----------------

#Mask the precipitation values for the gauge-occupied pixels (prcp_masked)
rc4=ilwis.Engine.do("mapcalc",'"@1*(@2/10)"',rc2_1,rc3_1)
# succeded in May, but fail in the end of June.
# I installed the updated version of ilwis 4 in June 13th.
# I tried the other commands to test multiplication and division: 
#rctemp=ilwis.Engine.do("mapcalc",'"@1*0.1"',rc3_1) #fail
#rctemp=rc3_1/10 #fail
#rctemp=(rc3_1*0.1) #fail
#rctemp=ilwis.Engine.do("binarymathraster",rc3_1,0.1,times) #fail
#rc4=ilwis.Engine.do("mapcalc",'"@1*@2"',rc2_1,rc3_1) #fail

rc4.store("prcp_masked", "map", "ilwis3")
print (rc4.name())

#---------------------start the additive bias correction

rc5=ilwis.Engine.do("mapcalc",'"@2-@1"',rc1,rc4)
rc5.store("bias_add_temp", "map", "ilwis3")
print (rc5.name())

rc6=ilwis.Engine.do("mapcalc",'"iff(@1==?,0,@1)"',rc5)
rc6.store("bias_add_for_sum", "map", "ilwis3")
print (rc6.name())

rc7 = ilwis.Engine.do('linearrasterfilter', rc6,'"code=1 1 1 1 1 1 1 1 1, 0.1111111"')  
rc7.store("add_sum", "map", "ilwis3")
print (rc7.name())

rc8=ilwis.Engine.do("mapcalc",'"iff(@1==0,0,1)"',rc6)
rc8.store("bias_add_for_count", "map", "ilwis3")
print (rc8.name())

rc9 = ilwis.Engine.do('linearrasterfilter', rc8,'"code=1 1 1 1 1 1 1 1 1, 0.1111111"')  
rc9.store("add_count", "map", "ilwis3")
print (rc9.name())

rc10=ilwis.Engine.do("mapcalc",'"@1/@2"',rc7, rc9)
rc10.store("bias_add_for_count", "map", "ilwis3")
print (rc10.name())

rc11=ilwis.Engine.do("mapcalc",'"iff(@1==?,0,@1)"',rc10)
rc11.store("bias_add", "map", "ilwis3")
print (rc11.name())

rc12=ilwis.Engine.do("mapcalc",'"@1+@2"',rc1, rc11)
rc12.store("hydro_add", "map", "ilwis3")
print (rc12.name())



##---------------------start the ratio bias correction



#to make "bias_rat_temp", the result has a problem, some points are missing!
# I want to find out the reason. But this piece of code got stuck the previous step: ("mapcalc",'"@1*(@2/10)"',rc2_1,rc3_1)
# method 1
rc14=ilwis.Engine.do("mapcalc",'"iff(@2>0,@2/@1,1)"',rc1,rc4)
rc14.store("bias_rat_temp", "map", "ilwis3")
print (rc14.name())
# method 2
#rc30=ilwis.Engine.do("mapcalc",'"@2/@1"',rc1,rc4)
#rc14=ilwis.Engine.do("mapcalc",'"iff(@1>0,@2,1)"',rc4,rc30)
#rc14.store("bias_rat_temp", "map", "ilwis3")


rc15=ilwis.Engine.do("mapcalc",'"iff(@1==?,0,@1)"',rc14)
rc15.store("bias_rat_for_sum", "map", "ilwis3")
print (rc15.name())

rc16=ilwis.Engine.do('linearrasterfilter', rc15,'"code=1 1 1 1 1 1 1 1 1, 0.1111111"')  
rc16.store("rat_sum", "map", "ilwis3")
print (rc16.name())

rc17=ilwis.Engine.do("mapcalc",'"iff(@1==0,0,1)"',rc14)
rc17.store("bias_rat_for_count", "map", "ilwis3")
print (rc17.name())

rc18=ilwis.Engine.do('linearrasterfilter', rc17,'"code=1 1 1 1 1 1 1 1 1, 0.1111111"')  
rc18.store("rat_count", "map", "ilwis3")
print (rc18.name())

rc19=ilwis.Engine.do("mapcalc",'"@1/@2"',rc16,rc18)
rc19.store("average_rat", "map", "ilwis3")
print (rc19.name())

rc20=ilwis.Engine.do("mapcalc",'"iff(@1==?,0,@1)"',rc19)
rc20.store("bias_rat", "map", "ilwis3")
print (rc20.name())

rc21=ilwis.Engine.do("mapcalc",'"iff(@1>0,@1*@2,@1)"',rc1, rc20)
rc21.store("hydro_rat", "map", "ilwis3")
print (rc21.name())


#__________________________Stage 3_____________________________________
#calculate the difference between the masked precipitation and the corrected satellite precipitation (by additive bias correction)
rc13=ilwis.Engine.do("mapcalc",'"abs(@1-@2)"',rc4,rc12)
rc13.store("diff_abs_add", "map", "ilwis3")
print (rc13.name())

#calculate the difference between the masked precipitation and the corrected satellite precipitation (by ratio bias correction)
rc22=ilwis.Engine.do("mapcalc",'"abs(@1-@2)"',rc4,rc21)
rc22.store("diff_abs_rat", "map", "ilwis3")
print (rc22.name())

rc24=ilwis.Engine.do("mapcalc",'"abs(@1)"',rc12)
rc24.store("rc24", "map", "ilwis3")

rc25=ilwis.Engine.do("mapcalc",'"abs(@1)"',rc21)
rc25.store("rc25", "map", "ilwis3")

# if additive bias correction provides smaller error, choose the additive bias corrected rainfal. Vice versa. 
rc26=ilwis.Engine.do("mapcalc",'"iff(@2<@4,@1,@3)"',rc24, rc13, rc25, rc22)
rc26.store("cosch_temp", "map", "ilwis3")
print (rc26.name())
rc13=ilwis.Engine.do("mapcalc",'"abs(@1-@2)"',rc4,rc12)
rc13.store("diff_abs_add", "map", "ilwis3")
print (rc13.name())

#calculate the difference between the masked precipitation and the corrected satellite precipitation (by ratio bias correction)
rc22=ilwis.Engine.do("mapcalc",'"abs(@1-@2)"',rc4,rc21)
rc22.store("diff_abs_rat", "map", "ilwis3")
print (rc22.name())

rc24=ilwis.Engine.do("mapcalc",'"abs(@1)"',rc12)
rc24.store("rc24", "map", "ilwis3")

rc25=ilwis.Engine.do("mapcalc",'"abs(@1)"',rc21)
rc25.store("rc25", "map", "ilwis3")

# if additive bias correction provides smaller error, choose the additive bias corrected rainfal. Vice versa. 
rc26=ilwis.Engine.do("mapcalc",'"iff(@2<@4,@1,@3)"',rc24, rc13, rc25, rc22)
rc26.store("cosch_temp", "map", "ilwis3")
print (rc26.name())

#rc23=ilwis.Engine.do("mapcalc",'"iff(@2<@4,abs(@1),abs(@3))"',rc12, rc13, rc21, rc22)
#rc23.store("cosch_temp", "map", "ilwis3")
#print (rc21.name())

#for pixels on which no gauges are located (undefined pixels), choose the uncorrected(original) satellite data for them
rc27=ilwis.Engine.do("mapcalc",'"iff(@1==?,@2,@1)"',rc26, rc1)
rc27.store("cosch", "map", "ilwis3")
print (rc27.name())

#___________________________________________________________
rc28=ilwis.Engine.do('linearrasterfilter', rc2_1,'"code=9 9 9 9 9 9 9 9 9, 0.1111111"')  
rc28.store("gauge_temp_mask", "map", "ilwis3")
print (rc28.name())

rc29=ilwis.Engine.do("mapcalc",'"@1*(@2/10)"', rc28, rc3)
rc29.store("prcp_masked_big", "map", "ilwis3")
print (rc29.name())

#calculate the difference between the masked precipitation and the corrected satellite precipitation (by additive bias correction)
rc30=ilwis.Engine.do("mapcalc",'"abs(@1-@2)"',rc29,rc12)
rc30.store("diff_abs_add_big", "map", "ilwis3")
print (rc30.name())

#calculate the difference between the masked precipitation and the corrected satellite precipitation (by ratio bias correction)
rc31=ilwis.Engine.do("mapcalc",'"abs(@1-@2)"',rc29,rc21)
rc31.store("diff_abs_rat_big", "map", "ilwis3")
print (rc31.name())

# if additive bias correction provides smaller error, choose the additive bias corrected rainfal. Vice versa. 
rc32=ilwis.Engine.do("mapcalc",'"iff(@2<@4,@1,@3)"',rc24, rc30, rc25, rc31)
rc32.store("cosch_temp_big", "map", "ilwis3")
print (rc32.name())

#for pixels on which no gauges are located (undefined pixels), choose the uncorrected(original) satellite data for them
rc33=ilwis.Engine.do("mapcalc",'"iff(@1==?,@2,@1)"',rc32, rc1)
rc33.store("cosch_big", "map", "ilwis3")
print (rc33.name())
#___________________________________________________________





