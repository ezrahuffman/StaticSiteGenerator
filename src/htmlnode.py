from typing import List, Dict

class HTMLNODE: 
    def __init__(self, tag:str = None, value:str = None, children: List = None, props:Dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children : List[HTMLNODE] = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        
        props_lst = list(map(lambda x: f"{x[0]}=\"{x[1]}\"", self.props.items()))
        return " " + " ".join(props_lst)
    
    def get_repr_string(self) -> str:
        print_lst = [self.tag, self.value, "children: "]
        if self.children != None:
            for child in self.children:
                print_lst.append(child.get_repr_string())
        print_lst.append("props:")
        for k, v in self.props.items():
            print_lst.append(f"{k}:{v}")
        return "\n".join(print_lst)

    def __repr__(self):
        return self.get_repr_string()
    



    
         

    