import os
import re
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ARTICLES_DIR = "articles"

os.makedirs(ARTICLES_DIR, exist_ok=True)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def generate_title():
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write engaging blog titles about vehicles, cars, trucks, and automotive culture."
            },
            {
                "role": "user",
                "content": "Generate a short, catchy vehicle-related blog article title."
            }
        ]
    )
    return resp.choices[0].message.content.strip()


def generate_article(title):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write informative, enthusiastic blog articles about vehicles."
            },
            {
                "role": "user",
                "content": f"Write a detailed blog article about vehicles titled: '{title}'."
            }
        ]
    )
    return resp.choices[0].message.content.strip()


def main():
    title = generate_title()
    article = generate_article(title)

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{date_str}-{slug}.html"
    filepath = os.path.join(ARTICLES_DIR, filename)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>

<header>
    <h1>{title}</h1>
    <p><em>Published on {date_str}</em></p>
    <nav>
        <a href="../index.html">Home</a> |
        <a href="../gallery.html">Gallery</a> |
        <a href="../articles/">Articles</a>
    </nav>
</header>

<main>
    <article>
        <p>{article.replace('\n\n', '</p><p>')}</p>
    </article>
</main>

</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Article created: {filepath}")


if __name__ == "__main__":
    main()
