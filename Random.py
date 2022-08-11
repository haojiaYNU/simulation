import random
import heapq
import copy

#parameter setting
Freq_of_mobileCPU = 1.8 #GHZ
Require_CPU_cycles = 100 #required CPU cycles
Bandwidth = 20 #MB/S
Task_simulation = ["streamcluster","bodytrack","vips","raytrace","X264"]
Size_of_Task = [0.74,10.27,15.87,4.07,1.76] #size(MB) corresponding to the task
Execution_Platform = ['Mobile','1', '2', '3', '4', '5', '6'] #execution platform including mobile terminal and 6 ESs
SizeZip = dict(zip(Task_simulation,Size_of_Task))
Execution_Delay_on_ES = dict(zip(Task_simulation,
[
[9.47, 9.22, 11.58, 7.98, 7.72, 8.03],#
[6.12, 5.14, 8.52, 7.88, 4.26, 5.27],#
[5.88, 4.32, 6.31, 5.21, 2.94, 3.21],#
[8.59, 9.72, 15.44, 9.67, 8.35, 5.47],#
[3.66, 3.23, 4.02, 4.67, 3.21, 2.84] #
])) #executaion delay predicted by EPBN

sample1_list =[
[['streamcluster', 'Mobile', 2.96], ['bodytrack', '5', 6.314], ['vips', '6', 6.384], ['raytrace', '6', 6.284], ['X264', '2', 3.582]]

]
Sum=[]
for i in range(len(sample1_list)):
    sum=0
    for j in range(len(sample1_list[i])):
        task = sample1_list[i][j][0]
        Platform = Execution_Platform[random.randrange(len(Execution_Platform))]
        if Platform == 'Mobile':
            ExeDelay = (Require_CPU_cycles * SizeZip[task]) / (Freq_of_mobileCPU * 10)
        else:
            ExeDelay = round(Execution_Delay_on_ES[task][int(Platform) - 1] + (SizeZip[task] * 2 / Bandwidth))
        sample1_list[i][j][1]=Platform
        sample1_list[i][j][2]=ExeDelay
        sum=sum+sample1_list[i][j][2]
    Sum.append(sum)
