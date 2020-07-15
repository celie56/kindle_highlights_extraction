"""Extract Kindle Highlights from file and generate Markdown highlightss."""
from pathlib import Path

import highlights
import settings


def title_to_path(title: str, output_folder: str) -> str:
    title = title.replace(' ', '_')
    return str(Path(output_folder, title + '.md').resolve())


def main():
    """Extract kindle highlights and print most highlighted titles."""
    user_settings = settings.get_settings()
    output_folder = user_settings.output_folder

    readings = highlights.extract_highlights()
    for reading in readings:
        out_filepath = title_to_path(reading.scrubbed_title, output_folder)
        with open(out_filepath, 'w') as out_file:
            out_file.write(reading.to_markdown())


if __name__ == '__main__':
    main()
