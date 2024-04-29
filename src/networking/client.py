import socket

DEFAULT_PORT = 42069


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket()
        self.client_id = 0

    def connect(self, addr: str, port: int = DEFAULT_PORT):
        self.socket.connect((addr, port))
        self.socket.sendall(b'hello')


if __name__ == "__main__":
    client = Client()
    client.connect('127.0.0.1')
