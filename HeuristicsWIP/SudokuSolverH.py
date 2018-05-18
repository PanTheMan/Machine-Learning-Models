from SudokuSetupH import *
NumMoves = 0
import time
start_time = time.time()

def BackTrack(board):
	global NumMoves
	NumMoves+=1
	# Check finished board
	if board.FinishCheck():
		print("DONE")
		return True

	# Choose next variable
	NextMove = board.MostConstrainedSquare()

	# While the move still has possible choices
	while NextMove.StillPossible():
		# Choose least constraining value
		lcv = board.LeastConstrainingValue(NextMove)
		# print(NextMove.row,NextMove.col)
		# print("Tried:",random)

		# Check basic constraints ie same row, col and box are satsified
		if board.CheckConstraints(NextMove,lcv):
			# If passed update the square
			board.UpdateSq(NextMove,lcv)
			# Then do a forward check, by removing the random value
			if board.ForwardCheck(NextMove):
				# If forward check passes (Removing random value doesn't result in zero possibilities for a square)
				res = BackTrack(board)
				# If res is true, we finished!	
				if res:
					return res
				#Failed otherwise
				# Restore by adding back random value to possibilities
				board.RestoreConstraints(NextMove)
	# Call backtrack on nextmove
	board.Backtrack(NextMove)

	#NextMove.Backtrack([])
	return False

# Puzzle data rows for evil,hard,medium,easy
easy = [[0,6,1,0,0,0,0,5,2],
		[8,0,0,0,0,0,0,0,1],
		[7,0,0,5,0,0,4,0,0],
		[9,0,3,6,0,2,0,4,7],
		[0,0,6,7,0,1,5,0,0],
		[5,7,0,9,0,3,2,0,6],
		[0,0,4,0,0,9,0,0,5],
		[1,0,0,0,0,0,0,0,8],
		[6,2,0,0,0,0,9,3,0]]
medium = [[5,0,0,6,1,0,0,0,0],
			[0,2,0,4,5,7,8,0,0],
			[1,0,0,0,0,0,5,0,3],
			[0,0,0,0,2,1,0,0,0],
			[4,0,0,0,0,0,0,0,6],
			[0,0,0,3,6,0,0,0,0],
			[9,0,3,0,0,0,0,0,2],
			[0,0,6,7,3,9,0,8,0],
			[0,0,0,0,8,6,0,0,5]]

evil = [[0,6,0,8,2,0,0,0,0],
		[0,0,2,0,0,0,8,0,1],
		[0,0,0,7,0,0,0,5,0],
		[4,0,0,5,0,0,0,0,6],
		[0,9,0,6,0,7,0,3,0],
		[2,0,0,0,0,1,0,0,7],
		[0,2,0,0,0,9,0,0,0],
		[8,0,4,0,0,0,7,0,0],
		[0,0,0,0,4,8,0,2,0]]
hard = [[0,4,0,0,2,5,9,0,0],
		[0,0,0,0,3,9,0,4,0],
		[0,0,0,0,0,0,0,6,1],
		[0,1,7,0,0,0,0,0,0],
		[6,0,0,7,5,4,0,0,9],
		[0,0,0,0,0,0,7,3,0],
		[4,2,0,0,0,0,0,0,0],
		[0,9,0,5,4,0,0,0,0],
		[0,0,8,9,6,0,0,5,0]]
def BoardSetup(puzzle):	
	global NumMoves

	f = open("C:/Users/ericp/Documents/results.txt","r+")
	for i in range(50):
		start_time = time.time()
		board = ConstructBoard(puzzle)
	# board.PrintBoard()
		BackTrack(board)
	# board.PrintBoard()
	# print("{} {}\n".format(NumMoves, (time.time() - start_time)))
		f.write("{} {}\n".format(NumMoves, (time.time() - start_time)))	
		NumMoves = 0
	f.close()
BoardSetup(easy)

