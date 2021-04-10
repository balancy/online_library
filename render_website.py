import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import sliced


def read_library_info():
    """Read library info from json file.

    :return: list of all books from json file
    """

    with open("library_.json", "r", encoding="utf-8") as file:
        library = json.load(file)

    for book in library:
        book["img_src"] = f"/{book['img_src']}"
        book["book_path"] = f"/{book['book_path']}"

    return list(sliced(library, 20))


def rebuild(template):
    """Rebuild index.html every time template.html is changed.

    :param template: template to follow
    """

    library_chunked = read_library_info()
    number_of_pages = len(library_chunked)

    for chunk_number, library_piece in enumerate(library_chunked, start=1):
        rendered_page = template.render(
            library=library_piece,
            current_page_number=chunk_number,
            number_of_pages=number_of_pages,
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

    os.makedirs("media/books/", exist_ok=True)
    os.makedirs("media/images/", exist_ok=True)

    template = env.get_template("template.html")
    rebuild(template)

    server = Server()
    server.watch("template.html", rebuild)

    server.serve(root='.', default_filename="pages/index1.html")
