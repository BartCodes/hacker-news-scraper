from urllib.parse import urljoin

# Base URL for Hacker News
BASE_URL = "https://news.ycombinator.com/"

# URL for robots.txt
ROBOTS_URL = urljoin(BASE_URL, "robots.txt")

# Output CSV filename
CSV_FILENAME = "hacker_news_data.csv"

# Headers for the CSV file
CSV_HEADERS = ['Title', 'URL', 'HN_Link', 'Score']

# Timeout for HTTP requests in seconds
REQUEST_TIMEOUT = 10

# Default crawl delay from robots.txt (if specified)
# Note: Not currently used as we only fetch one page
DEFAULT_ROBOTS_CRAWL_DELAY = 30 