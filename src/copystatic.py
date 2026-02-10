import os
import shutil
from markdown_to_html import extract_title, markdown_to_html_node


def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    _copy_recursive(src, dst)


def _copy_recursive(src, dst):
    items = os.listdir(src)
    for name in items:
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file {src_path} -> {dst_path}")
        else:
            os.mkdir(dst_path)
            _copy_recursive(src_path, dst_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w') as f:
        print(template, file=f)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    items = os.listdir(dir_path_content)
    for item in items:
        full_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_path) and item.endswith(".md"):
            with open(full_path) as f:
                md = f.read()
            with open(template_path) as f:
                template = f.read()
            content = markdown_to_html_node(md).to_html()
            title = extract_title(md)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", content)
            os.makedirs(dest_dir_path, exist_ok=True)
            end_path = os.path.join(dest_dir_path, item)
            end_path = end_path.replace(".md", ".html")
            with open(end_path, 'w') as f:
                print(template, file=f)
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, item))


