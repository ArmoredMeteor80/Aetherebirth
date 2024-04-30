

from ..map import MapManager
from ..entity import Entity


class NetworkEntity(Entity):
    def __init__(self, id, name, x, y, size=32):
        self.id = id
        super().__init__(name, x, y, size)

    def setPos(self, x, y):
        self.position[0] = x
        self.position[1] = y
        return self


class NetworkEntityManager():
    def __init__(self, map_manager: MapManager) -> None:
        self.network_entities = {}
        self.map_manager = map_manager

    def add(self, id: int, network_entity: NetworkEntity):
        self.network_entities[str(id)] = network_entity
        self.map_manager.maps[self.map_manager.current_map].group.add(self.network_entities[str(id)])

    def remove(self, id: int):
        del self.network_entities[str(id)]

    def getEntity(self, id):
        if(id in self.network_entities):
            return self.network_entities[str(id)]


    def updatePlayers(self, players: dict):
        player_list = []
        for player in players:
            if(not str(player['id']) in self.network_entities):
                entity = NetworkEntity(player['id'], "bob", player['position']['x'], player['position']['y'])
                entity.change_animation(player['animation'])
                self.add(player['id'], entity)
            else: 
                entity = self.network_entities[player['id']]
                entity.setPos(player['position']['x'], player['position']['y']).change_animation(player['animation'])
            player_list.append(player['id'])

        for entity_id in self.network_entities:
            entity = self.network_entities[entity_id]
            if(not entity.id in player_list):
                del self.network_entities[entity]

