from Player import *
from Button import *
from config import *
from Graphic import *
from Board import *
from time import sleep
#
class Game:
    def __init__(self):
        self.turn = BLUE
        self.player_1_ready = False
        self.player_2_ready = False
        self.endgame = False
        self.playerWin = ''
        self.matrix = Board().matrix  
    def main(self):
        pass

