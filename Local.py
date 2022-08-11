import random
import heapq
import copy

#parameter setting
Freq_of_mobileCPU = 1.8 #GHZ
Require_CPU_cycles = 100 #required CPU cycles
Task_simulation = ["streamcluster","bodytrack","vips","raytrace","X264"]
Size_of_Task = [0.74,10.27,15.87,4.07,1.76] #size(MB) corresponding to the task
Execution_Platform = 'Mobile' #execution platform including mobile terminal and 6 ESs
size = 0
for i in range(5):
    index_task = random.randrange(len(Task_simulation))
    task = Task_simulation[index_task]
    size = size + Size_of_Task[index_task]
ExeDelay = (Require_CPU_cycles * size) / (Freq_of_mobileCPU * 10)




