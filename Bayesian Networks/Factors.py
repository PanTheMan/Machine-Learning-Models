# CS486 Assignment 2
# ID 20576124
# User: Expan

# Implementation of the 5 functions for variable elimination algorithm

import numpy as np
from functools import *
import itertools

# 0 for false 1 for true

class Factor:
	def __init__(self,variableList, assignmentLists, probList):
		self.variables = variableList
		dimensions = ()
		for var in variableList:
			dimensions += (2,)
		# Set empty numpy array
		self.array = np.zeros(dimensions)

		# For each assignment which will be len(variableList) size of True or False values for each variable
		for i in range(len(assignmentLists)):
			Index = ()
			for assignment in assignmentLists[i]:
				# If assignment is true, then 1
				if assignment:
					Index += (1,)
				# Else 0
				else:
					Index += (0,)
			# Set probability at Index 
			self.array[Index] = probList[i]

		# Special case when we have one variable and it's only one possible value due to evidence
		self.SetVariablePair = []
	#print array
	def Print(self):

		# Row contains len(self.variables)+1 placeholders (1 for the value and one for each variable)
		row = "{!s:{width}}"
		
		for v in self.variables:
			row += '{!s:{width}}'



		# List of iterators to go through each value

		# Special case when we restrict so that there's only one value and one variable in the array (Messes it up because it expects 2 values for one variable)
		if(self.array.size == 1):
			row += "{!s:{width}}"
			# Print special header
			print(row.format("Value", self.SetVariablePair[0], width=10))
			print(row.format("{0:.7f}".format(self.array[0]).rstrip('0').rstrip('.'), self.SetVariablePair[1], width=10))
		else:
			# Print header
			print(row.format("Value", *self.variables, width=10))
			iterator = list(itertools.product([0, 1], repeat=len(self.variables)))
			for it in iterator:
				print(row.format("{0:.7f}".format(self.array[it]).rstrip('0').rstrip('.'), *[True if val == 1 else False for val in it], width=10))

	def Restrict(self, variable, value):
		sliceArray = []
		# Create slice index 
		for var in self.variables:
			# If restricting on variable, use 1 if True and 0 else
			if var == variable:
				if value:
					sliceArray.append(1)
				else:
					sliceArray.append(0)
			# If not the restricten variable, slice over all values for the variable
			else:
				sliceArray.append(slice(0,2))
		# New array is the sliced version
		self.array = self.array[sliceArray]
		# Remove the variable from variable list

		# Consider special case when it's the only variable left, in which case do nothing
		self.variables = [v for v in self.variables if v != variable]

		if len(self.variables) == 0:
			self.SetVariablePair = [variable,value]

	def multiply(self, other):
		# New variables is all unique variables from combined list
		NewVariables = self.variables+[var for var in other.variables if var not in self.variables]
		# Create new factor
		Product = Factor(NewVariables,[],[])
		# Create all possible indexes for the new product array, by creating all lists of size len(NewVariables) where each element is 0 or 1
		lst = list(itertools.product([0, 1], repeat=len(NewVariables)))
		
		# Create special variable index location for "other factor" for each iterator of the Product factor 
		IdxOfOtherInNew = []
		for var in other.variables:
			IdxOfOtherInNew.append(NewVariables.index(var))

		# For each iterator of product array, calculate probability based on self and other factors
		for it in lst:
			idxs = ()

			# get 1 or 0 values for each variable in other factor
			for x in IdxOfOtherInNew:
				idxs += (it[x],)

			# Because of how NewVariables is set up, i just slice the first len(self.variables) to get index for self factor
			# idxs will contain index for other factor
			Product.array[it] = self.array[it[0:len(self.variables)]] * other.array[idxs]

		return Product

	# Sumout function
	def sumout(self,variable):
		sliceArray = []
		# Find index of the variable in the variable list
		idx = self.variables.index(variable)
		# Then sum based on the axis to get new variable, new array has 1 less dimension than before
		self.array = np.sum(self.array,axis=idx)
		# Remove variable from the variable list
		self.variables = [v for v in self.variables if v != variable]

	# Normalize
	def normalize(self):
		# Get total sum using numpy methods
		sumTotal = np.sum(self.array)
		# Then divide by scalar vector
		self.array = self.array / sumTotal

# Special Function to print out intermediate steps and all
def FormatPrint(statement,factors):
	print(statement)
	print('-'*50)
	for factor in factors:
		# print(factor.array)
		factor.Print()
		print()
	print('-'*50)

def inference(factorList, queryVariables, hiddenVariables, evidenceList):
	# assumed format for evidence is list of lists, and list has two values, first is variable, second is value
	# Gather variable names
	evidenceVariables = [evidence[0] for evidence in evidenceList]
	# Remove variables not used anywhere
	hiddenVariables = [ x for x in hiddenVariables if x not in queryVariables and x not in evidenceVariables ]

	for evidence in evidenceList:
	    for factor in factorList:
	        # If the evidence variable is used in the factor, restrict based on evidence values
	        if evidence[0] in factor.variables:
	            factor.Restrict(evidence[0], evidence[1])

	# Printout what evidence was used
	if len(evidenceList) > 0:
		evid =  [ '{!s}, {!s}'.format(evid[0],evid[1]) for evid in evidenceList]
	else:
		evid = 'None'
	FormatPrint('Result of restricting factors on evidence {!s}'.format(evid), factorList)

	# Now remove all variables one by one
	for hiddenVar in hiddenVariables:
		# Find all factors using hiddenVar
		factorsWithHiddenVar = []
		for factor in factorList:
			for var in factor.variables:
				if var == hiddenVar:
					factorsWithHiddenVar.append(factor)
					# Break because we found one
					break

	    # Get rest of the factors with no hiddenVar in them
		factorList = [ factor for factor in factorList if factor not in factorsWithHiddenVar ]

	    # If there are factors with HiddenVar, multiply them all together
		if len(factorsWithHiddenVar) > 0:
			productFactor = reduce(Factor.multiply, factorsWithHiddenVar)
		else:
			continue

		FormatPrint('New product factor on {!s}'.format(hiddenVar),[productFactor])
	    
		# Sum over variable
		productFactor.sumout(hiddenVar)
		FormatPrint('Summing out variable {!s} to get final intermediate factor'.format(hiddenVar),[productFactor])

		# Add new factor back to list
		factorList.append(productFactor)

	# After removing all hidden variables, should only have query variables left
	inferredFactor = reduce(Factor.multiply, factorList)
	FormatPrint('Result of final multiplication with only query variables: {!s}'.format(queryVariables),[inferredFactor])
	# Normalize at the end
	inferredFactor.normalize()
	FormatPrint('Normalized result',[inferredFactor])
	return inferredFactor
