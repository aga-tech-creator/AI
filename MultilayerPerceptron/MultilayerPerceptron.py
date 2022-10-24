import random
import enum
import math
from tokenize import Double
import numpy as np
import PerceptronRunnerLogicPortsData as prLogicPortsData
import PerceptronRunnerBalanceData as prBalanceData

class MultilayerPerceptron:
    def __init__(self, sampleRange, amountOfNeuronInterm, arrayTeta, mi):
        self.amountOfNeuronInterm = amountOfNeuronInterm
        self.arrayTeta = arrayTeta
        self.mi = mi
        self.sampleRange = sampleRange
        self.intermWeights = []
        self.outputWeights = []
        self._generateRandomOutputWeights()
        self._generateRandomIntermWeights()

    def _generateRandomIntermWeights(self):
        for i in range(self.sampleRange + 1):
            self.intermWeights.append([])

            for j in range(self.amountOfNeuronInterm):
                self.intermWeights[i].append(random.uniform(-0.3, 0.3))

    def _generateRandomOutputWeights(self):
        for i in range(self.amountOfNeuronInterm + 1):
            self.outputWeights.append([])

            for j in range(self.arrayTeta):
                self.outputWeights[i].append(random.uniform(-0.3, 0.3))

    def _sigmoid(self, x):
        sig = 1 / (1 + math.exp(-x))

        return sig

    def learn(self, vectorIn, vectorOut):
        vectorIn += [1]
        vectorHidden = []

        for j in range(self.amountOfNeuronInterm):
            sum = 0
            for i in range(self.sampleRange + 1):
                sum += vectorIn[i] * self.intermWeights[i][j]
            
            vectorHidden.append(self._sigmoid(sum))

        vectorHidden.append(1)

        teta = []
        for j in range(len(vectorOut)):
            sum = 0
            for i in range(len(vectorHidden)):
                sum += vectorHidden[i] * self.outputWeights[i][j]

            teta.append(self._sigmoid(sum))

        deltaTeta = []

        for j in range(len(vectorOut)):
            deltaTeta.append(teta[j] * (1 - teta[j]) * (vectorOut[j] - teta[j]))

        deltaHidden = []
        
        for j in range(self.amountOfNeuronInterm + 1):
            sum = 0
            for i in range(len(vectorOut)):
                sum += deltaTeta[i] * self.outputWeights[j][i]

            deltaHidden.append(vectorHidden[j] * (1 - vectorHidden[j]) * sum)

        for j in range(self.sampleRange + 1):
            for i in range(self.amountOfNeuronInterm):
                self.intermWeights[j][i] += self.mi * deltaHidden[i] * vectorIn[j]

        for j in range(self.amountOfNeuronInterm + 1):
            for i in range(self.arrayTeta):
                self.outputWeights[j][i] += self.mi * deltaTeta[i] * vectorHidden[j]

        return teta

class Data(enum.Enum):
    And = 1
    Or = 2
    Xor = 3
    Robot = 4
    Balance = 5

def main(argv):
    """
    argv[1] = Amount of sample / argv[2] = Amount of intermediate neurons /
    argv[3] = Amount of output neurons / argv[3] = mi / argv[5] = Defines which database
    will use
    """ 
    p = MultilayerPerceptron(int(argv[1]), int(argv[2]), int(argv[3]), float(argv[4]))
   
    if(int(argv[5]) == Data.And.value):
        runner = prLogicPortsData.And
    elif(int(argv[5]) == Data.Or.value):
        runner = prLogicPortsData.Or
    elif(int(argv[5]) == Data.Xor.value):
        runner = prLogicPortsData.Xor
    elif(int(argv[5]) == Data.Robot.value):
        runner = prLogicPortsData.Robot
    elif(int(argv[5]) == Data.Balance.value):
        runner = prBalanceData.Balance()

    for e in range(10000):
        ageError = 0.0

        for a in range(len(runner.baseE)):
            x = runner.baseE[a][0]
            y = runner.baseE[a][1]
            
            out = p.learn(x, y)
            sampleError = np.sum(np.fabs(np.array(y) - np.array(out)))
            ageError += sampleError

        print(f"Age: {e} - error: {ageError}")

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))