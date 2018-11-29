import simulator
import GA
import numpy as np
import ThreadClass
import time
import datetime

MATING_POOL_SIZE=5
POPULATION_SIZE=20
GENE_PER_CHROMOSOME=22
NUM_OF_GENERATION=10

def output(populations,fitness,outstr):
    oldtime=datetime.datetime.now()
    outstr="data/"+outstr
    outfile=open(outstr,"w")
    for i in range(POPULATION_SIZE):
        outfile.write("%d %d\n"%(populations[i],fitness[i]))
    outfile.write("average: %f\n"%(np.mean(fitness)))
    outfile.write("maximum: %d\n"%(np.max(fitness)))
    outfile.close()
    curtime=datetime.datetime.now()
    print("duration: %d mins %d seconds"%((curtime-oldtime).seconds//60,(curtime-oldtime).seconds%60))

def GF(populations):
    # threads=[]
    # for x in populations:
    #     task=ThreadClass.MyThread(GA.getFitness,(x,))
    #     task.start()
    #     threads.append(task)
    # ret=[task.get_result() for task in threads]
    # return np.array(ret)
    return np.array([GA.getFitness(x) for x in populations])

try:
    instr="version-init.txt"
    infile=open("data/"+instr,"r")
    populations,fitness=[],[]
    for i in range(POPULATION_SIZE):
        line=infile.readline().split()
        print(line)
        populations.append(int(line[0]))
        fitness.append(int(line[1]))
    populations=np.array(populations)
    fitness=np.array(fitness)
except:
    print("No such file!")
    print("Just generate the population randomly!")
    populations=np.random.randint((1<<GENE_PER_CHROMOSOME)-1,size=POPULATION_SIZE)
    fitness=GF(populations)
    output(populations,fitness,"version-init.txt")
finally:
    infile.close()

print(populations)
print(fitness)
print("average: ",np.mean(fitness))
print("maximum: ",np.max(fitness))
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
