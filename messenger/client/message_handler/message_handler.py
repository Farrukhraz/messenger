import json
from enum import Enum
from typing import Union


class MessageTypes(Enum):
    AuthenticationRequest = "AuthenticationRequest"
    AuthenticationResponse = "AuthenticationResponse"
    JoinChatRequest = "JoinChatRequest"
    JoinChatResponse = "JoinChatResponse"
    LeaveChatRequest = "LeaveChatRequest"
    LeaveChatResponse = "LeaveChatResponse"
    UserDisconnected = "UserDisconnected"
    UserMessage = "UserMessage"
    UserMessageDelivered = "UserMessageDelivered"
    UserMessageRead = "UserMessageRead"
    UserPresenceResponse = "UserPresenceResponse"
    UserPresenceRequest = "UserPresenceRequest"
    UserTyping = "UserTyping"


class MessageHandler:

    def get_message_data(self, message: bytes) -> Union[dict, str]:
        try:
            message_data = json.loads(message)
        except json.decoder.JSONDecodeError:
            message_data = message.decode(encoding='utf-8')
            # logger.waring('Received unsupported message format. '
            # f'Expected: json like message. Actual: {message_data}')
        return message_data

    def get_message_type(self, message_data: Union[str, dict]) -> str:
        message_type = json.loads(message_data).get('type')
        if message_type is None:
            raise NameError
        return message_type

    def handle_message(self, message: bytes) -> None:
        message_data = self.get_message_data(message)
        if not isinstance(message_data, dict):
            return
        try:
            message_type = self.get_message_type(message_data)
        except NameError as exc:
            # logger.warning("Unsupported message is received. 'type' key is absent in message data")
            return
        if message_type is MessageTypes.AuthenticationResponse.value:
            self.__handle_authentication_response(message_data)
        if message_type is MessageTypes.JoinChatRequest.value:
            self.__handle_join_chat_request(message_data)
        if message_type is MessageTypes.JoinChatResponse.value:
            self.__handle_join_chat_response(message_data)
        if message_type is MessageTypes.LeaveChatResponse.value:
            self.__handle_leave_chat_response(message_data)
        if message_type is MessageTypes.UserMessage.value:
            self.__handle_user_message(message_data)
        if message_type is MessageTypes.UserMessageDelivered.value:
            self.__handle_user_message_delivered(message_data)
        if message_type is MessageTypes.UserMessageRead.value:
            self.__handle_user_message_read(message_data)
        if message_type is MessageTypes.UserPresenceRequest.value:
            self.__handle_user_presence_request(message_data)
        if message_type is MessageTypes.UserTyping.value:
            self.__handle_user_typing(message_data)

    def __handle_authentication_response(self, message_data: dict):
        pass

    def __handle_join_chat_request(self, message_data: dict):
        pass

    def __handle_join_chat_response(self, message_data: dict):
        pass

    def __handle_leave_chat_response(self, message_data: dict):
        pass

    def __handle_user_message(self, message_data: dict):
        pass

    def __handle_user_message_delivered(self, message_data: dict):
        pass

    def __handle_user_message_read(self, message_data: dict):
        pass

    def __handle_user_presence_request(self, message_data: dict):
        pass

    def __handle_user_typing(self, message_data: dict):
        pass
