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