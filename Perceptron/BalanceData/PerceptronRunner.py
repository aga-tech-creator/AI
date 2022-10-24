class Balance:
    def __init__(self):
        self.baseE = []
        self.digestDataBase()

    def digestDataBase(self):
        archiveBuffer = open("balance-scale.data", "r")
        archiveContent = archiveBuffer.read()
        archiveContent = archiveContent.replace("\n", ",")
        archiveContent = archiveContent.split(",")
        count = 0
        indexBaseE = 0
        
        for i in range(len(archiveContent) - 1):
            if count == 5: 
                count = 0
                indexBaseE += 1

            if count == 0: self.baseE.append([[]])

            if(archiveContent[i] == 'R'):
                self.baseE[indexBaseE].append([0, 0, 1])
            elif(archiveContent[i] == 'B'):
                self.baseE[indexBaseE].append([0, 1, 0])
            elif(archiveContent[i] == 'L'):
                self.baseE[indexBaseE].append([1, 0, 0])
            else:
                self.baseE[indexBaseE][0].append(int(archiveContent[i]))

            count += 1