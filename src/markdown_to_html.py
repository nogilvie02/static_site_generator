from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes.append(block_to_html_node(block, block_type))
    return ParentNode("div", html_nodes)


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.CODE:
            block = block[4:-3]
            text_node = TextNode(block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [html_node])
            return ParentNode("pre", [code_node])
        case BlockType.HEADING:
            tag = heading_tag(block)
            block = block[int(tag[1]) + 1:]
            children = text_to_children(block)
            return ParentNode(tag, children)
        case BlockType.QUOTE:
            result_quote = ""
            lines = block.split("\n")
            for line in lines:
                result_quote += line.lstrip(">").strip() + " "
            children = text_to_children(result_quote.strip())
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            children = []
            for line in lines:
                line = line.lstrip("- ")
                children.append(ParentNode("li", text_to_children(line)))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            children = []
            for line in lines:
                line = line.split(". ", 1)[1]
                children.append(ParentNode("li", text_to_children(line)))
            return ParentNode("ol", children)
        case BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children = text_to_children(text)
            return ParentNode("p", children)
        case _:
            raise TypeError("Invalid BlockType presented, cannot convert to HTMLNode")

        

def heading_tag(block):
    for i in range(min(len(block), 6)):
        if block[i] != "#":
            break
    return f"h{i}"


def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children
