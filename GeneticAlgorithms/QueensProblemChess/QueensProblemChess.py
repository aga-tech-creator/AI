from operator import attrgetter
import random
import math
import copy

class NQueens:
    def __init__(self, n, gene = None):
        self.sizeOfGene = n
        self.fitness = 0
        self.children = []
        self.possibleAlleles = []

        if gene is None:
            self.gene = []

            for i in range(n):
                self.possibleAlleles.append(i + 1)

            for i in range(n):
                # It randomly removes possible alleles at the same time as they are added in gene.
                self.gene.append(self.possibleAlleles.pop(random.randint(0, n - (i + 1))))
        else:
            self.gene = gene

    def getChildren(self, partner):
        genesOfChildren = []
        half = random.randint(0, self.sizeOfGene - 1) # Determining the randonly slice. 
    
        genesOfChildren.append(self.gene[0:half] + partner.gene[half:partner.sizeOfGene])
        genesOfChildren.append(partner.gene[0:half] + self.gene[half:self.sizeOfGene])
        # Merging the two lists.

        allelesToC1 = []
        allelesToC2 = []
        # Creating a list for the missing alleles for each child.

        # Checking which alleles are missing and adding to the list of missing alleles.
        j = half
        while j < self.sizeOfGene:
            if genesOfChildren[0][j] in genesOfChildren[0][0:half]:
                allelesToC2.append(genesOfChildren[0][j])
                genesOfChildren[0][j] = -1
            
            if genesOfChildren[1][j] in genesOfChildren[1][0:half]:
                allelesToC1.append(genesOfChildren[1][j])
                genesOfChildren[1][j] = -1

            j += 1

        # Randomizing the locus of missing alleles.
        random.shuffle(allelesToC1)
        random.shuffle(allelesToC2)

        # Placing the missing alleles at the repeated alleles in the children.

        for i in range(len(allelesToC1)):
            index = genesOfChildren[0].index(-1)
            genesOfChildren[0][index] = allelesToC1[i]

        for i in range(len(allelesToC2)):
            index = genesOfChildren[1].index(-1)
            genesOfChildren[1][index] = allelesToC2[i]

        self.children.append(NQueens(self.sizeOfGene, genesOfChildren[0]))
        self.children.append(NQueens(self.sizeOfGene, genesOfChildren[1]))

        return self.children

class GameOfQueens:
    def __init__(self, amountOfQueens, sizeOfChromossome, isMin):
        self.amountOfElitists = math.floor((amountOfQueens / 5))
        self.isMin = isMin
        self.amountOfQueens = amountOfQueens
        self.sizeOfChromossome = sizeOfChromossome
        self.popIni = []
        
        for i in range(self.amountOfQueens):
            self.popIni.append(self.generateIndividuals(self.sizeOfChromossome))

    def start(self, generations):
        actualGeneration = 0
        newPop = self.popIni
        perfectIndividual = None
        mutants = []
        popChildren = []
        elitists = []

        for i in range(generations):
            actualGeneration = i
            popCopied = newPop.copy()

            # Crossing parents.
            while len(popCopied) > 1:
                firstParent = popCopied.pop(random.randint(0, len(popCopied)-1))
                secondParent = popCopied.pop(random.randint(0, len(popCopied)-1))

                generatedChildren = firstParent.getChildren(secondParent)
                popChildren.append(generatedChildren[0])
                popChildren.append(generatedChildren[1])
            
            self._mutation(newPop, mutants)

            totalPop = newPop + popChildren + mutants

            perfectIndividual = self.fitness(totalPop)
            
            if perfectIndividual != None:
                break

            elitists = self.elitism(totalPop)

            newPop = self.selectInd(totalPop)

            newPop += elitists
            mutants = []
            popChildren = []
            elitists = []

        return (perfectIndividual, actualGeneration)

    def generateIndividuals(self, n):
        return NQueens(n)

    def fitness(self, pop):
        perfectIndividual = None

        k = 0
        while k < len(pop):

            n = len(pop[k].gene)
            j = 0

            for i in range(n):
                j = i + 1

                while j < n:
                    if (int(math.fabs((pop[k].gene[i] - pop[k].gene[j]))) == (j -i)):
                        pop[k].fitness += 1
                    
                    j += 1

            if pop[k].fitness == 0:
                perfectIndividual = pop[k]
                break

            if self.isMin == True:
                pop[k].fitness = 1 / pop[k].fitness

            k += 1

        return perfectIndividual

    def _mutation(self, pop, mutants):
        for i in range(len(pop)):
            commonInd = copy.copy(pop[i])
            pos1 = random.randint(0, self.sizeOfChromossome - 1)
            pos2 = random.randint(0, self.sizeOfChromossome - 1)
            allele1 = commonInd.gene[pos1]
            allele2 = commonInd.gene[pos2]

            while allele1 == allele2:
                pos1 = random.randint(0, self.sizeOfChromossome - 1)
                allele1 = commonInd.gene[pos1]

            commonInd.gene[pos1] = allele2
            commonInd.gene[pos2] = allele1
            
            mutants.append(commonInd)

    def elitism(self, pop):
        elitists = []
        popCopied = pop.copy()
        popCopied.sort( key=attrgetter('fitness') )

        for i in range(self.amountOfElitists):
            elitists.append(popCopied.pop())

        return elitists

    def roullete(self, pop):
        sum = 0

        for i in range(len(pop)):
            sum += pop[i].fitness

        if self.isMin == True:
            breakPoint = random.uniform(0.0, sum)
        else:
            breakPoint = random.randint(0, sum)

        i = 0
        aux = pop[i].fitness
        while i < len(pop) and aux < breakPoint:
            aux += pop[i].fitness
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
    game = GameOfQueens(30, 7, True)
    perfectIndividual = game.start(900)
    if perfectIndividual[0] == None:
        print("Insuficient generations to find the perfect individual.")
    else:        
        print(perfectIndividual[0].gene)
        print(perfectIndividual[1])

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))