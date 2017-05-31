# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:03:56 2017

@author: drago
"""

def Move(Input):
    '''Moves the probe up, down, or not at all
    Function Inputs:
        Input can be 1 of 3 things
            1)"up" or "Up" moves the probe up
            2)"down" or "Down" moves the probe down
            3) anything else stops the probe.
    Function Outputs:
        None'''
    if Input == "up" or Input == "Up":
        RaisePin.high()
        LowerPin.low()
    elif Input == "down" or Input == "Down":
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
    print("Home the Probe")
    Home()
    print("Taking measurement with probe")
    print("    Lowering probe")
    RefRead = ProbeEncoder.read()
    Move("down")
    start = utime.ticks_ms()
    current = utime.ticks_ms()
    tolerance = 5
    while True:
        # wait for readings from probe to change (delta) by the tolerance
        #   amount.
        CurrentRead = ProbeEncoder.read()
        delta = CurrentRead-RefRead
        # A fuck ton of debuggin statements. ctr + 1 to comment or uncomment
        #   sections of code FYI
#        print("        Current reading =   "+str(CurrentRead))
#        print("        Previous reading =  "+str(RefRead))
        RefRead = CurrentRead
#        print("        delta =             "+str(delta))
#        print("        tolerance=          "+str(tolerance))
#        print("        time passed in ms = "+str(current - start))
#        print("        exit cond 1:        "+str(delta)+" >= "+str(tolerance)+\
#                      " is "+str(delta <= tolerance))
#        print("        exit cond 2:        "+str(delta)+" <= "+\
#                      str(-tolerance)+" is "+str(delta >= -tolerance))
#        print("        exit cond 3:        "+str(current - start)+\
#                      " > 500 is "+str((current - start >500)))
        if delta <= tolerance and delta >= -tolerance and \
        (current - start >500):
            print("    Probe met surface")
            break
#        print("")
        utime.sleep_ms(100)
        current = utime.ticks_ms()
        
    
    # Check Reading is within the limits if the Limit flag is true
    Reading = ProbeEncoder.read()
    print("        Probe read: "+str(Reading))
    if Limit == True:
        if Reading > UpperLimit or Reading < LowerLimit:
            print("    probe reading was above upper limit of readings")
            ErrProbe.put(1)

    print("    Homing probe")
    Home()
    
    print("    ErrProbe = "+str(ErrProbe.get()))
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
    '''Function homes the probe by checking the reference tick for the
    probe. The function also has a timer if the reference tick doesn't
    work
    Function Inputs:
        None
    Function Outputs:
        None'''
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
                Move("Stop")
                print("        Probe is at reference tick, Zero out encoder")
                utime.sleep_ms(100)
                ProbeEncoder.zero()
                ProbeEncoder.position = 0
                utime.sleep_ms(500)
                print("        Probe homed at "+str(ProbeEncoder.position))
                break

def read():
    '''Function returns the read value from the Probe's Encoder
    Function Inputs:
        None
    Function Outputs:
        None'''
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

# Grab the ErrProbe error flag from setup
from setup import ErrProbe
