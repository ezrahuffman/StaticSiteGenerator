from htmlnode import HTMLNODE

class LeafNode(HTMLNODE):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError
        if self.tag == None: 
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"