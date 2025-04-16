# Hacker News Front Page Scraper

This Python script scrapes the titles, external URLs, Hacker News comment links, and scores for stories listed on the main page of Hacker News (https://news.ycombinator.com/).

## Features

- Fetches the Hacker News front page
- Extracts story titles, URLs, comment links, and scores
- Handles potential errors gracefully (network issues, parsing errors)
- Saves data to a CSV file
- Implements robots.txt compliance
- Implements comprehensive logging
- Uses proper error handling with custom exceptions
- Follows clean code principles and best practices

## Requirements

- Python 3.x
- Libraries listed in `requirements.txt`:
  - requests==2.31.0
  - beautifulsoup4==4.12.2
  - lxml==4.9.3

## Installation

1. Clone this repository or download the files
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the project directory:
```bash
python main.py
```

The script will:
1. Check robots.txt rules for compliance
2. Fetch the Hacker News front page
3. Parse the HTML content
4. Extract story data
5. Save the data to `hacker_news_data.csv`

## Output Format

The script generates a CSV file (`hacker_news_data.csv`) with the following columns:
- `Title`: The title of the story
- `URL`: The main URL the story links to
- `HN_Link`: The URL to the comments page on news.ycombinator.com
- `Score`: The point score of the story (integer)

## Code Structure

The code is organized into modules for better separation of concerns:

- `main.py`: The main entry point of the application that orchestrates the scraping process
- `utils/`: Contains utility modules:
    - `hacker_news_scraper.py`: Core scraping functionality
    - `storage.py`: Manages saving the extracted data to a CSV file
    - `robots_handler.py`: Handles robots.txt compliance
- `models/`: Contains data models:
    - `story_data.py`: Defines the Story class for holding scraped information
    - `robots_txt_rules.py`: Defines the data structure for robots.txt rules
- `exceptions/`: Defines custom exceptions:
    - `custom_exceptions.py`: Exception hierarchy for specific error conditions
- `config/`: Contains configuration modules:
    - `settings.py`: URL configurations, timeouts, and other constants
    - `logging_config.py`: Logging configuration
- `requirements.txt`: Lists project dependencies with specific versions

## Robots.txt Compliance

This scraper respects the website's robots.txt directives.

## Disclaimer

This script is for educational purposes. Please use responsibly and respect Hacker News's terms of service. Avoid running the script excessively.