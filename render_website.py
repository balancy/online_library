import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def read_library_info():
    """Read library info from json file.

    :return: list of all books from json file
    """

    with open("library.json", "r", encoding="utf-8") as file:
        library = json.load(file)

    return library


def rebuild(env):
    """Rebuild index.html every time template.html is changed.

    :param env: environment
    """

    template = env.get_template("template.html")

    rendered_page = template.render(
        library=read_library_info(),
    )

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(
            enabled_extensions=('html',),
            default_for_string=True,
            default=True,
            )
    )

    rebuild(env)

    server = Server()
    server.watch('template.html', rebuild)

    server.serve(root='.')
