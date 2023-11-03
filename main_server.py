from src.connections.server_conn import Server

if __name__ == '__main__':
    server = Server('127.0.0.1', 1212).main()