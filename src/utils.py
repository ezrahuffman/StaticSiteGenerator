from textnode import *
from leafnode import LeafNode
from typing import List
import re

def text_node_to_html_node(text_node: TextNode):
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
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception(f"Unrecognized text type {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str, text_type:TextType) -> List[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        first = True
        done = False
        text = old_node.text
        while not done:
            first_index = text.find(delimiter)
            if first_index == -1:
                done = True # didn't find any delimeters in the string
                new_nodes.append(TextNode(text, old_node.text_type))
                continue
            if first_index == len(text) - 1:
                done = True # only one delimeter found, don't do anything
                new_nodes.append(TextNode(text, old_node.text_type))
                continue
            second_index = text.find(delimiter, first_index + len(delimiter))
            if second_index == -1:
                done = True # only one delimeter found, don't do anything
                new_nodes.append(TextNode(text, old_node.text_type))
                continue

            if first:
                new_nodes.append(TextNode(text[:first_index], old_node.text_type))
            new_nodes.append(TextNode(text[first_index+len(delimiter):second_index], text_type))

            if second_index == len(text) - 1:
                done = True
                continue

            text = text[second_index+len(delimiter):]
    return new_nodes

def extract_markdown_images(text:str) -> List[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text:str) -> List[tuple]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_images(node.text)
        for link_info in links:
            search_str = f"![{link_info[0]}]({link_info[1]})"
            split = node.text.split(search_str, 1)
            new_nodes.append(TextNode(split[0], TextType.TEXT))
            if len(split) > 1:
                new_nodes.append(TextNode(link_info[0], TextType.IMAGE, link_info[1]))
                node.text = split[1]

        if len(links) == 0:
            new_nodes.append(node)
        elif node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        for link_info in links:
            search_str = f"[{link_info[0]}]({link_info[1]})"
            split = node.text.split(search_str, 1)
            new_nodes.append(TextNode(split[0], TextType.TEXT))
            if len(split) > 1:
                new_nodes.append(TextNode(link_info[0], TextType.LINK, link_info[1]))
                node.text = split[1]

        if len(links) == 0:
            new_nodes.append(node)
        elif node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text:str)->List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD )
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC )
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE )
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    