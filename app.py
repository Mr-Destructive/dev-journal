from datetime import datetime
import frontmatter
import markdown
import os 
from pathlib import Path

post_path = Path("pages/dev-journal")
output_path = os.path.abspath("pyites")

onlyfiles = os.listdir(post_path)
for file in onlyfiles:
    with open(Path(post_path) / file, "r") as f:
        content = f.read()
        post = frontmatter.loads(content)
        html_content = markdown.markdown(post.content, extensions=['fenced_code','codehilite'])
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        default_title = datetime.today().strftime('%Y-%m-%d')
        default_title = file.split(".")[0]
        title = str(post.get("title", default_title)) + ".html"
        with open(Path(output_path) / title, 'w') as f:
            f.write(html_content)
