import numpy as np
import random
import simulator


SIMULATE_PER_CHROMOSOME=1

cache=simulator.cache(lambda *vartuple:1)

players=[
    '5be824d7877e066ded50b599',
    '5be66437a421b05c5cfc08db',
    '5be833ed877e066ded50bce6',
    '5be65729a421b05c5cfc043c',
    '5bdd9678e5446d17d00b06e9',
    '5be66298a421b05c5cfc0841',
    '5be66151a421b05c5cfc07a3',
    '5be0532ce5446d17d00ce073']

'''
chromosome: 25-bit integer
'''
def decode(chromosome):
    return [74600491, 31718972, 111170161]

def getFitness(chromosome):
    def getAve(player,initData):
        result,cur,ave,counter,total=cache.run(player,initData)
        return ave
    initData=decode(chromosome)
    ret=np.mean([getAve(random.sample(players,2),initData)  for i in range(SIMULATE_PER_CHROMOSOME)])
    return ret

def selectMatingPool(populations,fitnesses,num_parents):
    index=np.argsort(-fitnesses)
    parents=np.array([populations[idx] for idx in index[0:num_parents]])
    return parents

def crossover(parents,offspring_size,GENE_PER_CHROMOSOME):
    crossoverPoint=GENE_PER_CHROMOSOME//2
    mask1=(1<<crossoverPoint)-1
    mask2=((1<<GENE_PER_CHROMOSOME)-1)^mask1
    nParents=parents.shape[0]
    mating=lambda a,b:(a&mask1)|(b&mask2)
    offspring=np.array([mating(parents[k],parents[(k+1)%nParents])
        for k in range(offspring_size)])
    return offspring

def mutation(offspring,GENE_PER_CHROMOSOME):
    nOffspring=offspring.shape[0]
    delta=[1<<random.randrange(GENE_PER_CHROMOSOME) for i in range(nOffspring)]
    offspring=offspring^delta
    return offspring
