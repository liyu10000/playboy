import curses
from random import randint, choice

class Game(object):
	def __init__(self, width=4, height=4, goal=2048):
		self.width = width
		self.height = height
		self.goal = goal
		self.score = 0
		self.highscore= 0
		self.board = [[0 for j in range(width)] for i in range(height)]

	def draw(self, stdscr, msg=""):
		stdscr.clear()
		def cast(line):
			stdscr.addstr(line+"\n")
		def draw_honrizontal_line():
			line = "+-----" * self.width + "+"
			cast(line)
		def draw_row(row):
			line = "".join("|{: ^5}".format(num) if num > 0 else "|     " for num in row) + "|"
			cast(line)		
		for row in self.board:
			draw_honrizontal_line()
			draw_row(row)
		draw_honrizontal_line()
		cast("")
		cast("======" * self.width + "=")
		cast("press 'wasd' or arrow keys to move, 'r' to restart, 'q' to quit")
		cast("board: {}x{}, goal: {}".format(self.width, self.height, self.goal))
		cast("current score: {}, best score: {}".format(self.score, self.highscore))
		if msg:
			cast("")
			cast("  "*self.width + msg + "  "*self.width)


	def spawn(self):
		new_num = 4 if randint(0,100) > 89 else 2
		(i, j) = choice([(i, j) for j in range(self.width) for i in range(self.height) if self.board[i][j] == 0])
		self.board[i][j] = new_num

	def reset(self):
		self.score = 0
		self.board = [[0 for j in range(self.width)] for i in range(self.height)]
		self.spawn()
		self.spawn()

	def update_score(self):
		self.score = max(map(max, self.board))
		return self.score >= self.goal

	def update_highscore(self):
		if self.score > self.highscore:
			self.highscore = self.score

	def move(self, action):
		def transpose(board):
			return [list(row) for row in zip(*board)]
		def flip(board):
			return [row[::-1] for row in board]
		# def rotate_right(board):
		# 	return flip(transpose(board))
		# def rotate_left(board):
		# 	return transpose(flip(board))

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
			return can_move

		actions = ("LEFT", "RIGHT", "UP", "DOWN")
		moves = {}
		moves["LEFT"] = lambda board: [row_move_left(row) for row in board]
		moves["RIGHT"] = lambda board: flip(moves["LEFT"](flip(board)))
		moves["UP"] = lambda board: transpose(moves["LEFT"](transpose(board)))
		moves["DOWN"] = lambda board: transpose(moves["RIGHT"](transpose(board)))

		old_board = self.board
		self.board = moves[action](self.board)
		return can_move(self.board, actions, moves), old_board != self.board

	def run(self, stdscr):
		self.reset()
		self.draw(stdscr)
		while True:
			c = stdscr.getch()
			curses.flushinp()
			if c == ord("r"):
				self.reset()
				self.update_highscore()
			elif c == ord("q"):
				break
			else:
				action = None
				if c == ord("w") or c == curses.KEY_UP:
					action = "UP"
				elif c == ord("s") or c == curses.KEY_DOWN:
					action = "DOWN"
				elif c == ord("a") or c == curses.KEY_LEFT:
					action = "LEFT"
				elif c == ord("d") or c == curses.KEY_RIGHT:
					action = "RIGHT"
				else:
					continue
				can_move, has_moved = self.move(action)
				if can_move and has_moved:
					self.spawn()
			get_goal = self.update_score()
			if get_goal or not can_move:
				self.update_highscore()
				if not can_move:
					self.draw(stdscr, "YOU LOSE !!!")
				if get_goal:
					self.draw(stdscr, "YOU WIN !!!")
			else:
				self.draw(stdscr)
		

def main(stdscr):
	game = Game(width=4, height=4, goal=1024)
	game.run(stdscr)
	print("game ended.")

curses.wrapper(main)