#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue July 20 03:10:54 2022

@author: jgomes
"""
#import vtk
import glob
import sys
import os
import math
import vtktools
import numpy as np
sys.path.append("../../tools")

def GlobalVar(): # Defining global variables
    """ Defining dimensions of arrays """
    global nd, n, RD, X0
    global MaxVal, MinVal, GeneralTolerance
    global FMutacao, FCruzamento, DimPopulacao, NGeracoes
    global AlgOptimisation
    
    """ Boundary is a quarter-of-circle with radius RD=0.5
        Also domain's length is equal to X0=4. """  
    nd = 100; n = 3
    RD = 0.5; X0 = 4.0

    """ Parametros relacionados ao dominio de busca """
    MaxVal = 1.e-5; MinVal = 1.e-18
    GeneralTolerance = 1.e-8

    """ Lista de Resfriamento do Algoritmo de Otimizacao """
    # Para o algoritmo de Evolucao Diferencial
    AlgOptimisation = 'DE'
    FMutacao = 0.8; FCruzamento = 0.9; DimPopulacao = 20; NGeracoes = 50
    
    return

def GetBC_Coordinates():
    """ The simulated domain is a square of length of 4. The production takes place
           at 3 borders (as quarter-cycle) at 2nd, 3rd and 4th quarter of the 
           domain. 
           2nd quarter: 3.5 <= X <= 4.0 and 0.0 <= Y <= 0.5
           3rd quarter: 3.5 <= X <= 4.0 and 3.5 <= Y <= 4.0
           4th quarter: 0.0 <= X <= 0.5 and 3.5 <= Y <= 4.0           
           """
    GlobalVar()
    """ Dimension of arrays 
          nd = 4; n = 3
          """
    ndx = [nd, nd * 2, nd * 3]
    
    """ Boundary is a quarter-of-circle with radius RD=0.5
        Also domain's length is equal to X0=4. """  
    
    """ Generating 3.5 <= X <= 4.0 """
    Q1X = np.linspace(3.5, 4., ndx[0])
    """ Generating 0.0 <= X <= 0.5 """
    Q2X = np.linspace(0., 0.5, ndx[0])
    """ Allocating space for Y """
    Q1Y = np.zeros(ndx[0]); Q2Y = np.zeros(ndx[0]); Q3Y = np.zeros(ndx[0])
    
    """ Calculating Y based of the circle equation (for each quarter):
         Radius = RD = [ (X-X0)**2 + (Y-Y0)**2 ] **(0.5) """
    for i in range(ndx[0]):
        Q1Y[i] = math.sqrt(RD**2 - (Q1X[i] - X0)**2) ## Second Quarter
        Q2Y[i] = X0 - math.sqrt( -(Q1X[i] - X0)**2 + RD**2 ) ## Third Quarter
        Q3Y[i] = X0 - math.sqrt(RD**2 - Q2X[i]**2) ## Forth Quarter
        
    """ Allocating space for the Coordinate (as a numpy 2d array) """
    coord = np.zeros((ndx[2],n))
    
    """ Generating the numpy 2d array based on the circle equation """
    for i in range(ndx[2]):
        if i < (ndx[0]): # 2nd quarter
            for j in range(n):
                if j == 0: # X
                    coord[i][j] = Q1X[i]
                elif j == 1: # Y
                    coord[i][j] = Q1Y[i]
                else:
                    coord[i][j] = 0.
        elif (i >= ndx[0] ) and (i < ndx[1]): # 3th quarter
            ind = i - ndx[0]
            for j in range(n):
                if j == 0: # X
                    coord[i][j] = Q1X[ind]
                elif j == 1: # Y
                    coord[i][j] = Q2Y[ind]
                else:
                    coord[i][j] = 0.
        elif (i >= ndx[1]) and (i < ndx[2]): # 4th quarter
            ind = i - ndx[1]
            for j in range(n):
                if j == 0: # X
                    coord[i][j] = Q2X[ind]
                elif j == 1: # Y
                    coord[i][j] = Q3Y[ind]
                else:
                    coord[i][j] = 0.
            
    #print(coord)    
    return coord


def ExtractVelocSat(FileName):
    """ This function extracts velocity and saturation field from a vtu file.
          The current function only works for vtu files in serial, for parallel
          a new function needs to be generated. """
    
    """ File to be read -- check if the prescribed file do exist"""
    FileName2 = FileName + '_[0-9]*.vtu'
    filelist = glob.glob( FileName2 ); print('FileLists:', filelist)
    for f in filelist:
        try:
            os.stat(f)
        except:
            print("No such file: %s" % f)
            sys.exit(1)

        """ For practical reasons let's use file *_0.vtu for our calculations, thus
               DO make sure to rename (beforehand) the file of interest to 
               "TestInject_0.vtu" as, eg,
               scp -p OneInjectThreeProdts_200.vtu TestInject_0.vtu
               With this we ensure that we are extracting data from the same time-stamp """
        num = int(f.split(".vtu")[0].split('_')[-1])
        vtu = vtktools.vtu(f) # Extracting data from the VTU file through a VTK filter
        
        for name in vtu.GetFieldNames(): 
            if name.endswith("Time"):
                time = max(vtu.GetScalarRange(name))
                break
        #print('Time:', time)
        
        """ Extracting the spatial coordinates related to the boundaries (production). 
              This is a numpy 2d-array which is requested by the "vtu.ProbeData" filter
              of the "vtk" library """
        coord = GetBC_Coordinates()
        
        """ Extracting data from the prescribed spatial coordinates using the "vtu.ProbeData"
              filter. Syntax of this filter is 
                   vtu.ProbeData(coordinates, "field")
              where "field" is explicitly stated within the preamble of the vtu file.
              The outcome of trhe filter is an array. Here, we are interested (for the
               time being) on the following "fields": 
                  Saturation of phase 1 as "phase1::PhaseVolumeFraction" and
                  Velocity of phase 1 as "phase1::DarcyVelocity"
              Bear in mind that the velocity is extracted as an array with 3 components. """ 
        Saturation = vtu.ProbeData(coord, "phase1::PhaseVolumeFraction")
        DarcyVelocity = vtu.ProbeData(coord, "phase1::DarcyVelocity")
        
        """nSat = len(Saturation)
        for i in range(nSat):
            print(coord[i][:], Saturation[i], DarcyVelocity[i])"""
        
    return coord, Saturation, DarcyVelocity
