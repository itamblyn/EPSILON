#!/usr/bin/env python

import os, sys, commands
import numpy as np
import matplotlib.pyplot as plt

get_rlattice = commands.getoutput('grep -A 4 "reciprocal basis" OUT.conv | tail -3 > rlattice_txt')
inputFile = open('rlattice_txt','r')

b = np.zeros((3,3), dtype=np.float)

i = 0
for line in inputFile.readlines():
    for j in range(3):
        b[i][j] = float(line.split()[j])/.529177
    i = i+1

#print b

get_q = commands.getoutput('grep q\= xi0.log | awk \'{print $2, $3, $4}\' > the_ques')

inputFile = open('the_ques','r')

qarray = []

for line in inputFile.readlines():

    qarray.append([float(line.split()[0]),float(line.split()[1]),float(line.split()[2])])

inputFile.close()

#print 'Got the q vectors'

grepper = commands.getoutput('grep -A 10000000 "Crystal k+q WFs read from CWFEq" xi0.log \
| tail -n +2 > txt')

inputFile = open('txt','r')

a =[]

for line in inputFile.readlines():

    length = len(line.split())
    if (length == 6): 
        a.append([])

    if (length == 8):

        a[-1].append(line.split())

cleanup = commands.getoutput('rm the_ques txt')

print 'Finished reading the xi0.log file'

if (len(a) != len(qarray)): print 'Something is wrong'

xvalues = []
yvalues = []

rs = 2.07
kF = 3.63/(rs)

print 'kF =', kF

eps_array = []

for i in range(len(qarray)):

    qvec = qarray[i]
    #print 'qvec = ', qvec
    for j in range(len(a[i])):
        gvec = [float(a[i][j][0]), float(a[i][j][1]), float(a[i][j][2])]
        gvec_prime = [float(a[i][j][3]), float(a[i][j][4]), float(a[i][j][5])]
        if (gvec == gvec_prime):

            inverse_epsilon = float(a[i][j][6])
            qvec_plus_gvec = np.add(qvec,gvec)
            new_vector = b[0]*qvec_plus_gvec[0] + b[1]*qvec_plus_gvec[1] + b[2]*qvec_plus_gvec[2]
            #print '    new =', new_vector     
            vector_length = (new_vector[0]**2 + new_vector[1]**2 + new_vector[2]**2)**0.5
 
            eps_array.append([vector_length/kF, inverse_epsilon])

eps_array = np.array(eps_array)
#eps_array = np.sort(eps_array,axis=0)

outputFile = open('epsinv.dat','w')

xarray = []
yarray = []
for i in range(len(eps_array)):

    outputFile.write(str(eps_array[i][0]) + ' ' + str(eps_array[i][1]) + ' \n')
    xarray.append(eps_array[i][0])   
    yarray.append(eps_array[i][1])   
outputFile.close()


plt.scatter(xarray, yarray)
plt.show()

