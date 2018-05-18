#!/bin/python3
# CS 486 Assignment 3 Question 2
# By: Eric Pan
import math
# Constants
LabelOne = 1
LabelTwo = 2

# Classs to hold the test/training data articles
class Data:
	# Set to empty
	def __init__(self):
		self.listPoints = []
	# Add data points/examples
	def addPoint(self,point):
		self.listPoints.append(point)

	# Count how many examples in the data are label 1	
	def labelOneExamples(self):
		count = 0
		for point in self.listPoints:
			if point.getLabel() == LabelOne:
				count += 1
		return count

	# Count how many examples in the dataare label 2
	def labelTwoExamples(self):
		count = 0
		for point in self.listPoints:
			if point.getLabel() == LabelTwo:
				count += 1
		return count

	# Find which label is more popular
	def mode(self):
		# If we get more label twos, return 2 as the mode
		if self.labelOneExamples() < self.labelTwoExamples():
			return LabelTwo
		# If we get more label one, return 1 as the mode	
		elif self.labelTwoExamples() < self.labelOneExamples():
			return LabelOne
		# If the counts are equal, do a random number generator to decide what to return
		else:
			# print("RANDOM")
			if random.uniform(0,1) < 0.5:
				return LabelOne
			else:
				return LabelTwo

	# Check if there are still points
	def isEmpty(self):
		return not self.listPoints

	# Count how many examples there are in total
	def numberOfExamples(self):
		return len(self.listPoints)

	# Check if all the examples are the same label
	# if so, return the type 1/2, otherwise return False
	def SameType(self):
		type = self.listPoints[0].getLabel()
		for point in self.listPoints[1:]:
			# If the label is ever different from the others, return False immediately
			if point.getLabel() != type:
				return False
		# Otherwise they are all the same label, so return it
		return type

	# Calculate entropy for data set
	def entropy(self):
		# Get total number of data points and return 0 if we have none
		totalNum = self.numberOfExamples()
		if totalNum == 0:
			return 0

		# Get number of label one and two data points, and calculate the fraction each label appears in the data
		labelOne = self.labelOneExamples()
		labelTwo = self.labelTwoExamples()
		labelOneFraction = labelOne/totalNum
		labelTwoFraction = labelTwo/totalNum
		# If any of the label counts don't have any such data points, set the other part to 0
		# Use the formula learned in class for entropy
		if labelOne == 0:
			return -labelTwoFraction*math.log(labelTwoFraction,2)
		elif labelTwo == 0:
			return -labelOneFraction*math.log(labelOneFraction,2)
		return -labelOneFraction*math.log(labelOneFraction,2) -labelTwoFraction*math.log(labelTwoFraction,2)

	# Function to split data in two lists based on label
	def split(self,attribute):
		appearsIn = Data()
		doesntAppear = Data()
		# Recurse through each data point and put them into 2 different data storage variables
		for point in self.listPoints:
			if point.checkContainsWord(attribute):
				appearsIn.addPoint(point)
			else:
				doesntAppear.addPoint(point)
		return [appearsIn,doesntAppear]

	# calculate remainder for an attribute
	def remainder(self,attribute):
		remain = 0
		splitSet = self.split(attribute)
		# Following formula for remainder
		for dataSet in splitSet:
			weight = (dataSet.labelOneExamples()+dataSet.labelTwoExamples())/self.numberOfExamples()
			entropy = dataSet.entropy()
			remain += weight*entropy
		return remain

	# Calculate total information gain for an attribute
	def InformationGain(self,attribute):
		# IG = Entropy - Remainder(A)
		entropy = self.entropy()

		remainder = self.remainder(attribute)
		return entropy-remainder

	# Choose the best attribute
	def ChooseAttribute(self,attributes):
		best = (-1,-1)
		# Parse through all the attributes
		for idx in range(1,len(attributes)+1):
			gain = self.InformationGain(idx)
			if gain > best[1]:
				best = (idx,gain)
		return Node(best[0],None,best[1])

# Article info, containing what words it has
class Article:
	def __init__(self,label,docId):
		self.label = label
		self.id = docId
		self.words = []
	# Add word to list of words article has
	def addWord(self, wordId):
		self.words.append(wordId)
	def getLabel(self):
		return self.label
	# Check if a word appears in the article
	def checkContainsWord(self,wordId):
		return wordId in self.words


# Get all the words and create one list containing all the words
def ConstructAttributes(wordFileName):
	listWords = []
	words =	open(wordFileName)
	word = words.readline()
	while word:
		listWords.append(word)
		word = words.readline()
	return listWords

# create articles for each unique docId and store them as data points
def ConstructTrainingData(dataFileName,labelFileName):
	TrainingData = Data()
	# Open files
	labelFile = open(labelFileName,'r')
	dataFile = open(dataFileName,'r')

	docId = 1
	label =	labelFile.readline()
	article = Article(int(label),int(docId))
	
	TrainingData.addPoint(article)
	
	# Recurse through all lines in the data file
	lineData = dataFile.readline()
	while lineData:
		# two values on eahc line
		document,word = lineData.split()
		# while this is for the same docId
		if int(document) == docId:
			article.addWord(int(word))
		# Otherwise, new document, so create new article and add it to TrainingData
		else:
			docId += 1
			label = labelFile.readline()
			article = Article(int(label),int(docId))
			TrainingData.addPoint(article)
			article.addWord(int(word))

		lineData = dataFile.readline()


	# Close files
	labelFile.close()
	dataFile.close()
	return TrainingData


# Load data
trainData = ConstructTrainingData("trainData.txt","trainLabel.txt")
attributes = ConstructAttributes("words.txt")
testData = ConstructTrainingData("testData.txt","testLabel.txt")

# Function to calculate Theta value for an attribute
# Same as slides
def thetaCalculate(examples,attribute):
	attrSplit = examples.split(attribute)
	TotalLabelOnes = examples.labelOneExamples()
	TotalLabelTwos = examples.labelTwoExamples()	
	# Idx = 0 contains how many examples have class 1 and DOES contain attribute
	# Idx = 1 contains how many examples have class 1 and DOES NOT contain attribute
	# Idx = 2 contains how many examples have class 2 and DOES contain attribute
	# Idx = 3 contains how many examples have class 2 and DOES NOT contain attribute
	counter = [attrSplit[0].labelOneExamples(),attrSplit[1].labelOneExamples(),attrSplit[0].labelTwoExamples(),attrSplit[1].labelTwoExamples()]
	thetaContainsAttrLabelOne = (counter[0]+1)/(TotalLabelOnes+2)
	thetaNotContainsAttrLabelOne = (counter[1]+1)/(TotalLabelOnes+2)
	thetaContainsAttrLabelTwo = (counter[2]+1)/(TotalLabelTwos+2)
	thetaNotContainsAttrLabelTwo = (counter[3]+1)/(TotalLabelTwos+2)
	# Holds the probabilities for an attribute
	return [[LabelOne,thetaContainsAttrLabelOne,thetaNotContainsAttrLabelOne,0],[LabelTwo,thetaContainsAttrLabelTwo,thetaNotContainsAttrLabelTwo,0]]

# Create a naive bayes model so that it has for each attribute, the related probabilities
def NaiveBayesModel(examples):
	model = []
	# Calculate theta values for each label
	thetaLabel1 = (examples.labelOneExamples()+1)/(examples.numberOfExamples()+2)
	thetaLabel2 = (examples.labelTwoExamples()+1)/(examples.numberOfExamples()+2)

	# Go through each attribute and calculate probabilities
	for attr in range(1,len(attributes)+1):
		# theta contains all probabilities for each label one and two and whether or not it contains attr
		theta = thetaCalculate(examples, attr)
		
		theta[0][3] = thetaLabel1
		theta[1][3] = thetaLabel2

		model.append(theta)
	return model

# Function to test data againist model created
def testModel(model,data):
	numCorrect = 0
	# Try each data point in data
	for point in data.listPoints:
		# Set the two probabilities i'm comparing, initially to the probabilities of label 1 and label 2
		ProbLabelOne = math.log(model[0][0][3])
		ProbLabelTwo = math.log(model[0][1][3])
		# For each attribute, increase the probability for each label by the natural log of the probability 
		for i in range(len(attributes)):
			probabilities = model[i]
			# i+1 is the actual wordId
			if point.checkContainsWord(i+1):
				ProbLabelOne += math.log(probabilities[0][1])
				ProbLabelTwo += math.log(probabilities[1][1])
			else:
				ProbLabelOne += math.log(probabilities[0][2])
				ProbLabelTwo += math.log(probabilities[1][2])
		# Check which probability is higher and get which label to choose
		res = 0
		if ProbLabelOne > ProbLabelTwo:
			res = LabelOne
		else:
			res = LabelTwo
		# If the label choosen, is the actual label, increase how many the model got correct
		if res == point.getLabel():
			numCorrect += 1
	return numCorrect

model = NaiveBayesModel(trainData)
totalCorrect = testModel(model,testData)
print("Total # of documents correctly classified for test data", totalCorrect)
print("Total # of documents in test data", testData.numberOfExamples())
print("Accuracy against test data: ", totalCorrect/testData.numberOfExamples()*100)
totalCorrect = testModel(model,trainData)
print("Total # of documents correctly classified for training data", totalCorrect)
print("Total # of documents in training data", trainData.numberOfExamples())
print("Accuracy: against training data", totalCorrect/trainData.numberOfExamples()*100)


# Get top 10 words
diff = []
# for each attribute, use the formula from the assignment and calculate the result
for i in range(len(attributes)):
	setRes = [0,0]
	setRes[0] = i
	setRes[1] = math.fabs(math.log(model[i][0][1])-math.log(model[i][1][1]))
	diff.append(setRes)

# Sort by the value to look for 10 biggest values
diff = sorted(diff, key = lambda x: x[1])
# Print the words
print("Top 10 words:")
for i in range(10):
	print(attributes[diff[len(attributes)-i-1][0]],diff[len(attributes)-i-1][1])



