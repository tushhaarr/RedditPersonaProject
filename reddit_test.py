import os
from dotenv import load_dotenv
import praw

# Load credentials from .env
load_dotenv()

print("🔍 DEBUG: Loading credentials...")
print("CLIENT_ID:", os.getenv("REDDIT_CLIENT_ID"))
print("SECRET:", os.getenv("REDDIT_CLIENT_SECRET"))
print("AGENT:", os.getenv("REDDIT_USER_AGENT"))

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

try:
    user = reddit.redditor("spez")
    print(f"✅ Connected. Fetching posts for u/{user.name}...")

    submissions = list(user.submissions.new(limit=5))
    for post in submissions:
        print("🔸", post.title)

except Exception as e:
    print("❌ ERROR:", e)
