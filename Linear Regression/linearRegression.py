#/usr/bin/python3
import numpy as np
import csv
# alpha = 0.0

xDataSets = [[],[],[],[],[],[],[],[],[],[]]
yDataSets= [[],[],[],[],[],[],[],[],[],[]]

# Import the data and labels
for i in range(10):
	with open('Assignment 3/fdata%d.csv' % (i+1), newline='') as datafile:
		dataReader = csv.reader(datafile, delimiter=' ', quotechar='|')
		with open('Assignment 3/flabels%d.csv' % (i+1), newline='') as labelsfile:
			labelsReader = csv.reader(labelsfile, delimiter=' ', quotechar='|')
			for dataRow,labelRow in zip(dataReader,labelsReader):
				xDataSets[i].append( [1]+list(map(float,dataRow[0].split(','))))
				yDataSets[i].append( float(labelRow[0])) 

# Try each alpha value
for alpha in np.arange(0.0,4.1,0.1):
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
				xTest = np.array(xDataSets[a])
				yTest = np.array(yDataSets[a])

		xTraining = np.array(trainingDataX)
		print(xTraining.shape)
		yTraining = np.array(trainingDataY)

		# Calculate weights w, using Aw = b
		A = np.linalg.inv(alpha*np.identity(xTraining.shape[1]) + np.transpose(xTraining).dot(xTraining))
		print(A.shape)
		w = A.dot(np.transpose(xTraining)).dot(yTraining)
		prediction = xTest.dot(w)

		# Use euclidean loss algorithm
		error += 0.5 * np.sum(np.square(yTest-prediction)) 
	print ("For alpha: %s, Avg acc: %s" % (alpha, error/10))

