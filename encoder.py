# -*- coding: utf-8 -*-
##
#  @file encoder.py
#  File containing class to control a Quad Encoder
#  @author Robert Tam
#  @author Tommy Yath
#  @author Berizohar Padilla
#  @copyright GPL Version 3.0

#------------------------------------------------------------------------------
# Pin Callouts
class Quad_Encoder:
    """Class of functions for a DC motor Quadratic encoder
    This class has two functions
        1: .read() returns the current position
        2: .zero() sets the postion to zero
    """
    
    def __init__(self,pin1,pin2,timer):
        """Initilizes the Encoder class by taking inputs and creating channels
        for said inputs.
        @ param pin1  : Pin location of channel A of the Encoder
        @ param pin2  : Pin location of channel B of the Encoder
        @ param timer : Timer channel associated with pin1 and pin2
        """
        # Module Importing
        import pyb
        
        self.timer=timer
        self.pin1=pin1
        self.pin2=pin2
        self.position = 0
        self.current = 0
        self.previous = 0
        self.delta = 0
        
        # Create Timer Channels
        self.ch1 = self.timer.channel(1,pyb.Timer.ENC_AB,pin=self.pin1)
        self.ch2 = self.timer.channel(2,pyb.Timer.ENC_AB,pin=self.pin2)
                
    def read(self):
        """Returns the current postion of the encoder
        """
        self.previous = self.current
        self.current = self.timer.counter()
        self.delta = self.current - self.previous
        
        if self.delta < -10000:
            self.delta += 2**14
        elif self.delta > 10000:
            self.delta -= 2**14
            
        self.position = self.position + self.delta
        return(self.position)
        
    def zero(self):
        """Sets the encoder postion to zero
        """
        self.position = 0
        self.current = 0
        self.previous = 0
        self.delta = 0

