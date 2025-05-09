from textnode import *
from htmlnode import *
from funcs import *
from blocks import *
from md_to_html import *#
from generate import *
import sys
import os

def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    content_path = os.path.join("content")
    public_path = os.path.join("docs")
    static_path = os.path.join("static")

    clean_public(public_path)
    copy_static(static_path, public_path)
    
    generate_pages_recursive(content_path, "src/template.html", public_path, basepath)
    
main()