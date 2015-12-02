from xml.etree.ElementTree import Element


class BaseEntity:
    pass


class Message(BaseEntity):
    def __init__(self, language, context=None, original=None, translation=None):
        self.language = language
        self.context = context
        self.original = original
        self.translation = translation

    @classmethod
    def from_xml_node(cls, language, node):
        context = node.get('name')
        original = node.text
        return cls(language, context=context, original=original)

    @classmethod
    def from_po_node(cls, language, node):
        context = node.msgctxt
        original = node.msgid
        translation = node.msgstr
        return cls(language, context=context, original=original, translation=translation)

    def to_original_xml(self):
        return self._to_xml(self.original)

    def to_translated_xml(self):
        return self._to_xml(self.translation)

    def _to_xml(self, text):
        xml_element = Element('string')

        if self.context:
            xml_element.set('name', self.context)

        xml_element.text = text

        return xml_element

    def to_po(self):
        translation = self.translation if self.translation is not None else ''
        return '''msgctxt "{context}"\nmsgid "{original}"\nmsgstr "{translation}"'''.format(context=self.context,
                                                                                            original=self.original,
                                                                                            translation=translation)

    def __repr__(self):
        return '{}: {}'.format(self.context, self.original)


class MessageLibrary(BaseEntity):

    def __init__(self, messages):
        self.messages = messages
