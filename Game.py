"""
checkers.py

A simple checkers engine written in Python with the pygame 1.9.1 libraries.

Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm

I adapted some code from checkers.py found at
http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py starting on line 159 of my program.

This is the final version of my checkers project for Programming Workshop at Marlboro College. The entire thing has been rafactored and made almost completely object oriented.

Funcitonalities include:

- Having the pieces and board drawn to the screen

- The ability to move pieces by clicking on the piece you want to move, then clicking on the square you would
  like to move to. You can change you mind about the piece you would like to move, just click on a new piece of yours.

- Knowledge of what moves are legal. When moving pieces, you'll be limited to legal moves.

- Capturing

- DOUBLE capturing etc.

- Legal move and captive piece highlighting

- Turn changes

- Automatic kinging and the ability for them to move backwords

- Automatic check for and end game.

- A silky smoooth 60 FPS!

Everest Witman - May 2014 - Marlboro College - Programming Workshop
"""

import pygame, sys
from pygame.locals import *
from Graphic import *
from Board import *
from time import sleep

pygame.font.init()

class Game:
	"""
	The main game control.
	"""

	def __init__(self, loop_mode):
		self.graphics = Graphics()
		self.board = Board()
		self.endit = False
		self.turn = BLUE
		self.selected_piece = None # a board location.
		self.hop = False
		self.loop_mode = loop_mode
		self.selected_legal_moves = []

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

	def player_turn(self):
		"""
		The event loop. This is where events are triggered
		(like a mouse click) and then effect the game state.
		"""
		mouse_pos = tuple(map(int, pygame.mouse.get_pos()))
		self.mouse_pos = tuple(map(int, self.graphics.board_coords(mouse_pos[0], mouse_pos[1]))) # what square is the mouse in?
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.hop)
			 #print("selected_legal_moves: ", self.selected_legal_moves)

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:
				print(self.hop)
				print(self.mouse_pos[0])
				if self.mouse_pos[0] < 650 : 
					if self.hop == False:
						if self.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant != None and self.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant.color == self.turn:
							self.selected_piece = self.mouse_pos

						elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0], self.selected_piece[1]):

							self.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])

							if self.mouse_pos not in self.board.adjacent(self.selected_piece[0], self.selected_piece[1]):
								self.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

								self.hop = True
								self.selected_piece = self.mouse_pos
							else:
								self.end_turn()

					if self.hop == True:
						if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.hop):
							self.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])
							self.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

						if self.board.legal_moves(self.mouse_pos[0], self.mouse_pos[1], self.hop) == []:
								self.end_turn()

						else:
							self.selected_piece = self.mouse_pos


	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

	def terminate_game(self):
		"""Quits the program and ends the game."""
		pygame.quit()
		sys.exit()

	def main(self):
		""""This executes the game and controls its flow."""
		self.setup()

		while True: # main game loop
			self.player_turn()
			self.update()

	def end_turn(self):
		"""
		End the turn. Switches the current player.
		end_turn() also checks for and game and resets a lot of class attributes.
		"""
		if self.turn == BLUE:
			self.turn = RED
		else:
			self.turn = BLUE

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == BLUE:
				print('RED WINS!')
				self.graphics.draw_message("RED WINS!")
			else:
				print('BLUE WINS!')
				self.graphics.draw_message("BLUE WINS!")
			print(self.turn)
			if(self.loop_mode):
				self.endit = True
			else:
				self.terminate_game()

	def check_for_endgame(self):
		"""
		Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
		"""
		for x in range(8):
			for y in range(8):
				if self.board.location(x, y).color == BLACK and self.board.location(x, y).occupant != None and self.board.location(x, y).occupant.color == self.turn:
					if self.board.legal_moves(x, y) != []:
						return False

		return True


