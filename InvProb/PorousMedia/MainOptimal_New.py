#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 01:16:39 2022

@author: Josiele, Matheus and Jeff
"""

#import sys
#import os, math
#import numpy as np
#import ExtractFields as EF
#import TestMat as TM
import AlgOpt as AO
from time import process_time

"""     Main Optimisation Code    """

# Start the stopwatch / counter 
t1_start = process_time()
print('Inicialisando o programa', t1_start, ' s')

"""
         Chamando o Algoritmo de Evolucao Diferencial  
                                                           """
AO.OptimisationCall()

# Stop the stopwatch / counter
t1_stop = process_time()
print('Terminando a execucao do programa', t1_stop, ' s')
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start, ' s') 

