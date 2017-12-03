import numpy as np
from game import Game
from NN import NeuralNet
import json

forceValidMoves = (input("Force Valid Moves? ") == "Y");

def fitnessFunction(net, printBoard=False):
    numMoves = 0
    game = Game()
    while True:
        #Pick the move with the highest rating (+1 is the bias)
        moveChoices = net.run(game.getLogState()+[1])
        s = sorted(zip(moveChoices, [0,1,2,3]), reverse=True)
        moveChoices = [x[1] for x in s]

        #Play that move
        result = game.step(moveChoices[0])
        if result == -1:
            if(forceValidMoves):
                for z in range(1, len(moveChoices)):
                    result = game.step(moveChoices[z])
                    if result != -1:
                        break;
                    if z + 1 == len(moveChoices):
                        return -10+numMoves+(3*np.log2(np.amax(game.board)))
            else:
                if(printBoard):
                    print("Fail End")
                    print(game)
                return -10+numMoves+(3*np.log2(np.amax(game.board)))
        if result == 0:
            if(printBoard):
                print("Normal End")
                print(game)
            return numMoves+(3*np.log2(np.amax(game.board)))
        numMoves+=1

numGenerations = 50000
populationSize = 500
population = []

numLayers = int(input("# Layers:"))
nodesPerLayer = int(input("# Nodes:"))

maxEvolution = [];
avgEvolution = [];

#Tries to import the progress of existing neural net
try:
    filename = "NetProgress_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json"
    with open(filename) as f:
        x = json.load(f)
        for y in x:
            population.append(NeuralNet(17, 4, numLayers, nodesPerLayer, y))
    filename = "NetResults_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json";
    with open(filename) as f:
        x = json.load(f);
        maxEvolution = x['max'];
        avgEvolution = x['average'];
except IOError:
    print("Error occured on file import, using random population")

#Fill the rest of the population if we didn't get a full population
while len(population) < populationSize:
    population.append(NeuralNet(17, 4, numLayers, nodesPerLayer))

i=len(avgEvolution)

while True:
    fitnesses = []
    for j in population:
        fitnesses.append((fitnessFunction(j)+fitnessFunction(j))/2)
    s = sorted(zip(fitnesses, population), key=lambda k:k[0], reverse=True)
    fitnesses = [x[0] for x in s]
    avg = np.average(fitnesses)
    amax = np.amax(fitnesses)
    print("Average:", avg);
    print("Max:", amax)
    avgEvolution.append(avg);
    maxEvolution.append(amax);
    population = [x[1] for x in s]
    if((i+1) % 50 == 0):
        print(str(i+1)+"th Generation:")
        fitnessFunction(population[0], printBoard=True)

    for j in range(populationSize-1, -1, -1):
        if np.random.random() < (j / populationSize):
            population.pop(j)
    variationChance = (numGenerations/(5*i + numGenerations))
    population.append(NeuralNet(17, 4, numLayers, nodesPerLayer))
    population.append(NeuralNet(17, 4, numLayers, nodesPerLayer))
    while len(population) < populationSize:
        parent1 = population[np.random.randint(len(population))].getWeights()
        parent2 = population[np.random.randint(len(population))].getWeights()
        newWeights = []
        #Method 1: Choose a breaking point, combine both, and add small mutations
        #breakPoint = np.random.random()*len(parent1)*len(parent1[0]*len(parent1[0][0]))
        for j in range(0, len(parent1)):
            newWeights.append([])
            for k in range(0, len(parent1[j])):
                newWeights[j].append([])
                for x in range(0, len(parent1[j][k])):
                    #More Method 1:
                    """if(j*len(parent1)*len(parent1[j])+k*len(parent1[j])+x):
                        newWeights[j][k].append(parent1[j][k][x] + ((2*np.random.random()-1)**21) * variationChance)
                    else:
                        newWeights[j][k].append(parent2[j][k][x] + ((2*np.random.random()-1)**21) * variationChance)"""
                    #Method 2: random combination of weights
                    if np.random.random() < 0.5:
                        newWeights[j][k].append(parent1[j][k][x]*(variationChance*(3*(np.random.random()-0.5)**3)+1) + (0.3*(2*np.random.random()-1)**5) * variationChance**2)
                    else:
                        newWeights[j][k].append(parent2[j][k][x]*(variationChance*(3*(np.random.random()-0.5)**3)+1) + (0.3*(2*np.random.random()-1)**5) * variationChance**2)
                    #Method 3: Average all the weights (Bad, Don't use)
                    """average = (parent1[j][k][x] + parent2[j][k][x]) / 2
                    average *= 2*variationChance*(np.random.random()-0.5)**3+1
                    average += (np.random.random()*2-1)**21 * variationChance
                    newWeights[j][k].append(average)"""
        population.append(NeuralNet(17, 4, numLayers, nodesPerLayer, newWeights))
    if (i+1)%50 == 0:
        filename = "NetProgress_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json";
        writeWeights = []
        for j in population:
            writeWeights.append(j.getWeights())
        with open(filename,  "w+") as f:
            json.dump(writeWeights, f)
        filename = "NetResults_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json";
        with open(filename,  "w+") as f:
            json.dump({'average':avgEvolution, 'max':maxEvolution}, f)
        print("Progress Saved!")
    i+=1
