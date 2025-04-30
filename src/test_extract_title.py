import unittest
from utils import *

class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        result = extract_title("# Hello")
        expected = "Hello"
        self.assertEqual(result, expected)
    
    def test_simple_title_fail(self):
        with self.assertRaises(Exception):
            result = extract_title("Hello")

    def test_multi_line(self):
        markdown = '''
Hello
# Title
something else

wow
'''
        result = extract_title(markdown)
        expected = "Title"
        self.assertEqual(result, expected)

    def test_simple_whitespace(self):
        result = extract_title("#      Hello\n")
        expected = "Hello"
        self.assertEqual(result, expected)