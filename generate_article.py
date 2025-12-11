
import os
import datetime
from openai import OpenAI

# Initialize client (correct new API)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------------------------------
# Generate a title
# --------------------------------------------------------
def generate_title():
    system_msg = (
        "You generate short, catchy, SEO-optimized titles for car modification articles. "
        "Keep them between 6–12 words."
    )

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",  # valid and cheap model
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": "Create a new article title."}
        ],
        max_tokens=32,
        temperature=0.7,
    )

    return resp.choices[0].message["content"].strip()

# --------------------------------------------------------
# Generate article body
# --------------------------------------------------------
def generate_article(title):
    system_msg = (
        "Write detailed but readable SEO car modification articles. "
        "Include an intro paragraph, 3 section headers, and a short conclusion."
    )

    prompt = f"Write a 600-word SEO-optimized article about: {title}"

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        max_tokens=900,
        temperature=0.7,
    )

    return resp.choices[0].message["content"].strip()

# --------------------------------------------------------
# Insert into index.html
# --------------------------------------------------------
def insert_into_index(html_block):
    # Read existing HTML
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Replace placeholder
    updated = html.replace(
        "<!-- AUTO_INSERT_ARTICLE_HERE -->",
        html_block + "\n<!-- AUTO_INSERT_ARTICLE_HERE -->"
    )

    # Save updated HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated)

# --------------------------------------------------------
# Main
# --------------------------------------------------------
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
