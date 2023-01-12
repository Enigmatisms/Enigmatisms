import feedparser
import pathlib
import re

rssUrl = "https://enigmatisms.github.io/atom.xml"
startMark = r"<!-- posts start -->"
endMark = r"<!-- posts end -->"
NUM = 6

def update_readme(start, end, repl):
    # Splicing complete regular expressions
    pattern = re.compile(
        r"(?<=(" + start + r")).*(?=(" + end + r"))",
        re.DOTALL,
    )
    # Get contents and rewrite README.md
    readme = pathlib.Path(__file__).parent.resolve() / "README.md"
    readme_contents = readme.open(encoding='utf-8').read()
    readme.open("w", encoding='utf-8').write(pattern.sub('\n' + repl + '\n', readme_contents))

def fetch_posts(url):
    blog = feedparser.parse(url)
    posts = blog['entries']
    markdown = "\n"
    main_post_num = 0
    
    for post in posts:
        if post.tags[0].term == 'snippet': continue
        markdown += f"※ {post.published[0:10]}《<a href=\"{post.link}\">{post.title}</a>》<br/>\n"
        main_post_num += 1
        if main_post_num >= NUM:
            break
    markdown += f"<br/><a href=\"{blog['feed']['link']}\">Read more..</a>\n"
    return markdown

if __name__ == "__main__":
    postsNew = fetch_posts(rssUrl)
    update_readme(startMark, endMark, postsNew)