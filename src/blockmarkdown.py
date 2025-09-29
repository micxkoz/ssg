from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        stripped_block = block.strip()
        if len(stripped_block) != 0:
            blocks.append(stripped_block)
    return blocks

def block_to_block_type(block):
    raise NotImplemented