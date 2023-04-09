from config import *
from Board import *
class PvP:
    def __init__(self, id):
        self.turn = [BLUE, RED]
        self.id = None
        self.ready = False
        self.board = None

    def get_player_move(self, p):
        return self.turn

    def play(self, player, move):
        pass

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went
