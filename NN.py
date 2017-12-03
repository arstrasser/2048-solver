import numpy as np
from scipy.special import expit

np.random.seed(123456)

def sigmoid(val, d=False):
    if(d):
        return sigmoid(val)*(1 - sigmoid(val))
    return  expit(val)#1 / (1 + np.exp(-val))

class Neuron:
    def __init__(self, numInputs, weights=None):
        self.weights = []
        for i in range(0, numInputs):
            if weights != None:
                self.weights.append(weights[i])
            else:
                self.weights.append(np.random.random()*2 - 1)
    def getOutput(self, inputs):
        output = 0.0
        for i in range(0, len(inputs)):
            output += float(inputs[i])*self.weights[i]
        return sigmoid(output)
    def __float__(self):
        return self.getOutput()

class NeuralNet:
    def __init__(self, numInputs, numOutputs, numHiddenLayers, numHiddenNodesPerLayer, weights=None):
        self.neurons = []
        for i in range(0, numHiddenLayers):
            self.neurons.append([])
            for j in range(0, numHiddenNodesPerLayer):
                if i == 0:
                    num = numInputs
                else:
                    num = numHiddenNodesPerLayer
                if weights != None:
                    self.neurons[i].append(Neuron(num, weights[i][j]))
                else:
                    self.neurons[i].append(Neuron(num))
        self.neurons.append([])
        i = len(self.neurons)-1
        for j in range(0, numOutputs):
            if weights != None:
                self.neurons[i].append(Neuron(numHiddenNodesPerLayer, weights[i][j]))
            else:
                self.neurons[i].append(Neuron(numHiddenNodesPerLayer))
    def getWeights(self):
        weights = []
        for i in self.neurons:
            curColumn = []
            for j in i:
                curColumn.append(j.weights)
            weights.append(curColumn)
        return weights
    def run(self, inputs):
        values = [inputs]
        for i in range(0, len(self.neurons)):
            theseValues = []
            for j in range(0, len(self.neurons[i])):
                theseValues.append(self.neurons[i][j].getOutput(values[i]))
            values.append(theseValues)
        return values[len(values)-1]
