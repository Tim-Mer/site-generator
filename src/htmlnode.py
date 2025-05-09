class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        tmp = ""
        if self.props is None:
            return tmp
        for item in self.props:
            tmp = f'{tmp}{item}="{self.props[item]}" '
        return tmp[:-1]
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if not type(self.value) is str:
            raise ValueError("Leaf is missing value")
        if self.tag == None:
            return self.value
        tmp = f"<{self.tag}"
        if not self.props == None:
            tmp = tmp + " " + super().props_to_html()
        tmp = f"{tmp}>{self.value}</{self.tag}>"
        return tmp
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not type(self.tag) is str:
            raise ValueError("ParentNode is missing tag")
        if (not type(self.children) is list) or self.children == []:
            raise ValueError("ParentNode is missing children")
        tmp = f"<{self.tag}"
        if not self.props == None:
            tmp = tmp + " " + super().props_to_html()
        tmp = tmp + ">"        
        for child in self.children:
            tmp = tmp + child.to_html()
        tmp = f"{tmp}</{self.tag}>"
        return tmp
            
        