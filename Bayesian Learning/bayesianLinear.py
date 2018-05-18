#/usr/bin/python3
import numpy as np
import csv
import math

xDataSets = [[],[],[],[],[],[],[],[],[],[]]
yDataSets= [[],[],[],[],[],[],[],[],[],[]]

# Import the data and labels
for i in range(10):
	with open('fdata%d.csv' % (i+1), newline='') as datafile:
		dataReader = csv.reader(datafile, delimiter=' ', quotechar='|')
		with open('flabels%d.csv' % (i+1), newline='') as labelsfile:
			labelsReader = csv.reader(labelsfile, delimiter=' ', quotechar='|')
			for dataRow,labelRow in zip(dataReader,labelsReader):
				xDataSets[i].append(list(map(float,dataRow[0].split(','))))
				yDataSets[i].append(float(labelRow[0])) 

# use the fact that each data point, x only has 2 values in it
def genBasis(deg, x1, x2):
	basisList = []
	for i in range(deg+1): 
		for j in range(deg+1 - i):
			basisList += [math.pow(x1, i) * math.pow(x2, j)]
	return basisList

for deg in range(1,5):
	# 10-fold
	error = 0.0
	for i in range(10):
		trainingDataX = []
		trainingDataY = []

		# Separate the data into training and test sets
		for a in range(10):
			if a != i:
				trainingDataX += xDataSets[a]
				trainingDataY += yDataSets[a]
			else:

				xTest = np.array([genBasis(deg,x[0],x[1]) for x in xDataSets[a]])
				yTest = np.array(yDataSets[a])

		test = [genBasis(deg,x[0], x[1]) for x in trainingDataX]
		xTraining = np.array(test)
		yTraining = np.array(trainingDataY)

		A = np.linalg.inv( np.transpose(xTraining).dot(xTraining) + np.identity(xTraining.shape[1]) )
		for m in range(len(xTest)):
			predict = yTraining.dot(xTraining.dot(np.transpose(A.dot(xTest[m]))))
			error += np.sum(np.square(yTest[m]-predict))/yTest.shape[0]
	print ("For degree: %s, Avg error: %s" % (deg, error/10))
