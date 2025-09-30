from enum import Enum
import re

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
    if re.match("^#{1,6} .+", block):
        return BlockType.HEADING
    if re.match(r"^`{3}(.|\n)+`{3}$", block):
        return BlockType.CODE
    if re.match(r"^>.+?(?:\n>.+?)*$", block):
        return BlockType.QUOTE
    if re.match(r"^- .+?(?:\n- .+?)*$", block):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d\. .+?(?:\n\d\. .+?)*$", block):
        numbers = re.findall(r"(^\d|(?<=\n)\d)", block)
        if all(map(lambda x, y: int(x) + 1 == int(y), numbers, numbers[1:])):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH