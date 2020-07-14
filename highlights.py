"""Highlights from kindle."""
from dataclasses import dataclass
from operator import attrgetter
from typing import (
    Dict,
    List,
)
from datetime import datetime, date

import settings

# May 5, 2020
DATE_FMT = '%B%d,%Y'


@dataclass
class Highlight:
    """Container class for highlights."""
    title: str = None
    meta_data: str = None
    text: str = None
    index: int = None

    _split_meta: List[str] = None
    _date_added: date = None

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

    @property
    def split_meta(self) -> List[str]:
        """Helper to split the meta data."""
        if not self._split_meta:
            self._split_meta = self.meta_data.split('|')
        return self._split_meta

    @property
    def date_added(self) -> date:
        """Date the highlight was added."""
        if not self._date_added:
            text = self.split_meta[-1]
            start = text.find(',') + 2
            text = text[start:]
            end = text.find(':') - 2
            text = text[:end]
            text = text.replace(' ','')
            self._date_added = datetime.strptime(text, DATE_FMT).date()
        return self._date_added

    def __lt__(self, other: 'Highlight') -> bool:
        return self.index < other.index

    def __hash__(self):
        return hash(self.title + self.text)

@dataclass
class Reading:
    title: str
    highlights: List[Highlight] = None

    def add(self, highlight: Highlight) -> None:
        if not self.highlights:
            self.highlights = []
        self.highlights.append(highlight)

    @property
    def num_highlights(self) -> int:
        return len(self.highlights)

    @property
    def last_highlight(self) -> Highlight:
        return sorted(self.highlights, key=attrgetter('date_added'))[-1]

    @property
    def last_highlight_date(self) -> date:
        return self.last_highlight.date_added

    def __hash__(self):
        return hash(self.title)

def get_kindle_highlights(highlights_file: str):
    """Given kindle clippings file path, open the path and return the data."""
    with open(highlights_file) as input_file:
        return input_file.readlines()


def parse_highlights(data: List[str]) -> Dict[str, Reading]:
    """Given a list of strings returns map of title to Reading."""
    output = {}
    highlight = Highlight()

    for index, line in enumerate(data):

        if highlight.filled():
            highlight.index = index
            title = highlight.title

            if title not in output:
                output[title] = Reading(title)
            output[title].add(highlight)

            highlight = Highlight()

        else:
            highlight.add_line(line)

    return output


def extract_highlights() -> List[Highlight]:
    """Extract highlights from a user defined file."""
    user_settings = settings.get_settings()
    highlights_data = get_kindle_highlights(user_settings.file_location)
    return parse_highlights(highlights_data)
