"""Highlights from kindle."""
from dataclasses import dataclass
from operator import attrgetter
from typing import List
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
            text = text.replace(' ', '')
            self._date_added = datetime.strptime(text, DATE_FMT).date()
        return self._date_added

    def to_markdown(self) -> str:
        """Return Markdown representation as string."""
        return f'> {self.text}'

    def __lt__(self, other: 'Highlight') -> bool:
        return self.index < other.index

    def __hash__(self):
        return hash(self.title + self.text)


@dataclass
class Reading:
    """Container for a reading and its highlights."""
    title: str
    highlights: List[Highlight] = None
    _scrubbed_title: str = None

    def add(self, highlight: Highlight) -> None:
        """Add Highlight to Reading collection."""
        if not self.highlights:
            self.highlights = []
        self.highlights.append(highlight)

    @property
    def num_highlights(self) -> int:
        """Return number of highlights in this reading."""
        return len(self.highlights)

    @property
    def first_highlight(self) -> Highlight:
        """Return latest highlight."""
        return sorted(self.highlights, key=attrgetter('index'))[0]

    @property
    def last_highlight(self) -> Highlight:
        """Return latest highlight."""
        return sorted(self.highlights, key=attrgetter('index'))[-1]

    @property
    def last_highlight_date(self) -> date:
        """Return latest highlight's date_added."""
        return self.last_highlight.date_added

    @property
    def scrubbed_title(self) -> str:
        """Return title minus common title issues."""
        if not self._scrubbed_title:
            title = self.title
            start = title.find('(')
            if start > -1:
                end = title.find(')', start)
                extra_text = title[start + 1:end]
                if extra_text in title[:start]:
                    title = title[:start]
                else:
                    title = title[:start] + title[start + 1:end]
            title = title.replace(' ', '_')
            title = title.replace('__', '_')
            title = title.replace('_-_', '-')
            title = title.replace('_–_', '-')
            if title[-1] == '_':
                title = title[:-1]
            title = title.replace('_', ' ')
            self._scrubbed_title = title
        return self._scrubbed_title

    def to_markdown(self) -> str:
        """Return Markdown representation as string."""
        output = f'# {self.scrubbed_title}\n\n'
        output += f'## Meta\n\n'
        output += f'Num highlights: {self.num_highlights}\n'
        output += f'First highlight: {self.first_highlight.date_added}\n'
        output += f'Latest highlight: {self.last_highlight_date}\n\n'
        output += f'## Highlights\n\n'
        output += '\n\n---\n\n'.join([h.to_markdown() for h in self.highlights])
        return output

    def __hash__(self):
        return hash(self.title)


def get_kindle_highlights(highlights_file: str):
    """Given kindle clippings file path, open the path and return the data."""
    with open(highlights_file) as input_file:
        return input_file.readlines()


def parse_highlights(data: List[str]) -> List[Reading]:
    """Given a list of strings returns List of Readings."""
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

    return output.values()


def extract_highlights() -> List[Reading]:
    """Extract highlights from a user defined file."""
    user_settings = settings.get_settings()
    highlights_data = get_kindle_highlights(user_settings.file_location)
    return parse_highlights(highlights_data)
