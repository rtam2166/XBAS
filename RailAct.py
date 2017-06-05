# -*- coding: utf-8 -*-
"""
File: RailAct.py
@author: Robert Tam
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
        
def Move(Side,Destination,stall=90):
    '''Moves the selected rail actuator to the given destination
    Function Inputs:
        Side indicates which rail actuator is being operated. The value is put
            into the function checkSide to determine the actuator being called.
        Destintion is the destination desired in steps.
        stall is the stall threshold of both the rail actuators. defaults to 65
            which we found to be weak enough not to hurt a person, but enough
            to move without stall. Set to higher stalls for specific commands
    Fucntion Outputs:
        If there was stall, returns "Stalled"
        If move was completed, returns "Completed move command"
        
    Note: This function was written very last minute and is untested
        '''
    
    # setting stall threshold
    Board2._setStallThreshold(stall)
    
    # determine side
    motor = checkSide(Side)
    
    # get status on motor being run (cleares errors)
    Board2.GetStatus(motor)
    
    # run motor. This gets the motor going for the GoUntil
    #   command later since we noticed the GoUntil command
    #   sometimes doesn't work until after a Run command.
    #   this was a last minute addition to help cover the 
    #   aforementioned bug and is not in the flow chart
    Board2.Run(motor,200)
    
    # start timer
    start = utime.ticks_ms()
    
    # while loop that waits for stall or a time out
    while True:
        current = utime.ticks_ms()
        if Board2.isStalled(motor):
            print('stalled')
            Board2.HardHiZ(motor)
        if current-start > 1000:
            utime.sleep(5)
            Board2.HardHiZ(motor)
            Home(motor)
            break
    
    # move motor to destination
    Board2.GoTo(motor,Destination)
    
    # check rail actuators for completion or stall
    while True:
        if Board2.isBusy(motor) == False and switch == 1:
            # gantry at switch, continue.
            print("    Board isn't busy anymore")
            Board2.GetStatus(motor)
            Board2.HardHiZ(motor)
            Board2._setStallThreshold(127)
            utime.sleep(1)
            return("Completed move command")
        elif Board2.isStalled(motor) == True:
            print("    Board stalled: True")
#                motor stalled, return an error and set flag
            Board2.HardHiZ(motor)
            Board2._setStallThreshold(127)
            utime.sleep(1)
            print("    rail actuator Stalled during move command")
            return("Stall occured")
        
        
def Home(Side):
    '''Function homes one or both of the rail actuators depending on the input
    Function Inputs:
        Side indicates which actuator (if not both) is being homed
    Fucntion Outputs:
        returns "Completed move command" when done
        
    Note: this function was written last minute and is untested
    '''
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
