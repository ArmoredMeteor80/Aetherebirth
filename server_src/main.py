#!/bin/python3.10
import argparse
import threading

from server import Server

config = {
    "MAX_PLAYERS": 10,
    "PORT": 5555
}

def start_server_thread(server_thread: threading.Thread):
    if(server_thread.is_alive()):
        print("Server is already running !")
    else:
        print("Launching server")
        server_thread.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Aetherebirth Server',
        description='An Aetherebirth server in python')
    parser.add_argument('-t', '--tui',
                    action='store_true',
                    help='If specified, a TUI will be available')
    
    args = parser.parse_args()

    server = Server()
    server_thread=threading.Thread(target=server.backend.run, name="Downloader", kwargs={"hostname":"0.0.0.0", "port":5555})

    if(args.tui):
        commands = {
            "help": lambda: print("Available commands:\n  help: displays this help\n  start: starts the server\n  stop: stops the server"),
            "start": server_thread.run,
            "stop": server.stop,
        }

        running = True
        while running:
            cmd = input("> ")
            if(cmd in commands):
                commands[cmd]()
            else:
                commands['help']()
    else:
        server_thread.run()

