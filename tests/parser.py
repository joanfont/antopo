import unittest
from antopo.core import StringsXML, StringsPO
from tests.fixtures.messages import message_library


class ParserTestSuite(unittest.TestCase):
    def test_parse_xml(self):
        xml_strings = StringsXML(message_library, 'es', 'en', 'tests/fixtures/messages_')
        xml_strings.build_translation_po()

        po_strings = StringsPO.from_file('tests/fixtures/messages_en.po', 'en', 'es')
        po_messages = po_strings.message_library

        self.assert_message_library_equals(message_library, po_messages)

    @classmethod
    def assert_message_library_equals(cls, message_library_1, message_library_2):
        messages_1 = list(message_library_1.messages)
        messages_2 = list(message_library_2.messages)

        l_messages_1 = len(messages_1)
        l_messages_2 = len(messages_2)

        assert l_messages_1 == l_messages_2

        for i in range(0, l_messages_1):
            message_1 = messages_1[i]
            message_2 = messages_2[i]
            cls.assert_message_entities_equal(message_1, message_2)

    @classmethod
    def assert_message_entities_equal(cls, message_1, message_2):
        assert message_1.original == message_2.original
        assert message_1.context == message_2.context
