from Player import *
from Button import *
from config import *
from Graphic import *
from Board import *
from Network import *
import pygame
from time import sleep
#
class Client:
    def __init__(self):
        self.player_turn = BLUE
        self.playing = True
        self.endgame = False
        self.op_ready = False
        self.playerWin = ''
        pygame.init()
        self.background = pygame.image.load('resources/bg_menu_2.png')
        self.n = Network()
        self.id = self.n.getP()
        
        if self.id == None:
            self.playing = None
        print(f'start with id: {self.id}')
        if self.id == '1':
            self.player_turn = RED
        
        
        
    def setup(self):
        self.graphic = Graphics(self)
        
        self.board = Board()
        self.runing = True
        self.turn = BLUE
        self.hop = False
        self.endit = False
        
        self.player = Player(loop_mode=False, game=self)
    
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
        self.graphic.update_display(self.board, self.player.selected_legal_moves, self.player.selected_piece)
    
    def reset(self):
        btn = [
            Button(x = WIN_WIDTH//2 - 100, y= WIN_HEIGHT//2 , width= 200, height = 50, fg=WHITE,bg=BLACK , content='Cáo từ', fontsize=25)
        ]
        while True:
            self.events()
                
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if btn[0].is_pressed(mouse_pos, mouse_pressed):
                self.playing = False 
                break
                
            for button in btn:    
                self.graphic.screen.blit(button.image, button.rect)
            pygame.display.update()
            self.graphic.clock.tick(FPS)
    def inputdata(self, game):
        if self.id == '0' and game.player_2_ready:
            self.op_ready = True
        if self.id == '1' and game.player_1_ready:
            self.op_ready = True
        self.turn = game.turn
        self.board.matrix = game.matrix
        self.endgame = game.endgame
        self.playerWin = game.playerWin
        
    def main(self):
        self.setup()
        while self.playing:  # main game loop
            if self.player_turn == self.turn:
                self.player.player_turn()
            else :
                pass
            game = self.n.send(DataSend( self.id, 'get', '')._str())
            self.inputdata(game)       
            self.update()
            if self.endgame:
                self.reset()

# c = Client()
# c.main()
# print('end')