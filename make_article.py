import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

# ============================================================
# PASTE YOUR GEMINI API KEY HERE
API_KEY = "AIzaSyB_9RC8fiyZWXf-hCv0DPztaMzGzwz-rI4"
# ============================================================

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://nbustos-dotcom.github.io/RootAccess"

CATEGORY_MAP = {
    "beginner": ("tag-beginner", "Beginner", "beginner"),
    "tutorial": ("tag-tutorial", "Tutorial", "tutorial"),
    "comparison": ("tag-comparison", "Comparison", "comparison"),
    "career": ("tag-career", "Career", "career"),
    "certification": ("tag-certification", "Certification", "certification"),
    "ctf": ("tag-ctf", "CTF", "ctf"),
    "lab": ("tag-lab", "Lab Setup", "lab"),
    "resources": ("tag-resources", "Resources", "resources"),
}

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["candidates"][0]["content"]["parts"][0]["text"]

def generate_article(topic):
    print(f"\n⚡ Generating article: {topic}")

    # Step 1 — get metadata
    meta_prompt = f"""
You are helping build a cybersecurity website called RootAccess targeted at beginners and students.
For the article topic: "{topic}"

Respond ONLY with a JSON object (no markdown, no backticks) with these exact keys:
- filename: a short kebab-case filename without .html (e.g. what-is-phishing)
- title: the full SEO article title including year 2026
- description: a meta description under 155 characters
- category: one of: beginner, tutorial, comparison, career, certification, ctf, lab, resources
- card_description: 1-2 sentence description for the homepage card (max 150 chars)
- read_time: estimated read time like "7 min read"
"""
    print("→ Getting metadata...")
    meta_raw = call_gemini(meta_prompt)
    meta_raw = re.sub(r'```json|```', '', meta_raw).strip()
    meta = json.loads(meta_raw)

    filename = meta["filename"] + ".html"
    title = meta["title"]
    description = meta["description"]
    category = meta["category"]
    card_description = meta["card_description"]
    read_time = meta["read_time"]
    cat_class, cat_label, cat_data = CATEGORY_MAP.get(category, ("tag-beginner", "Beginner", "beginner"))

    # Step 2 — generate article body
    body_prompt = f"""
Write a detailed, honest cybersecurity article for beginners titled: "{title}"

You are Nate Bustos, a CS student at Michigan Tech with a cybersecurity minor. You have real TryHackMe and CTF experience. Write in first person, conversational but informative. No fluff.

Return ONLY the inner HTML content that goes inside <div class="content-wrap"> — no outer tags, no markdown, no backticks.

Use these HTML elements:
- <p> for paragraphs
- <h2> for major sections
- <h3> for subsections  
- <ul> and <li> for lists
- <div class="callout"><p><strong>Label:</strong> text</p></div> for key takeaways
- <div class="warning"><p><strong>Reality check:</strong> text</p></div> for warnings
- <strong> for emphasis

End with a callout for next steps and this disclosure:
<div class="disclosure">
  <strong>Disclosure:</strong> Some links on this page may be affiliate links. I may earn a small commission if you sign up through them, at no extra cost to you. I only recommend tools I genuinely think are worth using.
</div>

Write at least 800 words of content.
"""
    print("→ Generating article content...")
    body_html = call_gemini(body_prompt)
    body_html = re.sub(r'```html|```', '', body_html).strip()

    # Step 3 — build full HTML file
    month_year = datetime.now().strftime("%B %Y")
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <link rel="canonical" href="{BASE_URL}/{filename}" />
  <title>{title} | RootAccess</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', sans-serif; background: #0a0e1a; color: #e0e0e0; line-height: 1.7; }}
    header {{ background: #0d1117; border-bottom: 1px solid #30363d; padding: 0 40px; height: 64px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
    .header-left {{ display: flex; align-items: center; gap: 12px; }}
    .header-left a {{ text-decoration: none; }}
    .header-left h1 {{ color: #58a6ff; font-size: 1.3rem; }}
    .header-left span {{ color: #8b949e; font-size: 0.8rem; border-left: 1px solid #30363d; padding-left: 12px; }}
    nav {{ display: flex; gap: 24px; }}
    nav a {{ color: #8b949e; text-decoration: none; font-size: 0.9rem; transition: color 0.2s; }}
    nav a:hover {{ color: #58a6ff; }}
    .article-hero {{ background: linear-gradient(135deg, #0d1117 0%, #161b22 60%, #0d1f3c 100%); padding: 60px 40px; border-bottom: 1px solid #30363d; text-align: center; }}
    .article-hero .back {{ color: #58a6ff; text-decoration: none; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 6px; margin-bottom: 20px; opacity: 0.8; }}
    .article-hero .back:hover {{ opacity: 1; }}
    .tag {{ display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px; }}
    .tag-beginner {{ background: rgba(35,134,54,0.15); color: #3fb950; }}
    .tag-tutorial {{ background: rgba(35,134,54,0.15); color: #3fb950; }}
    .tag-comparison {{ background: rgba(88,166,255,0.15); color: #58a6ff; }}
    .tag-career {{ background: rgba(210,153,34,0.15); color: #d2991a; }}
    .tag-certification {{ background: rgba(188,77,252,0.15); color: #bc4dfc; }}
    .tag-ctf {{ background: rgba(248,81,73,0.15); color: #f85149; }}
    .tag-lab {{ background: rgba(210,153,34,0.15); color: #d2991a; }}
    .tag-resources {{ background: rgba(88,166,255,0.15); color: #58a6ff; }}
    .article-hero h1 {{ font-size: 2.2rem; color: #ffffff; line-height: 1.3; max-width: 780px; margin: 0 auto 16px; text-align: center; }}
    .article-hero .meta {{ color: #8b949e; font-size: 0.88rem; display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }}
    .content-wrap {{ max-width: 780px; margin: 0 auto; padding: 60px 40px; }}
    .content-wrap h2 {{ color: #ffffff; font-size: 1.4rem; margin: 48px 0 16px; padding-bottom: 10px; border-bottom: 1px solid #30363d; }}
    .content-wrap h3 {{ color: #e0e0e0; font-size: 1.1rem; margin: 28px 0 12px; }}
    .content-wrap p {{ color: #c9d1d9; margin-bottom: 16px; font-size: 0.97rem; }}
    .content-wrap ul, .content-wrap ol {{ color: #c9d1d9; padding-left: 24px; margin-bottom: 16px; }}
    .content-wrap li {{ margin-bottom: 8px; font-size: 0.97rem; }}
    .content-wrap a {{ color: #58a6ff; text-decoration: none; }}
    .content-wrap a:hover {{ text-decoration: underline; }}
    .callout {{ background: rgba(88,166,255,0.08); border: 1px solid rgba(88,166,255,0.25); border-left: 4px solid #58a6ff; border-radius: 8px; padding: 20px 24px; margin: 28px 0; }}
    .callout p {{ margin: 0; color: #c9d1d9; }}
    .callout strong {{ color: #58a6ff; }}
    .warning {{ background: rgba(210,153,34,0.08); border: 1px solid rgba(210,153,34,0.25); border-left: 4px solid #d2991a; border-radius: 8px; padding: 20px 24px; margin: 28px 0; }}
    .warning p {{ margin: 0; color: #c9d1d9; }}
    .warning strong {{ color: #d2991a; }}
    .disclosure {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px 20px; margin-top: 48px; font-size: 0.82rem; color: #8b949e; }}
    footer {{ background: #0d1117; border-top: 1px solid #30363d; padding: 40px; text-align: center; color: #8b949e; font-size: 0.85rem; margin-top: 60px; }}
    footer .footer-brand {{ color: #58a6ff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }}
    footer a {{ color: #58a6ff; text-decoration: none; }}
    footer .footer-links {{ display: flex; justify-content: center; gap: 24px; margin: 12px 0; flex-wrap: wrap; }}
    @media (max-width: 600px) {{ header {{ padding: 0 20px; }} .header-left span {{ display: none; }} .article-hero {{ padding: 40px 20px; }} .article-hero h1 {{ font-size: 1.6rem; }} .content-wrap {{ padding: 40px 20px; }} }}
  </style>
</head>
<body>

<header>
  <div class="header-left">
    <a href="index.html"><h1>⚡ RootAccess</h1></a>
    <span>Free resources for security learners</span>
  </div>
  <nav>
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
  </nav>
</header>

<div class="article-hero">
  <a href="index.html" class="back">← Back to all articles</a>
  <div class="tag {cat_class}">{cat_label}</div>
  <h1>{title}</h1>
  <div class="meta">
    <span>👤 Nate Bustos — Michigan Tech CS Student</span>
    <span>📅 {month_year}</span>
    <span>⏱ {read_time}</span>
  </div>
</div>

<div class="content-wrap">
{body_html}
</div>

<footer>
  <div class="footer-brand">⚡ RootAccess</div>
  <div class="footer-links">
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
    <a href="how-to-get-into-cybersecurity.html">Start Here</a>
  </div>
  <p>Built for the cybersecurity community by a Michigan Tech CS student.</p>
  <p style="margin-top: 8px;">Some links are affiliate links — they help support this site at no extra cost to you.</p>
</footer>

</body>
</html>"""

    # Save article file
    article_path = os.path.join(REPO_DIR, filename)
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"✅ Saved: {filename}")

    # Step 4 — update index.html
    index_path = os.path.join(REPO_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index = f.read()

    new_card = f"""
    <div class="card" data-category="{cat_data}">
      <div class="card-top"><span class="tag {cat_class}">{cat_label}</span></div>
      <h3>{title}</h3>
      <p>{card_description}</p>
      <a href="{filename}" class="read-more">Read article →</a>
    </div>
"""
    index = index.replace("<!-- ADD NEW ARTICLE CARDS HERE -->", f"<!-- ADD NEW ARTICLE CARDS HERE -->{new_card}")

    # Update article count
    index = re.sub(
        r'(<div class="number">)(\d+)(</div>\s*<div class="label">Free Articles</div>)',
        lambda m: f'{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}',
        index
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)
    print("✅ Updated index.html")

    # Step 5 — update sitemap.xml
    sitemap_path = os.path.join(REPO_DIR, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        sitemap = f.read()

    new_url = f"""  <url>
    <loc>{BASE_URL}/{filename}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
    sitemap = sitemap.replace("</urlset>", new_url + "</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("✅ Updated sitemap.xml")

    print(f"\n🎉 Done! Article ready: {filename}")
    print(f"   Now run: git add . && git commit -m \"Add article: {title}\" && git push")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_article.py \"Your Article Topic\"")
        sys.exit(1)
    topic = " ".join(sys.argv[1:])
    generate_article(topic)
