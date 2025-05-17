from md_parser import *
from textnode import *
from htmlnode import *

print("Running Test.....")
result = text_to_textnodes("This is **bold** and _italic_ text")
print(result)