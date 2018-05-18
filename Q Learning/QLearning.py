# CS486 Assignment 4
# Eric Pan, expan
# 20576124
# Question 2

from gridworld import *
import math
import random

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


# Given all the Qvalues and the current state, choose the action with the highest value
def bestQValueAction(QValues,currState):
	bestQValue = None
	bestAction = None
	# Iterate through all the actions looking at QValue
	for action in actions:
		if bestQValue is None or bestQValue < QValues[currState,action]:
			bestQValue = QValues[currState,action]
			bestAction = action
	return bestAction,bestQValue		

# Function to implement the e-greedy formula
def ChooseAction(greedy,currState,QValues):
	# If we get a random value below greedy, we choose to do the best action
	if greedy > random.uniform(0,1):
		action, value = bestQValueAction(QValues,currState)
		return action
	# Otherwise, we just choose a random direction
	else:
		# Return a random direction 
		return actions[random.randint(0,3)]

# Similar to value iteration
# Given a state and an action, get the possible end states from the action
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


# Simulate what happens when an action is taken at the current state
def ResultAction(currState,action):
	# Get possible states
	possStates = getPossibleStates(currState,action)
	# Get a random number between 0 and 1
	randomRes = random.uniform(0,1)
	prevPossSum = 0
	# For each state see if number generated is that action
	for state in possStates:
		prevPossSum += grid[currState,state,action]
		# If number falls in the probabilitiy range
		if randomRes < prevPossSum:
			return state

# Q Learning function that follows the algorithm from class
def QLearning(discount,greedy):
	QValue = np.zeros((17,4))
	TimesVisited = np.zeros((17,4))
	# Start at 4
	currState = 4
	# Number 
	numTimesRan = 0
	# Run through 10000 times
	while numTimesRan < 10000:
		while currState != 16:
			# Get best action
			bestAction = ChooseAction(greedy, currState, QValue)
			# Get next state
			nextState = ResultAction(currState,bestAction)
			# Max q value calculation
			maxQsaNext = bestQValueAction(QValue,nextState)[1]
			# Incremente how many times we've done this action at the current state
			TimesVisited[currState,bestAction] += 1
			# Run the formula from class
			# try:
			QValue[currState,bestAction] = QValue[currState,bestAction] + (rewards[currState]+discount*maxQsaNext-QValue[currState,bestAction])/TimesVisited[currState,bestAction]
			# except:
				# print("problem")
			# Set currente state to next state
			currState = nextState

		# print("Finished episode")
		# Reset current state to the start
		currState = 4
		# Finished running one episode, so increment
		numTimesRan += 1
	
	for i in range(NUMSTATES):
		print(i,':',bestQValueAction(QValue,i)[1])

	for i in range(NUMSTATES):
		print(i,':', printActions[int(bestQValueAction(QValue,i)[0])])

print("For e=0.2")
QLearning(0.99,0.8)
print()
print("For e=0.05")
QLearning(0.99,0.95)
