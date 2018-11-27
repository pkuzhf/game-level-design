import numpy as np
import random
import simulator
import ThreadClass

SIMULATE_PER_CHROMOSOME=2

'''
chromosome: 22-bit integer
'''
def decode(chromosome):
    matrix=[[1]*5 for i in range(5)]
    matrix[0][2]=matrix[0][4]=matrix[1][4]=0
    for i in range(5):
        for j in range(5):
            if matrix[i][j]==1:
                matrix[i][j]=chromosome&1
                chromosome>>=1
    for i in range(5):
        matrix[i]+=reversed(matrix[i][0:4])
    for i in range(3,-1,-1):
        matrix.append(matrix[i])
    def row2int(a):
        ret=0
        for i in range(9): ret+=a[i]<<i
        return ret
    ret=[]
    for i in range(3):
        tmp=0
        for j in range(3): tmp+=row2int(matrix[3*i+j])<<(9*j)
        ret.append(tmp)
    return ret

def valueFunc(result):
    len=result.json()[0]['loglength']
    return max(0,50-abs(len-50))

cache=simulator.cache(valueFunc)

'''
top 8
'''
players=[
    '5be824d7877e066ded50b599',
    '5be83afe877e066ded50bf8f',
    '5be5860b801a7b208e5d2044',
    '5be66298a421b05c5cfc0841',
    '5be7dc0e877e066ded509346',
    '5be65247a421b05c5cfc01a6',
    '5be5ded3801a7b208e5d541f',
    '5be65233a421b05c5cfc0198']

def getFitness(chromosome):
    def getAve(player,initData):
        ave,counter,total=cache.run(player,initData)
        return ave
    initData=decode(chromosome)
    ret=0
    threads=[]
    for i in range(SIMULATE_PER_CHROMOSOME):
        task=ThreadClass.MyThread(getAve,(random.sample(players,2),initData))
        task.start()
        threads.append(task)
    for task in threads:
        ret+=task.get_result()
    ret/=SIMULATE_PER_CHROMOSOME
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