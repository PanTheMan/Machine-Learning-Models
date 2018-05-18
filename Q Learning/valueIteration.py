# CS486 Assignment 4
# Eric Pan, expan
# 20576124
# Question 1

from gridworld import *
import math

grid,rewards = gridWorld(0.05)
discount = 0.99
maxError = 0.01
# States are 0-16, 16 is special, actions are 0-3

# Constants for the movements
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
NUMSTATES = 17
actions = [UP,DOWN,LEFT,RIGHT]
printActions = ["UP","DOWN","LEFT","RIGHT"]

# Given an action and the current state, find all possible results from the action
def getPossibleStates(currState,action):
	# special case for 16 and 15
	if currState == 16:
		return [16]
	if currState == 15:
		return [16]	
	if currState == 0:
		return [0,1,4]
	else: 
		#In order of up,down,left,right
		possibleStates = [currState-4,currState+4,currState-1,currState+1]
		# if any of the states excede the boundaries of the scare, we can replace them with the currstate, since we wouldn't move
		possibleStates = [currState if state<0 or state>15 else state for state in possibleStates]
		# Special case when we're on the left side of the grid and move left,up,or down. Then we can replace the left movement with currstate
		if (currState == 4 or currState == 8 or currState == 12) and action != RIGHT :
			possibleStates[2] = currState
		# Similar special case to above lines, except on opposite sides
		if (currState == 3 or currState == 7 or currState == 11) and action != LEFT:
			possibleStates[3] = currState

		# Given an action, we can't move in the opposite direction, so remove from the list of 4 moves
		if action == UP:
			del possibleStates[DOWN]
		elif action == DOWN:
			del possibleStates[UP]
		elif action == RIGHT:
			del possibleStates[LEFT]
		else:
			del possibleStates[RIGHT]

		# Return the list of possible states, with duplicates removed
		return list(set(possibleStates))

# function to get the best action given currenstate and previous results
def GetBestAction(transition, currValues,currState):
	maxValue = None
	bestAction = None

	# Try each action and get best action value
	for action in actions:
		sumStateValues = 0
		possStates = getPossibleStates(currState,action)
		# For each state, get position value and sum it all up for an action
		for state in possStates:
			sumStateValues += transition[currState,state,action]*currValues[state]

		# If we get a bigger value, or it's the first value we calculated, set the maxValue variable to new max
		if maxValue is None or maxValue < sumStateValues:
			# print("Found max:",action)
			maxValue = sumStateValues
			bestAction = action
	# return value and action
	return maxValue,bestAction

# Function to run value iteration formula from class
def ValueIteration(transition,reward,gamma,error):
	# set variables up 
	newValues = np.zeros((17))
	oldValues = np.zeros((17))
	changeInValues = np.ones((17))
	bestActions = np.zeros((17))
	# variable flag to stop looping
	stop = True


	while True:
		# copy over the new values to the old 
		oldValues = np.copy(newValues)

		# For each state, find the best action to take
		for i in range(17):
			sumValue,action = GetBestAction(transition,oldValues,i)
			# calculate new values using the formula from class
			newValues[i] = reward[i] + gamma * sumValue
			# Set the change in values
			changeInValues[i] = abs(newValues[i]-oldValues[i])
			# array to hold the most recent best actions
			bestActions[i] = action
		# Check if we should finish looping, by looking at difference
		for i in range(17):
			if changeInValues[i] >= error:
				stop = False

		# If flag wasn't set to false, we're done
		if stop:
			break
		
		# reset flag
		stop = True

		# Shouldn't be reached here until the above break doesn't occur
		# print()
		# print(newValues)
		# print("CHANGE")
		# print(changeInValues)
		# print()


	print("OPTIMAL POLICY")

	for state in range(len(bestActions)):
		print(state, printActions[int(bestActions[state])])

	print("Optimal Values")
	for state in range(len(newValues)):
		print(state, newValues[state])

	return newValues

print("For a = 0.9, b = 0.05")
ValueIteration(grid,rewards,discount,maxError)
print()
print("For a = 0.8, b = 0.1")
grid,rewards = gridWorld(0.1)
ValueIteration(grid,rewards,discount,maxError)
