#!/usr/bin/env python3

# arguments:: project vtu
# extracts flow parameters for a number of points
# from a vtu file

import vtk
import sys
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import os
import csv

"""
print('Running the model')
path = os.getcwd()
binpath = '/data2/MultiFluids/ICFERST/bin/icferst'
os.system('rm -f ' + path+ '/*.vtu')
os.system(binpath + ' ' + path + '/*mpml')
"""


#TOLERANCE OF THE CHECKING
#The present values are just above the values I got when writing the script


##########################  AUTOMATIC STUFF  ###############################
Passed = False

filename = 'OneInjectThreeProdts_outfluxes.csv'
phase1_in = []
phase2_out = []
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in datareader:
        try:
            phase1_in.append(float(row[6]))#Cumulative injection of water
            phase2_out.append(float(row[7]))#Cumulative production of oil
        except:
            continue

#Check last cumulative production
diff = abs(phase1_in[2] + phase2_out[2])/abs(phase2_out[2])



print('In-out difference after 15 years: ' + str(diff))
Passed = False
#Check time to produce water with lower temperature than the reservoir
if (abs(diff) < 1e-3): Passed = True

#print time, temp

if (Passed): 
    print('Well production works OK')
else:
    print('Well production does NOT work')

############################# MORE AUTOMATIC STUFF  ###############################


print('#####   Now extracting fields   #####')

#RETRIEVE AUTOMATICALLY THE LAST VTU FILE
#Get path
path = os.getcwd()
AutoNumber = 0
for files in os.listdir(path):
    if files.endswith(".vtu"):
        pos = files.rfind('_')
        pos2 = files.rfind('.')
        AutoFile = files[:pos]
        AutoNumber = max(AutoNumber, int(files[pos+1:pos2]))

AutomaticFile = AutoFile
AutomaticVTU_Number = AutoNumber

#Plot the results in 2d?
showPlot = False

#NAME OF THE VARIABLE YOU WANT TO EXTRACT DATA FROM
data_name_rho = 'Density'
data_name_p = 'Pressure'
data_name_v = 'Velocity'
#Initial and last coordinate of the probe
#Initial and last coordinate of the probe
x0 = 4.5
x1 = 5.0

y0 = 0. # 1.0/float(NUMBER)
y1 = 0.5

z0 = 0.
z1 = 0.

#Resolution of the probe
npts = 100
resolution = npts

if (len(sys.argv)>1):
    filename   = sys.argv[1]
    vtu_number = int(sys.argv[2])
else:
    filename = AutomaticFile
    vtu_number = int(AutomaticVTU_Number)

#print 'reading data...'

U=[]
T=[]
S=[]
FSrho=[]
FSP=[]
FSV=[]

# serial
reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(filename+'_'+str(vtu_number)+'.vtu')

#reader.Update()
ugrid = reader.GetOutputPort()
#ugrid.Update()

###########Create the probe line#############

detector = []
hx = (x1 - x0) / resolution
hy = (y1 - y0) / resolution
hz = (z1 - z0) / resolution

Experimental_X = []
for i in range(resolution+1):
    detector.append([hx * i + x0, hy * i + y0, hz * i + z0])
    Experimental_X.append(hx * i + x0)
    

print( 'using',len(detector),'detectors')
points = vtk.vtkPoints()
points.SetDataTypeToDouble()

for i in range(len(detector)):
    points.InsertNextPoint(detector[i][0], detector[i][1], detector[i][2])

detectors = vtk.vtkPolyData()
detectors.SetPoints(points)

for i in range(len(detector)):
    points.InsertNextPoint(detector[i][0], detector[i][1], detector[i][2])

detectors = vtk.vtkPolyData()
detectors.SetPoints(points)

probe = vtk.vtkProbeFilter()
probe.SetInputConnection(ugrid)

probe.SetSourceConnection(ugrid)
probe.SetInputData(detectors)
probe.Update()

data = probe.GetOutput()

for j in range(points.GetNumberOfPoints()):
    FSrho.append(  data.GetPointData().GetScalars(data_name_rho).GetTuple(j))

for j in range(points.GetNumberOfPoints()):
    FSP.append(  data.GetPointData().GetScalars(data_name_p).GetTuple(j))

for j in range(points.GetNumberOfPoints()):
    FSV.append(  data.GetPointData().GetScalars(data_name_v).GetTuple(j))



if (showPlot):
	fig, ax = plt.subplots(3, sharex=True)
	x = []
	y = []
	yp = []
	yv = []
	for i in range(len(detector)):
		x.append(float(detector[i][0]))#+0.5)#In this test case the origin is in -0.5
		y.append(float(FSrho[i][0]))
		yp.append(float(FSP[i][0]))
		yv.append(float(FSV[i][0]))
	line = plt.Line2D(x, y, color='red', linewidth=2)
	line2 = plt.Line2D(Analytical_X, Analytical_Yrho, color='blue', linewidth=2)
	#line.text.set_color('red')
	#line.text.set_fontsize(16)
	ax[0].add_line(line)
	ax[0].add_line(line2)

	line3 = plt.Line2D(x, yp, color='red', linewidth=2)
	line4 = plt.Line2D(Analytical_X, Analytical_Yp, color='blue', linewidth=2)
	ax[1].add_line(line3)
	ax[1].add_line(line4)

	line5 = plt.Line2D(x, yv, color='red', linewidth=2)
	line6 = plt.Line2D(Analytical_X, Analytical_Yv, color='blue', linewidth=2)
	ax[2].add_line(line5)
	ax[2].add_line(line6)

	plt.show()
