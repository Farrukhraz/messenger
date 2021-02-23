# -*- coding: utf-8 -*-

import json

from datetime import datetime
from pathlib import Path
from typing import Union

from well_known_types.message_types import MessageTypes
from message_converter import MessageConverter


class MessageHandler:

    def __init__(self, protocols_dir_path: Path):
        self.__username = None
        self.__protocols_dir_path = protocols_dir_path
        self.__message_converter = MessageConverter(protocols_dir_path)

    def handle_message(self, message: bytes) -> None:
        message_data = self.__message_converter.get_message_data(message)
        if not isinstance(message_data, dict):
            return
        try:
            message_type = self.__message_converter.get_message_type(message_data)
        except NameError as exc:
            # logger.warning("Unsupported message is received. 'type' key is absent in message data")
            return
        if message_type == MessageTypes.AuthenticationResponse.value:
            self.__handle_authentication_response(message_data)
        elif message_type == MessageTypes.JoinChatRequest.value:
            self.__handle_join_chat_request(message_data)
        elif message_type == MessageTypes.JoinChatResponse.value:
            self.__handle_join_chat_response(message_data)
        elif message_type == MessageTypes.LeaveChatResponse.value:
            self.__handle_leave_chat_response(message_data)
        elif message_type == MessageTypes.UserMessage.value:
            self.__handle_user_message(message_data)
        elif message_type == MessageTypes.UserMessageDelivered.value:
            self.__handle_user_message_delivered(message_data)
        elif message_type == MessageTypes.UserMessageRead.value:
            self.__handle_user_message_read(message_data)
        elif message_type == MessageTypes.UserPresenceRequest.value:
            self.__handle_user_presence_request(message_data)
        elif message_type == MessageTypes.UserTyping.value:
            self.__handle_user_typing(message_data)

    def send_authentication_request_message(self, message_data: dict) -> None:
        pass

    def send_user_message(self, message_data: dict, temporary_communicator) -> None:
        message = self.__message_converter.get_user_message_message(message_data)
        temporary_communicator.sendall(message)

    def send_join_chat_request(self, message_data: dict) -> None:
        pass

    def send_leave_chat_request(self, message_data: dict) -> None:
        pass

    def __handle_authentication_response(self, message_data: dict) -> None:
        pass

    def __handle_join_chat_request(self, message_data: dict) -> None:
        pass

    def __handle_join_chat_response(self, message_data: dict) -> None:
        pass

    def __handle_leave_chat_response(self, message_data: dict) -> None:
        pass

    def __handle_user_message(self, message_data: dict) -> None:
        # ToDo Пока что просто вывод в std_out
        try:
            print(f"Message received: from {message_data.get('user').get('username')}; "
                  f"Sent at {message_data.get('time')}; "
                  f"Message: {message_data.get('message')}")
        except AttributeError as exc:
            # logger should be here
            print(f"Received message couldn't be read. Error: {exc}")
        # send UserMessageDelivered to sender

    def __handle_user_message_delivered(self, message_data: dict) -> None:
        pass

    def __handle_user_message_read(self, message_data: dict) -> None:
        pass

    def __handle_user_presence_request(self, message_data: dict) -> None:
        pass

    def __handle_user_typing(self, message_data: dict) -> None:
        pass
