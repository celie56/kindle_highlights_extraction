"""Extract Kindle Highlights from text file and show latest."""
import click
import highlights
from operator import attrgetter


@click.command()
@click.argument('num_highlights', required=True, default=5)
def main(num_highlights):
    """Extract kindle highlights and print latest titles."""
    readings = highlights.extract_highlights()
    sorted_readings = sorted(
        readings,
        key=attrgetter('last_highlight.index'),
        reverse=True,
    )
    num_highlights = int(num_highlights)
    for reading in sorted_readings[:num_highlights]:
        print(f'{reading.title}: {reading.last_highlight_date}')
        print()


if __name__ == '__main__':
    # This parameter is handled by click
    # pylint: disable=no-value-for-parameter
    main()
