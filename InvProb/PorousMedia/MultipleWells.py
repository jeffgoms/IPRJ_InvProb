#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 13:00:49 2020

@author: jgomes
"""
import math, sys

def VelocitySource(Coord, X):
    """ Generating a function for ICFERST that returns a tuple Vx & Vy for a 
        given X (X0,X1,X2) coordinate. The domain is 5 x 5 and a spherical 
        source is placed at coordinates (distX,distY) with radius rad. """
                
    vel_comp = math.sqrt( 2. * .5**2 ); Vel = 0.
    if Coord == 'X':
        Vel = vel_comp
    elif Coord == 'Y':
        Vel = vel_comp
    else:
        sys.exit('Coordinate not found')
        
    return Vel

def VelocitySource2(X):
    """ Generating a function for ICFERST that returns a tuple Vx & Vy for a 
        given X (X0,X1,X2) coordinate. The domain is 5 x 5 and a spherical 
        source is placed at coordinates (distX,distY) with radius rad. """
    Vx = 0.; Vy = 0.
    rad = 0.24 ; distX = 0.25; distY = 0.25
    vel_comp = math.sqrt( 2. * .5**2 )
    radius = ( X[0] - distX )**2 + ( X[1] - distY )**2 
    if radius <= rad**2:
        Vx = vel_comp ; Vy = vel_comp
    return (Vx, Vy)

def SaturationSource2(X):
    """ Generating a function for ICFERST that returns a value SatSouce for a 
        given X (X0,X1,X2) coordinate. The domain is 5 x 5 and a spherical 
        source is placed at coordinates (distX,distY) with radius rad. """
    SatSource = 0.
    rad = 0.24 ; distX = 0.25; distY = 0.25
    radius = ( X[0] - distX )**2 + ( X[1] - distY )**2 
    if radius <= rad**2:
        SatSource = 1.
    return SatSource

def PermPopulate(Dist,X):
    """ Generating a function for ICFERST that returns a value Perm for a 
        given X (X0,X1,X2) coordinate. The domain is 5 x 5. """
    if (Dist == 'Homogeneous') or (Dist == 'Homog'): 
        Perm = 1.e-6 #(in cm2)
        
    elif (Dist == 'Heterogeneous') or (Dist == 'Heterog'):
        import random
        random.seed()
        Perm = random.uniform(1.e-10,1.e-7) # Min and Max permeability (in cm2)
        Perm = Perm * 1.e-4 #(in m2)
        
    elif (Dist == 'Fractured') or (Dist == 'Fract'):
        import random
        random.seed() ; eps = 5.e-2; rad1 = 0.75; rad2 = 5. - rad1
        Perm = random.uniform(1.e-10,1.e-7); PermFract = random.uniform(1.e-3, 1.e-2) 
        
        if abs(X[0]-X[1]) <= eps and (X[1] > rad1) and (X[1] < rad2):# Fracture along the main diagonal
            Perm = PermFract
        elif (abs(X[1]-2.3) <= eps and (X[0] > 1.) and (X[0] < 4.)):
            # Fracture along the X-axis @ 2.3cm  vertical
            Perm = PermFract
            
    elif (Dist == 'HomogZone'):
        X0 = 0.; X1 = 2.5; X2 = 5.;
        if X[1] <= X1:
            if X[0] <= X1: # 1st quarter
                Perm = 1.e-6 # (in cm2)
            elif X[0] > X1: # 2nd quarter
                Perm = 8.e-6 # (in cm2)
            else:
                sys.exit('Out of the domain')
                
        elif X[1] > X1:
            if X[0] <= X1: # 4th quarter
                Perm = 5.e-6 # (in cm2)
            elif X[0] > X1: # 3rd quarter
                Perm = 4.e-6 # (in cm2)
            else:
                sys.exit('Out of the domain')

        else:
            sys.exit('Option not found')
        
    return Perm

        
    
    
