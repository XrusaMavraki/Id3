
# The main purpose of the parser is to read the give file with samples
# and generate a formed document(list) which we can work with.
# The extracted form is:  { 'value','value','value','value','className' }

class Parser(object):
    def __init__(self):
        self.data = []

    def read(self,fileName):
        with open('iris.data') as f:
            for line in f:
                line = line.strip('\n').split(',')
                self.data.append(line)
        return self.data