from SudokuSetupFC import *
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
	NextMove = board.RandomUnusedSquare()

	while len(NextMove.possibilities) != 0:
		random = NextMove.RandomValue()
		# print(NextMove.row,NextMove.col)
		# print("Tried:",random)
		if board.CheckConstraints(NextMove,random):
			board.UpdateSq(NextMove,random)
			if board.ForwardCheck(NextMove):

				res = BackTrack(board)
			
				if res:
					return res
				#Failed otherwise
				board.RestoreConstraints(NextMove)
	board.Backtrack(NextMove)

	#NextMove.Backtrack([])
	return False
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

	board = ConstructBoard(puzzle)
	board.PrintBoard()
# # #q	board.RestoreConstraints(board.squareList[8][2])
# # 	# board.UpdateSq(board.squareList[8][2],5)
# # 	# print(board.ForwardCheck(board.squareList[8][2]))
# # 	# board.RestoreConstraints(board.squareList[8][2])
# # 	# board.Backtrack(board.squareList[8][2])
# # 	# print("Test")
# # 	# print(board.squareList[8][2].possibilities)
# # 	# print(board.squareList[1][2].possibilities)
# # 	#board.RestoreConstraints(board.squareList[2][8])
# # 	#print(board.UpdateSq(board.squareList[2][8],0))
# # 	# print(board.squareList[3][4].possibilities)
	BackTrack(board)
	board.PrintBoard()
 	print("{} {}".format(NumMoves, (time.time() - start_time)))
	# f = open("C:/Users/ericp/Documents/results.txt","r+")
	# for i in range(10):
	# 	start_time = time.time()
	# 	board = ConstructBoard(puzzle)

	# 	BackTrack(board)
	# 	f.write("{} {}\n".format(NumMoves, (time.time() - start_time)))	
	# 	NumMoves = 0
	# f.close()
BoardSetup(evil)

