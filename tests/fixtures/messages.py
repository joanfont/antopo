from antopo.entities import Message, MessageLibrary

messages = [
    Message('es', context='dummy_string', original='Lorem ipsum dolor sit amet'),
    Message('es', context='another_dummy_string', original='Lorem ipsum')
]

message_library = MessageLibrary(messages)