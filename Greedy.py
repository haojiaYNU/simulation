import random
import heapq
import copy

#parameter setting
Freq_of_mobileCPU = 1.8 #GHZ
Require_CPU_cycles = 100 #required CPU cycles
Bandwidth = 20 #MB/S
Task_simulation = ["streamcluster","bodytrack","vips","raytrace","X264"]
Size_of_Task = [0.74,10.27,15.87,4.07,1.76] #size(MB) corresponding to the task
Execution_Platform = ['Mobile', '1', '2', '3', '4', '5', '6']
SizeZip = dict(zip(Task_simulation,Size_of_Task))
Execution_Delay_on_ES = dict(zip(Task_simulation,
[
[9.47, 9.22, 11.58, 7.98, 7.72, 8.03],
[6.12, 5.14, 8.52, 7.88, 4.26, 5.27],
[5.88, 4.32, 6.31, 5.21, 2.94, 3.21],
[8.59, 9.72, 15.44, 9.67, 8.35, 5.47],
[3.66, 3.23, 4.02, 4.67, 3.21, 2.84]
])) #executaion delay predicted by EPBN

sample1_list = [
[['streamcluster', '4', 8.128], ['bodytrack', '1', 8.174], ['vips', '6', 6.384], ['raytrace', '6', 6.284], ['X264', '5', 3.562]]

    ]
delay = []

def Fit_Cal (Particle=[]):
    fit_cal =[]
    for i in range(len(Particle)):
        temp_sum = 0
        for j in range(5):
            temp_sum = Particle[i][j][2]+temp_sum
        fit_cal.insert(i,temp_sum)
    return fit_cal

for i in range(len(sample1_list)):
    temp_Platform = copy.deepcopy(Execution_Platform)
    for j in range(len(sample1_list[i])):
        task = sample1_list[i][j][0]
        temp = []
        Particle = []
        Exe = []
        for k in range(len(temp_Platform)):
            Platform = temp_Platform[k]
            if Platform == 'Mobile':
                ExeDelay = (Require_CPU_cycles * Size_of_Task[Task_simulation.index(task)]) / (
                            Freq_of_mobileCPU * 10)
            else:
                ExeDelay = Execution_Delay_on_ES[task][int(Platform) - 1] + \
                           (Size_of_Task[Task_simulation.index(task)] * 2 / Bandwidth)
            Particle.append([task, Platform, ExeDelay])
            Exe.append(ExeDelay)
        MinInd = Exe.index(min(Exe))
        sample1_list[i][j] = Particle[MinInd]
        DelInd = temp_Platform.index(Particle[MinInd][1])
        del temp_Platform[DelInd]

fit=Fit_Cal(sample1_list)