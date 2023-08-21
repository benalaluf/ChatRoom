from server.server import Server

if __name__ == '__main__':
    server = Server('localhost', 4343).accept_connections()