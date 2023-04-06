from Player import *
from gamebot import *
from Button import *
from config import *
from Graphic import *
from Board import *
import pygame
from time import sleep

class Game:
    def __init__(self):
        self.graphic = Graphics()
        self.board = Board()
        self.runing = True
        self.bot_mod = ['alpha_beta']
    def setup(self):
        self.turn = BLUE
        self.hop = False
        self.endit = False
        
        self.player = Player(loop_mode=True, game=self)
        
        self.bot = Bot(self, RED, mid_eval='piece_and_board',end_eval='sum_of_dist', method=self.bot_mod[0], depth=3)
        
        self.graphic.setup_window()
    
    def terminate_game(self):
        self.runing = False
        pygame.quit()
        sys.exit()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate_game() 
                
    def update(self):
        self.events()
        self.player.update()
        if self.player.check_for_endgame():
            if self.turn == BLUE:
                print('RED WINS!')
                self.graphic.draw_message("RED WINS!")
            else:
                print('BLUE WINS!')
                self.graphic.draw_message("BLUE WINS!")
                print(self.turn)
            if(self.player.loop_mode):
                self.endit = True
            else:
                self.terminate_game()
        self.graphic.update_display(self.board, self.player.selected_legal_moves, self.player.selected_piece)
        
    
    def draw(self):
        pass
    
    def main(self):
        while self.runing:
            self.setup()
            self.events()
            while True:  # main game loop
                if self.turn == BLUE:
                    self.player.player_turn()
                else:
                    count_nodes = self.bot.step(self.board, True)
                    print('Total nodes explored in this step are', count_nodes)
                self.update()
                if self.endit:
                    break

game = Game()
game.main()    