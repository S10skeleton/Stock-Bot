import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Loads your .env if you haven't already

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    print("Error: No Twitter bearer token found in environment.")
    exit()

def test_twitter_api():
    endpoint = "https://api.twitter.com/2/tweets/search/recent"

    # For example, searching for tweets mentioning $AAPL, excluding retweets, in English
    params = {
        "query": "$AAPL -is:retweet lang:en",
        "tweet.fields": "created_at,public_metrics,text",  
        "max_results": 2
    }

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    response = requests.get(endpoint, params=params, headers=headers)

    print("Status Code:", response.status_code)
    if response.status_code != 200:
        print("Error response:", response.json())
        return

    data = response.json()
    print("Raw JSON response:")
    print(data)

    # Optionally, print out just the tweet texts or other fields
    if "data" in data:
        for tweet in data["data"]:
            print(f"Tweet ID: {tweet['id']}")
            print(f"Created At: {tweet['created_at']}")
            print(f"Text: {tweet['text']}")
            print("----")

if __name__ == "__main__":
    test_twitter_api()
