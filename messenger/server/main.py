from socket import (
    socket,
    SOCK_STREAM,
    AF_INET,
    AddressFamily,
    SocketKind,
)


class Server:

    def __init__(self, port: int, host: str = "", connection_type: SocketKind = SOCK_STREAM,
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
                s.bind(self.__address)
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connection established with {addr}")
                    while not self.__to_stop:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(f"Received data from client: {data.decode(encoding='utf-8')}")
                        conn.sendall(data)
            else:
                raise ConnectionError(f"Unknown connection type. "
                                      f"Expected: SOCK_STREAM. Actual: {str(self.__conn_type)}")

    def stop(self) -> None:
        """ Switch-flag for stopping the server """
        self.__to_stop = True
