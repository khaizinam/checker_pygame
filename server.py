import socket
from _thread import *
import pickle
from Tranfer import *
from Game import *
from Board import *

class Server:
    def __init__(self):
        self.server = 'localhost'
        self.port = 8
        self.turn = '0'
        self.idCount = 0
        self.game = Game()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((self.server, self.port))

        self.s.listen(2)
        print("Waiting for a connection, Server Started")
        self.connected = set()
    def set_player_ready(self, p):
        if p == '0':
            self.game.player_1_ready = True
        else:
            self.game.player_2_ready = True
    def threaded_client(self, conn, p):
        conn.send(str.encode(str(p)))
        self.set_player_ready(str(p))
        while True:
            try:
                data_str = pickle.loads(conn.recv(2048))
                data_arr = data_str.split(',')
                id = data_arr[0]
                method = data_arr[1]
                data = data_arr[2]
                if not data_str:
                    break
                # co data
                else:
                    #get matrix
                    if method == 'get':
                        pass
                    
                    # update matrix
                    elif method == 'put':
                        self.game.turn = RED
                        if id == '1':
                            self.game.turn = BLUE
                            
                        self.game.matrix = Tranfer().str_matrix(data)
                        
                    elif method == 'end':
                        self.game.endgame = True
                        self.game.playerWin = id
                    #------------------
                    self.set_player_ready(id)
                    conn.sendall(pickle.dumps(self.game))
            except:
                break

        print("Lost connection")
        print("Closing Game", p)
        if str(p) == '0':
            self.game.player_1_ready = False
        else:
            self.game.player_2_ready = False
        if self.game.player_1_ready == False and  self.game.player_2_ready == False:
            self.game = Game()
        self.idCount -= 1
        conn.close()
        
    def main(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            self.idCount += 1
            p = 0
            if  self.idCount % 2 == 1:
               pass
            else:
                p = 1
            print(f"Creating a new game...{p}")
            start_new_thread(self.threaded_client, (conn, p))
            
server = Server()
server.main()