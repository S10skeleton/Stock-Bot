# sentiment_fetch.py
import os
import tweepy

# 1) Import load_dotenv
from dotenv import load_dotenv

# 2) Call load_dotenv() to actually load .env contents into environment variables
load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def fetch_tweets_for_symbol(symbol, max_results=10):
    """
    Fetch recent tweets containing the cashtag for the symbol,
    e.g. $AAPL for Apple.
    """
    # Twitter often uses the cashtag syntax $AAPL for stock mentions.
    query = f"${symbol} -is:retweet lang:en"

    # search_recent_tweets is for tweets from the last 7 days.  
    # If you need older data, you'll need Elevated/Academic access or different endpoints.
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["created_at", "text", "public_metrics"]
    )

    # response.data is usually a list of Tweet objects
    if not response.data:
        return []

    # Convert to a list of dicts
    tweets_list = []
    for tweet in response.data:
        tweets_list.append({
            "id": tweet.id,
            "text": tweet.text,
            "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
            "retweet_count": tweet.public_metrics["retweet_count"],
            "like_count": tweet.public_metrics["like_count"],
        })
    return tweets_list
