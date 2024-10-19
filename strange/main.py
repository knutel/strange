import markdown
import jinja2 as j2
import pathlib
import datetime
from collections import namedtuple
import shutil
import click
from strange.serve import watch_and_serve


Post = namedtuple("Post", "date, title, draft, link")

def process(out_folder, include_drafts=True):
    content_folder = pathlib.Path("content")
    theme_folder = pathlib.Path("theme")
    out_folder = pathlib.Path(out_folder)
    env = j2.Environment(
        loader=j2.FileSystemLoader("templates")) 
    input_paths = content_folder.glob("*.md")
    posts = []
    header = env.get_template("header_template.html").render()

    for input_path in input_paths:
        output_filename = input_path.with_suffix(".html").name
        md = markdown.Markdown(extensions=["meta", "fenced_code", "attr_list", "codehilite"])
        html = md.convert(input_path.read_text())
        post = Post(date=datetime.date.fromisoformat(md.Meta["date"][0]), title=md.Meta["title"][0], draft="draft" in md.Meta, link=output_filename)
        if include_drafts or not post.draft:
            if input_path.name == "about.md":
                template = env.get_template("about_template.html")
            else:
                posts.append(post)
                template = env.get_template("post_template.html")
            rendered = template.render(header=header, post=post, body=html)
            output_path = out_folder / output_filename
            output_path.write_text(rendered)

    posts.sort(key=lambda p: p.date)
    output_filename = out_folder / "index.html"
    posts_template = env.get_template("posts_template.html")
    rendered = posts_template.render(header=header, posts = posts)
    output_filename.write_text(rendered)

    input_paths = theme_folder.glob("*")
    for input_path in input_paths:
        output_path = out_folder / input_path.name
        shutil.copy(input_path, output_path)



@click.command()
@click.option("-s", "--serve", is_flag=True)
@click.option("-p", "--port", default=8000)
@click.option("--publish", is_flag=True, default=False)
def cli(serve, port, publish):
    if publish:
        process("publish", include_drafts=False)
    elif serve:
        watch_and_serve(process, "output", port)
    else:
        process("output")


if __name__ == "__main__":
    cli()

