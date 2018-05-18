#!/bin/python3
# CS 486 Assignment 3 Question 1
# By: Eric Pan
import random,math,sys

# Tree structure
# attribute - what's being tested at this node
# left subtree - default True (word (attribute) is in the article)
# right subtree - default False otherwise

# Constants
LabelOne = 1
LabelTwo = 2

class Node:
	# attribute - wordId
	# label - none if it's an internal node, otherwise 1 or 2 
	def __init__(self,attribute=None,label=None,gain=None,left=None,right=None):
		self.attribute = attribute
		self.label = label
		self.left = left
		self.gain = gain
		self.right = right

	# Function to print a tree
	def PrintTree(self, depth=0):
	    treeString = ""
	    # Recurse through right side of the tree
	    if self.right != None:
		    treeString += self.right.PrintTree(depth + 1)
		# If current node is an internal node
	    if self.attribute != None:
		    treeString += "\n" + ("  "*depth) + "({},{})".format(self.attribute,self.gain)
	    # If current node is a left node
	    else:
		    treeString += "\n" + ("  "*depth) + str(self.label)
		# Recurse through left side of the tree
	    if self.left != None:
	 	    treeString += self.left.PrintTree(depth + 1)

	    return treeString

	# Return the current node's attribute
	def getAttribute(self):
		return self.attribute
	
	# Function to test a point againist the decision tree
	def testPoint(self,point):
		# Check if current node is a leaf node
		if self.label != None:
			return self.label

		# Check if point has attribute word, and recurse left/right until leaf node is reached
		if point.checkContainsWord(self.attribute):
			return self.left.testPoint(point)
		else:
			return self.right.testPoint(point)

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

# Function DTL, same as the class's version
def DTL(examples,attributes, default,maxDepth):
	if examples.isEmpty():
		return Node(None,default)
	elif examples.SameType():
		return Node(None,examples.SameType())
	# If the maxDepth is reached return the current example's mode
	elif not attributes or maxDepth == 0:
		return Node(None,examples.mode())
	else:
		print("Choosing best attribute")
		best = examples.ChooseAttribute(attributes)
		print("Chosen ID:",best.attribute)
		print("Word is",attributes[best.attribute-1])
		result = examples.split(best.getAttribute())
		# Recurse left and right depending if it has the attribute or not
		best.left = DTL(result[0],attributes,examples.mode(),maxDepth-1)
		best.right = DTL(result[1],attributes,examples.mode(),maxDepth-1)
		return best

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

# Main function to categorize data
def TextCategorize(maxDepth):
	print("-"*20)
	print("Step 1: Construct decision tree")
	# construct decision tree and get attributes (words)
	trainData = ConstructTrainingData("trainData.txt","trainLabel.txt")
	attributes = ConstructAttributes("words.txt")
	
	dt = DTL(trainData,attributes,trainData.mode(),maxDepth)
	print("DECISION TREE:")
	print(dt.PrintTree())

	print("-"*20)
	print("Step 2: Test decision tree againist test data")
	testData = ConstructTrainingData("testData.txt","testLabel.txt")
	correct = 0
	for point in testData.listPoints:
		res = dt.testPoint(point)
		if res == point.getLabel():
			correct += 1
	print("# of Correct:",str(correct))
	print("Total # of test examples:",str(testData.numberOfExamples()))
	print("Accuracy: {}%".format(correct/testData.numberOfExamples() * 100))
	print("-"*20)
	print("Step 3: Test decision tree againist training data")
	correct = 0
	for point in trainData.listPoints:
		res = dt.testPoint(point)
		if res == point.getLabel():
			correct += 1
	print("# of Correct:",str(correct))
	print("Total # of training examples:",str(trainData.numberOfExamples()))
	print("Accuracy: {}%".format(correct/trainData.numberOfExamples() * 100))
			

# Main function
def main():
	script, maxDepth = sys.argv
	TextCategorize(int(maxDepth))

main()