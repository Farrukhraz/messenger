from socket import (
    socket,
    SOCK_STREAM,
    AF_INET,
    AddressFamily,
    SocketKind,
)


class Client:

    def __init__(self, host: str, port: int, connection_type: SocketKind = SOCK_STREAM,
                 connection_family: AddressFamily = AF_INET, *args, **kwargs):
        self.__host = host
        self.__port = port
        self.__address = (host, port, )
        self.__conn_type = connection_type
        self.__conn_family = connection_family
        self.__to_stop = False

    def run(self) -> None:
        with socket(family=self.__conn_family, type=self.__conn_type) as s:
            if not self.__conn_family == AF_INET:
                raise ConnectionError(f"Unknown connection family. "
                                      f"Expected: AF_INET. Actual: {str(self.__conn_family)}")
            if self.__conn_type == SOCK_STREAM:
                s.connect(self.__address)
                to_send = input('Write something to send to the server: ').encode(encoding='ascii')
                s.sendall(to_send)
                received_data = s.recv(1024)
            else:
                raise ConnectionError(f"Unknown connection type. "
                                      f"Expected: SOCK_STREAM. Actual: {str(self.__conn_type)}")
        print(f"Received data from the server: '{received_data.decode(encoding='utf-8')}'")

    def stop(self) -> None:
        """ Switch-flag for stopping the client """
        self.__to_stop = True