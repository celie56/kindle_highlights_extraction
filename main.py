import settings
from typing import List
from dataclasses import dataclass
from collections import Counter

@dataclass
class Highlight:
    title: str = None
    meta_data: str = None
    text: str = None

    def add_line(self, line: str) -> None:
        line = line.replace('\n', '').replace('\ufeff', '')
        if not self.title:
            self.title = line
        elif not self.meta_data:
            self.meta_data = line
        elif not self.text:
            self.text = line

    def filled(self) -> bool:
        return all([self.title, self.meta_data, self.text])


def get_kindle_highlights(highlights_file: str):
    """Given kindle clippings file path, open the path and return the data."""
    with open(highlights_file) as f:
        return f.readlines()

def parse_highlights(data: List[str]) -> List[Highlight]:
    """Given a list of text strings convert to Highlight objects."""
    output = []
    highlight = Highlight()

    for line in data:

        if highlight.filled():
            output.append(highlight)
            highlight = Highlight()

        else:
            highlight.add_line(line)

    return output

def extract_highlights() -> List[Highlight]:
    user_settings = settings.get_settings()
    highlights_data = get_kindle_highlights(user_settings.file_location)
    return parse_highlights(highlights_data)

def main():
    parsed_highlights = extract_highlights()
    titles = [h.title for h in parsed_highlights]
    count_titles = Counter(titles)
    for title, count in count_titles.most_common():
        print(f'{count}: {title}')

if __name__ == '__main__':
    main()
