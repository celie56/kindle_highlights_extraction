"""Extract Kindle Highlights from file and generate Markdown highlightss."""
from operator import attrgetter
from pathlib import Path

import highlights
import settings


def scrub_title(title: str) -> str:
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
    return title


def title_to_path(title: str, output_folder: str) -> str:
    title = scrub_title(title) + '.md'
    return str(Path(output_folder, title).resolve())


def main():
    """Extract kindle highlights and print most highlighted titles."""
    user_settings = settings.get_settings()
    output_folder = user_settings.output_folder

    readings = highlights.extract_highlights()
    for reading in readings:
        out_filepath = title_to_path(reading.title, output_folder)
        with open(out_filepath, 'w') as out_file:
            out_file.write(reading.to_markdown())


if __name__ == '__main__':
    main()
