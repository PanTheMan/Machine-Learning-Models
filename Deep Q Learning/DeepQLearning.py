# CS486 Assignment 4
# Eric Pan, expan
# 20576124
# Question 3
# I DON"T KNOW WHAT I"M DOING ANTYMORE

import gym
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
import numpy as np
from collections import deque

env = gym.make('CartPole-v0')

# Create the keras model
def buildModel(stateSize,totalActions,learning):
	# Neural Net for Deep-Q learning Model
	model = Sequential()
	# 2 hidden layers of 10 units
	# First layer has 4 inputs
	model.add(Dense(10, input_dim=stateSize, activation='relu'))
	model.add(Dense(10, activation='relu'))
	# 2 outputs
	model.add(Dense(totalActions, activation='linear'))
	# Create model, using adam learning optimizer	
	model.compile(loss='mse', optimizer=Adam(lr=learning))
	return model

# make the next move
def move(currState, epsilon,actionSize,model):
	# If generated number is less than epsilon, we choose a random action
	if random.uniform(0,1) <= epsilon:
		return random.randint(0,actionSize-1)
	# Otherwise we predict values, and choose highest value
	else:
		actionValues = model.predict(currState)
		return np.argmax(actionValues[0])

# def target(model,reward,epsilon):
	# target = (reward + epsilon * np.amax(model.predict(next_state)[0]))

def remember(memory,currState, reward,done,nextState, action):
	memory.append((currState,reward,done,nextState,action))

# Experience replay function
# Use the past batchSize of episodes to learn
# SOMETHING IS WRONG HERE
# OR MY MODEL JUST SUCKS
def replay(memory, batchSize,model,discount):
	batch = random.sample(memory, batchSize)
	# Iterate through batch
	for currState,reward,done,nextState,actions in batch:
		if done:
			target = reward
		else:
			# Q learn equation
			target = (reward + discount *np.amax(model.predict(nextState)[0]))

		# Get what is expected
		targetExpected = model.predict(currState)
		targetExpected[0][action] = target
		# Then fit to our model
		model.fit(currState, targetExpected, epochs=1, verbose=0)

stateSize = env.observation_space.shape[0]
actionSize = env.action_space.n

# Constants for model
discount = 0.99
epsilon = 0.05
maxSteps = 500
numEpisodes = 1000
learningRate = 0.1
target = 2
model = buildModel(stateSize,actionSize,learningRate)
memory = deque(maxlen=1000)
batchSize = 50

# Run through all the episodes we want
f = open("results.txt","w+")
for e in range(numEpisodes):
	currState = env.reset()
	# Reshape to use with sequential model
	currState = np.reshape(currState, [1, stateSize])
	# Play an episode until finished
	for step in range(maxSteps):
		# Make an action
		action = move(currState,epsilon,actionSize,model)
		# Environment gives us the next steps
		nextState, reward, done, placeholder = env.step(action)
		nextState = np.reshape(nextState,[1,stateSize])
		# remember the action
		remember(memory,currState,reward,done,nextState,action)
		# If the game is over early, break
		if done:
			# Note the score is how many steps were taken for the game 
			f.write("{} {}\n".format(e,step))
			print('Episode: ', e, "score",step)
			break
		# Start replay when we have at least batchSize in memory
		if len(memory) > batchSize:
			replay(memory,batchSize,model,discount)
		# if step != 0 and step % 2 == 0:
		# 	target(model,reward,epsilon) 
f.close()