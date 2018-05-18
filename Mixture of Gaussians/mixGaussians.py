#/usr/bin/python3
import numpy as np
import csv
import math
def gaussian(x, mu, sig):
	return np.exp(-np.power(x-mu, 2.) / (2*sig)) / np.sqrt(2*math.pi*sig)

# Import data
xDataSets = [[],[],[],[],[],[],[],[],[],[]]
yDataSets= [[],[],[],[],[],[],[],[],[],[]]

for i in range(10):
	with open('data%d.csv' % (i+1), newline='') as datafile:
		dataReader = csv.reader(datafile, delimiter=' ', quotechar='|')
		with open('labels%d.csv' % (i+1), newline='') as labelsfile:
			labelsReader = csv.reader(labelsfile, delimiter=' ', quotechar='|')
			for dataRow,labelRow in zip(dataReader,labelsReader):
				xDataSets[i].append( list(map(float,dataRow[0].split(','))))
				yDataSets[i].append( float(labelRow[0])) 


for i in range(10):
	print(i)
	correct = 0
	total = 0
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

	yTraining = np.array(trainingDataY)
	yTraining = yTraining - 5 

	# Maximum likelihood parameter calculation:
	# print(yTraining.size, np.size(xTraining,0))

	labels, counts = np.unique(yTraining, return_counts=True)
	pi = counts.astype('float')/yTraining.shape[0]
	muList = []
	sList = []
	for label in labels:
		classData = xTraining[yTraining == label]
		mu = np.mean(classData, axis=0)
		muList += [mu]
		classData= classData - mu
		covar = classData.transpose().dot(classData)/classData.shape[0]
		sList += [covar]


	yPred = np.zeros(xTest.shape[0], dtype='int')

	sigma = (sList[0]*counts[0] + sList[1]*counts[1]) / xTraining.shape[0]
	
	for idx in range(len(xTest)):
		probs = []
		for label in labels:
			label = int(label)
			prob = pi[label]
			prob *= np.exp(-1/2*(xTest[idx]-muList[label]).transpose().dot(np.linalg.inv(sigma)).dot(xTest[idx]-muList[label]))
			probs += [prob]
		if probs[0] > probs[1]:
			classify = 5
		else:
			classify = 6
		if classify == yTest[idx]:
			correct = correct + 1
		total = total + 1
	print("K = %d: %d/%d" % (i,correct,total))

