# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:10:41 2017

@author: drago
"""

def Move(Board1,Destination, probe = False):
    '''Function which utalizes code from the l6470nucleo.py file to drive the
    stepper motors.
    
    Function runs the gantry till it stalls (in which case the system throws an
    error and waits for user input) or it reaches the destination in which case
    it stops and exits the function.
    
    @param Destination is the input distance x in millimeters from the end of
            the X-Beam you want to run to.
    @param probe is True or False, defaulting to False if not called. If True,
            the function will call the probe function to do one measurement
            at the end of the move. If False, it will not do that measurement.
    @return Returns one of two things. If the probe == True, the system will
            retrn the value read by the probe at the end. If not, then the
            function will return "Done".'''
    
    DistancePerStep = 673/800000
    xOffset = 00000     # Distance from gantry home position to the closest end
                        #   of the X-Beam. Absolute distsnce in mm
    xLimit = 490       # Maximum travel of the gantry from the end of the
                        #   X-Beam to the Lead Screw Raiser minus the gantry 
                        #   width. Absolute units in mm.
    #ISSUE See above 2 variables
    import Probe
    
    print("Moving Gantry to position x: "+str(Destination))
    print("    Probe at the end of the move? "+str(probe))
    # Check that Destination is not outside of the limits
    if Destination <= -xOffset:
        # If the destination is less than -xOffset, then the destination is 
        #   behind the home position which would push the system against the 
        #   housing and possible break the switch.
        print("    Error Occured moving the Gantry, Destination behind home")
        ErrGantry.put(1)
        return("Error Occured")
    elif Destination  >= xLimit:
        # If the destination is greater than the xLimit, the gantry is running
        #   the risk of crashing against the leadscrew bearing end support
        #   raiser.
        print("    Error Occured moving the Gantry")
        ErrGantry.put(1)
        return("Error Occured")
    print('''    Destination of Gantry within limits, Destination past'''+\
          '''farthest position''')
    
    # Convert Destination in mm to revolutions to steps
    Destination = int(Destination/DistancePerStep)
    print("    Destination converted to "+str(Destination)+" number of steps")
    
    # Move to the new value of Destination
    print("    Moving Gantry to Destination")
    Board1.GoTo(2,Destination)
    
    # Wait for stall or finish flag
    print("    waiting for stall or completion of move command")
    while True:
        if Board1.isBusy(2) == True:
            # if finish, exit the function
            print("    Gantry in position, exit loop")
            break
        elif Board1.isStalled(2) == True:
            # if stall, stop gantry, throw error and return
            print('''    Error Occured moving the Gantry to position. '''+\
                 "Gantry stalled out")
            ErrGantry.put(1)
            return("Error Occured")
    
    # If done moving gantry and probe option is true, take measurement
    if probe == True:
        print("    Probe part of Move_Gantry_to() function called")
        # check the error flags to determine what mode the machine is in.
        #   if it is in calibration, then the probe does not need limits on
        #   its measurement. If it is leveling, then it does.
        if ErrCalibration.get() == 1:
            print("    Probe called for Calibration Mode")
            reading = Probe.Probe()
        elif ErrAssembly.get() == 1 or ErrLeveling.get() == 1:
            print("    Probe called for Leveling and Assembly Mode")
            UpprLimit = 1000
            LwrLimit = -1000
            reading = Probe(Limit = True, UpperLimit = UpprLimit,
                            LowerLimit = LwrLimit)

        if type(reading) == "Error Occured":
            # Error occured, but should have been solved as the Probe function
            #   shouldn't be able to finish if there was an error.
            print("    Error occured with probe in the Move_Gantry_to()")
            return("Error Occured")
        else:
            print("    No error occured with probe in the Move_Gantry_to()")
            return(reading)
    # Else if the gantry is done moving and probe option in false, return
    elif probe == False:
        print("    Probe part of Move_Gantry_to() function not called")
        return("Done")
        
def Home(Board1):
    global ErrGantry
    # Home Gantry Code. +/- 400 is the max speed of the gantry
    print("        Gantry GoUntil switch command")
    Board1.GoUntil(2,-300)
    # Check home status in while loop
    while True:
        if Board1.isBusy(2) == False:
            # gantry at switch, continue.
            break
        elif Board1.isStalled(2) == True:
            print("        Board stalled: "+str(Board1.isStalled(2)))
#                motor stalled, return an error and set flag
            Board1.HardHiZ(2)
            print("        Gantry Stalled during Home command")
            print("        ERROR ERROR ERROR, return error")
            ErrGantry.put(1)
            return("Error Occured")

    # Release switch for gantry
    print("        releasing switch for gantry")
    Board1.ReleaseSW(2,1)

    # Check home status in while loop
    while True:
        if Board1.isBusy(2) == False:
            # Both rail actuators are homed, continue.
            print("        Gantry completed ReleaseSW Command")
            break
        elif Board1.isStalled(2) == True:
            # motor stalled, return an error and set flag
            Board1.HardHiZ(2)
            print("        Gantry Stalled during Home command")
            print("        ERROR ERROR ERROR, return error")
            ErrGantry.put(1)
            return("Error Occured")
            
def Status(Board1):
    Board1.GetStatus(2,verbose = 1)
    
import task_share
import utime
from setup import ErrGantry , ErrCalibration, ErrLeveling, ErrAssembly