from htmlnode import *
from blocks import *
from funcs import *

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_htmlnode(block_type, block)
        block_nodes.append(node)
    return ParentNode("div", block_nodes)
        
def block_to_htmlnode(block_type: BlockType, block):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block.replace("\n", " ")))
        case BlockType.HEADING:
            return ParentNode(f"h{len(block) - len(block.lstrip('#'))}", text_to_children(block.lstrip('# ')))
        case BlockType.UNORDERED_LIST:
            return tag_list("ul", "li", block)
        case BlockType.ORDERED_LIST:
            return tag_list("ol", "li", block)
        case BlockType.QUOTE:
            if block.startswith('>'):
                block = block[1:]
                while block.startswith(' '):
                    block = block[1:]
            return ParentNode("blockquote", text_to_children(block))
        case BlockType.CODE:
            return ParentNode("pre", [text_node_to_html_node(TextNode(block.strip('```').lstrip("\n"), TextType.CODE))])
            
            
def tag_list(parent_tag, item_tag, items):
    # Needs to return an HTMLNode which has LeafNodes that are use item_tag
    html_list = []
    for item in items.split('\n'):
        list_item = ParentNode(item_tag, text_to_children(item.lstrip('- ').lstrip('0123456789. ')))
        html_list.append(list_item)
    return ParentNode(parent_tag, html_list)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_node = []
    for node in nodes:
        html_node.append(text_node_to_html_node(node))
    return html_node