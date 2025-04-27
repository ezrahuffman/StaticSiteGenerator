from textnode import *
from leafnode import LeafNode
from typing import List

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
            second_index = text.find(delimiter, first_index + 1)
            if second_index == -1:
                done = True # only one delimeter found, don't do anything
                new_nodes.append(TextNode(text, old_node.text_type))
                continue

            if first:
                new_nodes.append(TextNode(text[:first_index], old_node.text_type))
            new_nodes.append(TextNode(text[first_index+1:second_index], text_type))

            if second_index == len(text) - 1:
                done = True
                continue

            text = text[second_index+1:]
    return new_nodes
