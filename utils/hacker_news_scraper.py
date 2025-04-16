import requests
import logging
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin

from config.settings import BASE_URL, REQUEST_TIMEOUT
from models.story_data import StoryData
from exceptions.custom_exceptions import FetchError, ParseError, PermissionError, DataExtractionError, RobotsTxtError
from utils.robots_handler import RobotsHandler

logger = logging.getLogger(__name__)

class HackerNewsScraper:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.robots_handler = RobotsHandler()
        self.stories: List[StoryData] = []
        logger.info("HackerNewsScraper initialized.")

    def fetch_page(self) -> str:
        try:
            self.robots_handler.ensure_rules_fetched() 
            if not self.robots_handler.is_path_allowed('/'):
                 raise PermissionError("Access to the front page ('/') is disallowed by robots.txt")
        except RobotsTxtError as e:
            raise
            
        logger.info(f"Fetching {self.base_url}...")
        try:
            response = requests.get(self.base_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            logger.info("Successfully fetched page.")
            return response.text
        except requests.exceptions.RequestException as e:
            raise FetchError(f"Error fetching URL {self.base_url}: {e}") from e

    def parse_html(self, html_content: str) -> BeautifulSoup:

        logger.info("Parsing HTML content...")
        try:
            soup = BeautifulSoup(html_content, 'lxml') 
            logger.info("Parsing complete.")
            return soup
        except Exception as e:
            raise ParseError(f"Error parsing HTML: {e}") from e

    def _extract_title_and_primary_link(self, title_span: BeautifulSoup) -> tuple[str, str, str]:
        title = "N/A"
        url = "N/A"
        hn_link = "N/A"

        title_link = title_span.find('a')
        if not title_link:
            raise DataExtractionError("Could not find title link within title span")

        title = title_link.get_text(strip=True)
        href = title_link.get('href')

        if not href:
            raise DataExtractionError(f"Missing href attribute in title link for story '{title[:30]}...'")

        # Determine if it's an internal HN link (Ask HN, Show HN, etc.) or external
        if href.startswith('item?id='):
            url = 'N/A'  # No external URL for internal posts
            hn_link = urljoin(self.base_url, href)
        else:
            url = urljoin(self.base_url, href) # Assumes it's an external link

        return title, url, hn_link

    def _find_hn_comment_link(self, subtext_row: BeautifulSoup, base_url: str) -> str | None:
        """Finds the Hacker News comment link (item?id=...) in the subtext row."""
        if not subtext_row:
            return None

        links_in_subtext = subtext_row.find_all('a')
        for link in reversed(links_in_subtext):
            href_comment = link.get('href', '')
            if href_comment.startswith('item?id='):
                return urljoin(base_url, href_comment)
        return None # Return None if not found

    def _extract_score(self, subtext_row: BeautifulSoup, story_title: str) -> int:
        if not subtext_row:
            logger.warning(f"Could not find subtext row for story '{story_title[:30]}...' to extract score.")
            return 0 # Default score if subtext row missing

        score_span = subtext_row.find('span', class_='score')
        if not score_span:
            logger.debug(f"No score span found for story '{story_title[:30]}...'. Defaulting to 0.")
            return 0 # Default score if span missing

        score_text = score_span.get_text(strip=True)
        try:
            return int(score_text.split()[0])
        except (ValueError, IndexError):
            logger.warning(f"Could not parse score ('{score_text}') for story '{story_title[:30]}...'. Defaulting to 0.")
            return 0 # Default score if parsing fails

    def _extract_single_story(self, story_element: BeautifulSoup) -> StoryData:
        try:
            title_span = story_element.find('span', class_='titleline')
            if not title_span:
                raise DataExtractionError("Could not find title span (span.titleline)")

            title, url, hn_link = self._extract_title_and_primary_link(title_span)

            # If it was an external link, try to find the specific HN comment link
            if url != 'N/A':
                subtext_row = story_element.find_next_sibling('tr')
                found_hn_link = self._find_hn_comment_link(subtext_row, self.base_url)
                if found_hn_link:
                    hn_link = found_hn_link
                elif hn_link == "N/A": # Only log warning if we didn't already set hn_link from title
                     logger.warning(f"Could not find HN comment link (item?id=...) for story '{title[:30]}...'")

            subtext_row = subtext_row if url != 'N/A' else story_element.find_next_sibling('tr')
            score = self._extract_score(subtext_row, title)

            if not title or title == "N/A":
                 raise DataExtractionError("Failed to extract a valid title for a story.")

            return StoryData(title=title, url=url, hn_link=hn_link, score=score)

        except AttributeError as e:
            raise DataExtractionError(f"Missing expected HTML structure for a story: {e}") from e
        except DataExtractionError:
             raise
        except Exception as e:
            raise DataExtractionError(f"An unexpected error occurred during story extraction: {e}") from e

    def scrape_stories(self, soup: BeautifulSoup) -> List[StoryData]:
        logger.info("Extracting data from each story...")
        story_elements = soup.find_all('tr', class_='athing')
        logger.info(f"Found {len(story_elements)} potential story entries.")

        extracted_stories = []
        successful_extractions = 0
        failed_extractions = 0
        
        for i, story_element in enumerate(story_elements, 1):
            try:
                story_data = self._extract_single_story(story_element)
                extracted_stories.append(story_data)
                successful_extractions += 1
            except DataExtractionError as e:
                logger.warning(f"Failed to extract data for story element #{i}: {e}")
                failed_extractions += 1
            except Exception as e:
                 logger.error(f"Unexpected error processing story element #{i}: {e}", exc_info=True)
                 failed_extractions += 1
                 
        self.stories = extracted_stories # Update the instance stories list
        logger.info(f"Story extraction complete. Success: {successful_extractions}, Failures: {failed_extractions}")
        
        if not self.stories:
             logger.warning("No stories were successfully extracted from the page.")
                          
        return self.stories 