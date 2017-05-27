# -*- coding: utf-8 -*-
##
#  @file main.py
#  @author Robert Tam
#  This program was written for an ME Senior Project.

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
    V3 = 3.3  # Third position
    V2 = 1.65 # Second position
    V1 = 1.1  # First position
    
    # The tolerance indicating the range of acceptable values
    tolerance = 0.25 # volts
    
    # Voltages and tolerances converted to value from 0 to 4095
    TickPerVolt = V1/4096
    V3 = V3/TickPerVolt
    V2 = V2/TickPerVolt
    V1 = V1/TickPerVolt
    tolerance = tolerance/TickPerVolt
    print("First Position value in ticks: "+str(V1))
    print("Second Position value in ticks: "+str(V2))
    print("Third Position value in ticks: "+str(V3))
    print("Three Pos Switch read value in ticks: "+str(value))
    
    # Check if the first position has been selected
    if value =< V1 + tolerance and value >= V1 - tolerance:
        print("Selected Mode 1")
        return(1)
           
    # Check if the second position has been selected
    elif value =< V2 + tolerance and value >= V2 - tolerance:
        print("Selected Mode 2")
        return(2)
           
    # Check if the third position has been selected
    elif value =< V3 + tolerance and value >= V3 - tolerance:
        print("Selected Mode 3")
        return(3)
           
    else:
        print("No Mode Selected")
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
    FileList = ["task_share.py",
                "main.py",
                "boot.py",
                "ImportSong.py",
                "l6470nucleo.py"]
                
    # Retrieve the system directory information as a list of strings
    files = os.listdir()
    
    # Open the Error Report text file in preparation of writing errors to
    f = open("Error Report.txt",'w')
    for file in FileList:
        
        if file in files == True:
            # If the file being checked is on the pyboard
            pass
        
        if file in files == False:
            # If the file being checked is not on the pyboard
            if Switch == 0:
                f.write('There was an error during the system initilization'+\
                        '\n\r')
                Switch = 1
            f.write("The file "+file+" is missing\n\r")
            print("The file "+file+" is missing")
            
            # If special action is required for a file, add an if statement
            #   here which checks for said file to write that specific
            #   recommended action here.
            
            f.write("Recommended action: Copy"+file+" from a backup onto the"+
                    " pyboard\n\r\n\r")
            
            # Written Error report should look like...
            #   There was an error during the initilization phase
            #   The file main.py is missing
            #   Recommened action: Copy main.py from a backup onto the pyboard
    
    # Finished writing to Error Report, close the text file
    f.close()
    
    if Switch != 0:
        # If there was an error, set flag
        ErrFileCheck.put(1)
        print("File Check Done, error occured")
        return("An Error Occured, please see the 'Error Report.txt' file")
    else:
        print("File Check Done, no errors")
        return(0)

def ImportBoltPattern():
    '''This function imports a bolt pattern file based on the value of buffer
    X-Beam. This is done by using the Python try function to attempt to import
    the bolt pattern file assotiated with the input given which should be the
    length of the X-Beam being worked upon. The input is from the
    ImportSwitchBoard() function. Example of how this would work is shown
    below.
    
    # Value in XBeam buffer is 500
    Input = XBeam.get()
    String = "BoltPattern"+str(Input)+".csv"
        i.e. BoltPattern500.csv
        
    After figureing out the file name, it tries to import the file. If the file
    exists, the function returns a list of integers. If the file does not 
    exist, then the program returns an error message
    
    @input  Function reads buffer X-Beam for the necessary input which should
            be the length of the X-Beam
    @return Function returns a string if there was an error and writes a
            message to the Error Report text file. If there was no error, the 
            function returns a list with two sub-lists, one containing strings
            of which side is to be bolted and the other containing positions
            relative to the gantry's zero position of where to move to.
    '''
                  
    print("Beginning to import BoltPatternXXX.csv")
    # Getting length value of the X-Beam from the buffer XBeam
    Input = XBeam.get()
    print("Working X-Beam "+str(Input))
    
    # Creating the name of the file to be imported
    FileName = "BoltPattern"+str(Input)+".csv"
    print("File name assotiated with X-Beam: "+FileName)
    
    # a function unique binary error flag indicating which error has occured.
    error = 0
    
    '''Open Error Report for editing'''
    f = open("Error Report.txt","w")
    print("File Opened, checking values")
    
    try:
        '''Attempt to import the BoltPattern file indicated by the input.'''
        with open(FileName,'r') as file:
            '''File does exist, process the data as indicated'''
            i = 1
            print("File Opened, splitting values into two seperate lists")
            for line in file:
                line = line.split(',')
                line[-1] = (line[-1].replace("\n",''))
                line[-1] = (line[-1].replace("\r",''))
                if i == 1:
                    BoltSide = line
                elif i == 2:
                    BoltData = line
                print("Line "+str(i)+" processed")
                i = i+1
               
    except FileNotFoundError:
        '''File doesn't exist, write to Error Report'''
        print("Unable to open BoltPatternXXX.csv file")
        ErrBoltCsv.put(1)
        string = "Error, Missing "+FileName
        f.write(string)
        f.close()
        return("Missing file error")
    
    '''Check the values in the BoltSide list. If there is an error, write
    to the Error Report text file.'''
    print("Checking items indicating sides in the BoltSide list")
    i = 1
    for item in BoltSide:
        if item != "R" and item != "L":
            ErrBoltCsv.put(1)
            string = "Error in "+FileName+", row 1 item "+str(i)+": '"+\
                        str(item)+"' is not a valid input"
            f.write(string)
            error = 1
            print("Item "+str(i)+" checked, "+string)
        else:
            print("Item "+str(i)+" checked, no errors")
        i = i+1
        
    '''Check the values in the BoltData list. If there is an error, write
    to the Error Report text file.'''
    print("Checking items indicating positions in the BoltData list")
    i = 1
    for item in BoltData:
        try:
            float(item)
        except ValueError:
            ErrBoltCsv.put(1)
            string = "Error in "+FileName+", row 2 item "+str(i)+": '"+\
                        str(item)+"' is not a valid input"
            f.write(string)
            error = 1
            print("Item "+str(i)+" checked, "+string)
        else:
            print("Item "+str(i)+" checked, no errors")
        i = i+1
    
    '''If there were no issues in the lists, return the two lists'''
    if error == 0:
        print("No Errors importing "+FileName)
        return([BoltSide,BoltData])
    elif error != 0:
        print("An error has occured, exiting function")
        f.close()
        return("An Error Occured, please see the 'Error Report.txt' file")

def ImportCalibration():
    '''This function imports a calibration file based on the value stored in
    the XBeam buffer. This is done by using the Python try function to attempt
    to import the calibration file assotiated with the input given which should
    be the length of the X-Beam being worked upon. The input is from the 
    ImportSwitchBoard() function. Example of how this would work is shown 
    below.
    
    # Value in XBeam buffer is 500
    Input = XBeam.get()
    String = "Calibration"+str(Input)+".csv"
        i.e. Calibration500.csv
        
    After figureing out the file name, it tries to import the file. If the file
    exists, the function returns a list of integers. If the file does not 
    exist, then the program returns an error message
    
    @input  This function takes inputs in by reading the buffer XBeam for the
            necessary information which is an integer indicating XBeam length
    @return This function returns a string if there was an error. If not, the
            function returns a list of values'''            
                  
    print("Beginning to import CalibrationXXX.csv")

    # Getting length value of the X-Beam from the buffer XBeam
    Input = XBeam.get()
    print("Working X-Beam "+str(Input))

    # Creating the name of the file to be imported
    FileName = "Calibration"+str(Input)+".csv"
    print("File name assotiated with X-Beam: "+FileName)

    # a function unique binary error flag indicating which error has occured.
    error = 0

    try:
        '''Attempt to import the Calibration file indicated by the input.'''
        with open(FileName,'r') as file:
            '''File does exist, process the data as indicated'''
            print("File Opened, processing data and checking items")
            for line in file:
                String = str(line)              # Bring in line of info from csv
                                                #    file
                List = String.split(',')      # Split line of info at the comma
                String = []
                i = 0
                for item in List:
                    '''Go through each item in List of info and try to make each
                    item a float. If not, return an error message indicating
                    which item was invalid.'''
                    try:
                        '''Try to turn the item into a float'''
                        List[i] = float(item)
                        print("Item "+str(i)+" checked and is valid")
                      
                    except ValueError:
                        '''Error indicating invalid input'''
                        String.append("Error in "+FileName+" Line "+str(i+1)+
                                      ": '"+item+"' is not a valid input")
                        ErrCalCsv.put(1)
                        print("Error in "+FileName+" Line "+str(i+1)+
                                      ": '"+item+"' is not a valid input")
                        error = 1
                      
                    except TypeError:
                        '''Error indicating invalid input'''
                        String.append("Error in "+FileName+" Line "+str(i+1)+
                                      ": '"+item+"' is not a valid input")
                        ErrCalCsv.put(1)
                        print("Error in "+FileName+" Line "+str(i+1)+
                                      ": '"+item+"' is not a valid input")
                        error = 1
                  
                    i = i+1
              
    except FileNotFoundError:
        '''Exception to report that the file is missing'''
        print("Unable to open CalibrationXXX.csv file")
        String = ["Error,Missing Calibration"+str(Input)+".csv File"]
        ErrCalCsv.put(1)
        error = 1
    
    if error == 0:
        print("No error importing "+FileName)
        return(List) # return the final list of values
                  
    elif error != 0:
        f = open("Error Report.txt","w")
        for item in String:
            f.write(item)
        f.close()
        print("Error Occured importing "+FileName)
        return("Error Occured")
    else:
        return('''Error Occured, error flag in ImportCalibration was not 0 or 1
               at the end of the function''')
    
def Lights_Sound_Off():
    '''Turns all LEDs and the buzzer off
    Function has no input paramaters or returned values'''
    RedLED.Low()
    YellowLED.Low()
    GreenLED.Low()
    Buzzer("Off")
    print("All Lights and Sound have been turned off")
    
def Lights_Sound_Action():
    '''This function turns on various LEDs and controls the buzzer depending on
    the error flags which have been raised. Function has no input paramaters or
    returned values'''
    print("Lights_Sound_Action() has been called. Let the show begin.")
    Lights_Sound_Off()      # Turn lights off
    Switch = 0              # Switch is bolean variable that switches each run
                            #   of the LEDs and buzzer so the system knows to
                            #   alternate
    Green = 0               # Valriable that says the green LED is to be used
    Yellow = 0              # Valriable that says the yellow LED is to be used
    Red = 0                 # Valriable that says the red LED is to be used
    Blink = 0               # Variable that says LEDs need to blink
    Stop = 0                # Variable that counts number of Go's pressed to 
                            #   exit function
    if ErrFileCheck.get() == 1:
        # If the file check error flag is raised, tell system to turn on all
        #   LEDs, no blinking
        Green = 1
        Yellow = 1
        Red = 1
        print("File Error detected")
    elif ErrGantry.get() == 1:
        # If the Gantry error flag is raised, tell system to turn on green and
        #   yellow LEDs, no blinking
        Green = 1
        Yellow = 1
        print("Gantry Error detected")
    elif ErrProbe.get() == 1:
        # If Probe flag raised, yellow and red LED, no blinking
        Yellow = 1
        Red = 1
        print("Probe Error detected")
    elif ErrBeamAct.get() == 1:
        # If beam actuator flag raised, green and red LED, no blinking
        Green = 1
        Red = 1
        print("Beam Actuator Error detected")
    elif ErrSong.get() == 1:
        # If Song error flag raised, all LEDs on, blinking
        Green = 1
        Yellow = 1
        Red = 1
        Blink = 1
        print("Piano Switch Board Combination Error detected")
    elif ErrRailActR.get()==1 or ErrRailActL.get() == 1:
        # If Either rail actuator flags are raised
        Green = 1
        Yellow = 1
        Red = 0
        Blink = 1
        print("One or Both of the Rail Actuators Error detected")
    else:
        # No error, Set Green LED, turn noise on 1 sec
        print("No Error detected, doing the green light and 1 second beep")
        GreenLED.High()
        Buzzer On
        utime.sleep(1000)
        Buzzer Off
        return()
        
    while True:
        Start = utime.ticks_ms()
        
        # Check Switch for what to do
        if Switch == 0:
            # Check Buzzer for if it should run or not. Should not run if Stop
            #   is not 0 meaning user hit go at some point.
            if Stop == 0:
                Buzzer("On")
                print("Sound On")
            else:
                print("Sound Off")
                Buzzer("Off")
            print("LEDs On")
            # Check what LEDs should be on
            if Green == 1:
                GreenLED.High()
            if Yellow == 1:
                YellowLED.High()
            if Red == 1:
                RedLED.High()
        else:
            # Buzzer should be off
            print("Sound Off")
            Buzzer("Off")
                
            # Check what LEDs should be blinking. If so, then the LEDs now
            #   need to be off.
            print("LEDs off")
            if Blink == 1:
                if Green == 1:
                    GreenLED.Low()
                if Yellow == 1:
                    YellowLED.Low()
                if Red == 1:
                    RedLED.Low()
            # Else just fall through to next part of the function
        print("Go pressed: "+str(Stop)+"\n\r")
                  
        Current = utime.ticks_ms()
        # Wait in the below while loop until the difference in time from the 
        #   beggining of the while loop to present >= 500ms or user hits go
        while True:
            if Go() == 1:
                if Stop == 0:
                    Stop = 1
                elif Stop != 0:
                    Stop == 2
                break
            elif (Current - Start) >= 500:
                break
            Current = utime.ticks_ms()
        
        # If user has hit go twice during the above while loop, exit function.
        #   i.e. hit it once, than hit it again when the function loops back to
        #   the above nested loop.
        if Stop == 2:
            Lights_Sound_Off()
            YellowLED.High()
            print("Exiting Lights_Sound_Action()")
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
    print("Beginning Error Handling")
    print("ErrInit =     "+str(ErrInit.get()))
    print("ErrSleep =    "+str(ErrSleep.get()))
    print("ErrCal =      "+str(ErrCal.get()))
    print("ErrLeveling = "+str(ErrLeveling.get()))
    print("ErrAssembly = "+str(ErrAssembly.get()))
    print("ErrProbe =    "+str(ErrProbe.get()))
    print("ErrGantry =   "+str(ErrGantry.get()))
    print("ErrBeamAct =  "+str(ErrBeamAct.get()))
    print("ErrRailActR = "+str(ErrRailActR.get()))
    print("ErrRailActL = "+str(ErrRailActL.get()))
                  
    # There was no issues with all of the named error flags, check all of the
    #   other error flags
    if ErrFileCheck.get() == 0 and  \
       ErrSong.get() == 0 and       \
       ErrBoltCsv.get() == 0 and    \
       ErrCalCsv.get() == 0:
                                   
        f = open("Error Report.txt","w")
        
        if ErrInit.get() == 1:
            f.write("There was an error during the system initilization\n\r")
        elif ErrSleep.get() == 1:
            f.write("There was an error with the sleep mode\n\r")
        elif ErrCal.get() == 1:
            f.write("There was an error with the calibration mode\n\r")
        elif ErrLeveling.get() == 1:
            f.write("There was an error with leveling the X-Beam during the"+
                     " Assembly mode\n\r")
        elif ErrAssembly.get() == 1:
            f.write("There was an error with assembling the X-Beam during the"+
                    " Assembly mode\n\r")
            
        if ErrProbe.get() == 1:
            f.write("Probe was unable to take valid measurements")
        elif ErrGantry.get() == 1:
            f.write("Gantry was unable to move to the destination")
        elif ErrBeamAct.get() == 1:
            f.write("Beam Actuator was unable to move to the destination")
        elif ErrRailActR.get() == 1 or ErrRailActL.get() == 1:
            if ErrRailActR.get() == 1 and ErrRailActL.get() == 1:
                x = "Both rail actuators"
            elif ErrRailActR.get() == 1:
                x = "The right rail actuator"
            elif ErrRailActL.get() == 1:
                x = "The left rail actuator"
            f.write(x+"Has attempted run past the maximum stroke length allowed")
        else:
            f.write("A possible issue has occurred where the system has not "+
                    "been accounted for all the\n\rpossible errors. Please "+
                    "identify and name the new error")
        f.close()
            
    # There were issues with any of the named files
    elif ErrFileCheck.get() == 1 or \
         ErrSong.get() == 1 or      \
         ErrBoltCsv.get() == 1 or   \
         ErrCalCsv.get() == 1:
        pass    # The above files have already written their error reports, so 
                #   they don't need to do anything here
    
    # After finishing up writing to the Error Report text file, now run the 
    #   function responsible for turning on and off the LEDs and sound.
    Lights_Sound_Action()
    
    # Now Home the system
    Home("All")
        
def callback():
    '''This is a function which runs during interrupts. This should occur when
    the emergecny stop button is pressed down. It waits until the emergency
    stop has been disengaged and initiates a soft restart'''
    print("Emergency Stop On")
    while True:
        if Emergency_Stop() == 0:
            break
    # Soft reset
    print("Emergency Stop Off")
    import sys
    sys.exit()

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
    MoveProbe("Down")
    
    tolerance = 0
    previous = 0
    while True:
        # wait for readings from probe to change (delta) by the tolerance amount
        current = ProbeEncoder.read()
        delta = current-previous
        print("        delta = "+str(delta))
        if delta <= tolerance or delta >= -tolerance:
            print(
            break
        
    
    # Check Reading is within the limits if the Limit flag is true
    if Limit = True
        if Reading > UpperLimit:
            print("    probe reading was above upper limit of readings")
            ErrProbe.put(1)
        elif Reading < LowerLimit:
            print("    probe reading was below lower limit of readings")
            ErrProbe.put(1)

    print("    Raising probe")
    MoveProbe("Up")
    
    while True:
        # wait until the probe has fully withdrawn to the reference tick.
        if ProbeReference.value() == 1:
            print("    Reference tick reached")
            break
    
    # If there was or was not an error
    if ErrProbe.get() == 0:
        print("    No error, exit")
        # No error, return
        return(Reading)
    else:
        # Error, return error message
        print("    Error Error Error Error")
        return("Error Occured")
        
def Move_Gantry_To(Destination, probe = False):
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
    StepsPerRev = 200           # Variable indicating the number of steps
                                #   per revolution for the stepper motor. This
                                #   is # of full steps per revolution.
    xOffset = 00000     # Distance from gantry home position to the closest end
                        #   of the X-Beam.
    xLimit = 00000      # Maximum travel of the gantry from the end of the
                        #   X-Beam to the Lead Screw Raiser minus the gantry 
                        #   width
    ISSUE See above 2 variables
    
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
    Destination = ((Destination + xOffset)/DistancePerRev)*StepsPerRev
    print("    Destination converted to "+str(Destination)+" number of steps")
    
    # Move to the new value of Destination
    print("    Moving Gantry to Destination")
    Board1.GoTo(1,Destination)
    
    # Wait for stall or finish flag
    print("    waiting for stall or completion of move command")
    while True:
        if Busy_Pin.value() == 1:
            # if finish, exit the function
            print("    Gantry in position, exit loop")
            break
        elif Board1.isStalled(1) == True:
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
        if ErrCal.get() == 1:
            print("    Probe called for Calibration Mode")
            reading = Probe()
        elif ErrAssembly.get() == 1 or ErrLeveling.get() == 1:
            print("    Probe called for Leveling and Assembly Mode")
            UpprLimit = ISSUE
            LwrLimit = ISSUE
            reading = Probe(Limit = True, UpperLimit = UpprLimit,LowerLimit = LwrLimit)

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
    
    print("Beginning to Home system")
    # Import time for all the sleep commands we will do
    import utime
                
    # Set the stall thresholds of the stepper drivers to the maximum
    #   ammount (which they should be already)
    Board1._setStallThreshold(16)
    Board2._setStallThreshold(16)
    
    # First Home Probe if Probe or all is listed in *arg
    if ('Probe' in arg) or ('All' in arg):
        print("    Homing the Probe")
        # If the probe registers at home, do nothing. If not, retract probe
        #   is at home
        if ProbeReference.value == 1:
            # True, do nothing
            print("        Probe is at reference tick, go to next object")
            pass
        else:
            # False, Retract Probe until it is at the reference tick
            print("        Probe is not at reference tick, raise probe")
            MoveProbe("Up")
            
            # While loop to check the probe for when its reaches reference
            #   tick
            while True:
                if ProbeReference.value == 1:
                    # True
                    print("        Probe is at reference tick, go to next object")
                    break
            
    # Now Home Righ and Left rail actuator
    print("    Homing one or both rail actuators")
    if ('RailActR' in arg) or ('All' in arg) or ('RailAct' in arg):
        # Home right actuator. Speed is up for debate
        print("        Homing the right rail actuator")
        Board2.GoUntil(2,-400)
                
    if ('RailActL' in arg) or ('All' in arg) or ('RailAct' in arg):
        # Home left actuator
        print("        Homing the left rail actuator")
        Board2.GoUntil(1,-400)
                
    if ('RailActR' in arg) or ('RailActL' in arg) or ('All' in arg) or \
        ('RailAct' in arg):
        print("        checking rail actuators for completion of move")
                
        # Check home status in while loop
        while True:
            if Busy_Pin.value() == 1:
                # Both rail actuators are @ their switches, continue.
                print("        actuator switches have been pressed, busy pin high")
                break
    
        # Rail Actuator @ swithces, release switch to back them off of
        #   switch which is their homed position.
        if ('RailActR' in arg) or ('All' in arg) or ('RailAct' in arg):
            # Release Switch Right
            print("        releasing right switch")
            Board2.ReleaseSW(2,1)
                
        if ('RailActL' in arg) or ('All' in arg) or ('RailAct' in arg):
            # Home left actuator
            print("        releasing left switch")
            Board2.ReleaseSW(1,1)
        
        # Check status via while loop
        while True:
            if Busy_Pin.value() == 1:
                print("        actuator switches have been pressed, busy pin high")
                break
            
    # Home screwdriver DC Motors and Solenoids
    if ('Screwdrivers' in arg) or ('All' in arg):
        # Turn of both DC motors and solenoids
        print("    Turning off all DC motors and Solenoids for srewdrivers")
        DCMotorRight("Off")
        DCMotorLeft("Off")
        SolenoidRight("Off")
        SolenoidLeft("Off")
        
    # Home Gantry
    if ('Gantry' in arg) or ('All' in arg):
        print("    Homing Gantry")
        # Home Gantry Code. +/- 400 is the max speed of the gantry
        print("        Gantry GoUntil switch command")
        Board1.GoUntil(1,-400)
        
        # Check home status in while loop
        while True:
            if Busy_Pin.value() == 1:
                # gantry at switch, continue.
                print("        Gantry completed GoUntil Command")
                break
            elif Board1.isStalled(1) == True:
                # motor stalled, return an error and set flag
                Board1.HardHiZ(1)
                print("        Gantry Stalled during Home command")
                print("        ERROR ERROR ERROR, return error")
                ErrGantry.put(1)
                return("Error Occured")

        # Release switch for gantry
        print("        releasing switch for gantry")
        Board1.ReleaseSW(1,1)

        # Check home status in while loop
        while True:
            if Busy_Pin.value() == 1:
                # Both rail actuators are homed, continue.
                print("        Gantry completed ReleaseSW Command")
                break
            elif Board1.isStalled(1) == True:
                # motor stalled, return an error and set flag
                Board1.HardHiZ(1)
                print("        Gantry Stalled during Home command")
                print("        ERROR ERROR ERROR, return error")
                ErrGantry.put(1)
                return("Error Occured")
        
    # Home Beam Actuator
    if ('Bact' in arg) or ('All' in arg):
        print("    Homing Beam Actuator")
        # Home beam actuator Code.
        Board1.GoUntil(2,-400)
        
        # Check home status in while loop
        while True:
            if Busy_Pin.value() == 1:
                # Both rail actuators are homed, continue.
                break
            elif Board1.isStalled(2) == True:
                # motor stalled, return an error and set flag
                Board1.HardHiZ(2)
                print("        Beam Actuator Stalled during Home command")
                print("        ERROR ERROR ERROR, return error")
                ErrBeamAct.put(1)
                return("Error Occured")

        # Release switch for beam actuator
        Board1.ReleaseSW(2,1)

        # Check home status in while loop
        while True:
            if Busy_Pin.value() == 1:
                # Both rail actuators are homed, continue.
                break
            elif Board1.isStalled(2) == True:
                # motor stalled, return an error and set flag
                Board1.HardHiZ(2)
                print("        Beam Actuator Stalled during Home command")
                print("        ERROR ERROR ERROR, return error")
                ErrBeamAct.put(1)
                return("Error Occured")
        
def Calibration_Mode():
    '''This function directs the XBAS machine to calibrate a machine csv file
    to a specific X-Beam indicated by length in the file name. The file to be
    edited is indicated by the user input in a piano switch board.
    Function Inputs:
        None
    Function Outputs:
        None
    '''
                  
    print("Beginning Calibration Mode")
                  
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
        ErrCal.put(1)
        
        # 2nd Layer. System will stay in this loop unless an error occurs or
        #   the system finishes calibration.
        while True:
            
            # Pre-Calibration Mode
            
            # Turn Yellow LED on indicating the system is initializing the 
            #   calibration mode. Runs once at the beginning of the function
            Lights_Sound_Off()
            YellowLED.High()
            
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
                print("Waiting in pre-Calibration Stage")
                # The calibration mode is ready to go, turn green light on and
                #   wait for go.
                Lights_Sound_Off()
                GreenLED.High()
                while True:
                    if Go() == 1:
                        # User hit go
                        Lights_Sound_Off()
                        YellowLED.High()    # Turn Yellow LED on Indicating the
                                            #   system is working now
                        break               # Exit the 3rd layer and resume in 
                                            #   2nd layer
                        print("Go selected, continuing function")
                    elif Mode() != 1:
                        # User has selected a different mode before hitting go,
                        #   exit the function
                        print("Another Mode selected, exiting function")
                        return()
            
            # User has hit go, import files. Will error if the file is missing
            #   and user must hit go twice(once to turn sound off, once to
            #   resume). After error, return to the pre-calibration stage by
            #   breaking from the 2nd loop back to the 1st loop.
            from ImportSong import ImportSong
            Output = ImportSong()
            if Output == "Error Occrured":
                # Error occured, handle the error, then break out of the 2nd 
                #   layer to the 1st layer
                break
            
            # Song imported, import calibration. If there is an issue, go to
            #   error and wait for user input upon which it breaks back into
            #   the 1st loop.
            Output = ImportCalibration()
            if Output == "Error Occrured":
                break
            
            # Now we've inported the Calibration file w/o error, save the value
            #   of Output to a variable for later use. Also take values out of
            #   the list output of ImportCalibration and save specific values
            #   to named variables for ease of use. Note, Offset adjusts the
            #   distance NearSide and FarSide so they are from the end of the
            #   X-Beam
            print("Transcribing calibration data over to local variables")
            CalibrationData = Output
            NearSide = Output(0)
            FarSide = Output(1)
            
            # Move Gantry to the near side
            print("Moving Gantry to the near side for calibration purposes")
            Output = Move_Gantry_To(NearSide, probe = False)
            
            # Check output for if an error occured. If no error occured, the
            #   function should have returned a number indicating the
            #   measurement.
            if Output == "Error Occured":
                # An error did occur, break back to 1st layer
                print("Error occured moving gantry, do error handling")
                break
                
            # Gantry is in position, check the "block" variable for if the
            #   machine needs to wait for user input or not
            if block == 1:
                print("Waiting for user input to do measurement")
                Lights_Sound_Off()
                GrennLED.High()
                while True:
                    # Sit in a while loop until the user hits Go()
                    if Go()=1:
                        print("Go pressed, taking measurement")
                        Lights_Sound_Off()
                        YellowLED.High()
                        break
            elif block == 2:
                  print("Bypassing user input, taking measurement.")
                        
            # XBAS now needs to take measurement
            Output = probe()
            
            # Check Output for error from probe()
            if Output == "Error Occured":
                print("Probe measurement error, do error handling")
                # Error Occured, exit 2nd layer to 1st layer for error handling.
                break
            
            # Store the data of the near side to the calibration data
            CalibrationData[2] = Output
            print("Substituting probe measurement into CalibrationData, value "+\
                 str(Output))
            
            # Calue of NearSide has been stored, now for FarSide
            print("Moving Gantry to the Farside for Calibration Purpose")
            Output = Move_Gantry_To(FarSide, probe = False)
            
            # Check output for if an error occured. If no error occured, the
            #   function should have returned a number indicating the
            #   measurement.
            if Output == "Error Occured":
                print("Gantry moving error, do error handling")
                # An error did occur, handle error and break back to 1st layer
                ErrorHandler()
                break
            
            # Gantry is in position, check the "block" variable for if the
            #   machine needs to wait for user input or not
            if block == 1:
                print("Waiting for user input to do measurement")
                Lights_Sound_Off()
                GrennLED.High()
                while True:
                    # Sit in a while loop until the user hits Go()
                    if Go()=1:
                        print("Go pressed, taking measurement")
                        Lights_Sound_Off()
                        YellowLED.High()
                        break
                elif block == 2:
                  print("Bypassing user input, taking measurement.")

            # XBAS now needs to take measurement
            Output = probe()

            # Check Output for error from probe()
            if Output == "Error Occured":
                # Error Occured, exit 2nd layer to 1st layer for error handling.
                print("Probe error occured, handle error")
                break

            # Store the data of the far side to the calibration data
            print("Substituting probe measurement into CalibrationData, value "+\
                 str(Output))
            CalibrationData[3] = Output
            
            # Calculate the difference between the level of the two points for 
            #   the calibration constant
            CalibrationData[4] = CalibrationData[3]-CalibrationData[2]
            print("Calculating and storing calibration constant, value "+\
                  str(CalibrationData[4]))
                    
            # At this point, there should have been no errors or such, so 
            #   finish up by storing information into the Calibration file for
            #   the X-Beam length being calibrated and signal the user that the
            #   machine is done.
            Input = XBeam.get()
            FileName = "Calibration"+str(Input)+".csv"
            print("Writing CalibrationData to "+FileName)
            f = open(FileName,'w')
            String = ''
            for item in CalibrationData:
                String = String + str(item) + ','
            String = String.rstrip(',')
            print("    writing line: "+String)
            f.write(String)
            
            # Home the Gantry
            print("Homing Gantry")
            Home("Gantry")
            
            # Zero flags and indicate that the system finished whatever the 
            #   calibration
            zero_flags()
            Lights_Sound_Action()
            
            # Exit Function
            print("Calibration Done, exiting function")
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

    print("Beginning Leveling half of the Assembly Mode")
    
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
            YellowLED.High()
            
            # Is this the first time running through this section of code?
            if switch == 0:
                # First Check Files are present
                Output = FileCheck()
                if type(Output)==str:
                    # If file is missing, break back into 1st layer where the
                    #   error handle function is (at the bottom)
                    break
            
            # Home function, home everything
            Home("All")
            
            # Check output
            if error occured:
                break
            
            if switch == 0:
                # Turn Green LED on indicating ready for user input
                Lights_Sound_Off()
                GreenLED.High()
            
                # Wait for user to hit go or to switch system modes to a
                #   different mode
                while True:
                    print("Waiting in pre-Assembly Stage")
                    if Go() == 1:
                        # Go was pressed, exit the 3rd Layer while loop and
                        #   resume the 2nd layer loop via a break command
                        print("User hit Go, continue leveling and assmembly")
                        break
                    elif Mode() != 3:
                        # Else if the 3 position switch is not set to 3 which
                        #   is the assembly mode, then exit this function via 
                        #   return
                        print("User selected different mode, exit function")
                        return()
            
            # Set switch to 1 so that on future runs, it skips the while loop
            #   for waiting for the user to hit go
            switch = 1
            
            # Turn Yellow Ligth on
            Lights_Sound_Off()
            YellowLED.High()
            
            # User has hit Go, read the piano board via ImportSong()
            from ImportSong import ImportSong
            Output = ImportSong()
            
            # Check Output for if an error occured
            if Output == "Error Occured":
                # Error occured, break 2nd layer loop to return to 1st layer 
                #   loop and handle error
                print("Error in ImportSong, handle error")
                break

            # ImportSong() had no issues, continue by importing Calibration
            #   Data
            Output = ImportCalibration()
            
            # Check Output of ImportCalibration for errors
            if Output == "Error Occured":
                # Error occured, break 2nd layer loop to return to 1st layer 
                #   loop and handle error
                print("Error in ImportCalibration, handle error")
                break
            
            # Take data from Import Calibration and Store it for future use
            print("Transcribe Calibrationdata to local variables")
            CalibrationData = Output
            NearSide = CalibrationData(0)
            FarSide = CalibrationData(1)
            CalConst = CalibrationData(4)

            # Import BoltPatternXXX.csv file for the X-Beam just to check
            #   that it is both present and valid.
            Output = ImportBoltPattern()
            
            # Check the output for an error
            if type(Output) == str:
                # If error, break out of 2nd layer into 1st layer for
                #   error handling
                print("Error in ImportBoltPattern, handle error")
                break
                
            # Move the Gantry to the far side and take the first measurement
            print("Moving Gantry to far side and take measurement")
            Output = Move_Gantry_To(Farside, probe = True)
            
            # Check function output
            if Output == 'Error Occured':
                # Error occured, break loop
                print("Error in moving Gantry or probe, handle error")
                break
            
            # Store output
            FarLevel = Output
            
            # Move the Gantry to the near side and take the first measurement
            print("Moving Gantry to near side and take measurement")
            Output = Move_Gantry_To(Nearside, probe = True)
            
            # Check function output
            if Output == 'Error Occured':
                # Error occured, break loop
                print("Error in moving Gantry or probe, handle error")
                break

            # Store output modified by calibration constant
            NearLevel = Output - CalConst
            print("Calculate nearside w/cal constant")
            print("    FarLevel "+str(FarLevel))
            print("    NearLevel "+str(NearLevel))
            
            # Level X-Beam by actuating X-Beam Actuator to raise the X-Beam
            #   to the level needed.
            x1 = distance from line constraint to x-beam actuator point contraint
            x2 = distance from where probe takes near side measurement to line constraint
            
            # Fraction indicating how much the point being leveled changes as
            #   the X-Beam actuator levels the beam
            x = x2/x1
            
            # Actuate X-Beam levveling actuator and measure
            print("Actuate X-Beam actuator")
            Output = Beam Actuator by ((NearLevel - FarLevel)/x,probe = True)
            
            # Check output
            if Output == 'Error Occured':
                # Error occured, break loop
                print("Error w/beam actuator, handle error")
                break
            
            # Store output
            NearLevel = Output - CalConst
            
            # Check, retry, and repeat
            Error = 0
            Tolerance = 
            while True:
                if NearLevel - FarLevel >= -Tolerance or NearLevel - FarLevel <= Tolerance:
                    # Within of range, continue whiile loop
                    break
                
                # Actuate X-Beam levveling actuator and measure
                print("X-Beam not leveled, re-attempt leveling with actuator")
                Output = Beam Actuator by ((NearLevel - FarLevel)/x, Probe = True)
                
                # Check output
                if Output == 'Error Occured':
                    # Error occured, break loop
                    Error = 1
                    break
            
            # if there was an error in the above while loop, its supposed to
            #   exit to the 1st loop. THis is the second break that helps
            #   achieve that.
            if Error == 1:
                print("Error w/beam actuator, handle error")
                break
            
            # At this point, the beam should be leveled with no errors. Home, 
            #   zero flags and exit function.
            while True:
                Home("Probe","Gantry")
                if no error:
                    break
            zero_flags()
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
    
    print("Beginning to Toque Down")
    
    # Rail Actuators constants
    DistancePerStep = .0079375 # mm linear travel per step
    
    # Position above rails in mm away from the motor. Does not have
    #   to be very accurate (+/- 1mm)
    PositionAboveRails = XXX # mm is the distance we determined too
                            # small for human fingers
    # Covert PositionAboveRails from distance in mm to steps for the 
    #   drivers
    PositionAboveRails = PositionAboveRails / DistancePerStep
    
    # Calculating position above granite from the motor just as with
    #   PositionAboveRails
    PositionAboveGranite = PositionAboveGranite / DistancePerStep
    
    # 1st Layer while loop
    while True:
        # Set torque for the approach to the rails at a very low stall torque
        print("setting stall threshold of rail actuators low")
        Board2._setStallThreshold() ISSUE test this
        
        # Turn on actuators and move twoards a position just above the rails
        print("move rail actuator to point above rails")
        if Input == "L":
            # Turn on left actuator
            print("    left actuator on")
            Board2.Goto(1,PositionAboveRails)
            
        elif Input == "R":
            # Turn on right actuator
            print("    right actuator on")
            Board2.Goto(2,PositionAboveRails)
        
        # 2nd Layer while Loop
        error = 0
        while True:
            # Check for if the rail actuator has stalled or if the rail
            #   actuator has reached destination. 
            
            if Board2.isStalled(1) == True and Input == "L":
                # Left actuator stalled, call error and break out of while
                #   loop for handling it
                print("    left actuator stalled")
                ErrRailActL.put(1)
                error = 1
                break
                
            elif Board2.isStalled(2) == True and Iput == "R":
                # Right actuator stalled, call error and break out of while
                #   loop for handling it
                print("    right actuator stalled")
                ErrRailActR.put(1)
                error = 1
                break
            
            elif Busy_Pin.value() == 1:
                # Check for completion (Done flag false), exit with no
                #   error called
                print("    actuator in position above rails")
                error = 0
                break
        # End of the 2nd Layer while loop, back in the 1st layer
        
    # Error Check, If an error was declared earlier, then skip
    #   the following code responsible for fully pressing down the
    #   rails and bolting down the screws
    if error == 0:
        # Set torque high
        print("setting torque high")
        Board2._setStallThreshold() ISSUE
        
        # Set actuators on depending on input
        print("moving rail actuator to point above granite")
        if Input == "L":
            # Turns left actuator on
            print("    left actuator on")
            Board2.Goto(1,PositionAboveGranite)
            
        elif Input == "R":
            # Turns right actuator on
            print("    right actuator on")
            Board2.Goto(2,PositionAboveGranite)
            
        # 2nd layer while loop checking destination and stall
        #   flags as before.
        while True:  
            if Busy_Pin.value() == 1:
                # Check for completion, call error if actuator moved
                #   to destination succesfully
                if Input == "L":
                    print("    left actuator reached destination, error.")
                    ErrRailActL.put(1)
                if Input == "R":
                    print("    right actuator reached destination, error.")
                    ErrRailActR.put(1)
                break
            if Board2.isStalled(1) == True or Board2.isStalled(2) == True:
                # Left or right actuator stalled, move on to next
                #   stage (torque down)
                print("Actuator stalled, begin torque down section")
                # Truning On solenoids based on side being done
                if Input == "L":
                    # Left Side
                    print("Left Solenoid On")
                    SolenoidLeft.High()
                if Input == "R":
                    # Right Side
                    print("Right Solenoid On")
                    SolenoidRight.High()
        
                # Import Time so system can wait for stuff to finish
                import utime

                # Wait for solenoids to extend
                utime.sleep(100)

                # Turn On motors depedning on side being done
                if Input == "L":
                    # Left Side
                    print("Left DC motor On")
                    DCMotorLeft.High()
                if Input == "R":
                    # Right Side
                    print("Right DC motor On")
                    DCMotorRight.High()

                # Sleep for X amount of time so the DC motor torques
                #   down the bolt.
                utime.sleep(5000)
                
                # Turn screwdriver motors and solenoids off
                print("all motors and solenoids off")
                DCMotorLeft.low()
                DCMotorRIght.low()
                SolenoidLeft.low()
                SolenoidRight.low()
    
                # Sleep till solenoids retract
                utime.sleep(100)
    
                # home the rail actoators depedning on side being done
                if Input == "L":
                    # Left Side
                    print("Homing Left Actuator")
                    Home("RailActL")
                if Input == "R":
                    # Right Side
                    print("Homing Right Actuator")
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
    
    print("Beginning Assembly half of the assembly mode")
    
    # Set Error Flag for mode
    ErrAssembly.put(1)
    
    # Beginning of the while loop for importing the data stored in 
    #   BoltPatternXXX.csv
    while True:
        print("ImportBoltPattern function called")
        Output = ImportBoltPattern()
        if type(Output) == str:
            # Error Occured
            print("Error importing Bolt Pattern csv file.")
            ErrorHandler()
            ErrAssembly.put(1)
        else:
            # No Error Occured
            break
        # End of while loop
    
    # Store Output into variables for later use. Also assign value to offset
    #   to adjust the Bolt
    print("Transcribing bolt pattern data to two seperate lists")
    BoltSide = Output(0)
    BoltData = Output(1)
    
    # For loop to run through the values of BoltSide and BoltData
    for counter in range(0,len(BoltData)):
        # Nested while loop to handle moving the gantry to the target point
        while True:
            # Run Gantry to position
            print("Moving gantry to position #"+str(counter)+": "+\
                  str(BoltData(counter)))
            Output = Move_Gantry_to(BoltData(counter))
            
            # Check output of the function for error
            if Output == "Error Occured":
                # Error Occured
                print("error occured moving ganty, handling error")
                ErrorHandler()
                ErrAssembly.put(1)
            else:
                # No Error Occured
                print("Gantry successfully moved, "+str(counter)"/"+\
                      str(len(BoltData))+" moves completed")
                break
            # End of while loop, go back to for loop and repeat entire
            #   process of moving gantry.
            
        # The gantry should be in position, press rails down and bolt them
        TorqueDown(BoltSide(counter))
        print("TorqueDown successfull, "+str(counter)"/"+\
                      str(len(BoltData))+" bolts completed")
        # End of for loop, go back to beginning unless done.
    
    # While loop to home system
    while True:
        # Home function call
        Output = Home("All")
        
        # Check for error
        if Output == "Error Occured":
            # Error Occured
            print("Error occured durring the homing function, handle error")
            ErrorHandler()
            ErrAssembly.put(1)
        else:
            # No Error Occured
            break
        # End of while loop
        
    # Zero Flags, indicate the system is done via Lights_Sound_Action(), and
    #   retrun
    zero_flags()
    Lights_Sound_Action()
    retrun()
    
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
    YellowLED.High()
    
    # Set the sleep mode error flag buffer to 1 so that if an issue occurs, the
    #   flag is already set.
    ErrSleep.put(1)
    
    # Turn all lights and sounds off, then turn on green lED
    Lights_Sound_Off()
    GreenLED.High()
    
    # Pre-Sleep mode: Wait in while loop for one of two exit conditions.
    #   1) User hits go
    #   2) User changes the system mode to something that isn't the sleep mode
    print("Sleep mode pre-stage")
    Timer = 0                   # Creating a timer variable
    Start = utime.ticks_ms()    # Creating a starting reference time
    while True:
        if Timer > 10*60*1000: # 10 min * 60s/min * 1000ms/s
            print("Timed Out, going to sleep")
            break
        elif Go() == 1:
            print("Go pressed, going to sleep")
            break
        elif Mode() != 2:
            print("Another mode selected, exiting function")
            return(1000)
        # increment Timer
        print("Time in Sleep pre-stage: "+str(Timer)+" ms")
        Current = utime.ticks_ms()
        Timer = Current - Start + Timer
        Start = Current
    
    # User must have hit go to have reached this point of the program. Turn of
    #   lights, turn yellow LED, then enter the new while loop that will try to
    #   home the system. Function will continue until the machine has been
    #   homed.
    # Ammendment, if the system spend 500ms or more in the while loop checking
    #   the Mode() function, then the system homes. Otherwise, if it spent less
    #   than that, it doesnt run the Home() function.
    if Input >= 500:
        Lights_Sound_Off()
        YellowLED.High()
        while True:
            print("Time spend in main checking Mode() >500ms")
            
            # If the system enters sleep mode, Home
            Output =  Home("All")
            
            # Check Output for Error
            if type(Output) == str:
                # If error, do the whole error handeler and when user hits go
                #   2nd time, repeat (ie home again)
                print("Error Homing, handle error")
                ErrorHandler()
                ErrSleep.put(1)
            elif type(Output) != str:
                # If there was no error, exit the loop and continue with the
                #   sleep function
                break
        
        # Reset Timer Clock
        Timer = 0
        Start = utime.ticks_ms()
        
    # Turn Ligths and Sounds off.
    Lights_Sound_Off()
    
    # Enter while loop and wait for user to change the mode before exiting the
    #   function
    print("Everything is done, goin to sleep.")
    while True:
        if Mode() != 2:
            # User has selected another mode, set flag, calculate time one last
            #   time, and exit the sleep function while returning time spent in
            #   sleep mode
            ErrSleep.put(0)
            Current = utime.ticks_ms()
            Timer = Timer + Current-Start
            print("User has changed the mode, waking up")
            return(Timer)
        elif Mode() == 2 and Timer < 600:
            # User has not selected another mode, increment the timer and sleep
            #   for 500ms minus how long it took to do get the current time.
            #   Also, if Timer > 600ms, the Timer will stop incrementing to
            #   prevent possible issues.
            Current = utime.ticks_ms()
            Timer = Timer + Current-Start
            if 500-(Current-Start) >= 0:
                utime.sleep_ms(500-(Current-Start))
            Start = Current
            print("shh, i've been asleep for "+str(Timer)+" ms")
    
#//////////////////////////////////////////////////////////////////////////////
'''                              Main Program                               '''
#//////////////////////////////////////////////////////////////////////////////
# Check Files
Output = FileCheck()

# Check Output of function FileCheck() for an error in the shape of a string
if type(Output)==str:
    # If there was an error, handle it
    print("error with files, handling error")
    ErrorHandler()
    
    # If there was an error and the user hit the go twice, do a soft reset,
    #   restarting the program from the beginning.
    print("SOFT RESET!!!!")
    import sys
    sys.exit()
    
# If there was no error, create all items
print("creating items")
# Pin Definition
import pyb

# Notable stepper driver pins
# Busy pin goes high when motor stops
Busy_Pin = pyb.Pin (pyb.Pin.cpu.C0, mode = pyb.Pin.OUT_PP, 
                      pull = pyb.Pin.PULL_DOWN)

# LED Pin Definition
RedLED = pyb.Pin (pyb.Pin.cpu., mode = pyb.Pin.OUT_PP, 
                      pull = pyb.Pin.PULL_DOWN)

YellowLED = pyb.Pin (pyb.Pin.cpu.C2, mode = pyb.Pin.OUT_PP, 
                         pull = pyb.Pin.PULL_DOWN)

GreenLED = pyb.Pin (pyb.Pin.cpu., mode = pyb.Pin.OUT_PP, 
                        pull = pyb.Pin.PULL_DOWN)

# Piezzo Buzzer
BuzzerPIN = pyb.Pin(pyb.Pin.cpu.A3, mode = pyb.Pin.OUT_PP, 
                        pull = pyb.Pin.PULL_DOWN)
timBuzzer = pyb.Timer(2,freq = 1500)
BuzzerChannel = timBuzzer.channel(4, pyb.Timer.PWM, pin = BuzzerPin)
def Buzzer(Input):
    if Input == "On":
        BuzzerChannel.pulse_width_percent(100)
    else:
        BuzzerChannel.pulse_width_percent(0)
        
# Solenoid and DC Motor Pin call outs and functions for controlling
#   said pins.
SolenoidLeftPin = pyb.Pin (pyb.Pin.cpu.B0, mode = pyb.Pin.OUT_PP)
def SolenoidLeft(Input):
    '''This function turns the left solenoid on and off
    Function Input: Input is a string of either "On" or "Off"
                    which turns the solenoid on or off'''
    if Input == "On":
        SolenoidLeftPin.Low()
    elif Input == "Off"
        SolenoidLeftPin.High()
        
SolenoidRightPin = pyb.Pin (pyb.Pin.cpu.B7, mode = pyb.Pin.OUT_PP)
def SolenoidRight(Input):
    '''This function turns the right solenoid on and off
    Function Input: Input is a string of either "On" or "Off"
                    which turns the solenoid on or off'''
    if Input == "On":
        SolenoidRightPin.Low()
    elif Input == "Off"
        SolenoidRightPin.High()
        
DCMotorLeftPin = pyb.Pin (pyb.Pin.cpu.A4, mode = pyb.Pin.OUT_PP)
def DCMotorLeft(Input):
    '''This function turns the left DC motor on and off
    Function Input: Input is a string of either "On" or "Off"
                    which turns the motor on or off'''
    if Input == "On":
        DCMotorLeftPin.Low()
    elif Input == "Off"
        DCMotorLeftPin.High()
        
DCMotorRightPin = pyb.Pin (pyb.Pin.cpu.B6, mode = pyb.Pin.OUT_PP)
def DCMotorRight(Input):
    '''This function turns the right DC motor on and off
    Function Input: Input is a string of either "On" or "Off"
                    which turns the motor on or off'''
    if Input == "On":
        DCMotorRightPin.Low()
    elif Input == "Off"
        DCMotorRightPin.High()

# The Piano Switch Board Pins numbered 0 to 4 from left to right, left most
#   switch being Note0
Note0 = pyb.Pin (pyb.Pin.cpu.A14, mode = pyb.Pin.OUT_PP,
                 pull = pyb.Pin.PULL_DOWN)

Note1 = pyb.Pin (pyb.Pin.cpu.A15, mode = pyb.Pin.OUT_PP,
                 pull = pyb.Pin.PULL_DOWN)

Note2 = pyb.Pin (pyb.Pin.cpu.C14, mode = pyb.Pin.OUT_PP,
                 pull = pyb.Pin.PULL_DOWN)

Note3 = pyb.Pin (pyb.Pin.cpu.C15, mode = pyb.Pin.OUT_PP,
                 pull = pyb.Pin.PULL_DOWN)

Note4 = pyb.Pin (pyb.Pin.cpu.H0, mode = pyb.Pin.OUT_PP,
                 pull = pyb.Pin.PULL_DOWN)

# Creating the Go button function call. Go() should give 0 or 1 depending on 
#   the pin input. Basically, equating Go_Pin.value() to Go() so I do less
#   typing.
Go_Pin = pyb.Pin(pyb.Pin.cpu.C4, mode = pyb.Pin.In)
Go = Go_Pin.value

# The same as the Go pin, but greating a short function call for the emergency
#   stop button.
Stop_Pin = pyb.Pin(pyb.Pin.cpu.C5, mode = pyb.Pin.In)

'''External Interrupt Pin'''
extint = pyb.ExtInt(Stop_Pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback)

'''Three Position Swtich Pin'''
ThreeSwitch_Pin = pyb.Pin(pyb.Pin.cpu.C3, mode = pyb.Pin.ANALOG)
adc = pyb.ADC(ThreeSwitch_Pin)
ThreeSwitch = adc.read

'''Probe Pins'''
#   H1 is the referencetick
ProbeReference = pyb.Pin(pyb.Pin.cpu.H1, mode = pyb.Pin.IN, pull = pyb.Pin.PULL_DOWN)

#   B9 high sends the probe up if B8 is low
RaisePin = pyb.Pin(pyb.Pin.cpu.B9, mode = pyb.Pin.OUT_PP, pull = pyb.Pin.PULL_DOWN)

#   B8 high sends the probe down if B9 is low
LowerPin = pyb.Pin(pyb.Pin.cpu.B8, mode = pyb.Pin.OUT_PP, pull = pyb.Pin.PULL_DOWN)

def MoveProbe(Input):
    '''Short function to control the probe moving up and down
    Input is string, either "Up", "Down", or "Stop", moving the probe up or down '''
    if Input == "Up":
        LowerPin.Low()
        RaisePin.High()
    elif Input == "Down":
        RaisePin.Low()
        LowerPin.High()
    elif Input == "Stop":
        RaisePin.Low()
        LowerPin.Low()
    
# Encoder Pins and Object for the Probe
#   C6 is encoder ch1
#   C7 is encoder ch2
#   ProbeEncoder is a Quadrature Encoder Object 
import QuadEncoder
pinC6 = pyb.Pin(pyb.Pin.cpu.C6, pyb.Pin.AF_PP,af=3)
pinC7 = pyb.Pin(pyb.Pin.cpu.C7, pyb.Pin.AF_PP,af=3)
ProbeEncoder = enc.Quad_Encoder(pinC6,pinC7,tim8)

'''Stepper Driver pin and  object creations'''
import l6470nucleo                  # Import file
SCK= pyb.Pin(pyb.Pin.cpu.A5)        # stby_rst_pin 
ncs1= pyb.Pin(pyb.Pin.cpu.A10)      # cs_pin for board 1
ncs2= pyb.Pin(pyb.Pin.cpu.A4)       # cs_pin for board 2
Board1 = l6470nucleo.Dual6470(1,ncs1,SCK) # Controls the Gantry (1) and
                                          # Beam Actuator (2)
Board2 = l6470nucleo.Dual6470(2,ncs2,SCK) # Controls Left (1) and Right
                                          # (2) rail actuators

import task_share
'''Variable Buffer Creation'''
print("Buffer object creation")

ErrInit = task_share.Share ('i', thread_protect = False,
                            name = "Initilization Error Flag")
ErrSleep = task_share.Share ('i', thread_protect = False,
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

# Zero the above buffers
zero_flags()

# Turn on only the yellow LED
Lights_Sound_Off()
YellowLED.High()

# Set error flag for the initilization phase
ErrInit.put(1)

# Set Timer measured in milliseconds. Initially set at 600 so the system
#   homes the first time round.
Timer = 600

print("Beginning main program")
# 1st Layer while loop
while True:
    # Check Timer
    if Timer >= 500:
        # Turn on Yellow LED
        Lights_Sound_Off()
        YellowLED.High()
        
        # home loop
        while True:
            # If Timer >= 5 sec, 
            print("Homing everything...")
            Output = Home('All')
            
            # Check Output of function for error
            if Output == "Error Occured":
                # Error, do stuff
                print("Error homing, handle it")
                ErrorHandler()
            else:
                # No error, break this 'home loop' and exit back to the 1st
                #   layer.
                break
            # End of 'home loop'
        
        # Create Timer Variables
        import utime
        Start = utime.ticks_ms()
        Timer = 0
        
        # Turn on the Green Light
        Lights_Sound_Off()
        GreenLED.High()

        print("Checking mode")
        # 2nd Layer While Loop to check mode
        while True:
            
            # Check mode by calling a function which checks the three position
            #   switch
            if Mode() == 1:
                # If switch is in 1st position...
                print("Mode 1: Calibration Mode selected")
                # Run Calibration Mode
                Calibration_Mode()
                
                # Set Timer > 500 so the system homes after the calibration
                #   mode
                Timer = 600
                
                # break out of 2nd layer back to 1st layer
                break
                
            if Mode() == 2:
                # If switch is in 2nd position...
                print("Mode 2: Sleep Mode selected")
                Timer = Sleep_Mode()
                
                # break out of 2nd layer back to 1st layer
                break
            
            if Mode() == 3:
                # If switch is in 3rd position...
                print("Mode 3: Assembly Mode selected")
                # Run Leveling Mode
                Leveling_Mode()
                
                # Run Assembly Mode
                Assembly_Mode()
                
                # Set Timer > 500 so the system homes after the calibration
                #   mode
                Timer > 600
                
                # break out of 2nd layer back to 1st layer
                break
                
            # Increment Timer if no mode is selected
            Current = utime.ticks_ms()
            Timer = (Current - Start) + Timer
            print("Nothing selected?")
            
            # End of the 2nd Layer
        
        # End of 1st Layer
