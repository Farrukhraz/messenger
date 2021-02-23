# -*- coding: utf-8 -*-

import json

from datetime import datetime
from pathlib import Path
from typing import Union

from well_known_types.message_types import MessageTypes


class MessageConverter:

    def __init__(self, protocols_dir_path: Path):
        self.__protocols_dir_path = protocols_dir_path

    def get_message_data(self, message: bytes) -> Union[dict, str]:
        try:
            message_data = json.loads(message)
        except json.decoder.JSONDecodeError:
            message_data = message.decode(encoding='utf-8')
            # logger.waring('Received unsupported message format. '
            # f'Expected: json like message. Actual: {message_data}')
        return message_data

    def get_message_type(self, message_data: Union[str, dict]) -> str:
        message_type = message_data.get('type')
        if message_type is None:
            raise NameError
        return message_type

    def get_user_message_message(self, message_data: dict, encoding: 'str' = "utf-8") -> bytes:
        protocol_path = self.__get_protocol_path(MessageTypes.UserMessage)
        protocol_data = self.__deserialize_json(protocol_path)
        user_from = message_data.get('username')
        user_to = message_data.get('send_to')
        user_message = message_data.get('message')
        if None in (user_from, user_to, user_message):
            raise ValueError("One of user_to/user_from/user_message is not given. "
                             f"Given data: {message_data}")
        protocol_data['user']['username'] = user_from
        protocol_data['send_to']['user']['username'] = user_to
        protocol_data['message'] = user_message
        protocol_data['time'] = self.__get_iso_time()
        protocol_data['encoding'] = encoding
        return self.__serialize_message(protocol_data, encoding)

    def __get_protocol_path(self, protocol_name: MessageTypes) -> Path:
        a = protocol_name.value
        path = self.__protocols_dir_path.joinpath(f"{a}.json")
        if not path.is_file():
            raise FileNotFoundError
        return path

    def __get_iso_time(self) -> str:
        """
        Get time in ISO format
        Format: YYYY-MM-DDThh:mm:ss±hh:mm
        Ex:     2005-08-09T18:31:42+03:30
        """
        return datetime.now().astimezone().replace(microsecond=0).isoformat()

    def __deserialize_json(self, file_path: Path) -> 1:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __serialize_message(self, data: dict, encoding: str = 'utf-8') -> bytes:
        return json.dumps(data, ensure_ascii=False).encode(encoding=encoding)

