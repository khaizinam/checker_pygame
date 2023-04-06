import Game
from gamebot import *
from Button import *
from config import *
import pygame
from time import sleep
##COLORS##
#             R    G    B
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GOLD = (255, 215,   0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


def main():
    while True:
        game = Game.Game(loop_mode=True)
        game.setup()
        clock = pygame.time.Clock()
        bot = Bot(game, RED, mid_eval='piece_and_board',
                          end_eval='sum_of_dist', method='alpha_beta', depth=3)
        #random_bot_blue = Bot(
            #game, BLUE, mid_eval='piece_and_board_pov', method='alpha_beta', depth=3, end_eval='sum_of_dist')
        reset_btn = True
        while True:  # main game loop
            if game.turn == BLUE:
                 # TO start player's turn uncomment the below line and comment a couple  of line below than that
                game.player_turn()
                # count_nodes = random_bot_blue.step(game.board, True)
                # print('Total nodes explored in this step are', count_nodes)
            else:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                # game.player_turn()
                count_nodes = bot.step(game.board, True)
                print('Total nodes explored in this step are', count_nodes)
            game.update()
            if game.endit:
                break
        button = Button(WIN_WIDTH //2 ,WIN_HEIGHT //2, 100, 100, BLACK , WHITE, 'restart', 15)
        while reset_btn:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    game.terminate_game()
            
            if button.is_pressed(mouse_pos, mouse_pressed):
                reset_btn = False
            game.graphics.screen.blit(button.image,button.rect)
            game.graphics.clock.tick(60)
            pygame.display.update()
            



if __name__ == "__main__":
    main()
    pass
