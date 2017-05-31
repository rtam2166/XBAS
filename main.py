# -*- coding: utf-8 -*-
##
#  @file main.py
#  @author Robert Tam
#  This program was written for an ME Senior Project.
# -*- coding: utf-8 -*-

# importing modules for buffers and functions
print('Program initilizing')
import Gantry
import Probe
import BeamActuator
import setup
from setup import ErrInit,\
                    ErrSleep,\
                    ErrCalibration,\
                    ErrLeveling, \
                    ErrAssembly, \
                    ErrBoltCsv,\
                    ErrCalCsv,\
                    ErrGantry,\
                    ErrProbe,\
                    ErrRailActL,\
                    ErrRailActR,\
                    ErrBeamAct,\
                    ErrFileCheck,\
                    ErrSong,\
                    XBeam,\
                    zero_flags
                    
def paramatarize():
    
    # Set the registers which need to be modified for the motor to go
    # This value affects how hard the motor is being pushed
    K_VAL = 80
    Board1._set_par_1b ('KVAL_HOLD', K_VAL)
    Board1._set_par_1b ('KVAL_RUN', K_VAL)
    Board1._set_par_1b ('KVAL_ACC', K_VAL)
    Board1._set_par_1b ('KVAL_DEC', K_VAL)
    # Speed at which we transition from slow to fast V_B compensation
    INT_SPEED = 1032 #3141
    Board1._set_par_2b ('INT_SPEED', INT_SPEED)
    # Acceleration and deceleration back EMF compensation slopes
    ST_SLP = 25
    Board1._set_par_1b ('ST_SLP', ST_SLP)
    Board1._set_par_1b ('FN_SLP_ACC', ST_SLP)
    Board1._set_par_1b ('FN_SLP_DEC', ST_SLP)
    # Set the maximum speed at which motor will run
    MAX_SPEED = 30
    Board1._set_par_2b ('MAX_SPEED', MAX_SPEED)
    # Set the maximum acceleration and deceleration of motor
    ACCEL = 5
    DECEL = 20
    Board1._set_par_2b ('ACC', ACCEL)
    Board1._set_par_2b ('DEC', DECEL)
    
    # Set the number of Microsteps to use
    SYNC_EN = 0x00
    SYNC_SEL = 0x10
    STEP_SEL = 8
    Board1._set_MicroSteps (SYNC_EN, SYNC_SEL, STEP_SEL)
            
    # Set the Stall Threshold
    STALL_TH = 127
    Board1._setStallThreshold(STALL_TH)
    
         # Set the registers which need to be modified for the motor to go
            # This value affects how hard the motor is being pushed
    K_VAL = 80
    Board2._set_par_1b ('KVAL_HOLD', K_VAL)
    Board2._set_par_1b ('KVAL_RUN', K_VAL)
    Board2._set_par_1b ('KVAL_ACC', K_VAL)
    Board2._set_par_1b ('KVAL_DEC', K_VAL)
    # Speed at which we transition from slow to fast V_B compensation
    INT_SPEED = 1032 #3141
    Board2._set_par_2b ('INT_SPEED', INT_SPEED)
    # Acceleration and deceleration back EMF compensation slopes
    ST_SLP = 25
    Board2._set_par_1b ('ST_SLP', ST_SLP)
    Board2._set_par_1b ('FN_SLP_ACC', ST_SLP)
    Board2._set_par_1b ('FN_SLP_DEC', ST_SLP)
    # Set the maximum speed at which motor will run
    MAX_SPEED = 20
    Board2._set_par_2b ('MAX_SPEED', MAX_SPEED)
    # Set the maximum acceleration and deceleration of motor
    ACCEL = 5
    DECEL = 12
    Board2._set_par_2b ('ACC', ACCEL)
    Board2._set_par_2b ('DEC', DECEL)
    
    # Set the number of Microsteps to use
    SYNC_EN = 0x00
    SYNC_SEL = 0x10
    STEP_SEL = 8
    Board2._set_MicroSteps (SYNC_EN, SYNC_SEL, STEP_SEL)
            
            # Set the Stall Threshold
    STALL_TH = 127
    Board2._setStallThreshold(STALL_TH)


def Mode():
    '''Function which is used to read and return the selection of the three
    position switch.
    @input  Inputs are the read values of pin ThreeSwitch()
    @return Returns either a 1, 2, or 3 corresponding with the selection of the
    three position switch which are differentiated by different resistor values
    hardcoded below.'''
    
    # Get the reading from the three position switch analog pin
    value = ThreeSwitch()
    
    # Pins by Voltage in voltage
    V3 = 4030
    V2 = 1950
    V1 = 1300
    tolerance = 200
#    print("First Position value in ticks: "+str(V1))
#    print("Second Position value in ticks: "+str(V2))
#    print("Third Position value in ticks: "+str(V3))
#    print("Tolerance of "+str(tolerance))
#    print("Three Pos Switch read value in ticks: "+str(value))
    
    # Check if the first position has been selected
    if (value <= (V1 + tolerance)) and (value >= (V1 - tolerance)):
#        print("Selected Mode 1")
        return(1)
           
    # Check if the second position has been selected
    elif (value <= (V2 + tolerance)) and (value >= (V2 - tolerance)):
#        print("Selected Mode 2")
        return(2)
           
    # Check if the third position has been selected
    elif value <= V3 + tolerance and value >= V3 - tolerance:
#        print("Selected Mode 3")
        return(3)
           
    else:
#        print("No Mode Selected")
        return(0)
    
def FileCheck():
    '''Function checks for files in the same directory and writes to the error
    report, listing the files from FileList that are missing. After that, if
    the Switch has been set to 1 (meaning an file was missing), it sets the
    ErrFileCheck to 1 and runs the ErrorHandler() function. This function
    also completely takes care of its own error report.
    Takes no paramaters.
    @return Function returns a string if an error occured, an integer if not.
    '''
    print("Checking Files")
    Switch = 0      # Indicates if an error has occured. Used so that the error
                    #   message indicating that the error occured during the
                    #   initilization phase is written only once at the
                    #   beginning of the report.
    import os       # Import os for the listdir() function
    
    # List of strings of file names to check for in the system directory
    FileList = ["main.py",
                "boot.py",
                "l6470nucleo.py",
                "encoder.py",
                "task_share.py",
                "BeamActuator.py",
                "Gantry.py",
                "Probe.py",
                "Import.py",
                "setup.py"]
                
    # Retrieve the system directory information as a list of strings
    files = os.listdir()
#    print("files present")
#    print(files)
#    print("")
    # Open the Error Report text file in preparation of writing errors to
    f = open("Error Report.txt",'w')
    for file in FileList:
        print("    file being checked: "+str(file))
        if file not in files:
            # If the file being checked is not on the pyboard
            if Switch == 0:
                f.write('There was an error during the system initilization'+\
                        '\r\r\n')
                Switch = 1
            f.write("The file "+file+" is missing\r\r\n")
            print("        The file "+file+" is missing")
            
            # If special action is required for a file, add an if statement
            #   here which checks for said file to write that specific
            #   recommended action here.
            
            f.write("    Recommended action: Copy "+file+" from a backup onto"+
                    " the pyboard\r\r\n")
            
            # Written Error report should look like...
            #   There was an error during the initilization phase
            #   The file main.py is missing
            #   Recommened action: Copy main.py from a backup onto the pyboard
    
    # Finished writing to Error Report, close the text file
    f.close()
    
    if Switch != 0:
        # If there was an error, set flag
        print("File Check Done, error occured, please press (deliberatly) "+\
              "the go once to turn the noise off")
        # Perfrom special error handling unique to this function which must be
        #   done here for the system to work
        import utime
        RedLED.high()
        YellowLED.high()
        GreenLED.high()
        switch = 0
        go = 0
        Time = 0
        while True:
            start = utime.ticks_ms()
            if switch == 0 and go == 0:
                BuzzerChannel.pulse_width_percent(100)
            elif switch == 1 and go == 0:
                BuzzerChannel.pulse_width_percent(0)
            else:
                BuzzerChannel.pulse_width_percent(0)
            if Go() == 1 and go == 0:
                go = 1
                BuzzerChannel.pulse_width_percent(0)
                print("Go hit first time, sleep for 0.25 seconds.")
                utime.sleep_ms(250)
                print("Buzzer Off, please press the go button once more"+\
                      " to resume")
            elif Go() == 1 and go == 1:
                break
            if go == 0:
                current = utime.ticks_ms()
                Time = Time + (current-start)
                start = current
            if Time >= 1000 and go == 0:
                if switch == 0:
                    switch = 1
                else:
                    switch = 0
                Time = 0
        return("Error Occured")
    else:
        print("File Check Done, no errors")
        return([files,FileList])
    
def Lights_Sound_Off():
    '''Turns all LEDs and the buzzer off
    Function has no input paramaters or returned values'''
    RedLED.low()
    YellowLED.low()
    GreenLED.low()
    BuzzerChannel.pulse_width_percent(0)
#    print("All Lights and Sound have been turned off")
    
def Lights_Sound_Action():
    '''This function turns on various LEDs and controls the buzzer depending on
    the error flags which have been raised. Function has no input paramaters or
    returned values'''
    Lights_Sound_Off()      # Turn lights off
#    print("Lights_Sound_Action() has been called. Let the show begin.")
    import utime
    switch = 0              # Switch is bolean variable that switches each run
                            #   of the LEDs and buzzer so the system knows to
                            #   alternate
    Green = 0               # Valriable that says the green LED is to be used
    Yellow = 0              # Valriable that says the yellow LED is to be used
    Red = 0                 # Valriable that says the red LED is to be used
    Blink = 0               # Variable that says LEDs need to blink
    Stop = 0                # Variable that counts number of Go's pressed to 
                            #   exit function

    if ErrGantry.get() == 1:
        # If the Gantry error flag is raised, tell system to turn on green and
        #   yellow LEDs, no blinking
        Green = 1
        Yellow = 1
#        print("Gantry Error detected")
    elif ErrProbe.get() == 1:
        # If Probe flag raised, yellow and red LED, no blinking
        Yellow = 1
        Red = 1
#        print("Probe Error detected")
    elif ErrBeamAct.get() == 1:
        # If beam actuator flag raised, green and red LED, no blinking
        Green = 1
        Red = 1
#        print("Beam Actuator Error detected")
    elif ErrSong.get() == 1:
        # If Song error flag raised, all LEDs on, blinking
        Green = 1
        Yellow = 1
        Red = 1
        Blink = 1
#        print("Piano Switch Board Combination Error detected")
    elif ErrRailActR.get()==1 or ErrRailActL.get() == 1:
        # If Either rail actuator flags are raised
        Green = 1
        Yellow = 1
        Red = 0
        Blink = 1
#        print("One or Both of the Rail Actuators Error detected")
    else:
        # No error, Set Green LED, turn noise on 1 sec
#        print("No Error detected, doing the green light and 1 second beep")
        GreenLED.high()
        BuzzerChannel.pulse_width_percent(100)
        utime.sleep(1)
        BuzzerChannel.pulse_width_percent(0)
        return
        
    while True:
        Start = utime.ticks_ms()
        
        # Check Switch for what to do
        if switch == 0:
            # Check Buzzer for if it should run or not. Should not run if Stop
            #   is not 0 meaning user hit go at some point.
            if Stop == 0:
                BuzzerChannel.pulse_width_percent(100)
#                print("Sound On")
            else:
#                print("Sound Off")
                BuzzerChannel.pulse_width_percent(0)
            # Check what LEDs should be on
            if Green == 1:
                GreenLED.high()
            if Yellow == 1:
                YellowLED.high()
            if Red == 1:
                RedLED.high()
        else:
            # Buzzer should be off
#            print("Sound Off")
            BuzzerChannel.pulse_width_percent(0)
                
            # Check what LEDs should be blinking. If so, then the LEDs now
            #   need to be off.
            if Blink == 1:
#                print("LEDs off")
                if Green == 1:
                    GreenLED.low()
                if Yellow == 1:
                    YellowLED.low()
                if Red == 1:
                    RedLED.low()
#        print("Go pressed: "+str(Stop))
#        print("Go() reads "+str(Go())+"\r\r\n")
                  
        Current = utime.ticks_ms()
        # Wait in the below while loop until the difference in time from the 
        #   beggining of the while loop to present >= 500ms or user hits go
        while True:
            if Go() == 1:
#                print("Go pressed")
                if Stop == 0:
                    Stop = 1
                    # wait .25 sec for button to be released
                    utime.sleep_ms(250)
                elif Stop == 1:
                    Stop = 2
                    break
            elif (Current - Start) >= 500:
                break
            Current = utime.ticks_ms()
        
        # If user has hit go twice during the above while loop, exit function.
        #   i.e. hit it once, than hit it again when the function loops back to
        #   the above nested loop.
        if Stop == 2:
            Lights_Sound_Off()
            YellowLED.high()
#            print("Exiting Lights_Sound_Action()")
            return()
            
        # Toggle switch so the system toggles sound and LEDs
        if switch == 0:
            switch = 1
        elif switch == 1:
            switch = 0
        
def ErrorHandler():
    '''This function checks flags, prints errors, sets lights, and makes noise
    accordingly.
    '''
    
    # print statements for debugging purposes
#    print("Beginning Error Handling")
#    print("ErrInit =        "+str(ErrInit))
#    print("ErrSleep =       "+str(ErrSleep))
#    print("ErrCalibration = "+str(ErrCalibration))
#    print("ErrLeveling =    "+str(ErrLeveling))
#    print("ErrAssembly =    "+str(ErrAssembly))
#    print("ErrProbe =       "+str(ErrProbe))
#    print("ErrGantry =      "+str(ErrGantry))
#    print("ErrBeamAct =     "+str(ErrBeamAct))
#    print("ErrRailActR =    "+str(ErrRailActR))
#    print("ErrRailActL =    "+str(ErrRailActL))
#    print("")
                  
    # There was no issues with all of the named error flags, check all of the
    #   other error flags
    if ErrSong.get() == 0 and       \
       ErrBoltCsv.get() == 0 and    \
       ErrCalCsv.get() == 0:
                                   
        f = open("Error Report.txt","w")
            
        if ErrProbe.get() == 1:
#            print("Error with probe, writing error")
            f.write("Probe was unable to take valid measurements")
        elif ErrGantry.get() == 1:
#            print("Error with gantry, writing error")
            f.write("Gantry was unable to move to the destination")
        elif ErrBeamAct.get() == 1:
#            print("Error with beam actuator, writing error")
            f.write("Beam Actuator was unable to move to the destination")
        elif ErrRailActR.get() == 1 or ErrRailActL.get() == 1:
            if ErrRailActR.get() == 1 and ErrRailActL.get() == 1:
                x = "Both rail actuators"
            elif ErrRailActR.get() == 1:
                x = "The right rail actuator"
            elif ErrRailActL.get() == 1:
                x = "The left rail actuator"
            print("error with the "+x)
            f.write(x+"Has attempted run past the maximum stroke length "+\
                    "allowed")
        f.close()
    
    # After finishing up writing to the Error Report text file, now run the 
    #   function responsible for turning on and off the LEDs and sound.
    Lights_Sound_Action()
    
#    print("Exiting Error Handler")
    # Now Home the system
#    Home("All")
        
def callback(line):
    '''This is a function which runs during interrupts. This should occur when
    the emergecny stop button is pressed down. It waits until the emergency
    stop has been disengaged and initiates a soft restart'''
    print("Emergency Stop pressed...")
    while True:
        if Stop_Pin.value() == 0:
            print("... and released")
            break
    import pyb
    pyb.hard_reset()

def Home(*arg):
    '''Function Homes parts as indicated by the *arg which is a tuble of
    strings of whatever the user inputs. For reference, google Python optional
    arguments.
    Inputs: 
        *agr: can be any to all of the following
            Probe:          Homes the probe
            RailActR:       Homes Right rail actuator
            RailActL:       Homes Left rail actuator
            Screwdrivers:   Homes the screwdrivers
            Gantry:         Homes the Gantry
            Bact:           Homes the Beam Actuator
            RailAct:        Homes both rail actuators
            All:            Homes everything
    Outputs:
        None'''
    
#    print("Beginning to Home system")
    
    # Set the stall thresholds of the stepper drivers to the maximum
    #   ammount (which they should be already)
    Board1._setStallThreshold(16)
    Board2._setStallThreshold(16)
    
    # First Home Probe if Probe or all is listed in *arg
    if ('Probe' in arg) or ('All' in arg):
        Probe.Home()
            
    # Now Home Righ and Left rail actuator
#    print("    Homing one or both rail actuators")
    if ('RailActR' in arg) or ('All' in arg) or ('RailAct' in arg):
        # Home right actuator. Speed is up for debate
#        print("        Homing the right rail actuator")
        Board2.GoUntil(2,-400)
                
    if ('RailActL' in arg) or ('All' in arg) or ('RailAct' in arg):
        # Home left actuator
#        print("        Homing the left rail actuator")
        Board2.GoUntil(1,-400)
                
    if ('RailActR' in arg) or ('RailActL' in arg) or ('All' in arg) or \
        ('RailAct' in arg):
#        print("        checking rail actuators for completion of move")
                
        # Check home status in while loop
        while True:
            if Board2.isBusy(1) == 1:
                # Both rail actuators are @ their switches, continue.
#                print("        actuator switches have been pressed, busy "+\
#                      "pin high")
                break
    
        # Rail Actuator @ swithces, release switch to back them off of
        #   switch which is their homed position.
        if ('RailActR' in arg) or ('All' in arg) or ('RailAct' in arg):
            # Release Switch Right
#            print("        releasing right switch")
            Board2.ReleaseSW(2,1)
                
        if ('RailActL' in arg) or ('All' in arg) or ('RailAct' in arg):
            # Home left actuator
#            print("        releasing left switch")
            Board2.ReleaseSW(1,1)
        
        # Check status via while loop
        while True:
            if Board2.isBusy(1) == 1:
#                print("        actuator switches have been pressed, busy "+\
#                      "pin high")
                Board2.HardHiZ(1)
                Board2.HardHiZ(2)
                break
            
    # Home screwdriver DC Motors and Solenoids
    if ('Screwdrivers' in arg) or ('All' in arg):
        # Turn of both DC motors and solenoids
#        print("    Turning off all DC motors and Solenoids for srewdrivers")
        DCMotorRightPin.high()
        DCMotorLeftPin.high()
        SolenoidRightPin.high()
        SolenoidLeftPin.high()
        
    # Home Gantry
    if ('Gantry' in arg) or ('All' in arg):
        Gantry.Home()
        
    # Home Beam Actuator
    if ('Bact' in arg) or ('All' in arg):
        BeamActuator.Home()
        
def Calibration_Mode():
    '''This function directs the XBAS machine to calibrate a machine csv file
    to a specific X-Beam indicated by length in the file name. The file to be
    edited is indicated by the user input in a piano switch board.
    Function Inputs:
        None
    Function Outputs:
        None
    '''
                  
#    print("Beginning Calibration Mode")
    
    # Variable switch is used to identify if this is the first time running
    #   through this program or not.
    switch = 0
    
    # Variable block is a hardcoded user input that determines the behavior
    #   of the program
    #   Value of 1 indicates that the user is using a short block that they
    #       manually have to move for calibration, thus the machine waits
    #       after moving the gantry for the user to hit go.
    #   Value of 2 indicates the user is using a long block for calibration
    #       that they don't have to move, so the machine will not wait for
    #       user input and just go.
    block = 1

    # 1st layer
    while True:            
        
        # Set Error Flag fir this mode
        ErrCalibration.put(1)
        
        # 2nd Layer. System will stay in this loop unless an error occurs or
        #   the system finishes calibration.
        while True:
            
            # Pre-Calibration Mode
            
            # Turn Yellow LED on indicating the system is initializing the 
            #   calibration mode. Runs once at the beginning of the function
            Lights_Sound_Off()
            YellowLED.high()
            
            # If first time running through this section of code
            if switch == 0:
                # First Check Files are present
                Output = FileCheck()
                if type(Output)==str:
                    # If file is missing, handle the error than break back into 
                    #   1st layer.
                    break
            
            # Home Machine
            Output = Home("All")
            
            # Error Check
            if Output == "Error Occured":
                  break
            
            if switch == 0:
#                print("Waiting in pre-Calibration Stage")
                # The calibration mode is ready to go, turn green light on and
                #   wait for go.
                Lights_Sound_Off()
                GreenLED.high()
                while True:
                    if Go() == 1:
                        # User hit go
                        Lights_Sound_Off()
                        YellowLED.high()    # Turn Yellow LED on Indicating the
                                            #   system is working now
                        break               # Exit the 3rd layer and resume in 
                                            #   2nd layer
#                        print("Go selected, continuing function")
                    elif Mode() != 1:
                        # User has selected a different mode before hitting go,
                        #   exit the function
#                        print("Another Mode selected, exiting function")
                        return()
            
            # User has hit go, import files. Will error if the file is missing
            #   and user must hit go twice(once to turn sound off, once to
            #   resume). After error, return to the pre-calibration stage by
            #   breaking from the 2nd loop back to the 1st loop.
            Output = Import.Song()
            if Output == "Error Occrured":
                # Error occured, handle the error, then break out of the 2nd 
                #   layer to the 1st layer
                break
            
            # Song imported, import calibration. If there is an issue, go to
            #   error and wait for user input upon which it breaks back into
            #   the 1st loop.
            Output = Import.Calibration()
            if Output == "Error Occrured":
                break
            
            # Now we've inported the Calibration file w/o error, save the value
            #   of Output to a variable for later use. Also take values out of
            #   the list output of ImportCalibration and save specific values
            #   to named variables for ease of use. Note, Offset adjusts the
            #   distance NearSide and FarSide so they are from the end of the
            #   X-Beam
#            print("Transcribing calibration data over to local variables")
            CalibrationData = Output
            NearSide = Output(0)
            FarSide = Output(1)
            
            # Move Gantry to the near side
#            print("Moving Gantry to the near side for calibration purposes")
            Output = Gantry.Move(NearSide, probe = False)
            
            # Check output for if an error occured. If no error occured, the
            #   function should have returned a number indicating the
            #   measurement.
            if Output == "Error Occured":
                # An error did occur, break back to 1st layer
#                print("Error occured moving gantry, do error handling")
                break
                
            # Gantry is in position, check the "block" variable for if the
            #   machine needs to wait for user input or not
            if block == 1:
#                print("Waiting for user input to do measurement")
                Lights_Sound_Off()
                GreenLED.high()
                while True:
                    # Sit in a while loop until the user hits Go()
                    if Go()==1:
#                        print("Go pressed, taking measurement")
                        Lights_Sound_Off()
                        YellowLED.high()
                        break
                        
            # XBAS now needs to take measurement
            Output = Probe()
            
            # Check Output for error from probe()
            if Output == "Error Occured":
#                print("Probe measurement error, do error handling")
                # Error Occured, exit 2nd layer to 1st layer for error handling.
                break
            
            # Store the data of the near side to the calibration data
            CalibrationData[2] = Output
#            print("Substituting probe measurement into CalibrationData, "+\
#                  "value "+str(Output))
            
            # Calue of NearSide has been stored, now for FarSide
#            print("Moving Gantry to the Farside for Calibration Purpose")
            Output = Gantry.Move(FarSide, probe = False)
            
            # Check output for if an error occured. If no error occured, the
            #   function should have returned a number indicating the
            #   measurement.
            if Output == "Error Occured":
#                print("Gantry moving error, do error handling")
                # An error did occur, handle error and break back to 1st layer
                ErrorHandler()
                break
            
            # Gantry is in position, check the "block" variable for if the
            #   machine needs to wait for user input or not
            if block == 1:
#                print("Waiting for user input to do measurement")
                Lights_Sound_Off()
                GreenLED.high()
                while True:
                    # Sit in a while loop until the user hits Go()
                    if Go()==1:
#                        print("Go pressed, taking measurement")
                        Lights_Sound_Off()
                        YellowLED.high()
                        break

            # XBAS now needs to take measurement
            Output = Probe()

            # Check Output for error from probe()
            if Output == "Error Occured":
                # Error Occured, exit 2nd layer to 1st layer for error handling
#                print("Probe error occured, handle error")
                break

            # Store the data of the far side to the calibration data
#            print("Substituting probe measurement into CalibrationData, "+\
#                  "value "+str(Output))
            CalibrationData[3] = Output
            
            # Calculate the difference between the level of the two points for 
            #   the calibration constant
            CalibrationData[4] = CalibrationData[3]-CalibrationData[2]
#            print("Calculating and storing calibration constant, value "+\
#                  str(CalibrationData[4]))
                    
            # At this point, there should have been no errors or such, so 
            #   finish up by storing information into the Calibration file for
            #   the X-Beam length being calibrated and signal the user that the
            #   machine is done.
            Input = XBeam
            FileName = "Calibration"+str(Input)+".csv"
#            print("Writing CalibrationData to "+FileName)
            f = open(FileName,'w')
            String = ''
            for item in CalibrationData:
                String = String + str(item) + ','
            String = String.rstrip(',')
#            print("    writing line: "+String)
            f.write(String)
            
            # Exit Function
#            print("Calibration Done, exiting function")
            return('Done')
        # End of 2nd Layer loop
    
    # End of 1st layer loop
    ErrorHandler()
    
def Leveling_Mode():
    '''This function is part 1 of the assembly mode which is leveling the
    X-Beam relative to the datum surface.
    Function Inputs:
        None
    Function Outputs:
        None
    '''

#    print("Beginning Leveling half of the Assembly Mode")
    
    # Variable switch indicates if this is the first time the code is
    #   running through the code. This is for the purpose of skipping
    #   the pre-stage every run through after the first, ie after
    #   error handling.
    switch = 0
    
    # While Loop 1st Layer
    while True:
        
        # Set error flag for this mode
        ErrLeveling.put(1)
        
        # While Loop 2nd Layer
        while True:
            
            # Pre Assembly Mode
            
            # Turn Yellow LED on indicating the system is initializing the 
            #   mode. Only does this once for the functions first
            #   run
            Lights_Sound_Off()
            YellowLED.high()
            
            # Is this the first time running through this section of code?
            if switch == 0:
                # First Check Files are present
                Output = FileCheck()
                if type(Output)==str:
                    # If file is missing, break back into 1st layer where the
                    #   error handle function is (at the bottom)
                    break
            
            # Home function, home everything
            Output = Home("All")
            
            # Check output
            if Output == "Error Occured":
                break
            
            if switch == 0:
                # Turn Green LED on indicating ready for user input
                Lights_Sound_Off()
                GreenLED.high()
            
                # Wait for user to hit go or to switch system modes to a
                #   different mode
                while True:
#                    print("Waiting in pre-Assembly Stage")
                    if Go() == 1:
                        # Go was pressed, exit the 3rd Layer while loop and
                        #   resume the 2nd layer loop via a break command
#                        print("User hit Go, continue leveling and assmembly")
                        break
                    elif Mode() != 3:
                        # Else if the 3 position switch is not set to 3 which
                        #   is the assembly mode, then exit this function via 
                        #   return
#                        print("User selected different mode, exit function")
                        return()
            
            # Set switch to 1 so that on future runs, it skips the while loop
            #   for waiting for the user to hit go
            switch = 1
            
            # Turn Yellow Ligth on
            Lights_Sound_Off()
            YellowLED.high()
            
            # User has hit Go, read the piano board via ImportSong()
            Output = Import.Song()
            
            # Check Output for if an error occured
            if Output == "Error Occured":
                # Error occured, break 2nd layer loop to return to 1st layer 
                #   loop and handle error
#                print("Error in ImportSong, handle error")
                break

            # ImportSong() had no issues, continue by importing Calibration
            #   Data
            Output = Import.Calibration()
            
            # Check Output of ImportCalibration for errors
            if Output == "Error Occured":
                # Error occured, break 2nd layer loop to return to 1st layer 
                #   loop and handle error
#                print("Error in ImportCalibration, handle error")
                break
            
            # Take data from Import Calibration and Store it for future use
#            print("Transcribe Calibrationdata to local variables")
            CalibrationData = Output
            NearSide = CalibrationData(0)
            FarSide = CalibrationData(1)
            CalConst = CalibrationData(4)

            # Import BoltPatternXXX.csv file for the X-Beam just to check
            #   that it is both present and valid.
            Output = Import.BoltPattern()
            
            # Check the output for an error
            if type(Output) == str:
                # If error, break out of 2nd layer into 1st layer for
                #   error handling
#                print("Error in ImportBoltPattern, handle error")
                break
                
            # Move the Gantry to the far side and take the first measurement
#            print("Moving Gantry to far side and take measurement")
            Output = Gantry.Move(FarSide, probe = True)
            
            # Check function output
            if Output == 'Error Occured':
                # Error occured, break loop
#                print("Error in moving Gantry or probe, handle error")
                break
            
            # Store output
            FarLevel = Output
            
            # Move the Gantry to the near side and take the first measurement
#            print("Moving Gantry to near side and take measurement")
            Output = Gantry.Move(NearSide, probe = True)
            
            # Check function output
            if Output == 'Error Occured':
                # Error occured, break loop
#                print("Error in moving Gantry or probe, handle error")
                break

            # Store output modified by calibration constant
            NearLevel = Output - CalConst
#            print("Calculate nearside w/cal constant")
#            print("    FarLevel "+str(FarLevel))
#            print("    NearLevel "+str(NearLevel))
            
            # Level X-Beam by actuating X-Beam Actuator to raise the X-Beam
            #   to the level needed.
#            x1 = distance from line constraint to x-beam actuator point contraint
#            x2 = distance from where probe takes near side measurement to line constraint
            
            # Fraction indicating how much the point being leveled changes as
            #   the X-Beam actuator levels the beam
            x = x2/x1
            
            # Actuate X-Beam levveling actuator and measure
#            print("Actuate X-Beam actuator")
            Output = BeamActuator.Move((NearLevel - FarLevel)/x,
                                           probe = True)
            
            # Check output
            if Output == 'Error Occured':
                # Error occured, break loop
#                print("Error w/beam actuator, handle error")
                break
            
            # Store output
            NearLevel = Output - CalConst
            
            # Check, retry, and repeat
            Error = 0
            Tolerance = 100
            while True:
                if NearLevel - FarLevel >= -Tolerance or\
                    NearLevel - FarLevel <= Tolerance:
                    # Within of range, continue whiile loop
                    break
                
                # Actuate X-Beam levveling actuator and measure
#                print("X-Beam not leveled, re-attempt leveling with actuator")
                Output = BeamActuator.Move((NearLevel - FarLevel)/x,
                                               Probe = True)
                
                # Check output
                if Output == 'Error Occured':
                    # Error occured, break loop
                    Error = 1
                    break
            
            # if there was an error in the above while loop, its supposed to
            #   exit to the 1st loop. THis is the second break that helps
            #   achieve that.
            if Error == 1:
#                print("Error w/beam actuator, handle error")
                break
            
            # At this point, the beam should be leveled with no errors. Home, 
            #   zero flags and exit function.
            return('Done')
        # End of the 2nd Layer
        
    ErrorHandler()
    # End of the First Layer
                        
def TorqueDown(Input):
    '''Function Torques down the side indicated by the input
    Function inputs:
        Input is a character "L" or "R", indicating that either the
        left or right side needs to be torqued down.
    Function outputs:
        None'''
    
#    print("Beginning to Toque Down")

    # Rail Actuators constants
    DistancePerStep = .0079375 # mm linear travel per step
    
    # Position above rails in mm away from the motor. Does not have
    #   to be very accurate (+/- 1mm)
    PositionAboveRails = 10 # mm is the distance we determined too
                            # small for human fingers
    # Covert PositionAboveRails from distance in mm to steps for the 
    #   drivers
    PositionAboveRails = PositionAboveRails / DistancePerStep
    
    # Calculating position above granite from the motor just as with
    #   PositionAboveRails
    PositionAboveGranite = 10
    PositionAboveGranite = PositionAboveGranite / DistancePerStep
    
    # 1st Layer while loop
    while True:
        # Set torque for the approach to the rails at a very low stall torque
#        print("setting stall threshold of rail actuators low")
        Board2._setStallThreshold(4)
        
        # Turn on actuators and move twoards a position just above the rails
#        print("move rail actuator to point above rails")
        if Input == "L":
            # Turn on left actuator
#            print("    left actuator on")
            Board2.Goto(1,PositionAboveRails)
            
        elif Input == "R":
            # Turn on right actuator
#            print("    right actuator on")
            Board2.Goto(2,PositionAboveRails)
        
        # 2nd Layer while Loop
        error = 0
        while True:
            # Check for if the rail actuator has stalled or if the rail
            #   actuator has reached destination. 
            
            if Board2.isStalled(1) == True and Input == "L":
                # Left actuator stalled, call error and break out of while
                #   loop for handling it
#                print("    left actuator stalled")
                ErrRailActL = 1
                error = 1
                break
                
            elif Board2.isStalled(2) == True and Input == "R":
                # Right actuator stalled, call error and break out of while
                #   loop for handling it
#                print("    right actuator stalled")
                ErrRailActR = 1
                error = 1
                break
            
            elif Board2.isBusy(2) == 1:
                # Check for completion (Done flag false), exit with no
                #   error called
#                print("    actuator in position above rails")
                error = 0
                break
        # End of the 2nd Layer while loop, back in the 1st layer
        
    # Error Check, If an error was declared earlier, then skip
    #   the following code responsible for fully pressing down the
    #   rails and bolting down the screws
    if error == 0:
        # Set torque high
#        print("setting torque high")
        Board2._setStallThreshold(16)
        
        # Set actuators on depending on input
#        print("moving rail actuator to point above granite")
        if Input == "L":
            # Turns left actuator on
#            print("    left actuator on")
            Board2.Goto(1,PositionAboveGranite)
            
        elif Input == "R":
            # Turns right actuator on
#            print("    right actuator on")
            Board2.Goto(2,PositionAboveGranite)
            
        # 2nd layer while loop checking destination and stall
        #   flags as before.
        while True:  
            if Board2.isBusy(2) == 1:
                # Check for completion, call error if actuator moved
                #   to destination succesfully
                if Input == "L":
#                    print("    left actuator reached destination, error.")
                    ErrRailActL.put(1)
                if Input == "R":
#                    print("    right actuator reached destination, error.")
                    ErrRailActR.put(1)
                break
            if Board2.isStalled(1) == True or Board2.isStalled(2) == True:
                # Left or right actuator stalled, move on to next
                #   stage (torque down)
#                print("Actuator stalled, begin torque down section")
                # Truning On solenoids based on side being done
                if Input == "L":
                    # Left Side
#                    print("Left Solenoid On")
                    SolenoidLeftPin.low()
                if Input == "R":
                    # Right Side
#                    print("Right Solenoid On")
                    SolenoidRightPin.low()
        
                # Import Time so system can wait for stuff to finish

                # Wait for solenoids to extend
                utime.sleep(100)

                # Turn On motors depedning on side being done
                if Input == "L":
                    # Left Side
#                    print("Left DC motor On")
                    DCMotorLeftPin.low()
                if Input == "R":
                    # Right Side
#                    print("Right DC motor On")
                    DCMotorRightPin.low()

                # Sleep for X amount of time so the DC motor torques
                #   down the bolt.
                utime.sleep(5000)
                
                # Turn screwdriver motors and solenoids off
#                print("all motors and solenoids off")
                DCMotorLeftPin.high()
                DCMotorRightPin.high()
                SolenoidLeftPin.high()
                SolenoidRightPin.high()
    
                # Sleep till solenoids retract
                utime.sleep(100)
    
                # home the rail actoators depedning on side being done
                if Input == "L":
                    # Left Side
#                    print("Homing Left Actuator")
                    Home("RailActL")
                if Input == "R":
                    # Right Side
#                    print("Homing Right Actuator")
                    Home("RailActR")
    
                # Program done, return
                return()
        
        # end 2nd layer, back in 1st layer
        # Home the rail actuators in preparation for error handling.
        Home("RailAct")
        
        # Error Handling and set mode error back
        ErrorHandler()
        ErrAssembly.put(1)
        # End of 1st layer, resume at beginning 

def Assembly_Mode():
    '''Function that runs after the beam is leveled to force rails into 
    position and torque them down.
    Function Inputs:
        None
    Function Outputs:
        None
    '''
    
#    print("Beginning Assembly half of the assembly mode")
    
    # Set Error Flag for mode
    ErrAssembly.put(1)
    
    # Beginning of the while loop for importing the data stored in 
    #   BoltPatternXXX.csv
    while True:
#        print("ImportBoltPattern function called")
        Output = Import.BoltPattern()
        if type(Output) == str:
            # Error Occured
#            print("Error importing Bolt Pattern csv file.")
            ErrorHandler()
            ErrAssembly = 1
        else:
            # No Error Occured
            break
        # End of while loop
    
    # Store Output into variables for later use. Also assign value to offset
    #   to adjust the Bolt
#    print("Transcribing bolt pattern data to two seperate lists")
    BoltSide = Output(0)
    BoltData = Output(1)
    
    # For loop to run through the values of BoltSide and BoltData
    for counter in range(0,len(BoltData)):
        # Nested while loop to handle moving the gantry to the target point
        while True:
            # Run Gantry to position
#            print("Moving gantry to position #"+str(counter)+": "+\
#                  str(BoltData(counter)))
            Output = Gantry.Move(BoltData(counter))
            
            # Check output of the function for error
            if Output == "Error Occured":
                # Error Occured
#                print("error occured moving ganty, handling error")
                ErrorHandler()
                ErrAssembly.put(1)
            else:
                # No Error Occured
#                print("Gantry successfully moved, "+str(counter)+"/"+\
#                    str(len(BoltData))+" moves completed")
                break
            # End of while loop, go back to for loop and repeat entire
            #   process of moving gantry.
            
        # The gantry should be in position, press rails down and bolt them
        TorqueDown(BoltSide(counter))
#        print("TorqueDown successfull, "+str(counter)+"/"+\
#                      str(len(BoltData))+" bolts completed")
        # End of for loop, go back to beginning unless done.
        
    # Zero Flags, indicate the system is done via Lights_Sound_Action(), and
    #   retrun
    zero_flags()
    Lights_Sound_Action()
    return
    
def Sleep_Mode(Input):
    '''This is the sleeping mode for the machine. It homes the machine and goes
    to sleep.
    Function Inputs:
        The amount of time spend checking the Mode()
    Function Outputs:
        Time spent in the sleep mode after if finishes homing with no issues.
    '''
    
    # Turn all lights and sounds off, then turn on yellow lED
    Lights_Sound_Off()
    YellowLED.high()
    
    # Set the sleep mode error flag buffer to 1 so that if an issue occurs, the
    #   flag is already set.
    ErrSleep.put(1)
    
    # Turn all lights and sounds off, then turn on green lED
    Lights_Sound_Off()
    GreenLED.high()
    
    # Pre-Sleep mode: Wait in while loop for one of two exit conditions.
    #   1) User hits go
    #   2) User changes the system mode to something that isn't the sleep mode
#    print("Sleep mode pre-stage")
#    Timer = 0                   # Creating a timer variable
#    Start = utime.ticks_ms()    # Creating a starting reference time
    while True:
#        if Timer > 600000:  # 10 min * 60s/min * 1000ms/s
##            print("Timed Out, going to sleep")
#            break
        if Go() == 1:
#            print("Go pressed, going to sleep")
            break
        elif Mode() != 2:
#            print("Another mode selected, exiting function")
            return(1000)
        # increment Timer
#        print("Time in Sleep pre-stage: "+str(Timer)+" ms")
#        Current = utime.ticks_ms()
#        Timer = Current - Start + Timer
#        Start = Current
    
    # User must have hit go to have reached this point of the program. Turn of
    #   lights, turn yellow LED, then enter the new while loop that will try to
    #   home the system. Function will continue until the machine has been
    #   homed.
    # Ammendment, if the system spend 500ms or more in the while loop checking
    #   the Mode() function, then the system homes. Otherwise, if it spent less
    #   than that, it doesnt run the Home() function.
    if Input >= 500:
        Lights_Sound_Off()
        YellowLED.high()
        while True:
#            print("Time spend in main checking Mode() >500ms")
            
            # If the system enters sleep mode, Home
            Output =  Home("All")
            
            # Check Output for Error
            if type(Output) == str:
                # If error, do the whole error handeler and when user hits go
                #   2nd time, repeat (ie home again)
#                print("Error Homing, handle error")
                ErrorHandler()
                ErrSleep = 1
            elif type(Output) != str:
                # If there was no error, exit the loop and continue with the
                #   sleep function
                break
        
        # Reset Timer Clock
#        Timer = 0
#        Start = utime.ticks_ms()
        
    # Turn Ligths and Sounds off.
    Lights_Sound_Off()
    
    # Enter while loop and wait for user to change the mode before exiting the
    #   function
#    print("Everything is done, goin to sleep.")
    while True:
        if Mode() != 2:
            # User has selected another mode, set flag, calculate time one last
            #   time, and exit the sleep function while returning time spent in
            #   sleep mode
            ErrSleep.put(0)
#            Current = utime.ticks_ms()
#            Timer = Timer + Current-Start
#            print("User has changed the mode, waking up")
            return(600)
#        elif Mode() == 2 and Timer < 600:
#            # User has not selected another mode, increment the timer and sleep
#            #   for 500ms minus how long it took to do get the current time.
#            #   Also, if Timer > 600ms, the Timer will stop incrementing to
#            #   prevent possible issues.
#            Current = utime.ticks_ms()
#            Timer = Timer + Current-Start
#            if 500-(Current-Start) >= 0:
#                utime.sleep_ms(500-(Current-Start))
#            Start = Current
#            print("shh, i've been asleep for "+str(Timer)+" ms")
#//////////////////////////////////////////////////////////////////////////////
'''                              Main Program                               '''
#//////////////////////////////////////////////////////////////////////////////
#print("Hello World")
import pyb
import utime

# Pin Definition
print("Creating pins")

# Notable stepper driver pins

# LED Pin Definition
print("    creating LED pins")
RedLED = pyb.Pin (pyb.Pin.cpu.C4, mode = pyb.Pin.OUT_PP, 
                      pull = pyb.Pin.PULL_DOWN)

YellowLED = pyb.Pin (pyb.Pin.cpu.C2, mode = pyb.Pin.OUT_PP, 
                         pull = pyb.Pin.PULL_DOWN)

GreenLED = pyb.Pin (pyb.Pin.cpu.B0, mode = pyb.Pin.OUT_PP, 
                        pull = pyb.Pin.PULL_DOWN)

# Piezzo Buzzer
BuzzerPin = pyb.Pin(pyb.Pin.cpu.A3, mode = pyb.Pin.OUT_PP, 
                        pull = pyb.Pin.PULL_DOWN)
timBuzzer = pyb.Timer(2,freq = 1500)
BuzzerChannel = timBuzzer.channel(4, pyb.Timer.PWM, pin = BuzzerPin)
BuzzerChannel.pulse_width_percent(0)

# Solenoid and DC Motor Pin call outs and functions for controlling
#   said pins.
print("    Creating solenoid pins")
SolenoidLeftPin = pyb.Pin (pyb.Pin.cpu.D2, mode = pyb.Pin.OUT_PP,
                           pull = pyb.Pin.PULL_DOWN)
SolenoidLeftPin.high()
        
SolenoidRightPin = pyb.Pin (pyb.Pin.cpu.B6, mode = pyb.Pin.OUT_PP,
                            pull = pyb.Pin.PULL_DOWN)
SolenoidRightPin.high()

print("    Creating DC motor pins")
DCMotorLeftPin = pyb.Pin (pyb.Pin.cpu.C11, mode = pyb.Pin.OUT_PP,
                          pull = pyb.Pin.PULL_DOWN)
DCMotorLeftPin.high()
        
DCMotorRightPin = pyb.Pin (pyb.Pin.cpu.B7, mode = pyb.Pin.OUT_PP,
                           pull = pyb.Pin.PULL_DOWN)
DCMotorRightPin.high()

# Creating the Go button function call. Go() should give 0 or 1 depending on 
#   the pin input. Basically, equating Go_Pin.value() to Go() so I do less
#   typing.
print("    Creating go pin")
Go_Pin = pyb.Pin(pyb.Pin.cpu.C4, mode = pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
Go = Go_Pin.value

'''Three Position Swtich Pin'''
print("    Creating 3 pos switch pin")
ThreeSwitch_Pin = pyb.Pin(pyb.Pin.cpu.C3, mode = pyb.Pin.ANALOG)
adc = pyb.ADC(ThreeSwitch_Pin)
ThreeSwitch = adc.read

# Check Files
Output = FileCheck()

# Check Output of function FileCheck() for an error in the shape of a string
if type(Output)==str:
    # If there was an error, handle it
#    print("error with files, error handled by special exception error error"+
#          " handling section of FileCheck()")
    
    # If there was an error and the user hit the go twice, do a soft reset,
    #   restarting the program from the beginning.
#    print("SOFT RESET!!!!")
    import sys
    sys.exit()
    
# If there was no error, create all items
print("    creating class objects")


'''Stepper Driver pin and  object creations'''
import l6470nucleo                  # Import file
SCK= pyb.Pin(pyb.Pin.cpu.B5)        # stby_rst_pin 
ncs1= pyb.Pin(pyb.Pin.cpu.A10)      # cs_pin for board 1
ncs2= pyb.Pin(pyb.Pin.cpu.A4)       # cs_pin for board 2
Board1 = l6470nucleo.Dual6470(1,ncs1,SCK) # Controls the Gantry (2) and
                                          # Beam Actuator (1)
Board2 = l6470nucleo.Dual6470(1,ncs2,SCK) # Controls Left (1) and Right
                                          # (2) rail actuators
                                          # Beam Actuator (1)
paramatarize()
Board1.HardHiZ(1)
Board1.GetStatus(1)
Board1.HardHiZ(2)
Board1.GetStatus(2)
Board2.HardHiZ(1)
Board2.GetStatus(1)
Board2.HardHiZ(2)
Board2.GetStatus(2)

print("    creating interrupt for emergency stop")
# The same as the Go pin, but greating a short function call for the emergency
#   stop button. This pin is defined last as to prevent memory issues found
#   importing task_share.
Stop_Pin = pyb.Pin(pyb.Pin.cpu.C5, mode = pyb.Pin.IN, pull = pyb.Pin.PULL_UP)

'''External Interrupt Pin'''
import micropython
micropython.alloc_emergency_exception_buf(100)
extint = pyb.ExtInt(Stop_Pin, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP,
                    callback)

print("    importing misc files")
import Import

# Zero the above buffers
zero_flags()
"""
# Turn on only the yellow LED
Lights_Sound_Off()
YellowLED.high()

# Set error flag for the initilization phase
#ErrInit = 1

# Set Timer measured in milliseconds. Initially set at 600 so the system
#   homes the first time round.
Timer = 600

#print("Beginning main program")
# 1st Layer while loop
while True:
    # Check Timer
    if Timer >= 500:
        # Turn on Yellow LED
        Lights_Sound_Off()
        YellowLED.high()
        
        # home loop
        while True:
            # If Timer >= 5 sec, 
            Output = Home('All')
            
            # Check Output of function for error
            if Output == "Error Occured":
                # Error, do stuff
                ErrorHandler()
            else:
                # No error, break this 'home loop' and exit back to the 1st
                #   layer.
                break
            # End of 'home loop'
        
#        # Create Timer Variables
#        import utime
#        Start = utime.ticks_ms()
#        Timer = 0
        
        # Turn on the Green Light
        Lights_Sound_Off()
        GreenLED.high()

        # 2nd Layer While Loop to check mode
        while True:
            
            # Check mode by calling a function which checks the three position
            #   switch
            if Mode() == 1:
                # If switch is in 1st position...
                # Run Calibration Mode
                Calibration_Mode()
                
                # Set Timer > 500 so the system homes after the calibration
                #   mode
                Timer = 600
                
                # break out of 2nd layer back to 1st layer
                break
                
            if Mode() == 2:
                # If switch is in 2nd position...
                Timer = Sleep_Mode(600)
                
                # break out of 2nd layer back to 1st layer
                break
            
            if Mode() == 3:
                # If switch is in 3rd position...
                # Run Leveling Mode
                Leveling_Mode()
                
                # Run Assembly Mode
                Assembly_Mode()
                
                # Set Timer > 500 so the system homes after the assembly
                #   mode
                Timer = 600
                
                # break out of 2nd layer back to 1st layer
                break
            
            # Increment Timer if no mode is selected
#            Current = utime.ticks_ms()
#            Timer = (Current - Start) + Timer
            
            # End of the 2nd Layer
        
        # End of 1st Layer
        """