import matplotlib.pyplot as plt
import json

numLayers = int(input("# Layers:"))
nodesPerLayer = int(input("# Nodes:"))
forceValidMoves = (input("Force Valid Moves? ") == "Y");

maxEvolution = [];
avgEvolution = [];

#Tries to import the progress of existing neural net
filename = "NetResults_"+str(numLayers)+"x"+str(nodesPerLayer)+"_"+str(forceValidMoves)+".json";
with open(filename) as f:
    x = json.load(f);
    maxEvolution = x['max'];
    avgEvolution = x['average'];

plt.plot(avgEvolution[0:10000]);
plt.plot(maxEvolution[0:10000]);
plt.show();
