from pathlib import Path

from copy_dir import recreate_folder, generate_pages_recursively

def main():
    recreate_folder(Path('public'), Path('static'))
    generate_pages_recursively(Path('content'),
                  Path('template.html'),
                  Path('public'))

main()