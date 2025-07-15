# RedditPersonaProject
This project analyzes a Reddit user's posts and comments to generate a user persona based on their tone, interests, and writing style.
It uses the:
-The Reddit API to fetch user data
-HuggingFace Transformers (`t5-small`) to summarize posts/comments
-A rule-based engine to categorize traits

# Requirements
Make sure you have Python 3.8 or later installed.

Main libraries used:
-`praw` (Reddit API)
-`python-dotenv` (to load `.env`)
-`transformers` (for summarization)
-`torch` (required backend for transformers)


# Environment Setup
You need a `.env` file in your root directory.
Here’s how it should look (refer to `.env.example`):
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=your_user_agent_here

How to Run the Script
To run the script:
You will be prompted to enter a Reddit profile URL, such as:
https://www.reddit.com/user/spez/

The script will:
1. Fetch the user's recent Reddit activity
2. Analyze the tone, writing style, and topics
3. Generate a user persona
4. Save the output in a `.txt` file named like `spez_persona.txt`

# Output Example
Sample output file (`Hungry-Move-6603_persona.txt`):
User Persona for u/Hungry-Move-6603

Name (Alias): Hungry-Move-6603
Goals/Interests: Politics / Governance, Urban Living / Economy
Personality: Reflective
Writing Style: Detailed
Activity Level: Low
Sample Insight:
uttar pradesh sarkar, adhiwakta, nyay palika, mahamantri, skoda laura, adrak lsson are a thing of past..

Source Link:
https://www.reddit.com/r/india/comments/xyz123/comment/abc456/

Local AI Summary:
This user frequently discusses regional governance, public systems, and economic trends with a reflective tone..

If you face any setup issues, feel free to raise an issue in this repo or email the developer.
Thank you! Happy Codding!
