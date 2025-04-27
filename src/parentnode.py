from htmlnode import HTMLNODE

class ParentNode(HTMLNODE):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode requires a tag")
        if self.children == None:
            raise ValueError("ParentNode requires children")
        ret_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            ret_str += child.to_html() 
        ret_str += f"</{self.tag}>"
        return ret_str