# -*- coding: utf-8 -*-
#
## @file task_share.py
#  This file contains classes which allow tasks to share data without the risk
#  of data corruption by interrupts. 
#
#  @copyright This program is copyright (c) JR Ridgely and released under the
#  GNU Public License, version 3.0. 

import array
import gc
import pyb
import micropython


## This is a system-wide list of all the queues and shared variables. It is
#  used to create diagnostic printouts. 
share_list = []

class Share:
    """ This class implements a shared data item which can be protected 
    against data corruption by pre-emptive multithreading. Multithreading 
    which can corrupt shared data includes the use of ordinary interrupts as 
    well as the use of a Real-Time Operating System (RTOS). """

    ## A counter used to give serial numbers to shares for diagnostic use.
    ser_num = 0

    def __init__ (self, type_code, thread_protect = True, name = None):
        """ Allocate memory in which the shared data will be buffered. The 
        data type code is given as for the Python 'array' type, which 
        can be any of
        * b (signed char), B (unsigned char)
        * h (signed short), H (unsigned short)
        * i (signed int), I (unsigned int)
        * l (signed long), L (unsigned long)
        * q (signed long long), Q (unsigned long long)
        * f (float), or d (double-precision float)
        @param type_code The type of data items which the share can hold
        @param thread_protect True if mutual exclusion protection is used
        @param name A short name for the share, default @c ShareN where @c N
            is a serial number for the share """

        self._buffer = array.array (type_code, [0])
        self._thread_protect = thread_protect

        self._name = str (name) if name != None \
            else 'Share' + str (Share.ser_num)

        # Add this share to the global share and queue list
        share_list.append (self)


    @micropython.native
    def put (self, data, in_ISR = False):
        """ Write an item of data into the share. Any old data is overwritten.
        This code disables interrupts during the writing so as to prevent
        data corrupting by an interrupt service routine which might access
        the same data.
        @param data The data to be put into this share
        @param in_ISR Set this to True if calling from within an ISR """

        # Disable interrupts before writing the data
        if self._thread_protect and not in_ISR:
            irq_state = pyb.disable_irq ()

        self._buffer[0] = data

        # Re-enable interrupts
        if self._thread_protect and not in_ISR:
            pyb.enable_irq (irq_state)


    @micropython.native
    def get (self, in_ISR = False):
        """ Read an item of data from the share. Interrupts are disabled as
        the data is read so as to prevent data corruption by changes in
        the data as it is being read. 
        @param in_ISR Set this to True if calling from within an ISR """

        # Disable interrupts before reading the data
        if self._thread_protect and not in_ISR:
            irq_state = pyb.disable_irq ()

        to_return = self._buffer[0]

        # Re-enable interrupts
        if self._thread_protect and not in_ISR:
            pyb.enable_irq (irq_state)

        return (to_return)


    def __repr__ (self):
        """ This method puts diagnostic information about the share into a 
        string. """

        return ('{:<12s} Share'.format (self._name))