import unittest

from funcs import *

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic node")
        
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.link.node"})
        
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "This is an image node"})

    def test_invalid_text_type(self):
        with self.assertRaises(ValueError) as cm:
            node = TextNode("Invalid node", "INVALID_TYPE")
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Unsupported TextType: INVALID_TYPE")

    def test_link_missing_props(self):
        with self.assertRaises(ValueError) as cm:
            node = TextNode("This is a link node", TextType.LINK)
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "LINK nodes must have a valid href property")

    def test_image_missing_props(self):
        with self.assertRaises(ValueError) as cm:
            node = TextNode("This is an image node", TextType.IMAGE)
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "IMAGE nodes must have a valid src property")

    def test_empty_value(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_props_in_non_link_or_image(self):
        node = TextNode("This is a bold node", TextType.BOLD, "extra_props")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertIsNone(html_node.props)

    def test_none_value(self):
        with self.assertRaises(ValueError) as cm:
            node = TextNode(None, TextType.TEXT)
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "TextNode value cannot be None")

    def test_image_with_alt_text(self):
        node = TextNode("Custom alt text", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "Custom alt text"})

    def test_link_with_additional_props(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.node")
        html_node = text_node_to_html_node(node)
        html_node.props["target"] = "_blank"
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.link.node", "target": "_blank"})

    def test_unsupported_props(self):
        node = TextNode("This is a text node", TextType.TEXT, "unsupported_props")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)
    
    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("Hello **World** Again", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "World")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " Again")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        
    def test_split_nodes_delimiter_multiple(self):
        nodes = [TextNode("Hello **World** Again and Hello **World** Again", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "World")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " Again and Hello ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "World")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " Again")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("First`Node`Test", TextType.TEXT),
            TextNode("Second_Node_Test", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].text, "First")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Node")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "Test")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "Second")
        self.assertEqual(result[3].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, "Node")
        self.assertEqual(result[4].text_type, TextType.ITALIC)
        self.assertEqual(result[5].text, "Test")
        self.assertEqual(result[5].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_missing_second_delimiter(self):
        nodes = [TextNode("Hello**World", TextType.TEXT)]
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(str(cm.exception), "Second delimeter not found (Invalid Markdown syntax)")

    def test_split_nodes_delimiter_no_delimiters(self):
        nodes = [TextNode("NoDelimitersHere", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "NoDelimitersHere")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty_text(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty_nodes_list(self):
        nodes = []
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 0)

    def test_split_nodes_delimiter_nested_delimiters(self):
        nodes = [TextNode("Nested **bold **inside** text** example", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Nested ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold ")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "inside")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, " text")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " example")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple_delimiters_in_single_node(self):
        nodes = [TextNode("Multiple **bold** and **italic** delimiters", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Multiple ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " delimiters")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_single_character_delimiter(self):
        nodes = [TextNode("Single_Character_Delimiter", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Single")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Character")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, "Delimiter")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        
    def test_extract_markdown_images_basic(self):
        text = "Here is an image ![alt text](image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("alt text", "image.jpg"))

    def test_extract_markdown_images_multiple(self):
        text = "![image1](img1.jpg) and ![image2](img2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("image1", "img1.jpg"))
        self.assertEqual(result[1], ("image2", "img2.png"))

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 0)

    def test_extract_markdown_images_invalid_syntax(self):
        text = "![alt text(image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 0)

    def test_extract_markdown_links_basic(self):
        text = "Here is a [link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("link", "https://example.com"))

    def test_extract_markdown_links_multiple(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("Google", "https://google.com"))
        self.assertEqual(result[1], ("GitHub", "https://github.com"))

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 0)

    def test_extract_markdown_links_exclude_images(self):
        text = "Here is a [link](https://example.com) and an image ![alt text](image.jpg)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("link", "https://example.com"))

    def test_extract_markdown_links_invalid_syntax(self):
        text = "[link(https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 0)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        
    def test_split_images_no_images(self):
        node = TextNode(
            "This is text without any images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text without any images.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_invalid_syntax(self):
        node = TextNode(
            "This is text with an invalid ![image](https://example.com and another ![image](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with an invalid ![image](https://example.com and another ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://example2.com")],
            new_nodes,
        )

    def test_split_images_multiple_images(self):
        node = TextNode(
            "Here is an image ![first](https://example.com/first.jpg) and another ![second](https://example.com/second.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
            ],
            new_nodes,
        )
    
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    
    def test_split_link_no_links(self):
        node = TextNode(
            "This is text without any links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text without any links.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_invalid_syntax(self):
        node = TextNode(
            "This is text with an invalid [link](https://example.com and another [link](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with an invalid [link](https://example.com and another ", TextType.TEXT), TextNode("link", TextType.LINK, "https://example2.com")],
            new_nodes,
        )
    
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], nodes)
    
    def test_text_to_textnode_only_text(self):
        text = "This is plain text with no formatting."
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is plain text with no formatting.", TextType.TEXT),
        ], nodes)

    def test_text_to_textnode_only_bold(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ], nodes)

    def test_text_to_textnode_only_italic(self):
        text = "This is _italic_ text."
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ], nodes)

    def test_text_to_textnode_only_code(self):
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ], nodes)

    def test_text_to_textnode_combined_formatting(self):
        text = "This is **bold**, _italic_, and `code` text."
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ], nodes)

    def test_text_to_textnode_with_images_and_links(self):
        text = "Here is an ![image](https://example.com/image.jpg) and a [link](https://example.com)."
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("Here is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ], nodes)

    #def test_text_to_textnode_nested_formatting(self):
    #    text = "This is **bold and _italic_** text."
    #    nodes = text_to_textnodes(text)
    #    self.assertEqual([
    #        TextNode("This is ", TextType.TEXT),
    #        TextNode("bold and ", TextType.BOLD),
    #        TextNode("italic", TextType.ITALIC),
    #        TextNode(" text.", TextType.TEXT),
    #    ], nodes)

    def test_text_to_textnode_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual([], nodes)
    
if __name__ == "__main__":
    unittest.main()