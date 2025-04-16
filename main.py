import sys
import logging

from utils.hacker_news_scraper import HackerNewsScraper
from utils.storage import save_stories_to_csv
from exceptions.custom_exceptions import (
    ScraperError, PermissionError, FetchError, ParseError, SaveCsvError, RobotsTxtError
)
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def run_scraper():    
    scraper_instance = HackerNewsScraper()
    
    try:
        logger.info("Starting Hacker News scraping process...")
        
        html_content = scraper_instance.fetch_page()
        soup = scraper_instance.parse_html(html_content)
        
        stories = scraper_instance.scrape_stories(soup)
        
        save_stories_to_csv(stories)
        
        logger.info("Scraping process completed successfully.")

    except RobotsTxtError as e:
         logger.error(f"Robots.txt handling error: {e}")
         sys.exit(1)
    except PermissionError as e:
         logger.error(f"Permission Error: {e}")
         sys.exit(1)
    except FetchError as e:
        logger.error(f"Fetch Error: {e}")
        sys.exit(1)
    except ParseError as e:
        logger.error(f"Parse Error: {e}")
        sys.exit(1)
    except SaveCsvError as e:
         logger.error(f"CSV Save Error: {e}")
         sys.exit(1)
    except ScraperError as e:
         logger.error(f"Scraper Error: {e}")
         sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_scraper() 