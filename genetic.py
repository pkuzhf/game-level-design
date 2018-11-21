import simulator
import GA
import numpy as np

MATING_POOL_SIZE=2
POPULATION_SIZE=4
GENE_PER_CHROMOSOME=25
NUM_OF_GENERATION=5


populations=np.random.randint((1<<25)-1,size=POPULATION_SIZE)
fitnesses=np.array([GA.getFitness(x) for x in populations])
print(populations)
print("Initial result:",np.max(fitnesses))
print("===================================================")

for generation in range(NUM_OF_GENERATION):
    print("Generation : ",generation)
    parents=GA.selectMatingPool(populations,fitnesses,MATING_POOL_SIZE)
    nParents=parents.shape[0]
    offspring=GA.crossover(parents,POPULATION_SIZE-nParents,
        GENE_PER_CHROMOSOME)
    offspring=GA.mutation(offspring,GENE_PER_CHROMOSOME)
    populations=np.append(parents,offspring)
    fitnesses=np.array([GA.getFitness(x) for x in populations])
    print(populations)
    print("current result:",np.max(fitnesses))
    print("===================================================")
    