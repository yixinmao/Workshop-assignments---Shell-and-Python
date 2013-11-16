#!/usr/local/bin/python

import numpy as np
from os import listdir
import pdb

n = 49  # number of files
nl = 8387  # number of lines in each file


###########################################################
################ load lon, lat and data ###################
###########################################################
count = 0
lat = [[] for i in range(n)]
lon = [[] for i in range(n)]
data = np.empty((n, nl, 12))
for filename in listdir('./fluxes'):	
# read latitude and longitude into lists (lat and lon)
	lc = 7
	while (1):
		if filename[lc]!='_':
			lat[count].append(filename[lc])
			lc = lc + 1
		else:
			lc = lc + 1
			break
	while (1):
		if lc<len(filename):
			lon[count].append(filename[lc])
			lc = lc + 1
		else:
			break
	lat[count] = ''.join(lat[count])
	lon[count] = ''.join(lon[count])

# load data from each flux file
	data[count] = np.loadtxt('./fluxes/%s' % filename)
	count = count + 1

############################################################
####################### Problem 1 ##########################
############################################################
# calculate monthly mean precipitation for each grid
mon_prec = np.zeros((n, 12))
for i in range(n):  # for each grid
	count = np.zeros(12)
	for j in range(nl):
		mon_prec[i][int(data[i][j][1])-1] = mon_prec[i][int(data[i][j][1])-1] + data[i][j][3]
		count[int(data[i][j][1])-1] = count[int(data[i][j][1]-1)] + 1
	for j in range(12):  # average prec
		mon_prec[i][j] = mon_prec[i][j] / count[j]

# write results into files
for i in range(n):
	f = open('./monthly_prec/monthly_precipitation.<%s>_<%s>' %(lat[i], lon[i]), 'w')
	for j in range(12):
		f.write('%f\n' % mon_prec[i][j])
	f.close()
	

############################################################
###################### Problem 2 ###########################
############################################################
# calculate sum of weight
sum_w = 0
for i in range(n):
	w = np.cos(float(lat[i])/180.0*np.pi)
	sum_w = sum_w + w

# calculate areal mean
areal_mean_prec = np.empty(12)
for mon in range(12):
	sum = 0
	for i in range(n):
		w = np.cos(float(lat[i])/180.0*np.pi)
		sum = sum + mon_prec[i][mon] * w
	areal_mean_prec[mon] = sum / sum_w

# write results into file
f = open('areal_mean_monthly_prec', 'w')
for mon in range(12):
	f.write('%f\n' % areal_mean_prec[mon])
f.close()


				





