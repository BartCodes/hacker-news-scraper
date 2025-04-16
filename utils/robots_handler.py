import requests
import logging
from typing import Optional

from config.settings import ROBOTS_URL, REQUEST_TIMEOUT, DEFAULT_ROBOTS_CRAWL_DELAY
from models.robots_txt_rules import RobotsTxtRules
from exceptions.custom_exceptions import RobotsTxtError

logger = logging.getLogger(__name__)

class RobotsHandler:
    def __init__(self):
        self.rules: Optional[RobotsTxtRules] = None
        logger.info("RobotsHandler initialized.")

    def fetch_rules(self) -> RobotsTxtRules:
        logger.info(f"Fetching robots.txt from {ROBOTS_URL}...")
        try:
            response = requests.get(ROBOTS_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            content = response.text
            crawl_delay = DEFAULT_ROBOTS_CRAWL_DELAY
            disallowed_paths = []
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == 'crawl-delay':
                        try:
                            crawl_delay = int(value)
                        except ValueError:
                            logger.warning(f"Invalid Crawl-delay value '{value}' in robots.txt. Using default: {DEFAULT_ROBOTS_CRAWL_DELAY}")
                            crawl_delay = DEFAULT_ROBOTS_CRAWL_DELAY
                    elif key == 'disallow':
                        if value:
                            disallowed_paths.append(value)
            
            self.rules = RobotsTxtRules(
                crawl_delay=crawl_delay,
                disallowed_paths=disallowed_paths
            )
            logger.info(f"Successfully parsed robots.txt. Crawl-delay: {crawl_delay}, Disallowed paths: {len(disallowed_paths)}")
            return self.rules
            
        except requests.exceptions.RequestException as e:
            raise RobotsTxtError(f"Error fetching robots.txt: {e}") from e
        except Exception as e:
            raise RobotsTxtError(f"Unexpected error parsing robots.txt: {e}") from e

    def ensure_rules_fetched(self) -> None:

        if self.rules is None:
            logger.info("robots.txt rules not yet fetched. Fetching now...")
            self.fetch_rules()

    def is_path_allowed(self, path: str) -> bool:
        self.ensure_rules_fetched()
        assert self.rules is not None
        
        for disallowed_path in self.rules.disallowed_paths:
            if path.startswith(disallowed_path):
                logger.warning(f"Path '{path}' disallowed by rule '{disallowed_path}'")
                return False
        logger.debug(f"Path '{path}' is allowed.")
        return True 