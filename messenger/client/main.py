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
    # if client run from messenger/__main__.py (NOT CURRENTLY SUPPORTED)
    from messenger.client.message_handler import MessageHandler
    PROTOCOLS_PATH = Path().cwd().joinpath('protocols')


class Client:

    def __init__(self, host: str, port: int, connection_type: SocketKind = SOCK_STREAM,
                 connection_family: AddressFamily = AF_INET, *args, **kwargs):
        self.__host = host
        self.__port = port
        self.__address = (host, port, )
        self.__conn_type = connection_type
        self.__conn_family = connection_family
        self.__to_stop = False
        self.__message_handler = MessageHandler(PROTOCOLS_PATH)
        self.user = "Ivanov12345"

    def run(self) -> None:
        with socket(family=self.__conn_family, type=self.__conn_type) as s:
            if not self.__conn_family == AF_INET:
                raise ConnectionError(f"Unknown connection family. "
                                      f"Expected: AF_INET. Actual: {str(self.__conn_family)}")
            if self.__conn_type == SOCK_STREAM:
                try:
                    s.connect(self.__address)
                except ConnectionRefusedError as exc:
                    raise ConnectionError(f"Server is not running or other server error occurred. Error: {exc}")
                message = input('Write something to send to the server: ')
                to_send = dict(
                    username=self.user,
                    send_to="Petrov12345",
                    message=message,
                )
                # Сейчас тут вот так по глупому отправляется. В дальнейшем вынесу отправку сообщений
                # в отдельную корутину. И вообще сделаю принятие сообщений в через модуль select
                # s.sendall(to_send)
                self.__message_handler.send_user_message(to_send, temporary_communicator=s)
                received_data = s.recv(1024)
                self.__message_handler.handle_message(received_data)
            else:
                raise ConnectionError(f"Unknown connection type. "
                                      f"Expected: SOCK_STREAM. Actual: {str(self.__conn_type)}")
        # print(f"Received data from the server: '{received_data.decode(encoding='utf-8')}'")

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

