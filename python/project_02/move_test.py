def aprint(a):
	print("print array:")
	for row in a:
		print(row)

def transpose(board):
	return [list(row) for row in zip(*board)]

def flip(board):
	return [row[::-1] for row in board]

def row_move_left(row):
	nums = [num for num in row if num > 0]
	nums_new = []
	j = 0
	while j+1 < len(nums):
		if nums[j] == nums[j+1]:
			nums_new.append(nums[j]*2)
			j += 2
		else:
			nums_new.append(nums[j])
			j += 1
	if j == len(nums) - 1:
		nums_new.append(nums[j])
	return nums_new + [0 for i in range(len(row)-len(nums_new))]

def can_move(board, actions, moves):
	can_move = False
	for action in actions:
		if not moves[action](board) == board:
			can_move = True
			print("array changes at {}".format(action))
		else:
			print("array no change at {}".format(action))
	return can_move

actions = ("LEFT", "RIGHT", "UP", "DOWN")
moves = {}
moves["LEFT"] = lambda board: [row_move_left(row) for row in board]
moves["RIGHT"] = lambda board: flip(moves["LEFT"](flip(board)))
moves["UP"] = lambda board: transpose(moves["LEFT"](transpose(board)))
moves["DOWN"] = lambda board: transpose(moves["RIGHT"](transpose(board)))

board = [[2, 0, 0], 
		 [4, 2, 0], 
		 [4, 4, 0]]

aprint(board)

can_move(board, actions, moves)

aprint(transpose(board))
aprint(flip(board))

for action in actions:
	aprint(moves[action](board))