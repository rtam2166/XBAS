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
    
    DistancePerRev = 2          # Variable indicating the distance traveled
                                #   per revolution of the stepper motor,
                                #   dependent on the leadscrew pitch. Value is
                                #   in mm
    StepsPerRev = 200*8         # Variable indicating the number of steps
                                #   per revolution for the stepper motor. This
                                #   is # of microsteps per revolution.
    xOffset = 00000     # Distance from gantry home position to the closest end
                        #   of the X-Beam. Absolute distsnce in mm
    xLimit = 00000      # Maximum travel of the gantry from the end of the
                        #   X-Beam to the Lead Screw Raiser minus the gantry 
                        #   width. Absolute units in mm.
    #ISSUE See above 2 variables
    global ErrBeamAct
    global ErrCalibration
    global ErrAssembly
    global ErrLeveling
    import Probe
    
#    print("Moving Gantry to position x: "+str(Destination))
#    print("    Probe at the end of the move? "+str(probe))
    # Check that Destination is not outside of the limits
    if Destination <= -xOffset:
        # If the destination is less than -xOffset, then the destination is 
        #   behind the home position which would push the system against the 
        #   housing and possible break the switch.
#        print("    Error Occured moving the Gantry, Destination behind home")
        ErrBeamAct.put(1)
        return("Error Occured")
    elif Destination  >= xLimit:
        # If the destination is greater than the xLimit, the gantry is running
        #   the risk of crashing against the leadscrew bearing end support
        #   raiser.
#        print("    Error Occured moving the Gantry")
        ErrBeamAct.put(1)
        return("Error Occured")
#    print('''    Destination of Gantry within limits, Destination past'''+\
#          '''farthest position''')
    
    # Convert Destination in mm to revolutions to steps
    Destination = int(((Destination + xOffset)/DistancePerRev)*StepsPerRev)
#    print("    Destination converted to "+str(Destination)+" number of steps")
    
    # Move to the new value of Destination
#    print("    Moving Gantry to Destination")
    Board1.GoTo(1,Destination)
    
    # Wait for stall or finish flag
#    print("    waiting for stall or completion of move command")
    while True:
        if Board1.isBusy(1) == 1:
            # if finish, exit the function
#            print("    Gantry in position, exit loop")
            break
        elif Board1.isStalled(1) == True:
            # if stall, stop gantry, throw error and return
#            print('''    Error Occured moving the Gantry to position. '''+\
#                 "Gantry stalled out")
            ErrBeamAct.put(1)
            return("Error Occured")
    
    # If done moving gantry and probe option is true, take measurement
    if probe == True:
        print("    Probe part of Move_Gantry_to() function called")
        UpprLimit = 1000
        LwrLimit = -1000
        reading = Probe(Limit = True, UpperLimit = UpprLimit,
                        LowerLimit = LwrLimit)

        if type(reading) == "Error Occured":
            # Error occured, but should have been solved as the Probe function
            #   shouldn't be able to finish if there was an error.
#            print("    Error occured with probe in the Move_Gantry_to()")
            return("Error Occured")
        else:
#            print("    No error occured with probe in the Move_Gantry_to()")
            return(reading)
    # Else if the gantry is done moving and probe option in false, return
    elif probe == False:
#        print("    Probe part of Move_Gantry_to() function not called")
        return("Done")
        
def Home(Board1):
    global ErrBeamAct
    # Home Gantry Code. +/- 400 is the max speed of the gantry
    print("        Beam Actuator GoUntil switch command")
    Board1.GoUntil(1,-600)
    # Check home status in while loop
    while True:
        if Board1.isBusy(1) == False:
            # gantry at switch, continue.
            break
        elif Board1.isStalled(1) == True:
            print("        Board stalled: "+str(Board1.isStalled(2)))
#                motor stalled, return an error and set flag
            Board1.HardHiZ(1)
            print("        Beam Actuator Stalled during Home command")
            print("        ERROR ERROR ERROR, return error")
            ErrBeamAct.put(1)
            return("Error Occured")

    # Release switch for gantry
    print("        releasing switch for Beam Actuator")
    Board1.ReleaseSW(1,1)

    # Check home status in while loop
    while True:
        if Board1.isBusy(1) == False:
            # Both rail actuators are homed, continue.
            print("        Beam Actuator completed ReleaseSW Command")
            break
        elif Board1.isStalled(1) == True:
            # motor stalled, return an error and set flag
            Board1.HardHiZ(1)
            print("        Beam Actuator Stalled during Home command")
            print("        ERROR ERROR ERROR, return error")
            ErrBeamAct.put(1)
            return("Error Occured")
            
def Status(Board1):
    Board1.GetStatus(1,verbose = 1)

import task_share    
from setup import ErrBeamAct