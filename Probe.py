# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:03:56 2017

@author: drago
"""

def Move(Input):
    if Input == "up":
        RaisePin.high()
        LowerPin.low()
    elif Input == "down":
        RaisePin.low()
        LowerPin.high()
    else:
        RaisePin.high()
        LowerPin.high()

def Probe(Limit = False, UpperLimit = 0,LowerLimit = 0):
    '''Lower Probe, Take measurement, Check measurement, Raise the probe if no
    error. If not, throw an error.
    Function Inputs:
        Limit is True or False, defaulting to False. If the Limit is False, the
            function does not check teh value taken against the upper and lower
            limits. If True, it does compare.
    Function Outputs: Returns the value of the measurement taken. Otherwise
            returns message "Error Occured" if the reading is outside the
            given limits.
            '''
    print("Taking measurement with probe")
    print("    Lowering probe")
    Move("down")
    
    tolerance = 10
    previous = 100
    while True:
        # wait for readings from probe to change (delta) by the tolerance
        #   amount. take readings every .5 sec
        current = ProbeEncoder.read()
        delta = current-previous
        previous = current
        print("        delta = "+str(delta))
        print("        tolerance: "+str(tolerance))
        if delta <= tolerance and delta >= -tolerance:
            print("    Probe met surface")
            break
        print("")
        utime.sleep_ms(500)
        
    
    # Check Reading is within the limits if the Limit flag is true
    Reading = ProbeEncoder.read()
    if Limit == True:
        if Reading > UpperLimit or Reading < LowerLimit:
            print("    probe reading was above upper limit of readings")
            global ErrProbe
            ErrProbe.put(1)

    print("    Raising probe")
    Home()
    
    Move("stop")
    global ErrProbe
    print("    ErrProbe = "+str(ErrProbe))
    # If there was or was not an error
    if ErrProbe.get() == 0:
        print("    No error, exit")
        # No error, return
        return(Reading)
    else:
        # Error, return error message
        print("    Error Error Error Error")
        return("Error Occured")

def Home():
    if ProbeReference.value() != 1:
        # False, Retract Probe until it is at the reference tick
        print("        Probe is not at reference tick, raise probe")
        Move("up")
        
        # While loop to check the probe for when its reaches reference
        #   tick
        start = utime.ticks_ms()
        while True:
            current = utime.ticks_ms()
            if ProbeReference.value == 1 or (current - start) > 2000:
                # True
                print("        Probe is at reference tick, go to next "+\
                      "object")
                break

def read():
    return(ProbeEncoder.read())
    
# Encoder Pins and Object for the Probe
#   C6 is encoder ch1
#   C7 is encoder ch2
#   ProbeEncoder is a Quadrature Encoder Object 
import encoder as enc
import pyb
import utime

pinC6 = pyb.Pin(pyb.Pin.cpu.C6, pyb.Pin.AF_PP,af=3)
pinC7 = pyb.Pin(pyb.Pin.cpu.C7, pyb.Pin.AF_PP,af=3)
tim8 = pyb.Timer (8,freq=1000)
ProbeEncoder = enc.Quad_Encoder(pinC6,pinC7,tim8)

'''Probe Pins'''
#   H1 is the referencetick
ProbeReference = pyb.Pin(pyb.Pin.cpu.H1, mode = pyb.Pin.IN,
                         pull = pyb.Pin.PULL_DOWN)

#   B9 high sends the probe up if B8 is low
RaisePin = pyb.Pin(pyb.Pin.cpu.B9, mode = pyb.Pin.OUT_PP,
                   pull = pyb.Pin.PULL_DOWN)
RaisePin.high()

#   B8 high sends the probe down if B9 is low
LowerPin = pyb.Pin(pyb.Pin.cpu.B8, mode = pyb.Pin.OUT_PP,
                   pull = pyb.Pin.PULL_DOWN)
LowerPin.high()

from setup import ErrProbe
Home()
utime.sleep_ms(500)
ProbeEncoder.read()
ProbeEncoder.zero()