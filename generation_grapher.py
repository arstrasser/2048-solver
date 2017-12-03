import json
import numpy as np
from game import Game
from NN import NeuralNet
import matplotlib.pyplot as plt

numLayers = int(input("# Layers:"))
nodesPerLayer = int(input("# Nodes:"))

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

#Tries to import the progress of existing neural net
filename = "NetProgress_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json";
fitnesses = []
with open(filename) as f:
    x = json.load(f);
    for weights in x:
        net = NeuralNet(17, 4, numLayers, nodesPerLayer, weights)
        fitnesses.append(fitnessFunction(net))

plt.plot(sorted(fitnesses));
plt.show();
