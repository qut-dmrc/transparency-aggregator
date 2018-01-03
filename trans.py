import csv

from docopt import docopt
from trans_facebook import FB
import pandas as pd

def main():
    """ Fetch transparency reports for different platforms and convert to a common format

    Usage:
      transparency_aggregator.py [-vl] --all --output=FILE
      transparency_aggregator.py --version

    Options:
      -h --help     Show this screen.
      -v --verbose  Increase verbosity for debugging.
      -l --nolog    Don't save log to file -- for debugging only.
      -o FILE, --output=FILE     Save results to FILE in CSV format.
      --version  Show version.
      --all     Fetch all available transparency reports

    """

    args = docopt(main.__doc__, version='Transparency Aggregator v0.1')

    if args['--all']:
        df = pd.DataFrame()
        df_facebook = fetch_facebook()
        df = df.append(df_facebook)
        df.to_csv(args['--output'], quoting=csv.QUOTE_ALL, encoding="UTF-8")


def fetch_facebook():
    fb = FB()
    df = fb.fetch_all()
    return df

if __name__ == '__main__':
    main()