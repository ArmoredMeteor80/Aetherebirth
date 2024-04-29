import socket
import pickle

from ..entity import Player
from ..map import MapManager

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()
        print(self.player)

    def sendData(self, player: Player, map_manager: MapManager):
        self.send({
            "position": {
                "map": map_manager.current_map,
                "x": player.position[0],
                "y": player.position[1],
            },
            "name": player.player_name,
            "stats": player.stats,
            "actions": {
                "is_running": player.is_running,
                "is_exhausted": player.is_exhausted,
                "is_attacking": player.is_attacking
            }
        })

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
