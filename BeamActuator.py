# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:10:41 2017

@author: drago
"""

def Move(Destination, probe = False):
    '''Function which utalizes code from the l6470nucleo.py file to drive the
    stepper motors.
    
    Function runs the Beam Actuator till it stalls (in which case the system 
    throws an error and waits for user input) or it reaches the destination in 
    which case it stops and exits the function.
    
    @param Destination is the input distance x in millimeters from the bottom
            edge of the X-Beam
    @param probe is True or False, defaulting to False if not called. If True,
            the function will call the probe function to do one measurement
            at the end of the move. If False, it will not do that measurement.
    @return Returns one of two things. If the probe == True, the system will
            retrn the value read by the probe at the end. If not, then the
            function will return "Done".'''
    
    TickPerDistance = 111000/51.19 # ticks per mm determined experimentally
    Offset = 3       # Destance from home position of beam actuator to bottom
                        # edge of the X-Beam in mm
    Limit = 10       # Maximum travel of the beam actuator before something
                        # collides in mm. This is without the offset
    #ISSUE See above 2 variables
    import Probe
    
    print("Moving Beam Actuator to position x: "+str(Destination))
    print("    Probe at the end of the move? "+str(probe))
    # Check that Destination is not outside of the limits
    if Destination + Limit <= 0:
        # If the destination is less than -xOffset, then the destination is 
        #   behind the home position which would push the system against the 
        #   housing and possible break the switch.
        print("    Error Occured moving the Beam Actuator, Destination behind home")
        ErrBeamAct.put(1)
        return("Error Occured")
    elif Destination+Offset  >= (Limit):
        # If the destination is greater than the xLimit, the gantry is running
        #   the risk of crashing against the leadscrew bearing end support
        #   raiser.
        print("    Error Occured moving the Beam Actuator, destination past"+\
              " max limit")
        ErrBeamAct.put(1)
        return("Error Occured")
    print('''    Destination of Beam Actuator within limits''')
    
    # Convert Destination in mm to revolutions to steps
    Destination = int((Destination+Offset)*TickPerDistance)
    print("    Destination converted to "+str(Destination)+" number of steps")
    
    # Move to the new value of Destination
    print("    Moving Beam Actuator to Destination")
    Board1.GoTo(1,Destination)
    utime.sleep_ms(3000)
    
    # Wait for stall or finish flag
    print("    waiting for stall or completion of move command")
    while True:
#        print("Busy? : "+str(Board1.isBusy(1)))
#        print("Stalled? : "+str(Board1.isStalled(1)))
        if Board1.isBusy(1) == False:
            # if finish, exit the function
            print("    Beam Actuator in position, exit loop")
            Board1.HardHiZ(1)
            Board1.GetStatus(1,verbose = 0)
            break
        
        elif Board1.isStalled(1) == True:
            # if stall, stop gantry, throw error and return
            print("    Error Occured moving the Beam Actuator to position. "+\
                 "Beam Actuator stalled out")
            ErrBeamAct.put(1)
            Board1.HardHiZ(1)
            Board1.GetStatus(1,verbose = 0)
            return("Error Occured")
    
    # If done moving gantry and probe option is true, take measurement
    if probe == True:
        print("    Probe part of BeamActuator.Move() function called")
        reading = Probe.Probe()

        if type(reading) == "Error Occured":
            # Error occured, but should have been solved as the Probe function
            #   shouldn't be able to finish if there was an error.
            print("    Error occured with probe in the Move_Gantry_to()")
            return("Error Occured")
        else:
            print("    No error occured with probe in the BeamActuator.Move()")
            return(reading)
    # Else if the gantry is done moving and probe option in false, return
    elif probe == False:
        Board1.HardHiZ(1)
        Board1.GetStatus(1,verbose = 0)
        print("    Probe part of BeamActuator.Move() function not called")
        return("Done")
        
def Home():
    '''Home the Beam Actuator.
    Function input:
        Board1 is the l6470nucleo.Dual6470 class object that the beam actuator
        is a member of.
    Function output:
        outputs and "Error Occured" if there is an error.
        '''
        
    # Home Gantry Code. +/- 400 is the max speed of the gantry
    print("        Beam Actuator GoUntil switch command")
    Board1.GetStatus(1,verbose = 0)
    Board1.GoUntil(1,-400)
    utime.sleep_ms(250)
    # Check home status in while loop
    while True:
        if Board1.isBusy(1) == False:
            # gantry at switch, continue.
            print("        Board isn't busy anymore")
#            Board1.GetStatus(1)
            Board1.HardHiZ(1)
            Board1.GetStatus(1,verbose = 0)
            break
        elif Board1.isStalled(1) == True:
            print("        Board stalled: "+str(Board1.isStalled(1)))
#                motor stalled, return an error and set flag
            Board1.HardHiZ(1)
            Board1.GetStatus(1,verbose = 0)
            print("        Beam Actuator Stalled during Home command")
            print("        ERROR ERROR ERROR, return error")
            ErrBeamAct.put(1)
            return("Error Occured")

    # Release switch for gantry
    print("        releasing switch for Beam Actuator")
    Board1.ReleaseSW(1,1)
    utime.sleep_ms(500)

    # Check home status in while loop
    start = utime.ticks_ms()
    while True:
        if Board1.isBusy(1) == False:
            # Both rail actuators are homed, continue.
            print("        Beam Actuator completed ReleaseSW Command")
            Board1.HardHiZ(1)
            Board1.GetStatus(1,verbose = 1)
            break
        elif Board1.isStalled(1) == True:
            # motor stalled, return an error and set flag
            Board1.HardHiZ(1)
            Board1.GetStatus(1,verbose = 0)
            print("        Beam Actuator Stalled during Home command")
            print("        ERROR ERROR ERROR, return error")
            ErrBeamAct.put(1)
            return("Error Occured")
        current = utime.ticks_ms()
#        print("            timed "+str(current - start))
        if current - start > 1000:
            print("        retrying")
            Board1.ReleaseSW(1,1)
            utime.sleep_ms(1000)
            start = utime.ticks_ms()

def Status():
    '''Print information about the board's status for the Beam actuator
    to the repl
    Function Inputs:
        Board1 is the l6470.Dual6470 class object which correlates with
            the beam actuator
    Function Outputs:
        None'''
    Board1.GetStatus(1,verbose = 1)

from setup import ErrBeamAct, Board1
import utime
