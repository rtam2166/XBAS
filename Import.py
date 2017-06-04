# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:49:56 2017

@author: drago
"""
def Song():
    '''This function checks the piano board's last four switches (the pins
    called Note1 to Note4) and converts those four binary inputs into an
    integer. With four switches available, the range of corresponding integer
    inputs should be 0 to 15 (1-16 if you add 1 to the final number)
    
    Ammendment: due to issues with the piano switch board, this function
    was basically cut out. If the user still wishes to use the piano switch
    board, just delete XBeam.put(500) and uncomment the rest of the function
    '''
    XBeam.put(500)
    
#    
#    # Get Values from the switches and store into variables a, b, c, and d
#    # NOTE: as with Note0, reading 0 means true on the switch
#    if Note0.value() == 0:
#        a = 1
#    else:
#        a = 0
#    if Note1.value() == 0:
#        b = 1
#    else:
#        b = 0
#    if Note2.value() == 0:
#        c = 1
#    else:
#        c = 0
#    if Note3.value() == 0:
#        d = 1
#    else:
#        d = 0
#    if Note4.value() == 0:
#        e = 1
#    else:
#        e = 0
#        
#    # Calculating a binary number from four binary input
#    Number = (a*2**4 + b*2**3 + c*2**2 + d*2**1 + e*2**0) + 1
#        
#    # If the user has selected the combination of switches which correspond
#    #   to 1-16, than input the X-Beam length into the buffer XBeam that 
#    #   corresponds to that input. Additionally, if there is no input, than the
#    #   system will return an error.
#    if Number == 1:
#        Length = 500
#        
#    elif Number == 2:
#        ErrSong.put(1)
#        
#    elif Number == 3:
#        ErrSong.put(1)
#        
#    elif Number == 4:
#        ErrSong.put(1)
#        
#    elif Number == 5:
#        ErrSong.put(1)
#        
#    elif Number == 6:
#        ErrSong.put(1)
#        
#    elif Number == 7:
#        ErrSong.put(1)
#        
#    elif Number == 8:
#        ErrSong.put(1)
#        
#    elif Number == 9:
#        ErrSong.put(1)
#        
#    elif Number == 10:
#        ErrSong.put(1)
#        
#    elif Number == 11:
#        ErrSong.put(1)
#        
#    elif Number == 12:
#        ErrSong.put(1)
#        
#    elif Number == 13:
#        ErrSong.put(1)
#        
#    elif Number == 14:
#        ErrSong.put(1)
#        
#    elif Number == 15:
#        ErrSong.put(1)
#        
#    elif Number == 16:
#        ErrSong.put(1)
#        
#    # Note that with 5 switches, you can have up to 32 options. Add more elif
#    #   statements.
#        
#    if ErrSong.get() == 0:
#        XBeam.put(Length)
#        return("No Error")
#        
#    elif ErrSong.get() == 1:
#        f = open("Error Report.txt","w")
#        f.write('''An error occured during the initilization phase\n\r
#                The switch combination of the piano switch board does not correspond to any of\n\r
#                registered X-Beam lengths.\n\r
#                Recomendations:\n\r
#                    1) Check your switch combination\n\r
#                    2) Open ImportSong.py and check that the switch combination you've selected\n\r
#                        has a corresponding X-Beam length.\n\r
#                Note: Please remember to check that if you add an X-Beam Length to\n\r
#                      ImportSong.py, check that the corresponding Calibration and BoltPattern\n\r
#                      csv files are included''')
#        f.close()
#        return("Error Occured")

def BoltPattern():
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
    print("    Working X-Beam "+str(Input))
    
    # Creating the name of the file to be imported
    FileName = "BoltPattern"+str(Input)+".csv"
    print("    File name assotiated with X-Beam: "+FileName)
    
    # a function unique binary error flag indicating which error has occured.
    error = 0
    
    '''Open Error Report for editing'''
    f = open("Error Report.txt","w")
    print("    File Opened, checking values")
    
    try:
        '''Attempt to import the BoltPattern file indicated by the input.'''
        with open(FileName,'r') as file:
            '''File does exist, process the data as indicated'''
            i = 1
            print("    File Opened, splitting values into two seperate lists")
            for line in file:
                line = line.split(',')
                line[-1] = (line[-1].replace("\n",''))
                line[-1] = (line[-1].replace("\r",''))
                if i == 1:
                    BoltSide = line
                elif i == 2:
                    BoltData = line
                print("    Line "+str(i)+" processed")
                i = i+1
               
    except OSError:
        '''File doesn't exist, write to Error Report'''
        print("    Unable to open BoltPatternXXX.csv file")
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
            f.write('\r\r\n')
            error = 1
            print("    Item "+str(i)+" checked, "+string)
        else:
            print("    Item "+str(i)+" checked, no errors")
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
            f.write('\r\r\n')
            error = 1
            print("    Item "+str(i)+" checked, "+string)
        else:
            print("    Item "+str(i)+" checked, no errors")
        i = i+1
    
    '''If there were no issues in the lists, return the two lists'''
    if error == 0:
        print("    No Errors importing "+FileName)
        return([BoltSide,BoltData])
    elif error != 0:
        print("    An error has occured, exiting function")
        f.close()
        return("An Error Occured, please see the 'Error Report.txt' file")
        
def Calibration():
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
              
    except OSError:
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
        
from setup import ErrCalCsv, ErrBoltCsv, XBeam
