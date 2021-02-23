from enum import Enum


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
