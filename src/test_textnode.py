import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("this is a different text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("this is a text node", TextType.ITALIC)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_null_url(self):
        node = TextNode("this is a text node", TextType.ITALIC, None)
        self.assertIsNotNone(node)

    def test_not_eq_url(self):
        node = TextNode("this is a text node", TextType.BOLD, "http://google.com")
        node2 = TextNode("this is a text node", TextType.BOLD, "http://twitter.com")
        self.assertNotEqual(node, node2)