#!/usr/bin/env python
'''
********************************************************************************
*                                                                              *
*    CANTHERM                                                                  *
*                                                                              *
*    Copyright (C) 2018, Sandeep Sharma and James E. T. Smith                  *
*                                                                              *
*    This program is free software: you can redistribute it and/or modify      *
*    it under the terms of the GNU General Public License as published by      *
*    the Free Software Foundation, either version 3 of the License, or         *
*    (at your option) any later version.                                       *
*                                                                              *
*    This program is distributed in the hope that it will be useful,           *
*    but WITHOUT ANY WARRANTY; without even the implied warranty of            *
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             *
*    GNU General Public License for more details.                              *
*                                                                              *
*    You should have received a copy of the GNU General Public License         *
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.     *
*                                                                              *
********************************************************************************
'''

# the file passed to the program is the gaussian output file from which it reads
# the geometry of the molecule
# assumes that inertia.dat is present in the current directory and reads
# the inertia data

import sys
sys.path.append('/home/sandeeps/program/CanTherm')
import readGeomFc
import os
from numpy import *
import geomUtility

#inputFiles = ['1220.log','0120.log','1000.log','1120.log','2101.log','2120.log']
inputFiles = ['022.log', '112.log', '012.log', '120.log']

#inputFiles = ['12211.log','02211.log','22211.log','11011.log','11022.log']
#inputFiles = ['111122.log','212211.log', '102022.log', '002022.log',   '212122.log',   '022022.log']
harmonics = file('harmonics.dat_ring', 'w')
energy_base = readGeomFc.readHFEnergy(inputFiles[0][:-4] + '_rot0_6.log')
numRotors = 4
harmonics.write(str(len(inputFiles)) + '\n')
for files in inputFiles:
    y = matrix(zeros((13, 1), dtype=float))
    x = matrix(zeros((13, 11), dtype=float))
    energy = readGeomFc.readHFEnergy(files[:-4] + '_rot0_6.log')
#    harmonics.write(files+'\n')
    (geom, Mass) = readGeomFc.readGeom(open(files, 'r'))
    inertia = open('inertia.dat', 'r')
    (rotors) = readGeomFc.readGeneralInertia(inertia, Mass)
    if (files == inputFiles[0]):
        K = geomUtility.calculateD32(geom, Mass, rotors)
        detD = 1.0
        for i in range(numRotors):
            print(K[i])
            detD = detD * K[i]
        harmonics.write(str(float(detD)) + '\n')
    harmonics.write(str((energy - energy_base) * ha_to_kcal) + '\n')
    if (energy < energy_base):
        print(files, " has lower energy")
        exit()
    for i in range(numRotors):
        potgiven = []
        for j in range(13):
            angle = (-60.0 + j * 120.0 / 12.0) * 2 * math.pi / 360.0
            fname = files[:-4] + '_rot' + str(i) + '_' + str(j) + '.log'
            y[j] = (readGeomFc.readHFEnergy(fname) - energy) * ha_to_kcal
            x[j, 0] = 1.0
            for k in range(5):
                x[j, k + 1] = cos((k + 1) * angle)
                x[j, k + 6] = sin((k + 1) * angle)

            potgiven.append([angle, float(y[j])])

        XtX = transpose(x) * x
        XtY = transpose(x) * y
        b = linalg.inv(XtX) * XtY

        print('rotor', i, files)

        pot = []
        for j in range(21):
            angle = (-60.0 + j * 120 / 20.0) * 2 * math.pi / 360.0
            v = b[0]
            for k in range(5):
                v = v + b[k + 1] * cos((k + 1) * angle) + \
                    b[k + 6] * sin((k + 1) * angle)
            pot.append([angle, v])

        harmonics.write(str(float(b[0])) + '\n')
        for k in range(5):
            harmonics.write(str(float(b[k + 1])) +
                            '\t' + str(float(b[k + 6])) + '\n')
        harmonics.write('\n')

    harmonics.write('\n')
