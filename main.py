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
        self.background = pygame.image.load('resources/bg_menu_2.png')
    def setup(self):
        self.graphic = Graphics()
        self.board = Board()
        self.runing = True
        self.turn = BLUE
        self.hop = False
        self.endit = False
        
        self.player = Player(loop_mode=True, game=self)
        self.player2 = Player(loop_mode=True, game=self)
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
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 200, width= 200, height = 50, fg=WHITE,bg=BLACK , content='Ván nữa', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 - 100, width= 200, height = 50, fg=WHITE,bg=BLACK , content='Đổi người', fontsize=25),
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 , width= 200, height = 50, fg=WHITE,bg=BLACK , content='Cáo từ', fontsize=25)
        ]
        while True:
            self.graphic.screen.fill(BLACK)
            self.graphic.screen.blit(self.background, (0,0),(0,0,980,650))
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
                    # self.player2.player_turn()
                    count_nodes = self.bot.step(self.board, True)
                    # print('Total nodes explored in this step are', count_nodes)
                self.update()
                if self.endit:
                    self.playing = False               
    
    def menu_1(self):
        btn = [
            Button(x = 50, y= WIN_HEIGHT//2 - 100, width= 300, height = 50, fg=WHITE,bg=BLACK , content='Tại hạ không có bằng hữu', fontsize=25),
            Button(x = 50, y= WIN_HEIGHT//2, width= 300, height = 50, fg=WHITE,bg=BLACK , content='Solo với bằng hữu', fontsize=25),
            Button(x = 50, y= WIN_HEIGHT//2 + 100, width= 300, height = 50, fg=WHITE,bg=BLACK , content='Cáo Từ', fontsize=25)
        ] 
        while True:
            self.graphic.screen.fill(BLACK)
            self.graphic.screen.blit(self.background, (0,0),(0,0,980,650))
            self.events()
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if self.ischange == 0:
                if btn[0].is_pressed(mouse_pos, mouse_pressed):
                    self.isMainMenu = False
                    self.ischange = 20
                    break
                        
                elif btn[1].is_pressed(mouse_pos, mouse_pressed):
                    self.mode = 'pvp'
                        
                elif btn[2].is_pressed(mouse_pos, mouse_pressed):
                    self.terminate_game()
                            
            if self.ischange > 0:
                self.ischange -= 1
                
            for button in btn:    
                self.graphic.screen.blit(button.image, button.rect)
            self.graphic.clock.tick(FPS)  
            pygame.display.update()
            
    def menu_2(self):
        btn2 = [
            Button(x = 50, y= WIN_HEIGHT//2 - 100, width= 200, height = 50, fg=WHITE,bg=BLACK , content='Nhường ta chút', fontsize=25),
            Button(x = 50, y= WIN_HEIGHT//2, width= 200, height = 50, fg=WHITE,bg=BLACK , content='Hết sức đi', fontsize=25),
            Button(x = 50, y= WIN_HEIGHT//2 + 100, width= 200, height = 50, fg=WHITE,bg=BLACK , content='Quay về', fontsize=25),
        ]
        while True:
            self.graphic.screen.fill(BLACK)
            self.graphic.screen.blit(self.background, (0,0),(0,0,980,650))
            self.events()
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if self.ischange == 0:    
                if btn2[0].is_pressed(mouse_pos, mouse_pressed):
                    self.graphic.message = False
                    self.mainMenu = False
                    self.bot_mod =  self.bot_mod_default[0]
                    self.mode = 'bot'
                    self.isMenuRunning = False
                    break
                        
                elif btn2[1].is_pressed(mouse_pos, mouse_pressed):
                    self.graphic.message = False
                    self.mainMenu = False
                    self.bot_mod =  self.bot_mod_default[1]
                    self.mode = 'bot'
                    self.isMenuRunning = False
                    break
                        
                elif btn2[2].is_pressed(mouse_pos, mouse_pressed):
                    self.isMainMenu =  True
                    self.ischange = 20 
                    break
            if self.ischange > 0:
                self.ischange -= 1   
                        
            for button in btn2:    
                self.graphic.screen.blit(button.image, button.rect)
                
            self.graphic.clock.tick(FPS)  
            pygame.display.update()

    def main_menu(self):
        self.isMainMenu = True
        self.isMenuRunning = True
        self.ischange = 0
        while self.isMenuRunning:
            self.events()
                
            if self.isMainMenu:
                self.menu_1()
            else :
                self.menu_2()
                 
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