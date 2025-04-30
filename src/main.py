from textnode import *
import os
import shutil
from utils import markdown_to_html_node, extract_title

def main():
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template = "template.html"
    remove_dir(public_dir)
    copy_from_directory(static_dir, public_dir)
    generate_pages_recursive(content_dir, template, public_dir)

def copy_from_directory(from_dir, to_dir):
    if not os.path.exists(from_dir):
        raise Exception("From directory is not valid")
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    
    from_dir_contents = os.listdir(from_dir)
    for content in from_dir_contents:
        full_to_path =  os.path.join(to_dir, content)
        full_from_path = os.path.join(from_dir, content)
        if os.path.isfile(full_from_path):
            shutil.copy(full_from_path, full_to_path)
            print(f"copy file from {full_from_path} to {full_to_path}")
        else:
            os.mkdir(full_to_path)
            copy_from_directory(full_from_path, full_to_path)

def remove_dir(dir):
    if not os.path.exists(dir):
        print(f"directory {dir} doesn't exist, do nothing")
        return
    print(f"remove entire directory: {dir}")
    shutil.rmtree(dir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = read_file(from_path)
    template_content = read_file(template_path)
    generated_html = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    #print(template_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", generated_html)
    
    # wrote_file = False
    # while not wrote_file:
    try:
        with open(dest_path, 'w') as f:
            f.write(template_content)
    except Exception as e:
        raise e
    

def read_file(path):
    try:
        with open(path, 'r') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        print(f"file not found at {path}")
        return None
    except Exception as e:
        raise e
            
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    from_dir_contents = os.listdir(dir_path_content)
    for content in from_dir_contents:
        full_content_path = os.path.join(dir_path_content, content)
        full_dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(full_content_path):
            split = os.path.splitext(full_content_path)
            if split[1] == '.md':
                generate_page(full_content_path, template_path, full_dest_path[:-3] + ".html")
            else:
                shutil.copy(full_content_path, full_dest_path)
        else:
            os.mkdir(full_dest_path)
            generate_pages_recursive(full_content_path, template_path, full_dest_path)
        


if __name__ == "__main__":
    main()