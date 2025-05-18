from md_parser import *
from textnode import *
from htmlnode import *

#Test to observe my most recent assignment after a long hiatus
print("Running Test.....")
result = text_to_textnodes("This is **bold** and _italic_ text")
print(result)
#End test

#test to observe markdown_to_blocks
print("Running Test......")
md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
result = markdown_to_blocks(md)
print(result)
#End test