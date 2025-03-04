from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag : str = None, value : str = None, children : list = None, props : dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items()) if self.props else "" 

    def __repr__(self):
        return f"HTMLNode(tag= '{self.tag}', value= '{self.value}', children= {self.children}, props= {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        html = f"<{self.tag}"

        if self.props:
            for key, value in self.props.items():
                html += f' {key}="{value}"'

        html += f">{self.value}</{self.tag}>"
        return html

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing Tag")
        
        if len(self.children) == 0:
            raise ValueError("Children are required for ParentNode")

        open_tag = f"<{self.tag}"
        closing_tag = f"</{self.tag}>"

        if self.props:
            for key, value in self.props.items():
                open_tag += f' {key}="{value}"'
        open_tag += ">"

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return open_tag + children_html + closing_tag


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
        
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})