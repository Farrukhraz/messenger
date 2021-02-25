# -*- coding: utf-8 -*-

from socket import socket
from pathlib import Path

from message_converter import MessageConverter
from well_known_types.message_types import MessageTypes


class MessageHandler:

    def __init__(self, protocols_dir_path: Path):
        self.__protocols_dir_path = protocols_dir_path
        self.__message_converter = MessageConverter(protocols_dir_path)
        self.__communicator = None

    def handle_message(self, message: bytes) -> None:
        message_data = self.__message_converter.get_message_data(message)
        if not isinstance(message_data, dict):
            # Сделать логгер после 5го занятия
            # logger.warning("Incorrect message data. Data: {message_data}")
            return
        try:
            message_type = self.__message_converter.get_message_type(message_data)
        except NameError as exc:
            # logger.warning("Unsupported message is received. 'type' key is absent in message data")
            return
        if message_type == MessageTypes.UserMessage.value:
            self.__handle_user_message(message, message_data)
        elif message_type == MessageTypes.UserPresenceResponse.value:
            self.__handle_user_presence_response(message_data)

    def send_precence_request_message(self) -> None:
        # Temporarily Hardcode
        message_data = dict(
            username='Ivanov12345'
        )
        message = self.__message_converter.get_user_presence_request_message(message_data)
        self.__communicator.sendall(message)
        print(f"UserPresenceRequest sent")

    def __handle_user_message(self, message: bytes, message_data: dict) -> None:
        # Пока просто вывод в std_out
        try:
            from_username = message_data.get('user').get('username')
            to_username = message_data.get('send_to').get('user').get('username')
            # For now just redirect it back
            self.__communicator.sendall(message)
            print(f"'{from_username}' user's message sent to '{to_username}'")
        except AttributeError as exc:
            # logger should be here
            print(f"Received message couldn't be read. "
                  f"Message: {message_data} Error: {exc}")

    def __handle_user_presence_response(self, message_data: dict) -> None:
        try:
            time_ = message_data.get('time')
            username = message_data.get('user').get('username')
            result_status = message_data.get('result').get('status')
            result_desc = message_data.get('result').get('description')
            if not (200 <= int(result_status) < 300):
                raise ValueError(f"Presence came with '{result_status}' error from user "
                                 f"'{username}' at {time_}. Result description: {result_desc}")
            else:
                print(f"'{username}' user's Presence message received")
        except (AttributeError, ValueError) as exc:
            # logger should be here
            print(f"Received message couldn't be read. "
                  f"Message: {message_data} Error: {exc}")

    @property
    def communicator(self) -> socket:
        return self.__communicator

    @communicator.setter
    def communicator(self, communicator: socket) -> None:
        self.__communicator = communicator
