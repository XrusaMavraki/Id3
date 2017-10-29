
class Data:

    # Initialize everything we need to save the data
    def __init__(self):
        self.numOfClasses = {}
        self.frequencies = {}

    # Increase the number of a given class by 1.
    def increaseClass(self,className):
        self.numOfClasses[className] = self.numOfClasses.get(className,0) + 1

    # Increase the number of given values according to it's class by 1
    def increaseValues(self,value,className):
        if not value in self.frequencies:
            self.frequencies[value] = {}

        self.frequencies[value][className] = self.frequencies[value].get(className,0) + 1

    # Return the sum of all class that exist inside the docCountClass.
    def getNumOfClasses(self):
        return sum(self.numOfClasses.values())

    # Return all the keys of the dictionary DocCountClass.For example if we are having
    # having two classes A and B the function returns {[A,B]} where A and B are the name of the classes.
    def getClasses(self):
        return self.numOfClasses.keys()

    def getClassCounter(self, className):
        return self.numOfClasses.get(className,None)

    def getFrequency(self,value,className):
        try:
            return self.frequencies[value][className]
        except:
            return None
