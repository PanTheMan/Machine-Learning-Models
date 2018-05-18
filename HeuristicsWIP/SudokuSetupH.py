import random

class square:
	def __init__(self,value,i,j):
		self.row = i
		self.col = j
		# List of what's been tried
		self.assignments = []

		if value == 0:
			self.value = 0
			self.possibilities = list(range(1,10)) # Go from 1 to 9
		else:
			self.value = value
			self.possibilities = []

	def UpdateValue(self,value):
		if value != 0:
			self.value = value
#			self.assignments.append(value)

	# Soft reset when a value fails, but there are still choices
	def Restore(self, possibilities):
		self.value = 0
		# Make sure we don't add, what's already been tried
		self.possibilities = [ pos for pos in possibilities if pos not in self.assignments ]

	# When possibilties is 0, backtrack instead of soft resetting
	def Backtrack(self, possibilities):
		self.value = 0
		self.possibilities = possibilities
		self.assignments = []

	# Used before heuristics
	# def RandomValue(self):
	# 	val = random.choice(self.possibilities)
	# 	self.assignments.append(val)
	# 	self.possibilities.remove(val)
	# 	return val

	def StillPossible(self):
		if len(self.possibilities) == 0:
			return False
		else:
			return True

	def __eq__(self, other):
		return (self.row == other.row) and (self.col == other.col)

	def __ne__(self, other):
		return not self == other

class Board:
	def __init__(self):
		# Create all 81 squares
		self.squareList = [[square(0,i,j) for j in range(9)] for i in range(9)]
		self.UnusedSquares = []

	# For when random choices were used
	# Keeps track of unused squares to run random choices for

	# def AddUnusedSquares(self,Square):
	# 	self.UnusedSquares.append(Square)

	# def RemoveUnusedSquare(self,idx):
	# 	self.UnusedSquares.pop(idx)

	# Find square at row i, column j	
	def FindSquare(self,i,j):
		return self.squareList[i][j]

	# Randomly choose an unused square
	# def RandomUnusedSquare(self):
	# 	idx = random.randint(0, len(self.UnusedSquares)-1)
	# 	Square = self.UnusedSquares[idx]
	# 	self.RemoveUnusedSquare(idx)
	# 	return Square

	# Defines the columns attribute (For start)
	def Cols(self):
		y = []
		for i in range(9):
			col = []
			for j in range(9):
				col.append(self.squareList[j][i])
			y.append(col)
		self.columns = y

	# Defines the boxes attribute (For start)
	def Boxes(self):
		# Define all the box layouts
		BoxCorners = [(0,0), (0,3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
		boxes = []
		for corner in BoxCorners:
			box = []
			for i in range(corner[0],corner[0]+3):
				for j in range(corner[1],corner[1]+3):
					box.append(self.squareList[i][j])
			boxes.append(box)
		self.boxes = boxes

	# Check that if the square has value, then the board is still valid
	# Assumes, square hasn't been updated to value already
	def CheckConstraints(self,square,value):
		# Check if value is in list of row values
		if value in [sq.value for sq in self.squareList[square.row]]:
			return False
		# Check if value is in list of column values
		if value in [sq1.value for sq1 in self.columns[square.col]]:
			return False
		# Check if value is in list of box values
		if value in [sq2.value for sq2 in self.boxes[int(square.row/3)*3+int(square.col/3)]]:
			return False
		return True

	# Update square with value
	def UpdateSq(self,square, value):
		square.UpdateValue(value)

	# For setting up the board at the very beginning, since square needs to be referenced by row and col
	def SetupSq(self,i,j, value):
		square.UpdateValue(self.squareList[i][j],value)

	# Check if board is finished
	def FinishCheck(self):
		for row in self.squareList:
			# Remove None values since it's blank
			RowValues = [sq.value for sq in row if sq.value is not 0]
			if not CheckDiffNums(RowValues):
				return False
		for col in self.columns:
			# Remove None values since it's blank
			ColValues = [sq.value for sq in col if sq.value is not 0]
			if not CheckDiffNums(ColValues):
				return False
		for box in self.boxes:
			# Remove None values since it's blank
			BoxValues = [sq.value for sq in box if sq.value is not 0]
			if not CheckDiffNums(BoxValues):
				return False
		return True

	def PrintBoard(self):
		for i in range(9):
			for j in range(9):
				print(self.squareList[i][j].value, end=' ')
			print("")

	# For random values and square	
	# def Restore(self,square):
	# 	self.AddUnusedSquares(square)
	# 	square.Backtrack([])

	# For at the start:
	# Preprocess, by changing possibilities to consider initial values on the board
	def Preprocess(self):
		for row in self.squareList:
			for sq in row:
				if sq.value != 0:
					for test in self.columns[sq.col]:
						if sq.value in test.possibilities:
							test.possibilities.remove(sq.value)
					for test in self.squareList[sq.row]:
						if sq.value in test.possibilities:
							test.possibilities.remove(sq.value)
					for test in self.boxes[int(sq.row/3)*3+int(sq.col/3)]:
						if sq.value in test.possibilities:
							test.possibilities.remove(sq.value)


	def ForwardCheck(self,square):
		AffectedSquares = self.columns[square.col] + self.squareList[square.row] + self.boxes[int(square.row/3)*3+int(square.col/3)]
		# Look if valid
		for sq in AffectedSquares:
			if square.value in sq.possibilities and sq.value == 0 and len(sq.possibilities)==1:
				return False
		return True	

		for test in AffectedSquares:
			if square.value in test.possibilities and test.value == 0:
				# test.assignments.append(square.value)
				test.possibilities.remove(square.value)
		return True

		# # If here then that means we can remove it
		# for test in self.columns[square.col]:
		# 	if square.value in test.possibilities:
				
		# 		test.assignments.append(square.value)
		# 		test.possibilities.remove(square.value)
		# for test in self.squareList[square.row]:
		# 	if square.value in test.possibilities:
		# 		# if len(test.possibilities) == 1:
		# 		# 	return False
		# 		test.assignments.append(square.value)
		# 		test.possibilities.remove(square.value)
		# for test in self.boxes[int(square.row/3)*3+int(square.col/3)]:
		# 	if square.value in test.possibilities:
		# 		# if len(test.possibilities) == 1:
		# 		# 	return False
		# 		test.assignments.append(square.value)
		# 		test.possibilities.remove(square.value)

	def RestoreConstraints(self,square):
		possibilities = list(range(1,10))
		if square.value in possibilities:
			possibilities.remove(square.value)

		AffectedSquares = self.columns[square.col] + self.squareList[square.row] + self.boxes[int(square.row/3)*3+int(square.col/3)]

		for neighbour in AffectedSquares:
			if neighbour == square:
				continue
			# Squares already assigned, make sure we don't use that value again
			if neighbour.value != 0 and neighbour.value in possibilities:
				possibilities.remove(neighbour.value)
			# Square isn't in the neighbours possibilities and wasn't assigned to it (ie removed from the possibilities for constraint reasons)
			elif neighbour.value == 0: #and square.value not in neighbour.possibilities and square.value not in square.assignments:
				OtherNeighbours = self.columns[neighbour.col] + self.squareList[neighbour.row] + self.boxes[int(neighbour.row/3)*3+int(neighbour.col/3)]
				ValAlreadyInNeighbours = False
				for sq in OtherNeighbours:
					if sq != square and sq.value == square.value:
						ValAlreadyInNeighbours = True
						break
				if not ValAlreadyInNeighbours:
					neighbour.possibilities.append(square.value)
		
		square.Restore(possibilities)

	def Backtrack(self, square):
		possibilities = list(range(1,10))

		AffectedSquares = self.columns[square.col] + self.squareList[square.row] + self.boxes[int(square.row/3)*3+int(square.col/3)]
		for neighbour in AffectedSquares:
			# Value already used, make sure we don't use that value again
			if neighbour.value != 0 and neighbour.value in possibilities and neighbour != square:
				possibilities.remove(neighbour.value)

		square.Backtrack(possibilities)
		# self.AddUnusedSquares(square)


	def MostConstrainedSquare(self):
#		Most = self.squareList[0][0]
		Most = None
		for i in range(9):
			for j in range(9):
				square = self.squareList[i][j]
				if Most is None and square.value == 0:
					Most = square
				if Most is not None and Most != square and square.value ==0 and len(square.possibilities) > 0 and len(square.possibilities) < len(Most.possibilities):
					Most = square
		
		# IF there are no values left
		if Most is None:
			return Most
		
		MostConstrained = [Most]
		for i in range(9):
			for j in range(9):
				square = self.squareList[i][j]
				if square == Most:
					continue
				if square.value == 0 and len(square.possibilities) > 0 and len(square.possibilities) == len(Most.possibilities): 
					MostConstrained.append(square)

		if len(MostConstrained) > 1:
			Best = None
			MostNeighbours = 0
			for sq in MostConstrained:
				AffectedSquares = self.columns[sq.col] + self.squareList[sq.row] + self.boxes[int(sq.row/3)*3+int(sq.col/3)]
				NeighboursAffected = 0
				for NeighbourSq in AffectedSquares:
					if NeighbourSq != sq and NeighbourSq.value == 0:
						NeighboursAffected += 1
				if NeighboursAffected >= MostNeighbours:
					MostNeighbours = NeighboursAffected
					Best = sq
			return Best
		else:
			return Most

	# Forward check for LCV specifically
	def ForwardCheckLCV(self,AffectedSquares,square,value):
		for sq in AffectedSquares:
			if value in sq.possibilities and square != sq and sq.value == 0 and len(sq.possibilities)==1:
				return False
		return True

	def LeastConstrainingValue(self,square):
		TotalAffected = 82
		AffectedSquares = self.columns[square.col] + self.squareList[square.row] + self.boxes[int(square.row/3)*3+int(square.col/3)]
		maxValue = 0
		for val in square.possibilities:
			if not self.ForwardCheckLCV(AffectedSquares,square,val):
				square.possibilities.remove(val)
				square.assignments.append(val)
				continue
			tempAffected = 0
			for sq in AffectedSquares:
				if val in sq.possibilities and sq != square:
					tempAffected += 1

			if tempAffected < TotalAffected:
				maxTotal = tempAffected
				maxValue = val
		if maxValue != 0:
			square.possibilities.remove(maxValue)
			square.assignments.append(maxValue)
		return maxValue


# MAYBE PEROBLEMS?
def CheckDiffNums(list):
	# First part checks for duplicates, second checks for 1 to 9
	return len(list) == len(set(list)) and set(range(1,10)) == set(list)

def ConstructBoard(lists):
	board = Board()
		# Open file
	# data = open(fileName,'r').read().split('\n')
	for i in range(9):
		#rowData = data[i].split()
		for j in range(9):
			board.SetupSq(i,j,lists[i][j])#int(rowData[j]))
			# For random square and value
			# if lists[i][j] == 0:
				# board.AddUnusedSquares(board.FindSquare(i,j))
	board.Cols()
	board.Boxes()
	board.Preprocess()
	return board