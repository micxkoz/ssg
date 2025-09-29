import re
from textnode import TextType, TextNode

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

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    splitted_nodes = []
    if len(old_nodes) == 0:
        return splitted_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            splitted_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            splitted_nodes.append(node)
            continue
        
        text_to_split = node.text
        for image in images:
            splitted_text = text_to_split.split(f"![{image[0]}]({image[1]})", 1)
            if len(splitted_text[0]) > 0:
                splitted_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            splitted_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text_to_split = splitted_text[1]

        if len(splitted_text[1]) > 0:
            splitted_nodes.append(TextNode(splitted_text[1], TextType.TEXT))

    return splitted_nodes

def split_nodes_link(old_nodes):
    splitted_nodes = []
    if len(old_nodes) == 0:
        return splitted_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            splitted_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            splitted_nodes.append(node)
            continue
        
        text_to_split = node.text
        for link in links:
            splitted_text = text_to_split.split(f"[{link[0]}]({link[1]})", 1)
            if len(splitted_text[0]) > 0:
                splitted_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            splitted_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text_to_split = splitted_text[1]

        if len(splitted_text[1]) > 0:
            splitted_nodes.append(TextNode(splitted_text[1], TextType.TEXT))

    return splitted_nodes

def text_to_textnodes(text):
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    return result