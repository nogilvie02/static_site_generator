import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if text_type == TextType.BOLD and delimiter != "**":
            raise ValueError("Invalid bold delimiter")
        if text_type == TextType.ITALIC and delimiter != "_":
            raise ValueError("Invalid italic delimiter")
        if text_type == TextType.CODE and delimiter != "`":
            raise ValueError("Invalid code delimiter")

        parts = node.text.split(delimiter)

        # If even number of parts, then there’s an unmatched delimiter
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        # Build new nodes, skipping empty strings
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                # outside delimiters -> plain text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiters -> formatted
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.+?)\]\((.+?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if images == []:
                new_nodes.append(node)
                continue
            remaining_text_to_process = node.text
            for image in images:
                image_alt, image_url = image
                text_to_process, remaining_text_to_process = remaining_text_to_process.split(f'![{image_alt}]({image_url})', 1)
                if text_to_process != "":
                    new_nodes.append(TextNode(text_to_process, TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            if remaining_text_to_process != "":
                new_nodes.append(TextNode(remaining_text_to_process, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if links == []:
                new_nodes.append(node)
                continue
            remaining_text_to_process = node.text
            for link in links:
                link_alt, link_url = link
                text_to_process, remaining_text_to_process = remaining_text_to_process.split(f'[{link_alt}]({link_url})', 1)
                if text_to_process != "":
                    new_nodes.append(TextNode(text_to_process, TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            if remaining_text_to_process != "":
                new_nodes.append(TextNode(remaining_text_to_process, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes