import operator
from functools import reduce

class Classifier:

    def __init__(self,trainedData):
        self.data = trainedData

    def getPriorProbability(self,className):
        return self.data.getClassCounter(className) / self.data.getNumOfClasses()

    def classify(self,newData):

        classCounts = self.data.getNumOfClasses()
        classes = self.data.getClasses()

        probabillityOfClasses = {}
        d = list(newData.split(','))

        for _class in classes:
            prob = [self.getValuePropability(val,_class) for val in d]

            try:
                tokenSetProb = reduce(lambda a,b: a*b, (i for i in prob if i) )
            except:
                tokenSetProb = 0

            probabillityOfClasses[_class] = tokenSetProb * self.getPriorProbability(_class)
        return sorted(probabillityOfClasses.items(),
            key=operator.itemgetter(1),
            reverse=True)

    def getValuePropability(self,value,className):

        numOfClass = self.data.getClassCounter(className)

        try:
            valueFrequency = self.data.getFrequency(value,className)
        except:
            return None

        if valueFrequency is None:
            return 0.00000001

        valueProbability = valueFrequency / numOfClass

        return valueProbability
