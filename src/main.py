import os
import shutil
import sys

from markdown_blocks import markdown_to_html_node


def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    _copy_directory(source, destination)


def _copy_directory(source, destination):
    for entry in os.listdir(source):
        source_path = os.path.join(source, entry)
        destination_path = os.path.join(destination, entry)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            os.mkdir(destination_path)
            _copy_directory(source_path, destination_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Markdown document must contain an h1 heading")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    destination_directory = os.path.dirname(dest_path)
    if destination_directory:
        os.makedirs(destination_directory, exist_ok=True)
    with open(dest_path, "w") as destination_file:
        destination_file.write(page)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath
):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(source_path):
            generate_pages_recursive(
                source_path,
                template_path,
                os.path.join(dest_dir_path, entry),
                basepath,
            )
        elif entry.endswith(".md"):
            destination_name = f"{os.path.splitext(entry)[0]}.html"
            generate_page(
                source_path,
                template_path,
                os.path.join(dest_dir_path, destination_name),
                basepath,
            )


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
