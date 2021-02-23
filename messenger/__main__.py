import socket

from threading import Thread
from time import sleep

from messenger.client import Client
from messenger.server import Server


CLIENT_HOST = 'localhost'
SERVER_HOST = ''
SERVER_PORT = 7777
CONN_FAMILY = socket.AF_INET
CONN_TYPE = socket.SOCK_STREAM


def run_client():
    client = Client(host=CLIENT_HOST, port=SERVER_PORT,
                    connection_type=CONN_TYPE, connection_family=CONN_FAMILY)
    client.run()


def run_server():
    server = Server(host=SERVER_HOST, port=SERVER_PORT,
                    connection_type=CONN_TYPE, connection_family=CONN_FAMILY)
    server.run()


def main():
    server = Thread(target=run_server)
    client = Thread(target=run_client)

    server.start()
    sleep(1)
    client.start()


if __name__ == '__main__':
    main()
