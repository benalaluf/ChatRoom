from src.connections.server_conn import Server

if __name__ == '__main__':
    server = Server('0.0.0.0', 7874).main()