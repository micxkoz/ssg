from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    splitted_nodes = []
    if len(old_nodes) == 0:
        return splitted_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            splitted_nodes.append(node)
            continue

        counter = node.text.count(delimiter)
        if counter == 0:
            splitted_nodes.append(node)
            continue

        if counter % 2 != 0:
            raise ValueError("invalid Markdown")

        splitted_text = node.text.split(delimiter)
        for i in range(0,len(splitted_text)):
            if splitted_text[i] == "":
                continue

            if i % 2 == 0:
                splitted_nodes.append(TextNode(splitted_text[i], TextType.TEXT))
            else:
                splitted_nodes.append(TextNode(splitted_text[i], text_type))
        
    return splitted_nodes
        