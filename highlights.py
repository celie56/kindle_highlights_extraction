"""Highlights from kindle."""
from dataclasses import dataclass
from typing import List

import settings


@dataclass
class Highlight:
    """Container class for highlights."""
    title: str = None
    meta_data: str = None
    text: str = None
    index: int = None

    def add_line(self, line: str) -> None:
        """Given a line from a highlights text file, add to container."""
        line = line.replace('\n', '').replace('\ufeff', '')
        if not self.title:
            self.title = line
        elif not self.meta_data:
            self.meta_data = line
        elif not self.text:
            self.text = line

    def filled(self) -> bool:
        """Returns True if this Highlight has all elements filled in."""
        return all([self.title, self.meta_data, self.text])

    def __lt__(self, other: 'Highlight') -> bool:
        return self.index < other.index

    def __hash__(self):
        return hash(self.title + self.text)


def get_kindle_highlights(highlights_file: str):
    """Given kindle clippings file path, open the path and return the data."""
    with open(highlights_file) as f:
        return f.readlines()


def parse_highlights(data: List[str]) -> List[Highlight]:
    """Given a list of text strings convert to Highlight objects."""
    output = []
    highlight = Highlight()

    for index, line in enumerate(data):

        if highlight.filled():
            highlight.index = index
            output.append(highlight)
            highlight = Highlight()

        else:
            highlight.add_line(line)

    return output


def extract_highlights() -> List[Highlight]:
    """Extract highlights from a user defined file."""
    user_settings = settings.get_settings()
    highlights_data = get_kindle_highlights(user_settings.file_location)
    return parse_highlights(highlights_data)
