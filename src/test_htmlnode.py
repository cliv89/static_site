import unittest
from htmlnode import *
from textnode import *


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node = HTMLNode(props={"id": "test-node", "class" : "container"})
        self.assertEqual(node.props_to_html(), ' id="test-node" class="container"')
        
    def test_empty_initialization(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
        
    def test_custom_initialization(self):
        node = HTMLNode(tag="div", value="Hello", props={"style": "color: red;"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {"style": "color: red;"})
        
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode(tag="a", value="Click me!", props= {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_one = LeafNode("b", "Bold")
        child_two = LeafNode(None, "and normal text")
        parent_node = ParentNode("p", [child_one, child_two])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold</b>and normal text</p>")
            
    def test_to_html_with_no_childen(self):
        parent_node = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
            
        self.assertEqual(str(context.exception), "Children are required for ParentNode")
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props["href"], "https://example.com")
        
    def test_image(self):
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text for image")
