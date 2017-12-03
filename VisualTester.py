import numpy as np
from game import Game
from NN import NeuralNet
import json

numLayers = int(input("# Layers:"))
nodesPerLayer = int(input("# Nodes:"))
forceValidMoves = (input("Force Valid Moves? ") == "Y");

filename = "NetProgress_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json"

population = []
with open(filename) as f:
    x = json.load(f)
    for y in x:
        population.append(NeuralNet(17, 4, numLayers, nodesPerLayer, y))

testing = population[0]

numMoves = 0
game = Game()
while True:
    #Pick the move with the highest rating (+1 is the bias)
    moveChoices = testing.run(game.getLogState()+[1])
    s = sorted(zip(moveChoices, [0,1,2,3]), reverse=True)
    moveChoices = [x[1] for x in s]

    print(game)

    input("")
    print("")

    #Play that move
    result = game.step(moveChoices[0])
    if result == -1:
        if(forceValidMoves):
            for z in range(1, len(moveChoices)):
                result = game.step(moveChoices[z])
                if result != -1:
                    break;
        else:
            print(game)
            print("FAIL SCORE:",-10+numMoves+(3*np.log2(np.amax(game.board))))
            break;
    if result == 0:
        print("NORMAL SCORE:",numMoves+(3*np.log2(np.amax(game.board))))
        break;
    numMoves+=1
