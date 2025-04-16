from dataclasses import dataclass

@dataclass
class StoryData:
    title: str
    url: str
    hn_link: str
    score: int 