import math


class PMA:
    def __init__(self, alertCallback, size=0):
        # alert callback function
        self.__alertCallback = alertCallback
        # threshold variable for anomaly
        self.__threshold = 0
        # factorial vector
        self.__factorial = [1]
        # factorial vector size
        self.__factorial_size = 1
        # window vector
        self.__window = [0]*size
        # window vector size
        self.__window_size = size
        # package counter in interval
        self.__frame = 0
        # frame prediction
        self.__predicted = 0
        # poisson vector
        self.__poisson = []
        # time of last interval end
        self.__time = None
        # interval of frame
        self.__interval = None
        # frames counter
        self.__frames_count = 0

        # ------variables for window resize
        self.__alpha = 0.05
        self.__avg_old = 0
        self.__variance_old = 0
        self.__avg = 0
        self.__variance = 0
        self.__removed_frame = 0
        # ------
        # set factorial vector
        self.__adjustFactorial()
        # set poisson vector
        self.__adjustPoisson()

    # function to set factorial vector values
    def __adjustFactorial(self):
        print("window_size", self.__window_size)
        print("window", self.__window)
        # block to decrease factorial vector
        if(self.__factorial_size > self.__window_size):
            # decrese factorial size
            while (self.__factorial_size > self.__window_size):
                # remove last item from factorial vector
                self.__factorial.pop()
                # decrement variable that contains factorial size
                self.__factorial_size -= 1
        # block to increase factorial vector
        if(self.__factorial_size < self.__window_size):
            # increse factorial size
            while (self.__factorial_size < self.__window_size):
                # increment factorial vector with size * last item
                self.__factorial.append(
                    self.__factorial[-1] * self.__factorial_size)
                # increment variable that contains factorial size
                self.__factorial_size += 1
        #print("factorial", self.__factorial)
    # function to calculate poisson truncate vector

    def __adjustPoisson(self):
        # reset poissson vector
        self.__poisson = []
        # pre-calculate e^lambda
        e_lambda = math.exp(-self.__window_size)
        # iterate from  to window_size -1
        for k in range(self.__window_size):
            # append the result of iteration k to vector
            self.__poisson.append(math.pow(self.__window_size, k)
                                  * e_lambda / self.__factorial[k])
        #print("poisson", self.__poisson)

    def __adjustWindow(self, size):
        print(len(self.__window), size)
        if(size > self.__window_size):
            self.__window.insert(0, self.__removed_frame)
            self.__window_size += 1
            while(size > self.__window_size):
                self.__window.insert(0, 0)
                self.__window_size += 1
        else:
            while(size < self.__window_size):
                self.__removed_frame = self.__window.pop(0)
                self.__window_size -= 1
        print(len(self.__window))
        self.__adjustFactorial()
        self.__adjustPoisson()

    # generate prediction
    def __predict(self):
        # reset predicted
        self.__predicted = 0
        # iterate from 0 to window_size - 1
        for i in range(self.__window_size):
            # accumulate frame relevance * frame
            self.__predicted += (self.__poisson[i] * self.__window[i])

    # set initial value for time and interval
    def setStart(self, start_time, interval):
        # set variable time
        self.__time = start_time
        # set time interval
        self.__interval = interval

    # function to calculate variance
    def __calcVariance(self):
        # reset current variance
        self.__variance = 0
        # iterate window frames
        for frame in self.__window:
            # sommation
            self.__variance += math.pow(frame - self.__avg, 2)
        # divide summation by vector size
        self.__variance = self.__variance / self.__window_size
        # threshold 3 times standard deviation
        self.__threshold = 3 * math.pow(self.__variance, 0.5)
        #print("threshold:", self.__threshold)

    def __calcMinMax(self):
        min_value = float("inf")
        max_value = 0
        for frame in self.__window:
            min_value = (frame < min_value) * frame or min_value
            max_value = (frame > max_value) * frame or max_value
        return min_value, max_value

    # function to slide window and calculate statistics
    def __slideWindow(self):
        # save current variance as old
        self.__variance_old = self.__variance
        # save current avg as old
        self.__avg_old = self.__avg
        # save last frame removed
        self.__removed_frame = self.__window.pop(0)
        # append new frame to window
        self.__window.append(self.__frame)
        # calculate new avg
        self.__avg = sum(self.__window)/self.__window_size
        # calculate new variance
        self.__calcVariance()
        """
        if(self.__avg != 0 and self.__avg_old != 0):
            direct = self.__avg / self.__avg_old
            inverse = self.__avg_old / self.__avg
            rate = abs(direct - inverse)
            if(rate >= 1 + self.__alpha):
                min_value, max_value = self.__calcMinMax()
                variance_max = (self.__avg - min_value) * \
                    (max_value - self.__avg)
                adjust = abs(variance_max / self.__variance)
                self.__adjustWindow(self.__window_size * adjust)
        """
        # generate prediction
        self.__predict()
    # function to end model analysis

    def stop(self):
        # sum 1 to frames count
        self.__frames_count += 1
        # call anomaly test
        self.__anomaly()

    # function to check anomaly
    def __anomaly(self):
        # verify if it's above threshold
        if(self.__frames_count >= self.__window_size and self.__frame > self.__predicted + self.__threshold):
            # alert as higher frame, sending frame and predicted
            self.__alertCallback("higher", self.__frame, self.__predicted)
        # verify if it's below threshold
        elif (self.__frames_count >= self.__window_size and self.__frame < self.__predicted - self.__threshold):
            # alert as lower frame, sending frame and predicted
            self.__alertCallback("lower", self.__frame, self.__predicted)
        # verify if it's in training
        elif (self.__frames_count < self.__window_size):
            # alert as training frame, sending frame and predicted
            self.__alertCallback("training", self.__frame, self.__predicted)
        # frame within prediction
        else:
            # alert as normal frame, sending frame and predicted
            self.__alertCallback("normal", self.__frame, self.__predicted)

    # function to processo package in
    def packageIn(self, time):
        # verify if package time is out of frame time
        if(time > self.__time + self.__interval):
            # check frame anomaly
            self.__anomaly()
            # recalculate window and slide window
            self.__slideWindow()
            # set next frame base time
            self.__time += self.__interval
            # frames count increment
            self.__frames_count += 1
        # increment package in frame
        self.__frame += 1
