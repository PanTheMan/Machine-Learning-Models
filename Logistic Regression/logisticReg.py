#/usr/bin/python3
import numpy as np
import csv
import math

# Import data
xDataSets = [[],[],[],[],[],[],[],[],[],[]]
yDataSets= [[],[],[],[],[],[],[],[],[],[]]
def sigmoid(x):
	return 1/ (1+np.exp(-x))

def computeHessian(xTraining, weight):
	N = xTraining.shape[0]
	R = np.zeros((N,N))
	for i in range(N):
		R[i][i] = sigmoid(weight.transpose().dot(xTraining[1])) * (1-sigmoid(weight.transpose().dot(xTraining[1])))
	return xTraining.transpose().dot(R).dot(xTraining)

for i in range(10):
	with open('data%d.csv' % (i+1), newline='') as datafile:
		dataReader = csv.reader(datafile, delimiter=' ', quotechar='|')
		with open('labels%d.csv' % (i+1), newline='') as labelsfile:
			labelsReader = csv.reader(labelsfile, delimiter=' ', quotechar='|')
			for dataRow,labelRow in zip(dataReader,labelsReader):
				xDataSets[i].append( [1]+list(map(float,dataRow[0].split(','))))
				yDataSets[i].append( float(labelRow[0])) 
avg = 0
for i in range(10):
	trainingDataX = []
	trainingDataY = []
	correct = 0
	total = 0
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

	# newton iteration

	w = np.random.rand(xTraining.shape[1],1) * 0.02 - 0.01
	# print(w.shape)
	yTraining = yTraining[:,np.newaxis]
	for j in range(10):
		# Calculat gradient (L)
		val = sigmoid(xTraining.dot(w))
		sigma = yTraining - val
		gradient = xTraining.T.dot(sigma)

		# Calculate the hessian's R matrix
		Rs = -val * (1-val)
		R = np.diag(Rs.ravel())
		# Get hessian matrix
		H = xTraining.T.dot(R.dot(xTraining))
		# adjust weights
		w = w - np.linalg.inv(H).dot(gradient)


	for m in range(len(xTest)):
		probC1  = sigmoid(xTest[m].dot(w))
		if(probC1 >= 0.5):
			prediction = 6
		else:
			prediction = 5

		if prediction == yTest[m]:
			correct = correct + 1
		total = total + 1
	print("K=%d: %d/%d" % (i,correct, total))
	avg += correct
print(avg/1110)