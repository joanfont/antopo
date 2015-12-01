from xml.etree import ElementTree
from xml.etree.ElementTree import tostring
import functools
from antopo.entities import Message


class BaseStrings:
    DEFAULT_TARGET_FILE_PREFIX = 'messages_'

    def __init__(self, path, source_language, target_language, target_prefix=None):
        self.path = path
        self.source_language = source_language
        self.target_language = target_language

        self.target_prefix = target_prefix if target_prefix else self.DEFAULT_TARGET_FILE_PREFIX

        self.messages = self.parse()

    def parse(self):
        raise NotImplemented


class StringsXML(BaseStrings):
    def parse(self):
        tree = ElementTree.parse(self.path)
        strings = tree.findall('./string')
        build_message_fnx = functools.partial(Message.from_node, self.source_language)
        return map(build_message_fnx, strings)

    def translate(self):
        return map(lambda x: x.to_translated_xml(), self.messages)

    def get_target_filename(self):
        return '{target_prefix}{target_language}.po'.format(target_pefix=self.target_prefix, target=languageself.target_language)

    def build_translation_po(self):
        target_filename = self.get_target_filename()
        with open(target_filename, 'w+') as f:
            for message in self.messages:
                po_message = message.to_po()
                po_block = '{}\n\n'.format(po_message)
                f.write(po_block)


class StringsPO(BaseStrings):
    def parse(self):
        pass
