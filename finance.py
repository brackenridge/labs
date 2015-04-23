#!/usr/bin/python

import os
import sys

class FV:
    def __init__(self, present_value=None, rate=None, periods=None, frequency=None):
        self.pv = present_value
        self.rate = rate
        self.periods = periods
        if(frequency==None):
            self.freq = 1
        else:
            self.freq = float(frequency)

    def Calculate(self):
        return round((self.pv * pow(1+(self.rate/self.freq),(self.periods*self.freq))),2)


class PV:
    def __init__(self,fv=None, rate=None, periods=None,frequency=None):
        self.fv = fv
        self.rate = rate
        self.periods = periods
        if(frequency == None):
            self.freq=1
        else:
            self.freq = frequency

    def Calculate(self):
        return round( self.fv / ( pow(1+(self.rate/self.freq),(self.periods*self.freq))),2)

def FutureValue(present,rate=None,periods=None,frequency=None):
    return FV(present,rate,periods,frequency).Calculate()

def PresentValue(future,rate=None,periods=None,frequency=None):
    return PV(future,rate,periods,frequency).Calculate()

if __name__ == '__main__':
    fv = FV(present_value=1000,rate=.005,periods=12)
    result = fv.Calculate()
    if(result==1061.68):
        print "Calc successful"
    else:
        print "Calc unsuccessful {0}".format(result)
