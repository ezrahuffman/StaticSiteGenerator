from textnode import *
from leafnode import LeafNode
from typing import List
import re
from blocktype import BlockType
from htmlnode import HTMLNODE
from parentnode import ParentNode

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
    
def markdown_to_blocks(markdown:str)->List[str]:
    blocks = list(map(lambda x: x.strip(), markdown.split("\n\n")))
    blocks = list(filter(lambda x: x != "",blocks))
    return blocks

def is_list(block:str, is_ordered:bool)->bool:
    lines = block.split('\n')
    if not is_ordered:
        for line in lines:
            if line[:2] != "- ":
                return False
        return True
    # If ordered
    x = 1
    for line in lines:
        if line[:3] != f"{x}. ":
            return False
        x += 1
    return True

# header format is 1-6 #s followed by a space
def is_heading(s:str)->bool:
    l = min(len(s),  7)
    s = s[:l]
    i = 0
    while i < len(s) and s[i] == "#":
        i += 1 # nodes = text_to_textnodes(text)
    # ret_lst = []
    # for node in nodes:
    #     ret_lst.append(text_node_to_html_node(node))
    if i == len(s):
        return False
    else:
        return s[i] == " "

def block_to_block_type(block:str)->BlockType:
    if len(block) == 0:
        return BlockType.PARAGRAPH
    if is_heading(block):
        return BlockType.HEADING
    #TODO: maybe code blocks should have to be recognized by ```\n instead of just ```
    if len(block) >= 6 and  block[:3] == "```"  and block[-3:] == "```":
        return BlockType.CODE
    if block[0] == ">":
        return BlockType.QUOTE
    if is_list(block, False):
        return BlockType.UNORDERED_LIST
    if is_list(block, True):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text:str, block_type:BlockType)->List[HTMLNODE]:
    if block_type == BlockType.ORDERED_LIST or block_type == BlockType.UNORDERED_LIST:
        ret_list:List[HTMLNODE] = []
        lines = text.split('\n')
        for line in lines:
            line = line[2:]
            nodes = text_to_textnodes(line)
            children = []
            for node in nodes:
                children.append(text_node_to_html_node(node))
            list_line = ParentNode("li", children)
            ret_list.append(list_line)
        return ret_list
    if block_type == BlockType.HEADING:
        i = 0
        while text[i] == "#":
            i += 1
        text = text[i+1:]
        return text_to_children_helper(text)
    if block_type == BlockType.QUOTE:
        lines = text.split('\n')
        for i in range(len(lines)):
            if lines[i][0] == ">":
                lines[i] = lines[i][1:]
        text = "\n".join(lines)
        return text_to_children_helper(text)
    else:
        return text_to_children_helper(text)
    

def text_to_children_helper(text):
    ret_list:List[HTMLNODE] = []
    text = text.replace("\n", " ")
    nodes = text_to_textnodes(text)
    for node in nodes:
        ret_list.append(text_node_to_html_node(node))
    return ret_list

def block_type_to_tag(block, block_type):
    translation_map = {
        BlockType.PARAGRAPH:"p",
        BlockType.ORDERED_LIST:"ol",
        BlockType.UNORDERED_LIST:"ul",
        BlockType.QUOTE:"blockquote",
    }
    if block_type in translation_map:
        return translation_map[block_type]
    match block_type:
        case BlockType.HEADING:
            i = 1
            while block[i] == "#":
                i += 1
            return f"h{i}"
        case BlockType.CODE: #not sure if this is neccessary
            return "pre"
        case _:
            raise Exception("Unrecognized block type")
        
    

def markdown_to_html_node(markdown:str)->HTMLNODE:
    blocks:List[str] = markdown_to_blocks(markdown)
    first_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type != BlockType.CODE:
            html_children = text_to_children(block, block_type)
            block_parent = ParentNode(block_type_to_tag(block, block_type), html_children)
            first_children.append(block_parent)
        else:
            text = block[3:-3].strip()
            text_node = TextNode(text, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            block_parent = ParentNode(block_type_to_tag(block, block_type), [html_node])
            first_children.append(block_parent)
    return ParentNode("div", first_children)

def extract_title(markdown:str):
    lines = markdown.split('\n')
    for line in lines:
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("No Header line found (needs to be h1 i.e. start with '# ')")
    
        