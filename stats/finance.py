#!/usr/bin/python

import os
import sys

def val_times_rate(val, rate, freq):
    if(freq == None):
        freq=1
    return val * (1+(rate/freq))

def inflation(amt,rate,years):
    return amt*pow(1+rate,years)

class FV:
    def __init__(self, present_value=None, rate=None, periods=None, frequency=None):
        self.pv = present_value
        self.rate = rate
        self.periods = periods
        if(frequency==None):
            self.freq = 1
        else:
            self.freq = frequency

    def Calculate(self):
        return round((self.pv * pow(1+(self.rate/self.freq),(self.periods*self.freq))),2)

    def CalculateAtPeriods(self):
        present = self.pv
        for x in range(0, self.periods*self.freq):
            present = val_times_rate(present, self.rate,self.freq)
            yield round(present,2)

    def CalcPeriodWithdrawals(self,amt,wfreq):
        present = self.pv
        for x in range(0,self.periods*self.freq):
            present=val_times_rate(present,self.rate,self.freq)
            yield round(present,2)
            if((x%wfreq)==1):
                present = present-amt

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
