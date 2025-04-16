import csv
import logging
from typing import List

from config.settings import CSV_FILENAME, CSV_HEADERS
from models.story_data import StoryData
from exceptions.custom_exceptions import SaveCsvError

logger = logging.getLogger(__name__)

def save_stories_to_csv(stories: List[StoryData]) -> None:
    if not stories:
        logger.warning("No stories were scraped, skipping CSV save.")
        return
            
    logger.info(f"Writing {len(stories)} stories to {CSV_FILENAME}...")
    try:
        with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            
            for story in stories:
                writer.writerow({
                    'Title': story.title,
                    'URL': story.url,
                    'HN_Link': story.hn_link,
                    'Score': story.score
                })

        logger.info(f"Successfully wrote data to {CSV_FILENAME}")
    except IOError as e:
        raise SaveCsvError(f"Error writing to CSV file {CSV_FILENAME}: {e}") from e
    except Exception as e:
        raise SaveCsvError(f"An unexpected error occurred during CSV writing: {e}") from e 