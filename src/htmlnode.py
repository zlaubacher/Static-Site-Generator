class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        string = ""
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        html = f"<{self.tag}"
        if self.props:
            for prop_name, prop_value in self.props.items():
                html += f' {prop_name}="{prop_value}"'
        html += f">{self.value}</{self.tag}>"
        return html

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        errors = []

        if not self.tag:
            errors.append("ParentNode must have a tag")
        if not self.children:
            errors.append("ParentNode must have children")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        html = f"<{self.tag}>"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html