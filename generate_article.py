import os
import datetime
import requests

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY", "free")  # no real key needed

def ask_deepseek(prompt, system=""):
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 800,
    }

    r = requests.post(DEEPSEEK_URL, headers=headers, json=data)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def generate_title():
    system = (
        "You generate short, catchy, SEO-optimized titles for car modification articles. "
        "Keep them between 6–12 words."
    )
    return ask_deepseek("Create a new article title.", system).strip()


def generate_article(title):
    system = (
        "Write detailed but readable SEO car modification articles. "
        "Include an intro paragraph, 3 section headers, and a short conclusion."
    )
    prompt = f"Write a 600-word SEO-optimized article about: {title}"
    return ask_deepseek(prompt, system).strip()


def insert_into_index(html_block):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    updated = html.replace(
        "<!-- AUTO_INSERT_ARTICLE_HERE -->",
        html_block + "\n<!-- AUTO_INSERT_ARTICLE_HERE -->"
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated)


def main():
    title = generate_title()
    content = generate_article(title)
    date = datetime.date.today().strftime("%b %d, %Y")

    html_block = (
        f"<article>\n"
        f"  <h3>{title}</h3>\n"
        f"  <p><em>{date}</em></p>\n"
        f"  <p>{content}</p>\n"
        f"</article>"
    )

    insert_into_index(html_block)


if __name__ == "__main__":
    main()
