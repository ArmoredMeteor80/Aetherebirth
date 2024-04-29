import socket
from _thread import *
import sys
import pickle

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, Server Started")

players = {}


def threaded_client(conn: socket, player: dict):
    conn.send(str.encode("Connected"))
    conn.send(pickle.dumps(player))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            player['data'] = data

            if not data:
                print(f"Disconnected from player {player['num']}")
                break
            else:
                reply = players
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print(f"Lost connection to {player['name']}")
    conn.close()


current_player = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    players[addr] = {
        "num": current_player,
        "name": f"Player_{current_player}",
    }
    print(players)

    start_new_thread(threaded_client, (conn, players[addr]))
    current_player += 1
