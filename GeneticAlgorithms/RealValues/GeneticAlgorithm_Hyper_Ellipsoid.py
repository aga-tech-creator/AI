from operator import attrgetter
import random
import math
import copy

class NQueens:
    def __init__(self, dimension, gene = None):
        self.dimension = dimension
        self.realFitness = 0
        self.falseFitness = 0
        self.children = []

        if gene is None:
            self.gene = []

            for i in range(dimension):
                self.gene.append(random.uniform(-65.536, 65.536))
        else:
            self.gene = gene

    def getChildren(self, partner):
        self.children = []
        self.children.append(NQueens(self.dimension, gene=[]))
        self.children.append(NQueens(self.dimension, gene=[]))

        j = 0
        while j < self.dimension:
            # | P1i - P2i |
            x = math.fabs(self.gene[j] - partner.gene[j])

            value = self.gene[j] + (random.gauss(0, 0.25) * x)
            if value < -65.536:
                self.children[0].gene.append(-65.536)
            elif value > 65.536:
                self.children[0].gene.append(65.536)
            else:
                self.children[0].gene.append(value)

            value = self.gene[j] + (random.gauss(0, 0.25) * x)
            if value < -65.536:
                self.children[1].gene.append(-65.536)
            elif value > 65.536:
                self.children[1].gene.append(65.536)
            else:
                self.children[1].gene.append(value)

            j += 1

        return self.children

class GameOfQueens:
    def __init__(self, amountOfQueens, dimension, isMin):
        self.amountOfElitists = math.floor((amountOfQueens / 5))
        self.isMin = isMin
        self.amountOfQueens = amountOfQueens
        self.dimension = dimension
        self.popIni = []
        
        for i in range(self.amountOfQueens):
            self.popIni.append(self.generateIndividual(self.dimension))

    def start(self, generations):
        newPop = self.popIni
        perfectIndividual = None
        mutants = []
        popChildren = []
        elitists = []

        for i in range(generations):
            popCopied = newPop.copy()

            # Crossing parents.
            while len(popCopied) > 1:
                firstParent = popCopied.pop(random.randint(0, len(popCopied)-1))
                secondParent = popCopied.pop(random.randint(0, len(popCopied)-1))

                generatedChildren = firstParent.getChildren(secondParent)
                popChildren.append(generatedChildren[0])
                popChildren.append(generatedChildren[1])
                generatedChildren = []
            
            self._mutation(newPop, mutants)

            totalPop = newPop + popChildren + mutants

            self.fitness(totalPop)
            
            elitists = self.elitism(totalPop)

            newPop = self.selectInd(totalPop)

            newPop += elitists
            mutants = []
            popChildren = []
            elitists = []

        perfectIndividual = newPop[len(newPop) - 1]

        return perfectIndividual

    def generateIndividual(self, n):
        return NQueens(n)

    def fitness(self, pop):
        k = 0
        while k < len(pop):
            sum = 0

            for i in range(self.dimension):
                for j in range(i):
                    sum +=  math.pow(pop[k].gene[j], 2)

            fitness = sum

            pop[k].realFitness = fitness
            pop[k].falseFitness = 1 / fitness

            k += 1

    def _mutation(self, pop, mutants):
        selected = 0

        for i in range(len(pop)):
            ind = copy.copy(pop[i])

            for j in range(len(ind.gene)):
                if random.uniform(0, 1) < 0.1:
                    ind.gene[j] += random.gauss(0, 1)
                    selected += 1

            if selected == 0:
                index = random.randint(0, len(ind.gene) - 1)
                ind.gene[index] += random.gauss(0, 1)
            
            mutants.append(ind)

    def elitism(self, pop):
        elitists = []
        pop.sort( key=attrgetter('falseFitness') )

        i = len(pop) - 1
        while i > len(pop) - self.amountOfElitists - 1:
            elitists.append(pop[i])
            i -= 1

        return elitists

    def roullete(self, pop):
        sum = 0

        for i in range(len(pop)):
            sum += pop[i].falseFitness

        breakPoint = random.uniform(0.0, sum)

        i = 0
        aux = pop[i].falseFitness
        while i < len(pop) and aux < breakPoint:
            aux += pop[i].falseFitness
            i += 1
        
        return pop[i - 1]

    def selectInd(self, totalPop):
        selectedPop = []
        n = self.amountOfQueens - self.amountOfElitists

        for i in range(n):
            selectedPop.append(self.roullete(totalPop))
            totalPop.pop()

        return selectedPop

def main(argv):
    game = GameOfQueens(30, 3, True)
    perfectIndividual = game.start(1000)
    if perfectIndividual == None:
        print("Insuficient generations to find the perfect individual.")
    else:        
        print(perfectIndividual.gene)
        print(f'Fitness: {perfectIndividual.realFitness}')

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))