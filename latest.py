"""Extract Kindle Highlights from text file and show latest."""
import click
import highlights


@click.command()
@click.argument('num_highlights', required=True)
def main(num_highlights):
    """Extract kindle highlights and print latest titles."""
    parsed_highlights = sorted(highlights.extract_highlights())
    for highlight in parsed_highlights[-1 * int(num_highlights):]:
        print(highlight.title)
        print(highlight.text)
        print()


if __name__ == '__main__':
    # This parameter is handled by click
    # pylint: disable=no-value-for-parameter
    main()
