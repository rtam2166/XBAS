# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:16:28 2017

@author: drago
"""

def ImportSong():
    '''This function checks the piano board's last four switches (the pins
    called Note1 to Note4) and converts those four binary inputs into an
    integer. With four switches available, the range of corresponding integer
    inputs should be 0 to 15 (1-16 if you add 1 to the final number)'''
    
    from main import Note0
    from main import Note1
    from main import Note2
    from main import Note3
    from main import Note4
    from main import XBeam
    from main import ErrSong
    
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
        
    # Calculating a binary number from four binary input
    Number = (a*2**4 + b*2**3 + c*2**2 + d*2**1 + e*2**0) + 1
        
    # If the user has selected the combination of switches which correspond
    #   to 1-16, than input the X-Beam length into the buffer XBeam that 
    #   corresponds to that input. Additionally, if there is no input, than the
    #   system will return an error.
    if Number == 1:
        Length = 500
        
    elif Number == 2:
        ErrSong.put(1)
        
    elif Number == 3:
        ErrSong.put(1)
        
    elif Number == 4:
        ErrSong.put(1)
        
    elif Number == 5:
        ErrSong.put(1)
        
    elif Number == 6:
        ErrSong.put(1)
        
    elif Number == 7:
        ErrSong.put(1)
        
    elif Number == 8:
        ErrSong.put(1)
        
    elif Number == 9:
        ErrSong.put(1)
        
    elif Number == 10:
        ErrSong.put(1)
        
    elif Number == 11:
        ErrSong.put(1)
        
    elif Number == 12:
        ErrSong.put(1)
        
    elif Number == 13:
        ErrSong.put(1)
        
    elif Number == 14:
        ErrSong.put(1)
        
    elif Number == 15:
        ErrSong.put(1)
        
    elif Number == 16:
        ErrSong.put(1)
        
    # Note that with 5 switches, you can have up to 32 options. Add more elif
    #   statements.
        
    if ErrSong.get() == 0:
        XBeam.put(Length)
        return("No Error")
        
    elif ErrSong.get() == 1:
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