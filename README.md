# bachelorAssignment: Statistical Estimation of Rainfall by Integrating a Satellite-Based Algorithm and Rain Gauge Networks
The complete report of this project is [on this page](https://github.com/QiaoRenOreo/Rainfall-Estimation-using-Satellite-Based-Algorithm)

## Abstract
The spatial and temporal distribution of precipitation is very important for scientific uses and human being’s life [1]. The main goal of this study is to automate the process of producing precipitation estimates, based on gauge precipitation observation and satellite precipitation estimates. The scripts use ILWI-Python extensions (ilwis4). The algorithm applied in this study is Combined Scheme (CoSch) technique [1]. In order to generalize the script, two cases have been implemented: Latin America case and Africa case. The scripts and the precipitation estimation results produced in both cases are very useful for future work. 

## Keywords
  satellite-based rainfall estimation, gauge-based rainfall observation, combined scheme, additive bias correction, ratio bias correction

## Objective
The goal of this study is to develop scripts that automate and execute the Combined Scheme technique using ILWI-Python extensions.

## State of art
1) What are the advantages and disadvantage of gauge-based rainfall observation and satellite-based rainfall estimation? 
    The table shows a comparison between gauge-based rainfall observation and satellite-based rainfall estimation on their reliability and area coverage
![introduction_ppt](https://user-images.githubusercontent.com/46351057/50722303-ce97aa00-1107-11e9-89d9-fbbf45bf4a51.PNG)


2) What is the best merging technique? 
    Combined scheme (CoSch) technique consistently presents the best performance, among all the five merging techniques [1]. Combined scheme technique combines two approaches (additive bias correction and ratio bias correction) into a single method to remove the bias of the satellite estimates [3]. If the precipitation value corrected by additive bias correction (ADD) is closer to the gauge-based observation than the value corrected by ratio bias correction (ADD), then the ADD-corrected rainfall value is chosen [1]. Vice versa. 

## Methodology
![overview_2imgs](https://user-images.githubusercontent.com/46351057/50722236-ff2b1400-1106-11e9-9038-80cc29701089.PNG)

detailed flowchart of stage1,2,3 and 4 are [here](https://github.com/QiaoRenOreo/Rainfall-Estimation-using-Satellite-Based-Algorithm/tree/master/flowchart)

## Input 

![input_ppt](https://user-images.githubusercontent.com/46351057/50722240-0eaa5d00-1107-11e9-9da8-be448d63a405.png)

1) Rainfall statelite data (RFS) 

![input1_rainfall_satellite_data](https://user-images.githubusercontent.com/46351057/50722577-1caeac80-110c-11e9-83bb-b2715a84e2ff.PNG)

2) CPC precipitation

![input2_cpc_precipitation](https://user-images.githubusercontent.com/46351057/50722579-1d474300-110c-11e9-8a6a-5e10fb7620fb.PNG)

3) CPC gauge distribution

![input3_cpc_gauge_distribution](https://user-images.githubusercontent.com/46351057/50722580-1d474300-110c-11e9-97a7-33a76c4bf1fb.PNG)

4) Region of interest (ROI)

![input4_roi](https://user-images.githubusercontent.com/46351057/50722576-1caeac80-110c-11e9-9424-2e34932e5922.PNG)


## Results
![output_ppt](https://user-images.githubusercontent.com/46351057/50722239-0eaa5d00-1107-11e9-88d9-3b2f3f1943b0.PNG)
### A.	Result in the Latin America case
![output_latinamerica_12](https://user-images.githubusercontent.com/46351057/50722362-db68cd80-1108-11e9-8c69-1027f46efd19.png)
![output_latinamerica_34](https://user-images.githubusercontent.com/46351057/50722360-dad03700-1108-11e9-85b2-294375d250cf.png)
### B.	Results in the Africa Case
![output_africa_56_smallstoragespace](https://user-images.githubusercontent.com/46351057/50722436-e96b1e00-1109-11e9-83a8-d575c2df0a73.png)
![output_africa_78_smallstoragespace](https://user-images.githubusercontent.com/46351057/50722435-e96b1e00-1109-11e9-9f96-b465a747aacc.png)

Statistics results for basin management (Africa Case)

![output_africa_statistics](https://user-images.githubusercontent.com/46351057/50722609-7f07ad00-110c-11e9-8c62-46c20f7f8016.png)
