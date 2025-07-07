import os
import requests
from datetime import date, timedelta

BASE_URL = "https://app.metricool.com/api"

USER_TOKEN = os.getenv("METRICOOL_USER_TOKEN")
USER_ID = os.getenv("METRICOOL_USER_ID")
BLOG_ID = os.getenv("METRICOOL_BLOG_ID")

if not USER_TOKEN or not USER_ID or not BLOG_ID:
    raise ValueError("Missing required environment variables for authentication")

AUTH_PARAMS = {
    "userToken": USER_TOKEN,
    "userId": USER_ID,
    "blogId": BLOG_ID,
}

END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=365)

START_YMD = START_DATE.strftime("%Y%m%d")
END_YMD = END_DATE.strftime("%Y%m%d")
START_ISO = START_DATE.isoformat() + "T00:00:00"
END_ISO = END_DATE.isoformat() + "T23:59:59"

def fetch(endpoint: str, params: dict) -> dict:
    """Perform GET request to Metricool API and return JSON."""
    request_params = AUTH_PARAMS.copy()
    request_params.update(params)
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, params=request_params)
    response.raise_for_status()
    return response.json()

def main():
    data = {}

    # Stats Service endpoints (uses start/end as YYYYMMDD integers)
    stats_endpoints = {
        "instagram_posts": "/stats/instagram/posts",
        "instagram_reels": "/stats/instagram/reels",
        "instagram_stories": "/stats/instagram/stories",
    }

    for key, endpoint in stats_endpoints.items():
        data[key] = fetch(endpoint, {"start": START_YMD, "end": END_YMD})

    # Instagram Analytics endpoints (use from/to ISO 8601)
    analytics_endpoints = {
        "analytics_posts": "/v2/analytics/posts/instagram",
        "analytics_reels": "/v2/analytics/reels/instagram",
        "analytics_stories": "/v2/analytics/stories/instagram",
        "analytics_posts_hashtags": "/v2/analytics/posts/instagram/hashtags",
    }

    for key, endpoint in analytics_endpoints.items():
        data[key] = fetch(endpoint, {"from": START_ISO, "to": END_ISO})

    # Print summary
    for section, items in data.items():
        print(f"{section}: {len(items)} items")

if __name__ == "__main__":
    main()
