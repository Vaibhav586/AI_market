import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------
# 1. Fetch AI-related news
# -------------------------
def fetch_ai_news():
    url = f"https://newsapi.org/v2/everything?q=AI+Artificial+Intelligence&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles[:5]   # take top 5 articles


# -------------------------
# 2. Summarize each article
# -------------------------
def summarize_article(article):
    prompt = f"""
Summarize this AI news article into 2-3 bullet points that highlight
the key update and why it matters for AI trends.

Title: {article['title']}
Description: {article['description']}
Content: {article['content']}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -------------------------
# 3. Generate a Twitter Thread
# -------------------------
def generate_thread(summaries):
    prompt = f"""
Using the following AI news summaries, write a viral Twitter-style explainer thread.
Make it sharp, structured, engaging and easy to read.

News Summaries:
{summaries}

Format as:
- Hook
- 6–10 Thread Tweets
- Final CTA tweet
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -------------------------
# 4. Build the workflow
# -------------------------
def generate_ai_thread():
    articles = fetch_ai_news()
    summaries = ""

    for a in articles:
        s = summarize_article(a)
        summaries += s + "\n\n"

    thread = generate_thread(summaries)
    return thread


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    print("\nGenerating AI Market Trend Thread...\n")
    thread_text = generate_ai_thread()
    print(thread_text)
