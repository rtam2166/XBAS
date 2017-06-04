# -*- coding: utf-8 -*-
"""
Created on Mon May 29 19:32:20 2017

@author: drago
"""
def zero_flags():
    '''Function sets all error flag buffers to false aka 0 or its equivalent.
    No input paramaters or returned values. Does require for the task_share.py
    file to be present and the main section of this program to have been run
    so that the buffers exist.'''
    
    ErrInit.put(0)
    ErrSleep.put(0)
    ErrLeveling.put(0)
    ErrAssembly.put(0)
    ErrBoltCsv.put(0)
    ErrCalCsv.put(0)
    ErrGantry.put(0)
    ErrProbe.put(0)
    ErrRailActL.put(0)
    ErrRailActR.put(0)
    ErrBeamAct.put(0)
    ErrFileCheck.put(0)
    ErrSong.put(0)
    XBeam.put(0)
    print("Flags Zeroed")

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
        RedLED.high()
        YellowLED.high()
        GreenLED.high()
        switch = 0
        go = 0
        Time = 0
        while True:
            start = utime.ticks_ms()
            if switch == 0 and go == 0:
                Buzzer('on')
            elif switch == 1 and go == 0:
                Buzzer('off')
            else:
                Buzzer('off')
            if Go() == 1 and go == 0:
                go = 1
                Buzzer('off')
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

            
def paramatarize():
    '''Function paramatrizes the l6470nucleo.Dual6470 objects
    Function Inputs:
        None
    Function Outputs:
        None
        '''
    print('    parameterizing')
    # Set the registers which need to be modified for the motor to go
    # This value affects how hard the motor is being pushed
    print('    parameterizing board 1')
    K_VAL = 65
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
    
    # Set the minimum speed at which motor will run
    MIN_SPEED = 15
    Board1._set_par_2b ('MIN_SPEED', MIN_SPEED)
        
    # Set the maximum acceleration and deceleration of motor
    ACCEL = 1
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
    
    print('    parameterizing board 2')
     # Set the registers which need to be modified for the motor to go
        # This value affects how hard the motor is being pushed
    K_VAL = 60
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
    ACCEL = 12
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
    
def DCMotor(Side,Dir):
    '''Function for running the DC motors
    Function Inputs:
        Side can be any of the following and indicates which DC motor
            is being called upon.
            1) "Left", "left", "l", and "L" calls on the left motor
            2) "Right", "right", "r", and "R" calls on the right motor
            3) Anything else turns off both motors regardless of the 
                value of Dir
        Dir Indicates if the DC motors selected by Side is turned on or
            off. Takes the following inputs:
            1) "On" or "on" will turn the motor selected on
            2) "Off" or "off" will turn the selected motor off
    Function Outputs:
        None
        '''
    if Side == "Left" or Side == "left" or Side == "l" or Side == "L":
        if Dir == "on" or Dir == "On":
            DCMotorLeftPin.low()
        elif Dir == "off" or Dir == "Off":
            DCMotorLeftPin.high()
    elif Side == "Right" or Side == "right" or Side == "r" or Side == "R":
        if Dir == "on" or Dir == "On":
            DCMotorRightPin.low()
        elif Dir == "off" or Dir == "Off":
            DCMotorRightPin.high()
    else:
        DCMotorLeftPin.high()
        DCMotorRightPin.high()
            
def Solenoid(Side,Dir):
    '''Function for running the solenoids
    Function Inputs:
        Side can be any of the following and indicates which solenoid
            is being called upon.
            1) "Left", "left", "l", and "L" calls on the left solenoid
            2) "Right", "right", "r", and "R" calls on the right solenoid
            3) Anything else turns off both solenoids regardless of the 
                value of Dir
        Dir Indicates if the Solenoid selected by Side is turned on or
            off. Takes the following inputs:
            1) "On" or "on" will turn the solenoid selected on
            2) "Off" or "off" will turn the selected solenoid off
    Function Outputs:
        None
        '''
    if Side == "Left" or Side == "left" or Side == "l" or Side == "L":
        if Dir == "on" or Dir == "On":
            SolenoidLeftPin.low()
        elif Dir == "off" or Dir == "Off":
            SolenoidLeftPin.high()
    elif Side == "Right" or Side == "right" or Side == "r" or Side == "R":
        if Dir == "on" or Dir == "On":
            SolenoidRightPin.low()
        elif Dir == "off" or Dir == "Off":
            SolenoidRightPin.high()
    else:
        SolenoidLeftPin.high()
        SolenoidRightPin.high()
            
def Buzzer(Input,duty = 50):
    '''Function runs the buzzer, turning it on or off depending on the inputs.
    Function Inputs:
        Input can be one of the following.
            1) "On", or "on" indicate that the buzzer should turn on
            2) Anything else turns the buzzer off
        duty defaults to 100 and represents the duty cycle of the pwm wave
            controlling the buzzer. The function restricts the values of duty
            to be between 0 and 100 percent
            '''
    if Input == "On" or Input == "on":
        if duty > 100:
            duty = 100
        if duty < 0:
            duty = 0
        BuzzerChannel.pulse_width_percent(duty)
    else:
        BuzzerChannel.pulse_width_percent(0)

def callback(line):
    '''This is a function which runs during interrupts. This should occur when
    the emergecny stop button is pressed down. It waits until the emergency
    stop has been disengaged and initiates a soft restart'''
    print("Emergency Stop pressed...")
    RedLED.high()
    while True:
        if Stop_Pin.value() == 0:
            print("... and released")
            RedLED.low()
            break

    import pyb
    pyb.hard_reset()
    
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
        
import pyb
import utime
start = utime.ticks_ms()
# Pin Definition
print("Creating pins")

# Notable stepper driver pins

# LED Pin Definition
print("    creating LED pins")
RedLED = pyb.Pin (pyb.Pin.cpu.A8, mode = pyb.Pin.OUT_PP, 
                      pull = pyb.Pin.PULL_DOWN)

YellowLED = pyb.Pin (pyb.Pin.cpu.B10, mode = pyb.Pin.OUT_PP, 
                         pull = pyb.Pin.PULL_DOWN)

GreenLED = pyb.Pin (pyb.Pin.cpu.B4, mode = pyb.Pin.OUT_PP, 
                        pull = pyb.Pin.PULL_DOWN)

YellowLED.high()
RedLED.low()
GreenLED.low()

# Piezzo Buzzer
BuzzerPin = pyb.Pin(pyb.Pin.cpu.A1, mode = pyb.Pin.OUT_PP)
timBuzzer = pyb.Timer(5,freq = 2730)
BuzzerChannel = timBuzzer.channel(2, pyb.Timer.PWM, pin = BuzzerPin)
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
print("Creating class objects")

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
Board1.GetStatus(1,verbose = 0)
Board1.HardHiZ(2)
Board1.GetStatus(2,verbose = 0)
Board2.HardHiZ(1)
Board2.GetStatus(1,verbose = 0)
Board2.HardHiZ(2)
Board2.GetStatus(2,verbose = 0)

print("    creating interrupt for emergency stop")
# The same as the Go pin, but greating a short function call for the emergency
#   stop button. This pin is defined last as to prevent memory issues found
#   importing task_share.
Stop_Pin = pyb.Pin(pyb.Pin.cpu.C5, mode = pyb.Pin.IN, pull = pyb.Pin.PULL_DOWN)

'''External Interrupt Pin'''
import micropython
micropython.alloc_emergency_exception_buf(100)
extint = pyb.ExtInt(Stop_Pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN,
                    callback)
    
import task_share
# Variable Buffer Creation
ErrInit = task_share.Share ('i', thread_protect = False,
                            name = "Initilization Error Flag")
ErrSleep = task_share.Share ('i', thread_protect = False,
                             name = "Sleep Error Flag")
ErrCalibration = task_share.Share ('i', thread_protect = False,
                             name = "Sleep Error Flag")
ErrLeveling = task_share.Share ('i', thread_protect = False,
                                name = "X-Beam Leveling Error Flag")
ErrAssembly = task_share.Share ('i', thread_protect = False,
                                name = "X-Beam Error Flag")
ErrBoltCsv = task_share.Share ('i', thread_protect = False,
                               name = "BoltPattern.csv Error Flag")
ErrCalCsv = task_share.Share ('i', thread_protect = False,
                              name = "Calibration.csv Error Flag")
ErrGantry = task_share.Share ('i', thread_protect = False,
                              name = "Gantry Error Flag")
ErrProbe = task_share.Share ('i', thread_protect = False,
                             name = "Probe Error Flag")
ErrRailActL = task_share.Share ('i', thread_protect = False,
                                name = "Left Rail Actuator Error Flag")
ErrRailActR = task_share.Share ('i', thread_protect = False,
                                name = "Right Rail Actuator Error Flag")
ErrBeamAct = task_share.Share ('i', thread_protect = False,
                               name = "X-Beam Actuator Error Flag")
ErrSong = task_share.Share ('i', thread_protect = False,
                            name = "Incorrect Piano Board Input Flag")
ErrFileCheck = task_share.Share ('i', thread_protect = False,
                                 name = "File Check Error Flag")

# This buffer contains the value of the X-Beam Length indicated by the
#   combination of switches on the piano switch board.
XBeam = task_share.Share ('i', thread_protect = False,
                          name = "X-Beam Length")
current = utime.ticks_ms()
print('importing setup.py took '+str((current - start)/1000)+' seconds')
