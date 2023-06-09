import pygame, sys
from pygame.locals import *
from config import *
from time import sleep

pygame.font.init()
class Graphics:
	def __init__(self, game):
		self.caption = "Cờ vây cùng Gia Cát :))"
		self.game = game
		self.player_turn = 'Xanh'
		if self.game.player_turn == RED:
			self.player_turn = 'Đỏ'
		self.fps = FPS
		self.clock = pygame.time.Clock()

		self.window_width = WIN_WIDTH
		self.window_height = WIN_HEIGHT
		self.screen = pygame.display.set_mode(( self.window_width, self.window_height))
		pygame.display.set_caption(self.caption)
		self.background = pygame.image.load('resources/map.png')

		self.square_size = 650 // 8
		self.piece_size = self.square_size // 2

		self.message = False

	def update_display(self, board, legal_moves, selected_piece):
		"""
		This updates the current display.
		"""
		self.screen.fill(BLACK)
		self.screen.blit(self.background, (0,0),(0,0,980,650))

		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)
  
		font_obj = pygame.font.Font('arial.ttf', 35)
		text1 = font_obj.render(f'Bạn là quân {self.player_turn}', True, BLACK)
		tex1_rect = text1.get_rect()
		tex1_rect.center = (WIN_WIDTH - 150, WIN_HEIGHT // 2 + 100)
		#turn
		text = 'Đang chờ..'
		if self.game.op_ready: 
			if self.game.turn == self.game.player_turn:
				text = 'Lượt của bạn'
			else :
				text = 'Lượt đối phương...'
		else :
			text = 'Đang chờ..'
		text2 = font_obj.render(text, True, BLACK)
		tex2_rect = text2.get_rect()
		tex2_rect.center = (WIN_WIDTH - 150, WIN_HEIGHT // 2 + 200)
		# print
		self.screen.blit(text1, tex1_rect)
		self.screen.blit(text2, tex2_rect)
		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		"""
		Takes a board object and draws all of its squares to the display
		"""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size , y * self.square_size, self.square_size, self.square_size), )

	def draw_board_pieces(self, board):
		"""
		Takes a board object and draws all of its pieces to the display
		"""
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, tuple(map(int, self.pixel_coords((x, y)))), int(self.piece_size))

					if board.location(x,y).occupant.king == True:
						#print("228->", self.screen, GOLD, self.pixel_coords((x, y)), self.piece_size // 1.7, self.piece_size // 4)
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x, y)), int(self.piece_size // 1.7), self.piece_size // 4)


	def pixel_coords(self, board_coords):
		"""
		Takes in a tuple of board coordinates (x,y)
		and returns the pixel coordinates of the center of the square at that location.
		"""
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	def board_coords(self, pixel_x, pixel_y):
		"""
		Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
		"""
		return (pixel_x // self.square_size, pixel_y // self.square_size)

	def highlight_squares(self, squares, origin):
		"""
		Squares is a list of board coordinates.
		highlight_squares highlights them.
		"""
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def draw_message(self, message):
		"""
		Draws message to the screen.
		"""
		print("in here")
		self.message = True
		self.font_obj = pygame.font.Font('arial.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (WIN_WIDTH - 150, WIN_HEIGHT // 2 - 50)