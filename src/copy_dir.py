from shutil import copytree
from pathlib import Path

from functions import markdown_to_title, markdown_to_html_node


def recreate_folder(dest, src=None):
    if dest.is_file():
        return dest.unlink()

    if dest.exists():
        for file in dest.iterdir():
            recreate_folder(file)

        dest.rmdir()
        if src:
            copytree(src, dest)


def create_folder(dest):
    if dest.exists():
        return

    if not dest.parent.exists():
        create_folder(dest.parent)
    else:
        print('Creating', dest)
        dest.mkdir()


def generate_pages_recursively(source, template, dest, basepath):

    for file in source.iterdir():

        dir, parent, dest_dir = str(file), str(file.parent), str(dest)
        new_path = Path(dir.replace(parent, dest_dir))

        if file.is_dir():
            if not new_path.exists():
                create_folder(new_path)
            generate_pages_recursively(file, template, new_path, basepath)

        if not file.is_file():
            continue

        if '.md' in dir:
            dir = str(new_path)
            new_path = Path(dir.replace('.md', '.html'))

            print(f"Generating page from {file} to {new_path} using {template}")

            content = file.read_text()
            temp = template.read_text()

            title = markdown_to_title(content)
            html = markdown_to_html_node(content).to_html()

            # Set the title
            temp = temp.replace("{{ Title }}", title)
            # Set the html
            temp = temp.replace("{{ Content }}", html)
            # Fix local urls
            temp = temp.replace('href="/', f'href="{basepath}')
            temp = temp.replace('src="/', f'src="{basepath}')

            new_path.write_text(temp)
            print(f"{new_path} successfully created")
        else:
            temp = file.read_bytes()
            new_path.write_bytes()