import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            if text_type == TextType.BOLD:
                if delimiter != "**":
                    raise ValueError("Invalid bold delimiter")
            elif text_type == TextType.ITALIC:
                if delimiter != "_":
                    raise ValueError("Invalid italic delimiter")
            elif text_type == TextType.CODE:
                if delimiter != "`":
                    raise ValueError("Invalid code delimiter")
            
            node_values = node.text.split(delimiter)
            is_text_type = True
            for text in node_values:
                if is_text_type:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                    is_text_type = False
                else:
                    new_nodes.append(TextNode(text, text_type))
                    is_text_type = True

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.+?)\]\((.+?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)