import simulator
import GA
import numpy as np
import ThreadClass
import time

MATING_POOL_SIZE=2
POPULATION_SIZE=4
GENE_PER_CHROMOSOME=22

def output(populations,fitness,outstr):
    outstr="data/"+outstr
    outfile=open(outstr,"w")
    for i in range(POPULATION_SIZE):
        outfile.write("%d %d\n"%(populations[i],fitness[i]))
    outfile.write("average: %f\n"%(np.mean(fitness)))
    outfile.write("maximum: %d\n"%(np.max(fitness)))
    outfile.close()

def GF(populations):
    threads=[]
    for x in populations:
        task=ThreadClass.MyThread(GA.getFitness,(x,))
        task.start()
        threads.append(task)
    ret=[task.get_result() for task in threads]
    return np.array(ret)

print("Please input the number of generation:")
NUM_OF_GENERATION=int(input())
print("Please input the latest version:")
try:
    instr=input()
    infile=open("data/"+instr,"r")
    populations=np.array([int(input()) for i in range(POPULATION_SIZE)])
    fitness=np.array([int(input()) for i in range(POPULATION_SIZE)])
except:
    print("No such file!")
    print("Just generate the population randomly!")
    populations=np.random.randint((1<<25)-1,size=POPULATION_SIZE)
    fitness=GF(populations)

output(populations,fitness,"version"+"-init"+".txt")
print(populations)
print(fitness)
print("average:",np.mean(fitness))
print("maximum:",np.max(fitness))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print("===================================================")

for generation in range(NUM_OF_GENERATION):
    print("Generation : ",generation)
    parents=GA.selectMatingPool(populations,fitness,MATING_POOL_SIZE)
    nParents=parents.shape[0]
    offspring=GA.crossover(parents,POPULATION_SIZE-nParents,
        GENE_PER_CHROMOSOME)
    offspring=GA.mutation(offspring,GENE_PER_CHROMOSOME)
    populations=np.append(parents,offspring)
    fitness=GF(populations)
    output(populations,fitness,"version"+str(generation)+".txt")
    print(populations)
    print(fitness)
    print("average:",np.mean(fitness))
    print("maximum:",np.max(fitness))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print("===================================================")
