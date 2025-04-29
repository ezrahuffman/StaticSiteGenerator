import unittest
from utils import * 
from blocktype import BlockType

class TestBlockHeaders(unittest.TestCase):
    def test_block_type_heading(self):
        block = "### sometext"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_quote(self):
        block = ">sometext"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_type_ul(self):
        block = "- someitem\n- another item\n- and another"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_type_ol(self):
        block = "1. someitem\n2. another item\n3. and another"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_type_code(self):
        block = "```this is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_type_paragraph(self):
        block = "just some normal text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)