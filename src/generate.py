import os
import shutil
from textnode import *
from htmlnode import *
from funcs import *
from blocks import *
from md_to_html import *#
from generate import *
from pathlib import Path

def clean_public(dir="./public"):
    logging(f"Removing {dir}")
    if os.path.isdir(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

def copy_static(input_dir="./static/", output_dir="./public/"):
    for item in os.listdir(input_dir):
        in_file = os.path.join(input_dir, item)
        out_file = os.path.join(output_dir, item)
        if os.path.isfile(in_file):
            logging(f"Copying {in_file} to {output_dir}")
            shutil.copy(in_file, output_dir)
        else:
            if not os.path.isdir(out_file):
                logging(f"Making directory {out_file}")
                os.mkdir(out_file)
            copy_static(in_file, out_file)

def logging(msg):
    print(f"LOG: {msg}")
    pass

def extract_title(md):
    if md == "":
        raise Exception("Empty .md file")
    title = ""
    for line in md.split("\n"):
        if line.strip().startswith('# '):
            title = line.replace("# ", "")
            break
    if title == "":
        raise Exception("No title found")
    return title

def generate_page(from_path, template_path, dest_path, basepath):
    logging(f"Generating page from {from_path} to {dest_path}, using template {template_path}")
    input_md = ""
    with open(from_path, "r") as file:
        input_md = file.read()
    
    template = ""
    with open(template_path, "r") as file:
        template = file.read()
    
    input_html = markdown_to_html_node(input_md).to_html()
    title = extract_title(input_md)
    
    output_html = template.replace("{{ Title }}", title).replace("{{ Content }}", input_html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    Path(os.path.dirname(dest_path)).mkdir(parents=True, exist_ok=True)
    with Path(dest_path).open("w") as file:
        file.write(output_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, item), basepath)
        else:
            generate_page(path, template_path, os.path.join(dest_dir_path, item.replace(".md", ".html")), basepath)
    
    