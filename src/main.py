from textnode import TextNode, TextType
import shutil, os

def main():
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    copy_static()

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

main()