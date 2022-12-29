from datetime import datetime
import frontmatter
import markdown
import os 
from jinja2 import Template
from pathlib import Path

post_path = Path("pages/dev-journal")
output_path = os.path.abspath("pyites")

onlyfiles = os.listdir(post_path)
for file in onlyfiles:
    with open(Path(post_path) / file, "r") as f:
        content = f.read()
        post = frontmatter.loads(content)
        html_content = markdown.markdown(post.content, extensions=['fenced_code',])
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        default_title = datetime.today().strftime('%Y-%m-%d')
        default_title = file.split(".")[0]
        file_name = str(post.get("title", default_title)) + ".html"
        with open("templates/post_template.html") as f:
            template = Template(f.read())
        post_html = template.render(title=default_title, content=html_content)
        with open(Path(output_path) / file_name, 'w') as f:
            f.write(post_html)
