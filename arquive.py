class Arquive:
    def __init__(self, file):
        self.__file = file

    def load(self):
        arq = open(self.__file, mode="r", encoding="utf-8")
        string = arq.read()
        arq.close()
        return string

    def save(self, string):
        arq = open(self.__file, mode="W+", encoding="utf-8")
        arq.write(string)
        arq.close()

    def append(self, string):
        arq = open(self.__file, mode="a+", encoding="utf-8")
        arq.write(string)
        arq.close()

    def readAllLines(self):
        data = self.load()
        return data.split("\n")
