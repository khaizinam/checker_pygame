import socket
from _thread import *
import pickle
from Tranfer import *
from Game import *
from Board import *

class Server:
    def __init__(self):
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.turn = '0'
        self.idCount = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((self.server, self.port))

        self.s.listen(2)
        print("Waiting for a connection, Server Started")
        self.connected = set()
        
    def threaded_client(self, conn, p):
        conn.send(str.encode(str(p)))
        if p == '0':
            self.game.player_1_ready = True
        else:
            self.game.player_2_ready = True
        while True:
            try:
                data_str = pickle.loads(conn.recv(2048))
                data = data_str.split(',')
                if not data:
                    break
                # co data
                else:
                    #get matrix
                    if data[1] == 'get':
                        #data_str = Tranfer().matrix_str(self.game.matrix) 
                        conn.sendall(pickle.dumps(self.game))
                    
                    # update matrix
                    elif data[1] == 'put':
                        print(f'put method from client {data[0]} with data :\n{data[2]}')
                        if data[0] == '0':
                            self.game.turn = RED
                        elif data[0] == '1':
                            self.game.turn = BLUE
                            
                        self.game.matrix = Tranfer().str_matrix(data[2])
                        conn.sendall(pickle.dumps(self.game))
                    elif data[1] == 'end':
                        self.game.endgame = True
                        self.game.playerWin = data[0]
                        conn.sendall(pickle.dumps(self.game))

            except:
                break

        print("Lost connection")
        try:
            print("Closing Game", p)
        except:
            pass
        if p == '0':
            self.game.player_1_ready = False
        else:
            self.game.player_2_ready = False
        self.idCount -= 1
        conn.close()
        
    def main(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            self.game = Game()
            self.idCount += 1
            p = 0
            if  self.idCount % 2 == 1:
                print("Creating a new game...")
            else:
                p = 1
            start_new_thread(self.threaded_client, (conn, p))
            
server = Server()
server.main()