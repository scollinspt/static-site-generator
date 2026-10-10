from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        heading_level = len(block) - len(block.lstrip("#"))
        if 1 <= heading_level <= 6 and block[heading_level : heading_level + 1] == " ":
            return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{index}. ") for index, line in enumerate(lines, 1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(_heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(_code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(_quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(_list_to_html_node(block, "ul", 2))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(_ordered_list_to_html_node(block))
        else:
            children.append(_paragraph_to_html_node(block))
    return ParentNode("div", children)


def text_to_children(text: str):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def _heading_to_html_node(block: str) -> ParentNode:
    heading_level = len(block) - len(block.lstrip("#"))
    return ParentNode(f"h{heading_level}", text_to_children(block[heading_level + 1 :]))


def _code_to_html_node(block: str) -> ParentNode:
    code = block[4:-3]
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code)])])


def _quote_to_html_node(block: str) -> ParentNode:
    text = " ".join(line[1:].strip() for line in block.split("\n"))
    return ParentNode("blockquote", text_to_children(text))


def _list_to_html_node(block: str, tag: str, marker_length: int) -> ParentNode:
    items = [
        ParentNode("li", text_to_children(line[marker_length:]))
        for line in block.split("\n")
    ]
    return ParentNode(tag, items)


def _ordered_list_to_html_node(block: str) -> ParentNode:
    items = [
        ParentNode("li", text_to_children(line.split(". ", 1)[1]))
        for line in block.split("\n")
    ]
    return ParentNode("ol", items)


def _paragraph_to_html_node(block: str) -> ParentNode:
    return ParentNode("p", text_to_children(" ".join(block.split("\n"))))