"""
aggregator.py
-------------
Pull data from multiple sources: Twitter, StockTwits, Reddit, NewsAPI, RSS Feeds.
Combine them into a single list of { "text", "source", "created_at", ... } dicts.
"""

import os
import time
import requests

# Optional: If you plan to use load_dotenv for secrets
from dotenv import load_dotenv
load_dotenv()

############################
# TWITTER (X) FETCH (Stub) #
############################

def fetch_twitter_for_symbol(symbol, max_results=10):
    """
    Attempt to fetch tweets about the symbol (if not rate-limited).
    Returns a list of dicts, each with: {"text", "created_at", "source": "twitter", ... }
    If rate-limited or fails, raise an exception or return an empty list.
    """
    # PSEUDO-CODE / STUB
    # from your sentiment_fetch or test_twitter_api approach:
    # bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    # if not bearer_token: raise Exception("No Twitter token")

    # The query might be something like:
    # query = f"{symbol} -is:retweet lang:en"
    # ...
    # Or you might skip Twitter if you're hitting 429 repeatedly.

    # For demonstration, returning an empty list or a fake list:
    # return []  # If you prefer to skip
    tweets = []
    # Example fake data:
    # tweets = [
    #     { "text": f"{symbol} soared today!", "created_at": "2025-01-10T14:55:00Z", "source": "twitter" },
    # ]
    return tweets

#############################
# STOCKTWITS FETCH (Stub)   #
#############################

def fetch_stocktwits_for_symbol(symbol, max_results=10):
    """
    Use the StockTwits API for a symbol's feed.
    Docs: https://api.stocktwits.com/developers/docs
    GET https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json
    Returns list of { "text", "created_at", "source": "stocktwits" }
    """
    # Example:
    # url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
    # resp = requests.get(url)
    # data = resp.json()
    # messages = data["messages"]  # each message has "body", "created_at", etc.
    # ...
    # or handle errors
    # For now, we return a dummy list:
    messages = []
    return messages

#############################
# REDDIT FETCH (Stub)       #
#############################

def fetch_reddit_for_symbol(symbol, max_items=10):
    """
    Possibly use PRAW or direct requests + OAuth to fetch from a relevant subreddit or search.
    Return list of { "text", "created_at", "source": "reddit" }
    """
    # For PRAW, you'd do something like:
    # import praw
    # reddit = praw.Reddit(client_id=..., client_secret=..., user_agent=...)
    # subreddit = reddit.subreddit("stocks")
    # for submission in subreddit.search(f"{symbol}", limit=max_items):
    #     ...
    # Or for r/wallstreetbets, etc.
    # Return a list of dicts with text & created_at.

    # Dummy return
    posts = []
    return posts

#############################
# NEWSAPI FETCH (Stub)      #
#############################

def fetch_newsapi_for_symbol(symbol, max_items=10):
    """
    Use NewsAPI.org to fetch news articles related to the symbol.
    Return list of { "text", "created_at", "source": "news" }
    """
    # Example usage:
    # api_key = os.getenv("NEWSAPI_KEY")
    # endpoint = "https://newsapi.org/v2/everything"
    # params = {
    #     "q": symbol,
    #     "apiKey": api_key,
    #     "language": "en",
    #     "pageSize": max_items
    # }
    # resp = requests.get(endpoint, params=params)
    # data = resp.json()
    # articles = data["articles"]  # each has "title", "description", "publishedAt"
    # ...
    # Return them as a list of dicts with "text" = title or description, "created_at" = publishedAt

    articles = []
    return articles

#############################
# RSS FEEDS FETCH (Stub)    #
#############################

def fetch_rss_for_symbol(symbol, max_items=10):
    """
    Use feedparser or requests to parse RSS feeds from Yahoo/Google or other sources.
    Return list of { "text", "created_at", "source": "rss" }
    """
    # Example with feedparser (pip install feedparser):
    # import feedparser
    # feed_url = f"https://news.google.com/rss/search?q={symbol}"
    # feed = feedparser.parse(feed_url)
    # entries = feed.entries[:max_items]
    # ...
    # For each entry, you have title, link, published, etc.

    # Dummy return
    rss_items = []
    return rss_items

#############################
# AGGREGATE ALL SOURCES     #
#############################

def fetch_all_sentiment(symbol, max_items=10):
    """
    Attempts to fetch from all sources. If one fails or is rate-limited, it logs or skips.
    Returns a combined list of dicts: { "text", "created_at", "source", ... }
    """
    combined_data = []

    # 1) Twitter
    try:
        twitter_data = fetch_twitter_for_symbol(symbol, max_results=max_items)
        combined_data.extend(twitter_data)
    except Exception as e:
        print(f"Twitter error: {e}")

    # 2) StockTwits
    try:
        st_data = fetch_stocktwits_for_symbol(symbol, max_results=max_items)
        combined_data.extend(st_data)
    except Exception as e:
        print(f"StockTwits error: {e}")

    # 3) Reddit
    try:
        reddit_data = fetch_reddit_for_symbol(symbol, max_items=max_items)
        combined_data.extend(reddit_data)
    except Exception as e:
        print(f"Reddit error: {e}")

    # 4) NewsAPI
    try:
        newsapi_data = fetch_newsapi_for_symbol(symbol, max_items=max_items)
        combined_data.extend(newsapi_data)
    except Exception as e:
        print(f"NewsAPI error: {e}")

    # 5) RSS
    try:
        rss_data = fetch_rss_for_symbol(symbol, max_items=max_items)
        combined_data.extend(rss_data)
    except Exception as e:
        print(f"RSS error: {e}")

    return combined_data

#############################
# TEST OR DEMO              #
#############################

if __name__ == "__main__":
    # Example usage
    symbol_to_test = "AAPL"
    results = fetch_all_sentiment(symbol_to_test, max_items=5)
    print(f"Found {len(results)} combined items for {symbol_to_test}.")
    for item in results:
        print(item)
