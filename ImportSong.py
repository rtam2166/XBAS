# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:16:28 2017

@author: drago
"""

def ImportSong():
    '''This function checks the piano board's five switches (the pins
    called Note0 to Note4) and converts those four binary inputs into an
    integer. With four switches available, the range of corresponding integer
    inputs should be 0 to 15 (1-16 if you add 1 to the final number) switches
    are numbered from left to right'''
    
    print("Importing Song/Piano Board Pattern")
    import pyb
    import main
    
    # The Piano Switch Board Pins numbered 0 to 4 from left to right, left most
    #   switch being Note0
    Note0 = pyb.Pin (pyb.Pin.cpu.A14, mode = pyb.Pin.IN,
                     pull = pyb.Pin.PULL_UP)
    
    Note1 = pyb.Pin (pyb.Pin.cpu.A15, mode = pyb.Pin.IN,
                     pull = pyb.Pin.PULL_UP)
    
    Note2 = pyb.Pin (pyb.Pin.cpu.C14, mode = pyb.Pin.IN,
                     pull = pyb.Pin.PULL_UP)
    
    Note3 = pyb.Pin (pyb.Pin.cpu.C15, mode = pyb.Pin.IN,
                     pull = pyb.Pin.PULL_UP)
    
    Note4 = pyb.Pin (pyb.Pin.cpu.H0, mode = pyb.Pin.IN,
                     pull = pyb.Pin.PULL_UP)

    # Get Values from the switches and store into variables a, b, c, and d
    # NOTE: as with Note0, reading 0 means true on the switch
    if Note0.value() == 0:
        a = 1
    else:
        a = 0
    if Note1.value() == 0:
        b = 1
    else:
        b = 0
    if Note2.value() == 0:
        c = 1
    else:
        c = 0
    if Note3.value() == 0:
        d = 1
    else:
        d = 0
    if Note4.value() == 0:
        e = 1
    else:
        e = 0
    
    ''' MAJOR ISSUE 
    switch board switches 3 and 4, Notes 2 and 3 do not work, they 
    are set to 0 for the program to work...'''
    c = 0
    d = 0
    
    print("    Readings")
    print("    Note0: "+str(Note0.value())+" and a: "+str(a))
    print("    Note1: "+str(Note1.value())+" and b: "+str(b))
    print("    Note2: "+str(Note2.value())+" and c: "+str(c))
    print("    Note3: "+str(Note3.value())+" and d: "+str(d))
    print("    Note4: "+str(Note4.value())+" and e: "+str(e))
    print("    Note 2 and 3 are not working, values c and d have been set "+\
          "to 0")
    
    # Calculating a binary number from four binary input
    Number = (a*2**4 + b*2**3 + c*2**2 + d*2**1 + e*2**0) + 1
    
    print("    Read Combination: "+str(a)+str(b)+str(c)+str(d)+str(e)+\
          " = "+str(Number))
        
    # If the user has selected the combination of switches which correspond
    #   to 1-16, than input the X-Beam length into the buffer XBeam that 
    #   corresponds to that input. Additionally, if there is no input, than the
    #   system will return an error.
    Length = 0
    if Number == 1:
        Length = 500
        
    elif Number == 2:
        main.ErrSong.put(1)
        
    elif Number == 3:
        main.ErrSong.put(1)
        
    elif Number == 4:
        main.ErrSong.put(1)
        
    elif Number == 5:
        main.ErrSong.put(1)
        
    elif Number == 6:
        main.ErrSong.put(1)
        
    elif Number == 7:
        main.ErrSong.put(1)
        
    elif Number == 8:
        main.ErrSong.put(1)
        
    elif Number == 9:
        main.ErrSong.put(1)
        
    elif Number == 10:
        main.ErrSong.put(1)
        
    elif Number == 11:
        main.ErrSong.put(1)
        
    elif Number == 12:
        main.ErrSong.put(1)
        
    elif Number == 13:
        main.ErrSong.put(1)
        
    elif Number == 14:
        main.ErrSong.put(1)
        
    elif Number == 15:
        main.ErrSong.put(1)
        
    elif Number == 16:
        main.ErrSong.put(1)
        
    # Note that with 5 switches, you can have up to 32 options. Add more elif
    #   statements.
        
    if main.ErrSong.get() == 0:
        print("    X-Beam "+str(Length)+" selected")
        main.XBeam.put(Length)
        return("No Error")
        
    elif main.ErrSong.get() == 1:
        print("Selected Combination has no assotiated Length value")
        f = open("Error Report.txt","w")
        f.write('''An error occured during the initilization phase\n\r
                The switch combination of the piano switch board does not correspond to any of\n\r
                registered X-Beam lengths.\n\r
                Recomendations:\n\r
                    1) Check your switch combination\n\r
                    2) Open ImportSong.py and check that the switch combination you've selected\n\r
                        has a corresponding X-Beam length.\n\r
                Note: Please remember to check that if you add an X-Beam Length to\n\r
                      ImportSong.py, check that the corresponding Calibration and BoltPattern\n\r
                      csv files are included''')
        f.close()
        return("Error Occured")