from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        sametext = self.text == target.text
        sametype = self.text_type == target.text_type
        sameurl = self.url == target.url

        return sametext and sametype and sameurl
    
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    
    def to_html(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text).to_html()
            case TextType.BOLD:
                return LeafNode('b', self.text).to_html()
            case TextType.ITALIC:
                return LeafNode('i', self.text).to_html()
            case TextType.CODE:
                return LeafNode('code', self.text).to_html()
            case TextType.LINK:
                return LeafNode('a', self.text, {'href':self.url}).to_html()
            case TextType.IMAGE:
                return LeafNode('img', '', {'src':self.url,'alt':self.text}).to_html()
            case _:
                raise Exception('Wrong text type')