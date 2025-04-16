from dataclasses import dataclass
from typing import List

@dataclass
class RobotsTxtRules:
    crawl_delay: int
    disallowed_paths: List[str] 