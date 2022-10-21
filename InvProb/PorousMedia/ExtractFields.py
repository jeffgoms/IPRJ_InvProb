#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue July 20 23:51:12 2022

@author: jgomes
"""
#import vtk
import glob
import sys
import os
import math
import vtktools
import numpy as np
import TestMat as TM
sys.path.append("../../tools")
    
def LinkFldty_OptFcn():
    """ This function links the main optimisation function with Fluidity-ICFERST.
        ===>>>>  Permeability data (4 values, float) from the optimisation function 
                 MUST be allocated in a file named "KData.txt" with values separated
                 by ',', e.g.,
                      1.e-6, 8.e-6, 4.e-6, 5.e-6
                Fluidity-ICFERST will read the values through the "PermFcn.py" 
                function which is called by the *mpml file. """
        
    print('Running the Fluidity-ICFERST model')
    
    """ Running Fluidity-ICFERST """
    os.system('make serial_corner')
    
    """ Copying file produced by ICFERST ('OneInjectThreeProdts_130.vtu') to a
           dummy file ('TestInject_130.vtu'). Data will be extracted from this 
           file. """
    os.system('cp ./OneInjectThreeProdts_129.vtu ./TestInject_129.vtu')
    
    
    FileName = 'TestInject'
    Coord, Saturation, DarcyVelocity = TM.ExtractVelocSat(FileName)
    
    return Coord, Saturation, DarcyVelocity

#def ReadFineResolMeshFile(TimeStamp):
def ReadFineResolMeshFile():
    
    os.system('cp BackUpFineResolution/OneInjectThreeProdts_171.vtu ./FineTestInject_171.vtu')
    FileName = 'FineTestInject'
    Coord, Saturation, DarcyVelocity = TM.ExtractVelocSat(FileName)
    return Coord, Saturation, DarcyVelocity
    
