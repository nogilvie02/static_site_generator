import re
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import LeafNode, ParentNode


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type != BlockType.CODE:
            node = block_to_html_node(block, block_type)



def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.HEADING:
            tag = heading_tag(block)
            # format block
            return LeafNode(tag, block)
        case BlockType.QUOTE:
            # format block
            return LeafNode("blockquote", block)
        case BlockType.UNORDERED_LIST:
            # todo
            pass
        case BlockType.ORDERED_LIST:
            # todo
            pass
        case BlockType.PARAGRAPH:
            # todo
            return LeafNode("p", block)
        case _:
            raise TypeError("Invalid BlockType presented, cannot convert to HTMLNode")

        

def heading_tag(block):
    for i in range(min(len(block), 6)):
        if block[i] != "#":
            break
    return f"h{i}"