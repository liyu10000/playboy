import curses
from random import randrange, choice
import time

class Game(object):
	def __init__(self, width=4, height=4, win_val=2048):
		self.width = width
		self.height = height
		self.win_val = win_val
		self.score = 0
		self.highscore= 0
		self.board = [[0 for j in range(width)] for i in range(height)]
		#self.reset()

	def draw(self, stdscr):
		def cast(line):
			stdscr.addstr(line+"\n")
		def draw_honrizontal_line():
			line = "+-----" * self.width + "+"
			cast(line)
		def draw_row(row):
			line = " ".join("|{: ^5}".format(num) if num > 0 else "|     " for num in row) + "|"
			cast(line)
		for row in self.board:
			draw_honrizontal_line()
			draw_row(row)

	def run(stdscr):
		c = None
		while c != ord("q"):
			c = stdscr.getch()
			curses.flushinp()
			stdscr.clear()
			if c == ord("w") or c == curses.KEY_UP:
				stdscr.addstr("You pressed the 'w' key or up arrow")
			elif c == ord("s") or c == curses.KEY_DOWN:
				stdscr.addstr("You pressed the 's' key or down arrow")
			elif c == ord("a") or c == curses.KEY_LEFT:
				stdscr.addstr("You pressed the 'a' key or left arrow")
			elif c == ord("d") or c == curses.KEY_RIGHT:
				stdscr.addstr("You pressed the 'd' key or right arrow")
		

def main(stdscr):
	stdscr.clear()
	game = Game()
	while True:
		game.draw(stdscr)
	print("program ended.")

curses.wrapper(main)