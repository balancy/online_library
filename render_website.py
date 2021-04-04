import json

from jinja2 import Template
from livereload import Server


def read_library_info():
    """Read library info from json file.

    :return: list of all books from json file
    """

    with open("library.json", "r", encoding="utf-8") as file:
        library = json.load(file)

    return library


def rebuild():
    """Rebuild index.html every time template.html is changed."""

    template = Template(open("template.html").read())

    rendered_page = template.render(
        library=read_library_info(),
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    rebuild()

    server = Server()
    server.watch('template.html', rebuild)

    server.serve(root='.')
