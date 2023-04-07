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
        self.mainMenu = True
        self.bot_mod_default = ['random','minmax','alpha_beta']
        self.bot_mod =  self.bot_mod_default[1]
        self.graphic = Graphics()
        self.graphic.setup_window()
        self.mode = ''
        pygame.init()
    def setup(self):
        self.graphic = Graphics()
        self.board = Board()
        self.runing = True
        self.turn = BLUE
        self.hop = False
        self.endit = False
        
        self.player = Player(loop_mode=True, game=self)
        
        self.bot = Bot(self, RED, mid_eval='piece_and_board',end_eval='sum_of_dist', method=self.bot_mod, depth=3)
        

    
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
        btn = [
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 200, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Re Play', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 100, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Main Menu', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 , width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Exit', fontsize=25)
        ]
        while True:
            self.graphic.screen.fill(BLACK)
            self.events()
                
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if btn[0].is_pressed(mouse_pos, mouse_pressed):
                self.graphic.message = False
                break
            
            elif btn[1].is_pressed(mouse_pos, mouse_pressed):
                self.graphic.message = False
                self.mainMenu = True
                break
            
            elif btn[2].is_pressed(mouse_pos, mouse_pressed):
                self.terminate_game()
                
            for button in btn:    
                self.graphic.screen.blit(button.image, button.rect)
            pygame.display.update()
            self.graphic.clock.tick(FPS)
            
    def play(self):
        self.setup()
        while self.playing:  # main game loop
            if self.mode == 'bot':
                if self.turn == BLUE:
                    self.player.player_turn()
                else:
                    count_nodes = self.bot.step(self.board, True)
                    # print('Total nodes explored in this step are', count_nodes)
                self.update()
                if self.endit:
                    self.playing = False 
                
    def main_menu(self):
        btn = [
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 200, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='P v E', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 100, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='P v P', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 , width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Exit', fontsize=25)
        ]
        btn2 = [
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 100, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Easy', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Hard', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 + 100, width= 200, height = 50, fg=BLACK ,bg=WHITE, content='Back', fontsize=25),
        ]
        menu = True
        while True:
            self.graphic.screen.fill(BLACK)
            self.events()
                
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if menu:
                if btn[0].is_pressed(mouse_pos, mouse_pressed):
                    # self.graphic.message = False
                    # self.mainMenu = False
                    # self.mode = 'bot'
                    menu = False
                    # break
                
                elif btn[1].is_pressed(mouse_pos, mouse_pressed):
                    self.mode = 'pvp'
                
                elif btn[2].is_pressed(mouse_pos, mouse_pressed):
                    self.terminate_game()
                    
                for button in btn:    
                    self.graphic.screen.blit(button.image, button.rect)
            else :
                if btn2[0].is_pressed(mouse_pos, mouse_pressed):
                    self.graphic.message = False
                    self.mainMenu = False
                    self.bot_mod =  self.bot_mod_default[0]
                    self.mode = 'bot'
                    break
                
                elif btn2[1].is_pressed(mouse_pos, mouse_pressed):
                    self.graphic.message = False
                    self.mainMenu = False
                    self.bot_mod =  self.bot_mod_default[1]
                    self.mode = 'bot'
                    break
                
                elif btn2[2].is_pressed(mouse_pos, mouse_pressed):
                    menu = True
                    
                for button in btn2:    
                    self.graphic.screen.blit(button.image, button.rect)
            pygame.display.update()
            self.graphic.clock.tick(FPS)
                 
    def main(self):
        while self.runing:
            if self.mainMenu:
                self.main_menu()
            self.playing = True 
            self.events() 
            self.play()
            #lose/ win screen
            self.reset()

game = Game()
game.main()    