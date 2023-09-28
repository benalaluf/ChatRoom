from src.connections.server import Server

if __name__ == '__main__':
    server = Server('localhost', 6767).main()