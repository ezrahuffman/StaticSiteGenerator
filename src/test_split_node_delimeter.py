import unittest
from textnode import *
from utils import split_nodes_delimiter

class TestSplitNodeDelimeter(unittest.TestCase):
    def test_text_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_italics(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_italics_and_bold(self):
        node = TextNode("This is **text** with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)