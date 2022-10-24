import random
import enum
import math
from tokenize import Double
import numpy as np
import PerceptronRunner as pr

class Perceptron:
    def __init__(self, rangeIn, rangeOut, mi):
        self.mi = mi
        self.rangeOut = rangeOut
        self.rangeIn = rangeIn + 1
        self.weights = []
        self._generateRandomWeight()

    def _generateRandomWeight(self):
        for i in range(self.rangeOut):
            self.weights.append([])

            for j in range(self.rangeIn):
                self.weights[i].append(random.uniform(-0.3, 0.3))

    def _sigmoid(self, x):
        sig = 1 / (1 + math.exp(-x))

        return sig

    def learn(self, vectorIn, vectorOut):
        vectorIn = np.array([1] + vectorIn)
        vectorOut = np.array(vectorOut)
        newWeights = np.array(self.weights)
        out = []

        for i in range(vectorOut.size):
            out.append( self._sigmoid( np.sum( vectorIn * newWeights[i] ) ) )

        for i in range(vectorOut.size):
            newWeights[i] += self.mi * (vectorOut[i] - np.array(out[i])) * vectorIn
            
        self.weights = list(newWeights)

        return out

def main(argv):
    p = Perceptron(int(argv[1]), int(argv[2]), float(argv[3]))

    runner = pr.Balance()

    for e in range(1000):
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