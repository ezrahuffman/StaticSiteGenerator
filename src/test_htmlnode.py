import unittest

from htmlnode import HTMLNODE

class TestHTMLNode(unittest.TestCase):
    def test_html_prop_to_html(self):
        html_node = HTMLNODE("a", value="link", props={"href":"https://google.com"})
        generated_html = html_node.props_to_html()
        expected_html = " href=\"https://google.com\""
        self.assertEqual(generated_html, expected_html)

    def test_html_multiple_prop_to_html(self):
        html_node = HTMLNODE("a", value="link", props={"href":"https://google.com", "target":"_blank"})
        generated_html = html_node.props_to_html()
        expected_html = " href=\"https://google.com\" target=\"_blank\""
        self.assertEqual(generated_html, expected_html)

    def test_html_multiple_prop_to_html_fail(self):
        html_node = HTMLNODE("a", value="link", props={"href":"https://google.com", "target":"_blank"})
        generated_html = html_node.props_to_html()
        expected_html = " href=\"https://google.com\" target=\"\""
        self.assertNotEqual(generated_html, expected_html)

    def test_html_get_repr_string(self):
        node =  HTMLNODE("a", value="link", props={"href":"https://google.com", "target":"_blank"})
        s = node.get_repr_string()
        self.assertIsInstance(s, str)

    def test_null_html_node(self):
        node = HTMLNODE()
        self.assertIsNotNone(node)

    def test_to_html_not_implemented(self):
        node = HTMLNODE()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    
