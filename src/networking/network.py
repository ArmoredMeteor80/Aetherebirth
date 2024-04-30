import socket
import pickle
import json

from ..entity import Player
from ..map import MapManager


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)
        self.client.settimeout(10)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)


    def start(self):
        self.network_players = self.connect()
        return self


    def stop(self):
        self.client.close()
        return self

    def sendData(self, player: Player, map_manager: MapManager):
        return self.send({
            "position": {
                "map": map_manager.current_map,
                "x": player.position[0],
                "y": player.position[1],
            },
            "name": player.player_name,
            "stats": player.stats,
            "animation": player.animation_name
        })

    def getPlayers(self):
        return self.network_players

    def connect(self):
        try:
            self.client.connect(self.addr)
            return json.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data: any):
        try:
            self.client.send(bytes(json.dumps(data),encoding="utf-8"))
            #self.client.send(pickle.dumps(data))
            reply = self.client.recv(2048)
            return json.loads(reply.decode())
            #return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
