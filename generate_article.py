
import os
import datetime
import requests
import json

API_KEY = os.getenv("OPENAI_API_KEY")   # your DeepSeek key (sk-...)
API_URL = "https://api.deepseek.com/chat/completions"


def ask_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_title():
    prompt = (
        "Generate a short, catchy, SEO-optimized article title about car mods. "
        "Keep it between 6–12 words."
    )
    return ask_deepseek(prompt).strip()


def generate_article(title):
    prompt = (
        f"Write a 600-word SEO-optimized article about: {title}. "
        "Include intro, 3 sections, and a conclusion."
    )
    return ask_deepseek(prompt).strip()


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
