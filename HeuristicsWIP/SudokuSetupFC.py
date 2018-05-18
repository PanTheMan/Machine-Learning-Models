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
			#self.assignments.append(value)

	def UpdateValue(self,value):
		if value != 0:
			self.value = value
#			self.assignments.append(value)
#			self.assignments.append(value)

	# Soft reset when a value fails, but there are still choices
	def Restore(self, possibilities):
		self.value = 0
		self.possibilities = [ pos for pos in possibilities if pos not in self.assignments ]

	# When possibilties is 0, backtrack instead of soft resetting
	def Backtrack(self, possibilities):
		self.value = 0
		self.possibilities = possibilities
		self.assignments = []


	def RandomValue(self):
		val = random.choice(self.possibilities)
		self.assignments.append(val)
		self.possibilities.remove(val)
		return val

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
		self.squareList = [[square(0,i,j) for j in range(9)] for i in range(9)]
		self.UnusedSquares = []

	def AddUnusedSquares(self,Square):
		self.UnusedSquares.append(Square)

	def RemoveUnusedSquare(self,idx):
		self.UnusedSquares.pop(idx)
	
	def FindSquare(self,i,j):
		return self.squareList[i][j]
	# Returns list of rows
	def Rows(self):
		return self.squareList

	def RandomUnusedSquare(self):
		idx = random.randint(0, len(self.UnusedSquares)-1)
		Square = self.UnusedSquares[idx]
		self.RemoveUnusedSquare(idx)
		return Square

	# Returns list of columns
	def Cols(self):
		y = []
		for i in range(9):
			col = []
			for j in range(9):
				col.append(self.squareList[j][i])
			y.append(col)
		self.columns = y

	def Boxes(self):
		BoxCorners = [(0,0), (0,3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
		boxes = []
		for corner in BoxCorners:
			box = []
			for i in range(corner[0],corner[0]+3):
				for j in range(corner[1],corner[1]+3):
					box.append(self.squareList[i][j])
			boxes.append(box)
		self.boxes = boxes

	def CheckConstraints(self,square,value):
		if value in [sq.value for sq in self.squareList[square.row]]:
			return False
		if value in [sq1.value for sq1 in self.columns[square.col]]:
			return False

		if value in [sq2.value for sq2 in self.boxes[int(square.row/3)*3+int(square.col/3)]]:
			return False
		return True

	def UpdateSq(self,square, value):
		square.UpdateValue(value)

	def SetupSq(self,i,j, value):
		square.UpdateValue(self.squareList[i][j],value)

	def FinishCheck(self):
		if len(self.UnusedSquares) != 0:
			return False

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

	def Restore(self,square):
		self.AddUnusedSquares(square)
		square.Backtrack([])

	def StillPossible(self,square):
		return square.StillPossible()

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

	def TestForwardCheck(self,AffectedSquares,square):
		for sq in AffectedSquares:
			if square.value in sq.possibilities and sq.value == 0 and len(sq.possibilities)==1:
				return False
		return True	

	def ForwardCheck(self,square):
		AffectedSquares = self.columns[square.col] + self.squareList[square.row] + self.boxes[int(square.row/3)*3+int(square.col/3)]
		# Look if valid
		if not self.TestForwardCheck(AffectedSquares,square):
			return False

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
		self.AddUnusedSquares(square)


	def MostConstrainedValue(self):
		return

	def ForwardCheckLCV(self,AffectedSquares,value):
		for sq in AffectedSquares:
			if value in sq.possibilities and sq.value == 0 and len(sq.possibilities)==1:
				return False
		return True



	def LeastConstrainingValue(self,square):
		TotalAffected = 82
		AffectedSquares = self.columns[square.col] + self.squareList[square.row] + self.boxes[int(square.row/3)*3+int(square.col/3)]
		maxValue = 0

		for val in square.possibilities:
			if not ForwardCheckLCV(AffectedSquares,val):
				square.possibilities.remove(val)
				square.assignments.append(val)
				continue
			tempAffected = 0

			for sq in AffectedSquares:
				if val in sq.possibilities and sq != square:
					total += 1

			if total < TotalAffected:
				maxTotal = total
				maxValue = val
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
			if lists[i][j] == 0:
				board.AddUnusedSquares(board.FindSquare(i,j))
	board.Cols()
	board.Boxes()
	board.Preprocess()
	return board