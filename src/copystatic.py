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


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w') as f:
        print(template, file=f)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    items = os.listdir(dir_path_content)
    for item in items:
        full_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_path) and item.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(full_path, template_path, dest_path, basepath)
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, item), basepath)


