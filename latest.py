"""Extract Kindle Highlights from text file and show latest."""
import highlights


def main():
    """Extract kindle highlights and print latest titles."""
    parsed_highlights = highlights.extract_highlights()
    for highlight in parsed_highlights[:-10]:
        print(highlight)
        print()

if __name__ == '__main__':
    main()
