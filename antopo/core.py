from xml.dom import minidom
from xml.etree import ElementTree
import polib
import functools
from antopo.entities import Message, MessageLibrary


class BaseStrings:
    FILE_PREFIX = 'messages_'

    def __init__(self, message_library, source_language, target_language, file_prefix=None):
        self.message_library = message_library
        self.source_language = source_language
        self.target_language = target_language
        self.file_prefix = file_prefix if file_prefix else self.FILE_PREFIX

    @classmethod
    def from_file(cls, path, source_language, target_language, target_prefix=None):
        messages = cls.parse(path, source_language, target_language)
        return cls(messages, source_language, target_language, target_prefix)

    @classmethod
    def parse(cls, path, source_language, target_language):
        raise NotImplemented


class StringsXML(BaseStrings):
    @classmethod
    def parse(cls, path, source_language, target_language):
        tree = ElementTree.parse(path)
        strings = tree.findall('./string')
        build_message_fnx = functools.partial(Message.from_xml_node, source_language)
        messages = map(build_message_fnx, strings)
        return MessageLibrary(messages)

    def get_target_filename(self):
        return '{target_prefix}{target_language}.po'.format(target_pefix=self.file_prefix,
                                                            target=self.target_language)

    def build_translation_po(self):
        target_filename = self.get_target_filename()
        messages = self.message_library.messages
        with open(target_filename, 'w+') as f:
            for message in messages:
                po_message = message.to_po()
                po_block = '{}\n\n'.format(po_message)
                f.write(po_block)


class StringsPO(BaseStrings):
    @classmethod
    def parse(cls, path, source_language, target_language):
        po = polib.pofile(path)
        build_message_fnx = functools.partial(Message.from_po_node, source_language)
        messages = map(build_message_fnx, po)
        return MessageLibrary(messages)

    def get_source_filename(self):
        return '{source_prefix}{source_language}.xml'.format(source_prefix=self.file_prefix,
                                                             source_language=self.source_language)

    def get_target_filename(self):
        return '{target_prefix}{target_language}.xml'.format(target_prefix=self.file_prefix,
                                                             target_language=self.target_language)

    def build_original_xml(self):
        source_filename = self.get_source_filename()
        messages = self.message_library.messages
        root = ElementTree.Element('resources')
        for message in messages:
            xml_node = message.to_original_xml()
            root.append(xml_node)

        self._write_xml_to_file(source_filename, root)

    def build_translation_xml(self):
        target_filename = self.get_target_filename()
        messages = self.message_library.messages
        root = ElementTree.Element('resources')
        for message in messages:
            xml_node = message.to_translated_xml()
            root.append(xml_node)

        self._write_xml_to_file(target_filename, root)

    @staticmethod
    def _write_xml_to_file(path, root):
        rough_string = ElementTree.tostring(root, 'utf-8')
        xml_parsed = minidom.parseString(rough_string)
        xml_bytes = xml_parsed.toprettyxml('\t', encoding='utf-8')
        with open(path, 'wb+') as f:
            f.write(xml_bytes)
