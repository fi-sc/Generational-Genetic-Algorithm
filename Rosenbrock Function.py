#generational genetic algorithm
#formula 1 assignment

import random
import copy
import matplotlib.pyplot as plt
import numpy as np

N=20 #genome
P=100#population
generations = 900
MUTRATE = 0.1 #probability
MUTSTEP = 1#step size 
MIN = -100 #x
MAX = 100 #x

#multipoint crossover implemented
crosspoint = [5,12] 

population = []
offspring= [] 

#for graph
best = []    
mean = []

#initialisation class for arrays
class individual:
    def __init__(self):
        self.gene = [0] * N
        self.fitness = 0
        

#random sample between -100 and 100
for x in range (0, P):
    tempgene=[]
    for y in range (0, N):
        tempgene.append(random.uniform(MIN,MAX))
    newind = individual()
    newind.gene = tempgene.copy()
    population.append(newind)


#fitness function of function 1
def test_function(ind):
    utility = 0
    for i in range(N-1):
        utility += (100 * (ind.gene[i+1] - ind.gene[i] ** 2)**2 + (1 - ind.gene[i])** 2) #running sum
    return utility

for i in range(0,P):
    population[i].fitness = test_function(population[i]) #sends each gene to the test_function and returns the fitness


#loop of generation
for gen in range(0,generations): 
    offspring.clear() # clears the list at start of every generation

    #tournament selection
    off1 = []
    off2 = []
    for i in range(0,P):
        parent1 = random.randint(0,P-1)
        off1 = copy.deepcopy(population[parent1])
        parent2 = random.randint(0, P-1)
        off2 = copy.deepcopy(population[parent2])
        if off1.fitness < off2.fitness: # < for minimisation
            offspring.append(off1)
        else:
            offspring.append(off2)
    
    
    #mutipoint point crossover
    toff1 = individual()
    toff2 = individual()
    temp = individual()
    for i in range(0,P,2): #splits offspring into 2 arrays
        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i+1])
        temp = copy.deepcopy(offspring[i])
        for x in crosspoint: #loops through crossover array
            for j in range (x,N):
                toff1.gene[j] = toff2.gene[j]
                toff2.gene[j] = temp.gene[j]
            offspring[i] = copy.deepcopy(toff1)
            offspring[i+1] = copy.deepcopy(toff2)


    #mutation
    for i in range(0,P):
        newind = individual()
        newind.gene = []
        for j in range(0,N):
            gene = offspring[i].gene[j]
            mutprob = random.random()
            if mutprob < MUTRATE: # add or remove a small random number 
                alter = random.uniform(-MUTSTEP,MUTSTEP)
                gene = gene + alter
                if gene > MAX: 
                    gene = MAX
                if gene < MIN: 
                    gene = MIN
            newind.gene.append(gene)


        offspring[i] = copy.deepcopy(newind)#copies data


    #fitness function 
    for i in range(0,P):
        offspring[i].fitness = test_function(offspring[i]) #sends each gene to the test_function and returns the fitness
    
    #elitism
    population_sorted = sorted(population, key = lambda f:f.fitness) #sorts population
    offspring = sorted(offspring, key = lambda f:-f.fitness)  #sorts offspring
    topNum = population_sorted[0].fitness #gets best fitness (lowest) from populaton
    offspring[0].fitness = topNum #appends lowest fitness to highest in offspring


    #mean fitness
    population = copy.deepcopy(offspring)
    total = 0
    for i in range(0,P):
        total+=population[i].fitness
    mean.append(total/P) #add all and divie by total

    bestfit = population[0].fitness
    
    #best fitness 
    for i in range(1,P):
        if population[i].fitness < bestfit: # < to find smallest fitness
            bestfit = population[i].fitness
    best.append(bestfit)

#for testing and result purposes
#print("Final Result: ")
#print(bestfit)
#print("All Mean: ")
#print(mean)

#for graph
plt.title("Algorithm 1 Minimisation")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.plot(best)
plt.plot(mean)
plt.legend(['Best','Mean'])
plt.show()












    

