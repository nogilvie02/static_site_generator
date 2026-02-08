# Block Markdown
from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    result_blocks = []

    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            result_blocks.append(block)
    return result_blocks


def is_heading(block):
    return re.match(r"^#{1,6} .+", block) is not None


def is_code(block):
    return block.startswith("```\n") and block.endswith("```") and len(block) > 6


def is_quote(block):
    lines = block.split("\n")
    for line in lines:
        if not line or line[0] != ">":
            return False
    return True


def is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if not line or line[0:2] != "- ":
            return False
    return True


def is_ordered_list(block):
    lines = block.split("\n")
    for i, line in enumerate(lines, start=1):
        if not line or line[0:3] != f"{i}. ":
            return False
    return True


def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH