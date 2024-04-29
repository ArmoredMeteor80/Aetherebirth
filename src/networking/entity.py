

from ..map import MapManager
from ..entity import Entity


class NetworkEntity(Entity):
    def __init__(self, id, name, x, y, size=32):
        self.id = id
        super().__init__(name, x, y, size)

    def setPos(self, x, y):
        self.position[0] = x
        self.position[1] = y


class NetworkEntityManager():
    def __init__(self, map_manager: MapManager) -> None:
        self.network_entities = {}
        self.map_manager = map_manager

    def add(self, id: int, network_entity: NetworkEntity):
        self.network_entities[id] = network_entity
        self.map_manager.maps[self.map_manager.current_map].group.add(self.network_entities[id])

    def remove(self, id: int):
        del self.network_entities[id]

    def getEntity(self, id):
        if(id in self.network_entities):
            return self.network_entities[id]


    def updatePlayers(self, players: dict):
        player_list = []
        for player in players:
            print(player)
            if(not player['id'] in self.network_entities):
                self.add(player['id'], NetworkEntity(player['id'], "bob", player['position']['x'], player['position']['y']))
            else: 
                self.network_entities[player['id']].setPos(player['position']['x'], player['position']['y'])
            player_list.append(player['id'])

        for entity_id in self.network_entities:
            entity = self.network_entities[entity_id]
            if(not entity.id in player_list):
                del self.network_entities[entity]

