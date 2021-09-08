import time

class Timer:
    def __init__(self, interval, callback):
        self.__start_time = None
        self.__stop_time = None
        self.__interval = interval
        self.__callback = callback
        self.__on = False
        self.__count = 0

    def setInterval(self, interval):
        self.__interval = interval

    def start(self):
        self.__on = True
        self.__timeHandler()

    def stop(self):
        self.__on = False

    def __timeHandler(self):
        self.__count = 0
        self.__start_time = time.time()
        while(self.__on):
            time.sleep(self.__interval)
            self.__callback()
            self.__count += 1
        self.__stop_time = time.time()
    
    def getInfo(self):
        return {"start_time":self.__start_time, "stop_time": self.__stop_time, "count":self.__count}
