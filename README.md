# Rainfall-Estimation-using-Satellite-Based-Algorithm
bachelorAssignment: Estimation of Rainfall by Integrating a Satellite-Based Algorithm and Rain Gauge Networks

## Abstract
The spatial and temporal distribution of precipitation is very important for scientific uses and human being’s life [1]. The main goal of this study is to automate the process of producing precipitation estimates, based on gauge precipitation observation and satellite precipitation estimates. The scripts use ILWI-Python extensions (ilwis4). The algorithm applied in this study is Combined Scheme (CoSch) technique [1]. In order to generalize the script, two cases have been implemented: Latin America case and Africa case. The scripts and the precipitation estimation results produced in both cases are very useful for future work. 

Keywords: combined scheme, additive bias correction, ratio bias correction

## Objective
The goal of this study is to develop scripts that automate and execute the Combined Scheme technique using ILWI-Python extensions.

## State of art
1) What are the advantages and disadvantage of gauge-based rainfall observation and satellite-based rainfall estimation? 
![stateofart_gauge_vs_satellite](https://user-images.githubusercontent.com/46351057/50721090-596ea980-10f4-11e9-8dec-fb0cc2c5160f.png)

2) What is the best merging technique? 
Combined scheme (CoSch) technique consistently presents the best performance, among all the five merging techniques [1]. Combined scheme technique combines two approaches (additive bias correction and ratio bias correction) into a single method to remove the bias of the satellite estimates [3]. If the precipitation value corrected by additive bias correction (ADD) is closer to the gauge-based observation than the value corrected by ratio bias correction (ADD), then the ADD-corrected rainfall value is chosen [1]. Vice versa. 

## methodology
![flowchart_follow the material overview](https://user-images.githubusercontent.com/46351057/50721035-532bfd80-10f3-11e9-86a5-236d1c98e2d6.jpg)
![flowchart_same structure as the material_stage1](https://user-images.githubusercontent.com/46351057/50721036-53c49400-10f3-11e9-8072-27fd747f851f.jpg)
![flowchart_same structure as the material_stage2](https://user-images.githubusercontent.com/46351057/50721037-545d2a80-10f3-11e9-9f52-3abce787957b.jpg)
![flowchart_same structure as the material_stage3](https://user-images.githubusercontent.com/46351057/50721038-54f5c100-10f3-11e9-9446-8b5fa624f773.jpg)
![flowchart_same structure as the material_stage4](https://user-images.githubusercontent.com/46351057/50721034-532bfd80-10f3-11e9-97be-1920d7e6bb66.jpg)



