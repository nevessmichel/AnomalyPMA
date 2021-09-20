class Arquive:
    #class constructor
    def __init__(self, file, encoding = "utf-8"):
        #save file path
        self.__file = file
        #save encoding
        self.__encoding = encoding

    #function to load all file as string
    def load(self):
        #open file in read mode
        arq = open(self.__file, mode="r", encoding=self.__encoding)
        #load all content as string
        string = arq.read()
        #close file
        arq.close()
        # return string
        return string

    #function to overwrite file
    def save(self, string):
        #open/create file in write mode
        arq = open(self.__file, mode="W+", encoding=self.__encoding)
        #overwrite content
        arq.write(string)
        #close file
        arq.close()
        
    #function to append content
    def append(self, string):
        #open/create file in append mode
        arq = open(self.__file, mode="a+", encoding=self.__encoding)
        #write content
        arq.write(string)
        #close file
        arq.close()

    #function to read content split in lines
    def readAllLines(self):
        #load content as string
        data = self.load()
        #return splited data
        return data.split("\n")
