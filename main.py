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
        self.runing = True
    def setup(self):
        self.graphic = Graphics()
        self.board = Board()
        self.runing = True
        self.bot_mod = ['alpha_beta']
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
        self.graphic.update_display(self.board, self.player.selected_legal_moves, self.player.selected_piece)
        
    
    def draw(self):
        pass
    def reset(self):
        restart_button = Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 + 50, width= 200, height = 100, fg=BLACK ,bg=WHITE, content='Re Play', fontsize=25)
        runing = True
        while runing:
            self.events()
                
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.graphic.message = False
                runing = False
            self.graphic.screen.blit(restart_button.image, restart_button.rect)
            pygame.display.update()
            
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
            self.reset()

game = Game()
game.main()    