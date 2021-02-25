# -*- coding: utf-8 -*-

import argparse

from socket import (
    socket,
    SOCK_STREAM,
    AF_INET,
    AddressFamily,
    SocketKind,
)
from pathlib import Path


if Path(__file__).absolute().parent == Path().cwd():
    from message_handler import MessageHandler
    PROTOCOLS_PATH = Path().cwd().parent.joinpath('protocols')
else:
    raise EnvironmentError("Error! Please start the server from /messenger/server directory "
                           "by 'python main.py' command")


class Server:

    def __init__(self, port: int, host: str = "", connection_type: SocketKind = SOCK_STREAM,
                 connection_family: AddressFamily = AF_INET, *args, **kwargs):
        self.__host = host
        self.__port = port
        self.__address = (host, port, )
        self.__conn_type = connection_type
        self.__conn_family = connection_family
        self.__to_stop = False
        self.__message_handler = MessageHandler(PROTOCOLS_PATH)

    def run(self) -> None:
        # ToDo make the server work with multiple clients
        with socket(family=self.__conn_family, type=self.__conn_type) as s:
            if not self.__conn_family == AF_INET:
                raise ConnectionError(f"Unknown connection family. "
                                      f"Expected: AF_INET. Actual: {str(self.__conn_family)}")
            if self.__conn_type == SOCK_STREAM:
                s.bind(self.__address)
                s.listen()
                print("Server started and waiting for connections...")
                conn, addr = s.accept()
                self.__message_handler.communicator = conn
                with conn:
                    print(f"Connection established with {addr}")
                    self.__message_handler.send_precence_request_message()
                    while not self.__to_stop:

                        received_message = conn.recv(4096)
                        self.__message_handler.handle_message(received_message)
                        # if not received_message:
                        #     break
                        # print(f"Received data from client: {received_message.decode(encoding='utf-8')}")
                        # conn.sendall(received_message)
            else:
                raise ConnectionError(f"Unknown connection type. "
                                      f"Expected: SOCK_STREAM. Actual: {str(self.__conn_type)}")

    def stop(self) -> None:
        """ Switch-flag for stopping the server """
        self.__to_stop = True


def get_args():
    parser = argparse.ArgumentParser(description="Run a server")
    parser.add_argument('-addr', '--address', default='',
                        help='TCP server address')
    parser.add_argument('-p', '--port', default=7777,
                        help='TCP server port')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    server = Server(port=args.port, host=args.address)
    server.run()
