from textnode import *
from htmlnode import *
import re

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            if text_node.text == None:
                raise ValueError('TextNode value cannot be None')
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            if text_node.url == None:
                raise ValueError('LINK nodes must have a valid href property')
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url == None:
                raise ValueError('IMAGE nodes must have a valid src property')
            return LeafNode('img', "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError('Unsupported TextType: INVALID_TYPE')


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    len_delimiter = len(delimiter)
    pos1 = 0
    pos2 = 0
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            pos1 = node.text.find(delimiter)
            if not pos1 == -1:
                pos2 = node.text[pos1+len(delimiter):].find(delimiter)
                if pos2 == -1:
                    raise ValueError('Second delimeter not found (Invalid Markdown syntax)')
                pos2 = pos1 + node.text[pos1+len(delimiter):].find(delimiter) + len_delimiter
                new_nodes.append(TextNode(node.text[:pos1],node.text_type))
                new_nodes.append(TextNode(node.text[pos1+len_delimiter:pos2], text_type))
                new_nodes.extend(split_nodes_delimiter([TextNode(node.text[pos2+len_delimiter:], node.text_type)], delimiter, text_type))
            else:
                new_nodes.append(node)      
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if matches == []:
                new_nodes.append(node)
            else:
                image_alt, image_link = matches[0]
                sections = node.text.split(f"![{image_alt}]({image_link})", 1)
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if not sections[1] == "":
                    new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if matches == []:
                new_nodes.append(node)
            else:
                link_alt, link = matches[0]
                sections = node.text.split(f"[{link_alt}]({link})", 1)
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link))
                if not sections[1] == "":
                    new_nodes.extend(split_nodes_link([TextNode(sections[1], TextType.TEXT)]))
    return new_nodes



def text_to_textnodes(text: str):
    bold_delimeter = "**"
    italic_delimeter = "_"
    code_delimeter = "`"
    nodes = []
# text
    if text == "":
        return nodes
    nodes = [TextNode(text, TextType.TEXT)]
# bold
    nodes = split_nodes_delimiter(nodes, bold_delimeter, TextType.BOLD)
# italic
    nodes = split_nodes_delimiter(nodes, italic_delimeter, TextType.ITALIC)
# code
    nodes = split_nodes_delimiter(nodes, code_delimeter, TextType.CODE)
# image
    nodes = split_nodes_image(nodes)
# link
    nodes = split_nodes_link(nodes)   
    
    return nodes