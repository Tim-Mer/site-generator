from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def markdown_to_blocks(md: str):
    blocks = [x.strip() for x in md.split("\n\n") if x]
    return blocks

def block_to_block_type(md):
    if md == "":
        raise Exception("Not allowed empty block")
    marker = md.split()[0]
    lines = md.split("\n")
    # Is paragraph unless other type found
    type = BlockType.PARAGRAPH
    # Checking for headings
    if re.match(r"^#{1,6}$", marker):
        type =  BlockType.HEADING
        
    # Checking for code block
    #TODO: Implement ability to specify programming language?
    elif marker == "```":
        if md.split()[-1] ==  "```":
            type = BlockType.CODE
    
    # Checking for quote
    elif marker == ">":
        type = BlockType.QUOTE
        
    # Checking for unordered list
    elif marker == "-":
        if list(filter(lambda x: x.strip()[0] != "-", lines)) == []:
            type = BlockType.UNORDERED_LIST
    
    # Check for ordered list      
    elif marker == "1.":
        counter = 1
        for line in lines:
            if line == "":
                raise Exception("No gaps allowed in block object")
            if line.split()[0] == f"{counter}.":
                counter += 1
        if counter == len(lines)+1:
            type = BlockType.ORDERED_LIST
        
    return type