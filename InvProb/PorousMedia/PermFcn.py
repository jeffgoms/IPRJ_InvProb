#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed July 21 1:11:34 2022

@author: jgomes
"""
import sys
import shutil
import numpy as np

def PermPopulate(X):
    """ Generating a function for ICFERST that returns a value Perm for a 
        given X (X0,X1,X2) coordinate. The domain is 4 x 4. """
    X0 = 0.; X1 = 2.; X2 =4.; n = 4;

    K = np.zeros(n); K = [7.90517951679e-07, 1.00000001e-10, 1.00000001e-10, 1.00000001e-10]

    
    #PermK = [1.e-6, 8.e-6, 4.e-6, 5.e-6]# --> Original K

    
    if X[1] <= X1:
        if X[0] <= X1: # 1st quarter
          Perm = K[0] # (in cm2)
        elif X[0] > X1: # 2nd quarter
          Perm = K[1] # (in cm2)
        else:
          sys.exit('Out of the domain')
                
    elif X[1] > X1:
        if X[0] <= X1: # 4th quarter
          Perm = K[3] # (in cm2)
        elif X[0] > X1: # 3rd quarter
          Perm = K[2] # (in cm2)
        else:
          sys.exit('Out of the domain')

    else:
        sys.exit('Option not found')

        
    return Perm
