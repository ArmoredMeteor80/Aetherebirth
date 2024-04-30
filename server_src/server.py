import random
import threading
from pygase import GameState, Backend


class Server:
    def __init__(self) -> None:
        self.game_state = GameState(
            players={},
        )
        self.ids = {}#Key: client_address, value: player_id
        
        self.backend = Backend(self.game_state, self.time_step, event_handlers={})
        
        # Register the handlers.
        self.backend.game_state_machine.register_event_handler("JOIN", self.on_join)
        self.backend.game_state_machine.register_event_handler("LEAVE", self.on_leave)
        self.backend.game_state_machine.register_event_handler("MOVE", self.on_move)

    def stop(self):
        self.backend.shutdown()

    def time_step(self, game_state, dt):
        return {}

    # "MOVE" event handler
    def on_move(self, player_id, new_position, animation, **kwargs):
        print(self.game_state.players)
        print(f"{self.game_state.players[player_id]['name']} moved to {new_position}")
        return {"players": {player_id: {"position": new_position, "animation": animation}}}


    # "JOIN" event handler
    def on_join(self, player_name, client_address, **kwargs):
        print(f"{player_name} joined.")
        player_id = self.max_id()
        # Notify client that the player successfully joined the game.
        self.backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
        return {
            # Add a new entry to the players dict
            "players": {player_id: {"name": str(player_name), "position": (0, 0)}},
        }

    def on_leave(self, game_state, client_address, **kwargs):
        player_name = self.game_state.players[self.ids[client_address]]['name']
        print(f"{player_name} left.")
        player_id = len(game_state.players)
        # Notify client that the player successfully joined the game.
        self.backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
        return {
            # Add a new entry to the players dict
            "players": {player_id: {"name": str(player_name), "position": (0, 0)}},
        }

    def max_id(self):
        max_id = 0
        for client in self.ids:
            if(self.ids[client] > max_id):
                max_id = self.ids[client]
        return max_id+1


