import random
import heapq
import copy

#parameter setting
Prob_crossover = 0.4
Prob_mutation = 0.2
Initial_population = 100
Num_Particle_to_be_updated = 30
Num_iteration = 100
personal_iteration = 100
Freq_of_mobileCPU = 1.8 #GHZ
Require_CPU_cycles = 100 #required CPU cycles
Bandwidth = 20 #MB/S
Velocity = 3
Task_simulation = ["streamcluster","bodytrack","vips","raytrace","X264"]
Size_of_Task = [0.74,10.27,15.87,4.07,1.76] #size(MB) corresponding to the task
Execution_Platform = ['Mobile','1','2','3','4','5','6'] #execution platform including mobile terminal and 6 ESs ,'2','3','4','5','6'
#the delay predicted by EPBN, the benchmarks are "streamcluster","bodytrack","vips","raytrace","X264" respectively
Execution_Delay_on_ES = dict(zip(Task_simulation,
[
[9.47, 9.22, 11.58, 7.98, 7.72, 8.03], #
[6.12, 5.14, 8.52, 7.88, 4.26, 5.27], #
[5.88, 4.32, 6.31, 5.21, 2.94, 3.21], #
[8.59, 9.72, 15.44, 9.67, 8.35, 5.47], #
[3.66, 3.23, 4.02, 4.67, 3.21, 2.84] #
])) #executaion delay predicted by EPBN

#the initialization
def Initial (Initial_population=int):
    Ini = []
    for i in range(Initial_population):
        Particle = []
        for j in range(0, 5):
            index_task = j #random.randrange(len(Task_simulation))
            task = Task_simulation[index_task]  # task simulation
            index_platform = random.randrange(len(Execution_Platform))
            Platform = Execution_Platform[index_platform]  # platform selection
            if Platform == 'Mobile':
                ExeDelay = (Require_CPU_cycles * Size_of_Task[index_task]) / (Freq_of_mobileCPU * 10)
            else:
                ExeDelay = Execution_Delay_on_ES[task][int(Platform) - 1] + (Size_of_Task[index_task] * 2 / Bandwidth)
            Particle.append([task, Platform, ExeDelay])
        Ini.insert(i, Particle)
    return Ini

#the fitness calculation
def Fit_Cal (Particle=[]):
    fit_cal =[]
    for i in range(len(Particle)):
        temp_sum = 0
        for j in range(5):
            temp_sum = Particle[i][j][2]+temp_sum
        fit_cal.insert(i,temp_sum)
    return fit_cal

#Mutation
def Mutate(Particle = []):
    res = random.sample(range(0, len(Particle)), Velocity)
    for i in range(len(res)):
        ind_mut_particle = res[i] #find the particle
        ind_mut_task = random.randint(0,4) #find the location
        Mut_particle = Particle[ind_mut_particle][ind_mut_task]
        index_platform = random.randrange(len(Execution_Platform))
        Platform = Execution_Platform[index_platform]  # platform selection
        if Platform == 'Mobile':
            ExeDelay = (Require_CPU_cycles * Size_of_Task[Task_simulation.index(Mut_particle[0])]) / (Freq_of_mobileCPU * 10)
        else:
            ExeDelay = Execution_Delay_on_ES[Mut_particle[0]][int(Platform) - 1] +\
                   (Size_of_Task[Task_simulation.index(Mut_particle[0])] * 2 / Bandwidth)
        Mut_particle[1] = Platform
        Mut_particle[2] = ExeDelay
        Particle[ind_mut_particle][ind_mut_task] = Mut_particle
    return Particle

#calculate the personal and global best with the lowest execution delay
def P_G_best_Cal(Particle=[],personal_iteration=int):
    for i in range(personal_iteration):
        for j in range(len(Particle)):
            temp_delay = 0
            temp_particle = copy.deepcopy(Particle[j])
            ind = random.randrange(len(temp_particle))
            task = temp_particle[ind][0]
            Platform = Execution_Platform[random.randrange(len(Execution_Platform))]
            if Platform == 'Mobile':
                ExeDelay = (Require_CPU_cycles * Size_of_Task[Task_simulation.index(task)]) / (Freq_of_mobileCPU * 10)
            else:
                ExeDelay = Execution_Delay_on_ES[task][int(Platform) - 1] + \
                           (Size_of_Task[Task_simulation.index(task)] * 2 / Bandwidth)
            temp_particle[ind][1] = Platform
            temp_particle[ind][2] = ExeDelay
            for k in range(len(temp_particle)):
                temp_delay = temp_delay + temp_particle[k][2]
            if temp_delay < Fit_Cal(Particle)[j]:
                Fit_Cal(Particle)[j] = copy.deepcopy(temp_delay)
                Particle[j] = copy.deepcopy(temp_particle)
    p_best = Particle
    g_best_index = Fit_Cal(Particle).index(min(Fit_Cal(Particle)))
    g_best = Particle[g_best_index]
    return p_best, g_best

#Crossover with the personal and global best
def Crossover(Particle = [],personal_iteration=int,Velocity=int):
    res = random.sample(range(0, len(Particle)), Velocity)
    p_best, g_best = P_G_best_Cal(Particle,personal_iteration)
    Particle[res[0]] = p_best [res[0]]
    Particle[res[1]] = p_best [res[1]]
    Particle[res[2]] = g_best
    return Particle

def main():
    Ini = Initial(Initial_population) #Initialization
    #select the updated particles from initial set
    Particle_to_be_updated = []
    S = sorted(enumerate(Fit_Cal (Ini)),key=lambda x:x[1]) [:Num_Particle_to_be_updated] #select the updated particles
    S_indice = [i[0] for i in S]
    for i in S_indice:
        Particle_to_be_updated.append(Ini[i])
    for j in range(Num_iteration):
        if random.random() > Prob_mutation:
            Particle_to_be_updated = Mutate(Particle_to_be_updated)
            break
        if random.random() > Prob_crossover:
            Particle_to_be_updated = Crossover(Particle_to_be_updated,personal_iteration,Velocity)
            break
    g_best_index = Fit_Cal(Particle_to_be_updated).index(min(Fit_Cal(Particle_to_be_updated)))
    g_best = Particle_to_be_updated[g_best_index]
    delay = min(Fit_Cal(Particle_to_be_updated))
    return g_best, delay