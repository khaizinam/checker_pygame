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
from Tranfer import DataSend, Tranfer
from config import *
from pygame import mixer
pygame.font.init()
pygame.mixer.init()
class Player:
	"""
	The main game control.
	"""

	def __init__(self, loop_mode, game):
		self.game = game
		self.selected_piece = None # a board location.
		self.loop_mode = loop_mode
		self.selected_legal_moves = []
		self.checkerSound = pygame.mixer.Sound('./Audio/checkerSound.mp3')
		self.loseSound = pygame.mixer.Sound('./Audio/loseSound.mp3')
		self.winSound = pygame.mixer.Sound('./Audio/winSound.mp3')
	def player_turn(self):
		"""
		The event loop. This is where events are triggered
		(like a mouse click) and then effect the game state.
		"""
		mouse_pos = tuple(map(int, pygame.mouse.get_pos()))
		self.mouse_pos = tuple(map(int, self.game.graphic.board_coords(mouse_pos[0], mouse_pos[1]))) # what square is the mouse in?
		if self.selected_piece != None:
			self.selected_legal_moves = self.game.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.game.hop)
			#print("selected_legal_moves: ", self.selected_legal_moves)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.terminate_game()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.mouse_pos[0] < 650 : 
					if self.game.hop == False:
						if self.game.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant != None and self.game.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant.color == self.game.turn:
							self.selected_piece = self.mouse_pos
						elif self.selected_piece != None and self.mouse_pos in self.game.board.legal_moves(self.selected_piece[0], self.selected_piece[1]):
							self.checkerSound.play()
							self.game.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])

							if self.mouse_pos not in self.game.board.adjacent(self.selected_piece[0], self.selected_piece[1]):
								self.game.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

								self.game.hop = True
								self.selected_piece = self.mouse_pos
							else:
								self.end_turn()

					if self.game.hop == True:
						self.checkerSound.play()
						if self.selected_piece != None and self.mouse_pos in self.game.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.game.hop):
							self.game.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])
							self.game.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

						if self.game.board.legal_moves(self.mouse_pos[0], self.mouse_pos[1], self.game.hop) == []:
								self.end_turn()

						else:
							self.selected_piece = self.mouse_pos

	def terminate_game(self):
		"""Quits the program and ends the game."""
		pygame.quit()
		sys.exit()

	def end_turn(self):
		"""
		End the turn. Switches the current player.
		end_turn() also checks for and game and resets a lot of class attributes.
		"""
		if self.game.turn == BLUE:
			self.game.turn = RED
		else:
			self.game.turn = BLUE

		self.selected_piece = None
		self.selected_legal_moves = []
		self.game.hop = False
		# online
		if self.loop_mode == False:
			print('sended to server')
			matrix_str = Tranfer().matrix_str(self.game.board.matrix)
			print(matrix_str)
			game = self.game.n.send(DataSend( self.game.id, 'put', matrix_str)._str())
			self.game.inputdata(game)
   
		if self.check_for_endgame():
			if self.loop_mode == False:
				game = self.game.n.send(DataSend( self.game.id, 'end', '')._str())
				self.game.inputdata(game)
			if self.game.turn == BLUE:
				self.game.graphic.draw_message("RED WINS!")
				self.loseSound.play()
			else:
				self.game.graphic.draw_message("BLUE WINS!")
				self.winSound.play()
			print(self.game.turn)
			self.game.endit = True

	def check_for_endgame(self):
		"""
		Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
		"""
		for x in range(8):
			for y in range(8):
				if self.game.board.location(x, y).color == BLACK and self.game.board.location(x, y).occupant != None and self.game.board.location(x, y).occupant.color == self.game.turn:
					if self.game.board.legal_moves(x, y) != []:
						return False

		return True


