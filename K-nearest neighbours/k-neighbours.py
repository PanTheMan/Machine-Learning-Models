#/usr/bin/python3
import csv, math, operator,random

# Calculate euclidean distance
def euclideanDist(point1, point2):
	distance = 0
	for x in range( len(point1) ):
		distance += pow((point1[x]-point2[x]),2)
	return math.sqrt(distance)

# Get the k nearest neighbours near the test point
def getNeighbours(training, testPoint, k):
	distances = []
	for x in range(len(training)):
		dist = euclideanDist(testPoint[0], training[x][0])
		distances.append((training[x][0], training[x][1], dist))

	distances.sort(key=operator.itemgetter(2))
	neighbours = []
	for x in range(k):
		neighbours.append(distances[x])
	# print("Testpoint: %s" % "".join([str(x) for x in testPoint] ))
	# print("Nearest neighbours: %s" % neighbours)
	return neighbours

# Given a list of points, get the most common label
def getLabel(neighbours):
	labelFive = 0
	labelSix = 0
	for neighbour in neighbours:
		if neighbour[1] == 5:
			labelFive += 1
		else:
			labelSix += 1
	if labelFive > labelSix:
		return 5
	# break ties randomly
	elif labelFive == labelSix:
		return random.randint(0, 1) + 5
	else:
		return 6


# Import data
dataSets = [[],[],[],[],[],[],[],[],[],[]]
for i in range(10):
	with open('data%d.csv' % (i+1), newline='') as datafile:
		dataReader = csv.reader(datafile, delimiter=' ', quotechar='|')
		with open('labels%d.csv' % (i+1), newline='') as labelsfile:
			labelsReader = csv.reader(labelsfile, delimiter=' ', quotechar='|')
			for dataRow,labelRow in zip(dataReader,labelsReader):
				dataSets[i].append( (list(map(int,dataRow[0].split(','))), int(labelRow[0])) )

# Increment k 
for k in range(1,31):
	# Keep track of how accurate this is
	totalPoints = 0
	totalCorrect = 0
	# 10-fold
	for i in range(10):
		trainingSet = []
		# Group all the training data
		for j in range( len(dataSets) ):
			if i != j:
				trainingSet += dataSets[j]

		testSet = dataSets[i]
		for point in testSet:
			neighbourList = getNeighbours(trainingSet, point, k)
			result = getLabel(neighbourList)
			if result == point[1]:
				totalCorrect += 1
			totalPoints += 1

	print("For k = %d: %d/%d" % (k, totalCorrect, totalPoints))