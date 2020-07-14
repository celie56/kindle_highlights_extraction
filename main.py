"""Extract Kindle Highlights from text file."""
from collections import Counter
from operator import attrgetter

import highlights


def main():
    """Extract kindle highlights and print most highlighted titles."""
    parsed_highlights = highlights.extract_highlights()
    for reading in sorted(
            parsed_highlights.values(),
            key=attrgetter('num_highlights'),
            reverse=True,
    ):
        print(f'{reading.title}: {reading.num_highlights}')


if __name__ == '__main__':
    main()
