

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
        del self.network_entities[id]

    def getEntity(self, id):
        if(id in self.network_entities):
            return self.network_entities[id]


    def updatePlayers(self, players: dict):
        player_list = []
        for player_id in players:
            player = players[player_id]
            print(player_id, player)
            if(not (str(player_id) in self.network_entities)):
                self.add(player_id, NetworkEntity(player_id, "bob", player['position'][0], player['position'][1]))
                print("Spawned fake player")
            else: 
                entity = self.network_entities[str(player_id)]
                entity.setPos(player['position'][0], player['position'][1])
                if(entity.animation_name != player['animation'] ):
                    entity.change_animation(player['animation'])
            player_list.append(player_id)

        for entity_id in self.network_entities:
            entity = self.network_entities[entity_id]
            if(not entity.id in player_list):
                print(f"Deleting {entity.id}")
                del self.network_entities[entity]

