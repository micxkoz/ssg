import shutil, os
import re
from blockmarkdown import markdown_to_html_node

def main():
    copy_static()
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_static(src_folder="static", dst_folder="public"):
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)
    os.mkdir(dst_folder)

    for item in os.listdir(src_folder):
        full_item = os.path.join(src_folder, item)
        if os.path.isfile(full_item):
            shutil.copy(full_item, dst_folder)
        else:
            copy_static(full_item, os.path.join(dst_folder, item))

def extract_title(markdown):
    header = re.search("\n?(?<!#)#{1} (.+)", markdown)
    if header:
        return header.group(1)
    raise ValueError("Missing header with title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as fp:
        markdown_file = fp.read()
    with open(template_path) as tp:
        template_file = tp.read()
    html_string = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_string)

    dir_part = os.path.dirname(dest_path)
    if dir_part != "":
        os.makedirs(dir_part, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(template_file)

if __name__ == "__main__":
    main()