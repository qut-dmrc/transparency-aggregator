from docopt import docopt
from trans_facebook import FB
from trans_writer_csv import TransparencyWriterCSV 
import pandas as pd
from utils import setup_logging
import logging

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

    setup_logging("transparency.log", verbose=args['--verbose'],
                  interactive_only=args['--nolog'])

    df = pd.DataFrame()
    df_facebook = fetch_facebook()
    df = df.append(df_facebook)

    if args['--all']:
        logging.info("Starting complete run, collecting historical data.")

        df = pd.DataFrame()
        df_facebook = fetch_facebook()
        df = df.append(df_facebook)

        logging.info("Finished complete run. Found {} rows total.".format(df.shape[0]))

        writer = TransparencyWriterCSV()

        writer.write(df, args['--output'])

def fetch_facebook():
    fb = FB()
    df = fb.fetch_all()
    return df


if __name__ == '__main__':
    main()
