import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_title():
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate a short interesting article title."},
            {"role": "user", "content": "Give me an article title."}
        ]
    )
    return resp.choices[0].message.content.strip()

def generate_article(title):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Write a detailed blog article."},
            {"role": "user", "content": f"Write an article titled: {title}"}
        ]
    )
    return resp.choices[0].message.content.strip()

def main():
    title = generate_title()
    article = generate_article(title)

    html = f"""
<html>
<head><title>{title}</title></head>
<body>
<h1>{title}</h1>
<p>{article}</p>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
