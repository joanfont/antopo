import unittest
from antopo.core import StringsXML, StringsPO
from tests.fixtures.messages import message_library


class ParserTest(unittest.TestCase):
    def test_parse_xml(self):
        xml_strings = StringsXML(message_library, 'es', 'en', 'fixtures/messages_')
        xml_strings.build_translation_po()

        po_strings = StringsPO.from_file('fixtures/messages_en.po', 'en', 'es')
        po_messages = po_strings.message_library

        self.assert_message_library_equals(message_library, po_messages)

    @classmethod
    def assert_message_library_equals(cls, message_library_1, message_library_2):

        messages_1 = list(message_library_1.messages)
        messages_2 = list(message_library_2.messages)

        assert len(messages_1) == len(messages_2)
        assert messages_1 == messages_2


