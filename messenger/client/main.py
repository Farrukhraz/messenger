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
    # if client run from messenger/client/main.py
    from message_handler import MessageHandler
    PROTOCOLS_PATH = Path().cwd().parent.joinpath('protocols')
else:
    raise EnvironmentError("Error! Please start the client from /messenger/client directory "
                           "by 'python main.py -addr localhost' command")


class Client:

    def __init__(self, host: str, port: int, connection_type: SocketKind = SOCK_STREAM,
                 connection_family: AddressFamily = AF_INET, *args, **kwargs):
        self.__host = host
        self.__port = port
        self.__address = (host, port, )
        self.__conn_type = connection_type
        self.__conn_family = connection_family
        self.__to_stop = False
        self.user = "Ivanov12345"
        self.__message_handler = MessageHandler(PROTOCOLS_PATH, self.user)

    def run(self) -> None:
        # ToDo use ZeroMQ or socket + select (lib)
        with socket(family=self.__conn_family, type=self.__conn_type) as s:
            if not self.__conn_family == AF_INET:
                raise ConnectionError(f"Unknown connection family. "
                                      f"Expected: AF_INET. Actual: {str(self.__conn_family)}")
            if self.__conn_type == SOCK_STREAM:
                try:
                    s.connect(self.__address)
                except ConnectionRefusedError as exc:
                    raise ConnectionError(f"Server is not running or unknown ServerError occurred. Error: {exc}")
                self.__message_handler.communicator = s
                self.__start_chat_session(s)
            else:
                raise ConnectionError(f"Unknown connection type. "
                                      f"Expected: SOCK_STREAM. Actual: {str(self.__conn_type)}")

    def __start_chat_session(self, sock: socket) -> None:
        while not self.__to_stop:
            received_data = sock.recv(1024)
            self.__message_handler.handle_message(received_data)

            message = input('Write something to send to the server: ')
            to_send = dict(
                username=self.user,
                send_to="Petrov12345",
                message=message,
            )
            self.__message_handler.send_user_message(to_send, temporary_communicator=sock)

    def stop(self) -> None:
        """ Switch-flag for stopping the client """
        self.__to_stop = True


def get_args():
    parser = argparse.ArgumentParser(description="Run a client")
    parser.add_argument('-addr', '--address', required=True,
                        help='TCP client address. To run on localhost, just write "-addr localhost"')
    parser.add_argument('-p', '--port', default=7777,
                        help='TCP client port')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    server = Client(port=args.port, host=args.address)
    try:
        server.run()
    except ConnectionError as ex:
        print(f"Error! Couldn't start client because the following error: \n'{ex}'")

