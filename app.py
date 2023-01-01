import frontmatter
import functools
import http.server
import markdown
import os
import tomli
import socketserver

from jinja2 import Template
from pathlib import Path


def load_config(file: str) -> dict:
    """
    Load the config file `pykyll.toml
    Return the config as a dict
    """
    config = {}
    with open(file, mode="rb") as f:
        config_file = tomli.load(f)
    config["site_name"] = Path(config_file["pages"]["site_name"])
    config["post_path"] = Path(config_file["pages"]["pages_path"])
    config["output_path"] = config_file["outputs"]["pytes_path"]
    config["page_template"] = config_file["templates"]["post_template"]
    config["feed_template"] = config_file["templates"]["feed_template"]
    config["author_name"] = config_file["author"]["name"]
    config["author_blog_link"] = config_file["author"]["blog_link"]
    return config


def load_feed(config: dict, posts: list):
    """
    open the feed templates
    for each post in the list of posts,
    write parse the variables into the template
    """

    with open(config["feed_template"]) as f:
        template = Template(f.read())

    feed_html = template.render(
        site_name=config["site_name"],
        posts=posts,
    )
    with open(Path(config["output_path"]) / "index.html", "w") as f:
        f.write(feed_html)


def load_pages(config: dict) -> list:
    """
    Get all the posts for the given config
    Return a list of posts
    """
    post_path = config["post_path"]
    output_path = config["output_path"]
    post_files = os.listdir(post_path)
    posts = []
    for file in post_files:
        with open(Path(post_path) / file, "r") as f:
            content = f.read()
            post = frontmatter.loads(content)
            html_content = markdown.markdown(
                post.content,
                extensions=[
                    "fenced_code",
                ],
            )
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            default_title = file.split(".")[0]
            post["title"] = default_title
            posts.append(post)
            render_templates(post, default_title, html_content, config)
    return posts


def render_templates(
    post: frontmatter.Post, title: str, html_content: str, config: dict
):
    """
    Create a html page given the post, html contene, title with config
    """
    default_file = str(post.get("title", title)) + ".html"

    with open(config["page_template"]) as f:
        template = Template(f.read())

    post_html = template.render(
        title=title,
        author=config["author_name"],
        user_blog=config["author_blog_link"],
        content=html_content,
    )
    with open(Path(config["output_path"]) / default_file, "w") as f:
        f.write(post_html)


def start_server(path: str):
    """
    Run the localserver with the path as pyites
    storing all the static pages for the site.
    """
    PORT = 8000
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=path)
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt as _:
            httpd.server_close()


def main():
    """
    load configuration
    load and parse posts from the config path
    create the feedpage
    create individual pages for posts
    start the server
    """
    config = load_config("pykyll.toml")
    posts = load_pages(config)
    load_feed(config, posts)
    start_server(config["output_path"])

main()
