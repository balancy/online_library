import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import sliced


def read_library_info():
    """Read library info from json file.

    :return: list of all books from json file
    """

    with open("library.json", "r", encoding="utf-8") as file:
        library = json.load(file)

    return list(sliced(library, 20))


def rebuild(template):
    """Rebuild index.html every time template.html is changed.

    :param template: template to follow
    """

    library_chunked = read_library_info()

    for chunk_number, library_piece in enumerate(library_chunked):
        rendered_page = template.render(
            library=library_piece,
        )

        with open(f"pages/index{chunk_number}.html", "w", encoding="utf-8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(
            enabled_extensions=("html",),
            default_for_string=True,
            default=True,
            )
    )

    os.makedirs("pages/books/", exist_ok=True)
    os.makedirs("pages/images/", exist_ok=True)

    template = env.get_template("template.html")
    rebuild(template)

    server = Server()
    server.watch("template.html", rebuild)

    server.serve(root='pages', default_filename="index0.html")
