from enum import Enum


class TextType(Enum):
    NORMAL="normal"
    BOLD="bold"
    ITALIC="italic"
    CODE="cold"
    LINK="link"
    IMAGE="image"

class TextNode:
    def __init__(self, text, text_type:Enum, url):
        self.text = text
        self.text_type:Enum = text_type
        self.url = url
    
    def __eq__(self, value):
        self_attr = vars(self)
        value_attr = vars(value)

        for attr in self_attr:
            if attr not in value_attr:
                return False
            if self_attr[attr] != value_attr[attr]:
                return False
            
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    