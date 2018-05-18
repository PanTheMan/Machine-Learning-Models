from SudokuSetup import *
NumMoves = 0
import time
start_time = time.time()
def BackTrack(board,assignment):
	global NumMoves
	NumMoves+=1
	# Check finished board
	if board.FinishCheck():
		print("DONE")
		return True

	# Choose next variable
	NextMove = board.RandomUnusedSquare()

	if(len(NextMove.possibilities)==0 and len(assignment)==0):
		print(len(assignment))
		print("Give up")
#	while there still are possibilities
	assignment.append(NextMove)

	while NextMove.StillPossible():
		random = NextMove.RandomValue()
		# print(NextMove.row,NextMove.col)
		# print("Tried:",random)
		if board.CheckConstraints(NextMove,random):
			board.UpdateSq(NextMove,random)
			# check = board.ForwardCheck(NextMove)
			# if not check:
			# 	print("Forwad Failed")
			# 	print(NextMove.row,NextMove.col)
			# 	print(NextMove.possibilities)
			# 	board.PrintBoard()
			# else:
			res = BackTrack(board,assignment)
		
			if res:
				return res
				#Failed otherwise
				# board.RestoreConstraints(NextMove)

		print("Check Constraints failed")

	assignment.pop()
	#NextMove.Backtrack([])
	board.Restore(NextMove)
	return False


def BoardSetup(fileName):	
	board = ConstructBoard(fileName)
	print
	board.PrintBoard()
	# board.UpdateSq(board.squareList[8][2],5)
	# print(board.ForwardCheck(board.squareList[8][2]))
	# board.RestoreConstraints(board.squareList[8][2])
	# board.Backtrack(board.squareList[8][2])
	# print("Test")
	# print(board.squareList[8][2].possibilities)
	# print(board.squareList[1][2].possibilities)
	#board.RestoreConstraints(board.squareList[2][8])
	#print(board.UpdateSq(board.squareList[2][8],0))
	# print(board.squareList[3][4].possibilities)
	BackTrack(board,[])
	board.PrintBoard()
	print("{} {}".format(NumMoves, (time.time() - start_time)))
	# f = open("C:/Users/ericp/Documents/results.txt","r+")
	# for i in range(50):
	# 	start_time = time.time()
	# 	board = ConstructBoard(fileName)

	# 	BackTrack(board,[])
	# 	f.write("{} {}".format(NumMoves, (time.time() - start_time)))	
	# 	print("Done")
	# f.close()
BoardSetup('C:/Python/Python36-32/easy.txt')
