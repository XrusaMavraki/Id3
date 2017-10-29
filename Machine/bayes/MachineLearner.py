from Data import Data


class MachineLearner(object):

    def __init__(self):
        self.data = Data()

    def Learn(self,value,className):
        self.data.increaseClass(className)
        for val in value:
             self.data.increaseValues(val,className)
