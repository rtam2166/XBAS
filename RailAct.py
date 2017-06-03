# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:28:59 2017

@author: drago
"""
def checkSide(Side):
    '''Function determines the rail actuator being called
    Function Inputs:
        Side indicates which rail actuator is being operated. It takes values
            of Right, right, r, R, and 1 for the right rail actuator. It takes
            values of Left, left, l, L, and 2 for the left rail actuator. 
            Both, both, b, B, or 3 indicates both rail actuators and is only
            for the Home command
    Function Outputs:
        Function outputs either a 1 or 2 corresponding to the right and left
        actuator respectivly
    '''
    if Side == 'right' or\
        Side == 'Right' or\
        Side == 'r' or\
        Side == 'R' or\
        Side == 1:
        return(1)
    elif Side == 'left' or\
        Side == 'Left' or\
        Side == 'l' or\
        Side == 'L' or\
        Side == 2:
        return(2)
        
def Move(Side,stall=90):
    '''Moves the selected rail actuator to the given destination
    Function Inputs:
        Side indicates which rail actuator is being operated. The value is put
            into the function checkSide to determine the actuator being called.
        Destintion is the destination desired in steps.
        stall is the stall threshold of both the rail actuators. defaults to 65
            which we found to be weak enough not to hurt a person, but enough
            to move without stall. Set to higher stalls for specific commands
    Fucntion Outputs:
        None'''
#    switch = 0
    print('    setting stall, wait a lot')
    Board2._setStallThreshold(stall)
    motor = checkSide(Side)
    Board2.GetStatus(motor)
    Board2.Run(motor,200)
    start = utime.ticks_ms()
    while True:
        current = utime.ticks_ms()
        if Board2.isStalled(motor):
            print('stalled')
            Board2.HardHiZ(motor)
        if current-start > 3000:
            utime.sleep(5)
            Board2.HardHiZ(motor)
            Home(motor)
            break
#    # sleep to let the motors get going
#    utime.sleep_ms(2000)
#    # check rail actuators for completion or stall
#    while True:
#        if Board2.isBusy(motor) == False and switch != 1:
#            print('    moving motor pt 1')
#            Board2.GetStatus(motor,verbose = 0)
#            Board2.Run(motor,100)
#            utime.sleep_ms(1000)
#            print('    moving motor pt 2')
#            Board2.GoTo(motor,Destination)
#        if Board2.isBusy(motor) == True and switch != 1:
#            utime.sleep_ms(500)
#            if Board2.isBusy(motor) == True and switch != 1:
#                switch = 1
#                print('    motor moved, switch is '+str(switch))
#        if Board2.isBusy(motor) == False and switch == 1:
#            # gantry at switch, continue.
#            print("    Board isn't busy anymore")
#            Board2.GetStatus(motor)
#            Board2.HardHiZ(motor)
#            Board2._setStallThreshold(127)
#            utime.sleep(1)
#            return("Completed move command")
#        elif Board2.isStalled(motor) == True:
#            print("    Board stalled: True")
##                motor stalled, return an error and set flag
#            Board2.HardHiZ(motor)
#            Board2._setStallThreshold(127)
#            utime.sleep(1)
#            print("    rail actuator Stalled during move command")
#            return("Stall occured")
        
        
def Home(Side):
    '''Function homes one or both of the rail actuators depending on the input
    Function Inputs:
        Side indicates which actuator (if not both) is being homed
    Fucntion Outputs:
        None'''
    print('homing rail actuator')
    motor = checkSide(Side)
    if motor == 1 or motor == 2:
        Board2.GoUntil(motor,-100)
    else:
        Board2.GoUntil(1,-100)
        Board2.GoUntil(2,-100)
    if Board2.isHome(motor) == False:
        print('    not home')
        while True:
            if Board2.isBusy(motor) == False:
                # gantry at switch, continue.
                print("        Board isn't busy anymore")
    #            Board1.GetStatus(1)
                Board2.HardHiZ(motor)
                Board2.GetStatus(motor,verbose = 0)
    #            Board2._setStallThreshold(127)
                print('        release switch')
                Board2.ReleaseSW(motor,1)
                utime.sleep(1)
                while True:
                    if Board2.isBusy(motor) == False or Board2.isHome(motor) == False:
                        Board2.HardHiZ(motor)
                        Board2.GetStatus(motor,verbose = 1)
                        utime.sleep(5)
                        return("Completed move command")
    else:
        print('    already Bhomed')

def Status(Side):
    motor = checkSide(Side)
    Board2.GetStatus(motor)
    
from setup import Board2
import utime