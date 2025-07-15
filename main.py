#Imported necessary library
import os
from urllib.parse import urlparse
from dotenv import load_dotenv    #Load environment variables
import praw                       #Python Reddit API Wrapper
from transformers import pipeline                  

#Loading API credentials from .env file
load_dotenv()

#Connect to Reddit API using credentials
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


#Extract the username from the profile URL
def extract_username(url):
    """This function takes Reddit profile URL and extracts the username from it"""

    return urlparse(url).path.strip('/').split('/')[-1]

#Fetch submissions and comments made by the user
def fetch_user_content(username, limit=100):
    """Fetch latest posts and comments from a Reddit user."""
    posts = []
    comments = []

    user = reddit.redditor(username)

    try:
        for submission in user.submissions.new(limit=limit):
            if submission.selftext.strip():  #It only keep non-empty posts
                posts.append({
                    "title": submission.title,
                    "body": submission.selftext,
                    "url": submission.url,
                    "permalink": f"https://www.reddit.com{submission.permalink}"
                })
    except Exception as e:
        print(f" Error while fetching posts: {e}")

    try:
        for comment in user.comments.new(limit=limit):
            if comment.body.strip():  
                comments.append({
                    "body": comment.body,
                    "permalink": f"https://www.reddit.com{comment.permalink}"
                })
    except Exception as e:
        print(f"Error while fetching comments: {e}")

    print(f" Retrieved {len(posts)} posts and {len(comments)} comments.")
    if posts:
        print("\n Sample Post:")
        print(posts[0]["title"])
        print(posts[0]["body"][:300])

    if comments:
        print("\n Sample Comment:")
        print(comments[0]["body"][:300])

    return posts, comments


#Building a basic user parsona based on keyword matching
# Local summarization pipeline
def local_model_summary(text_blocks):
    text = " ".join(text_blocks)
    if not text.strip():
        return "No textual content available to generate a persona."

    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
    input_text = "summarize: " + text[:1000]  # truncate for length limit
    summary = summarizer(input_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

#Build user persona with structure
def build_user_persona(posts, comments):
    all_texts = []
    citations = []

    for item in posts + comments:
        text = item.get("body") or item.get("title", "")
        if text.strip():
            all_texts.append(text.strip())
            citations.append(item.get("permalink"))

    if not all_texts:
        return {
            "Generated Persona": "No textual content available.",
            "Activity Level": "Low",
            "Topics": [],
            "Personality": [],
            "Style": [],
            "Sample": "",
            "Source": ""
        }

    summary_text = local_model_summary(all_texts)

    #Rule-based traits
    topics = []
    personality = []
    style = []

    if any("government" in t.lower() or "sarkar" in t.lower() for t in all_texts):
        topics.append("Politics / Governance")
    if any("rent" in t.lower() or "cost" in t.lower() for t in all_texts):
        topics.append("Urban Living / Economy")

    if any("i think" in t.lower() or "feels like" in t.lower() for t in all_texts):
        personality.append("Reflective")
    if any(len(t.split()) < 10 for t in all_texts):
        style.append("Concise")
    if any(len(t.split()) > 25 for t in all_texts):
        style.append("Detailed")

    return {
        "Generated Persona": summary_text.strip(),
        "Activity Level": "Low" if len(posts) + len(comments) < 20 else "Very Active",
        "Topics": list(set(topics)),
        "Personality": list(set(personality)),
        "Style": list(set(style)),
        "Sample": all_texts[0] if all_texts else "",
        "Source": citations[0] if citations else ""
    }

#Save persona as structured file
def save_persona(username, persona):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"User Persona for u/{username}\n\n")
        f.write(f" Name (Alias): {username}\n")
        f.write(f" Goals/Interests: {', '.join(persona['Topics']) or 'Not clearly defined'}\n")
        f.write(f" Personality: {', '.join(persona['Personality']) or 'Unknown'}\n")
        f.write(f" Writing Style: {', '.join(persona['Style']) or 'Neutral'}\n")
        f.write(f" Activity Level: {persona['Activity Level']}\n\n")
        f.write(f" Sample Insight:\n{persona['Sample']}\n\n")
        if persona['Source']:
            f.write(f" Source Link:\n{persona['Source']}\n\n")
        f.write(" Local AI Summary:\n" + persona["Generated Persona"] + "\n")
    print(f"\n Persona saved to {filename}")

#Main function
def main():
    profile_url = input("Enter Reddit profile URL: ").strip()
    username = extract_username(profile_url)

    print(f"\n Fetching data for u/{username}...")
    posts, comments = fetch_user_content(username)
    print(f"\n{len(posts)} posts and {len(comments)} comments fetched.")

    print("\n Generating user persona using local summarizer...")
    persona = build_user_persona(posts, comments)

    save_persona(username, persona)

if __name__ == "__main__":
    main()
