from Data import Data
from MachineLearner import MachineLearner
from Parser import Parser
from Classifier import Classifier
from split_script import *

read()

def getValueList(dataset):
    set = ""
    ff = []
    for x in range(0,len(dataset)):
        for y in range(0,4):
            if(y == 3):
                set += dataset[x][y]
            else:
                set += dataset[x][y] + ","
        ff.append(set)
        set = ""
    return ff

parserer = Parser()

# Main sequence

# Print instructions and import the dataset
print(open("information.info").read())

# file = input("Input DataSet path: ")
train_file = "iris_train.data"
listofData = parserer.read(train_file)
print("Training dataset: " + train_file + " imported\n")

test_file = "iris_test.data"
testData = parserer.read(test_file)
print("Training dataset: " + test_file + " imported\n")

machine1 = MachineLearner()
machine2 = MachineLearner()
parserer = Parser()

for x in range(0,len(listofData)):
    machine1.Learn(listofData[x],listofData[x][4])

for x in range(0,len(testData)):
    machine2.Learn(testData[x],testData[x][4])

c1 = Classifier(machine1.data)
c2 = Classifier(machine2.data)


maxClass = []
classifiedData = []
count = 0
for x in getValueList(testData):
    d = c1.classify(x)
    maxClass.append(d[0][0])

count = 0
for x in range(0,len(testData)):
    if(testData[x][4] == maxClass[x]): count = count+1


print(count / len(testData))

for x in getValueList(listofData):
    d = c2.classify(x)
    maxClass.append(d[0][0])

count = 0
for x in range(0,len(listofData)):
    if(listofData[x][4] == maxClass[x]): count = count+1

print (count/len(listofData))