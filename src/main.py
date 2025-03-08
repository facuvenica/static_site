from pathlib import Path
import sys

from copy_dir import recreate_folder, generate_pages_recursively

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    recreate_folder(Path('docs'), Path('static'))
    generate_pages_recursively(Path('content'),
                  Path('template.html'),
                  Path('docs'),
                  basepath)

main()