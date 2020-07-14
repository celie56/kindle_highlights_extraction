"""Extract Kindle Highlights from text file."""
from collections import Counter

import highlights


def main():
    """Extract kindle highlights and print most highlighted titles."""
    parsed_highlights = highlights.extract_highlights()
    titles = [h.title for h in parsed_highlights]
    count_titles = Counter(titles)
    import pdb; pdb.set_trace()
    for title, count in count_titles.most_common():
        print(f'{count}: {title}')


if __name__ == '__main__':
    main()
