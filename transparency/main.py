import logging

import pandas as pd
from docopt import docopt

from transparency.trans_facebook import TransFacebook
from transparency.trans_google_info import TransGoogleInfo
from transparency.trans_google_removal import TransGoogleRemoval
from transparency.trans_linkedin import TransLinkedin
from transparency.trans_manual import TransManual
from transparency.trans_snap import TransSnapInfo
from transparency.trans_snap_removal import TransSnapRemoval
from transparency.twitter_info import TransTwitterInfo
from transparency.twitter_removal import TransTwitterRemoval
from transparency.utils import setup_logging
from transparency.writer_csv import WriterCSV


def main():
    """ Fetch transparency reports for different platforms and convert to a common format

Usage:
  main.py [-vl] --csv-output=FILE (--get=SOURCE | --get-all)
  main.py --version
  main.py --help

Options:
  -h --help     Show this screen.
  -v --verbose  Increase verbosity for debugging.
  -l --nolog    Don't save log to file -- for debugging only.
  -c FILE, --csv-output=FILE     Save results to FILE in CSV format.
  --version  Show version.
  -a --get-all     Fetch all available transparency reports
  -s --get=SOURCE  Fetch data from SOURCE (e.g. facebook)

    """

    args = docopt(main.__doc__, version='Transparency Aggregator v0.1')

    get_from = args['--get']
    get_all = args['--get-all']
    csv_file = args['--csv-output']

    setup_logging("transparency.log", verbose=args['--verbose'],
                  interactive_only=args['--nolog'])

    if not csv_file:
        logging.warning("no output file specified, results will be discarded")

    logging.info("Starting complete run, collecting historical data.")
    df = pd.DataFrame()

    orchestrators = get_orchestrators()
    for (name, orc_class) in orchestrators.items():
        if (get_from and 'trans' + get_from == name.lower()) or get_all:
            df = df.append(fetch(orc_class))

    logging.info("Finished complete run. Found {} rows total.".format(df.shape[0]))
    summary = df.groupby(["platform", "property"]).size()
    logging.info("Summary:\n\n{}\n".format(summary.to_string()))

    if csv_file:
        logging.info('writing to ' + csv_file)
        writer = WriterCSV({})
        writer.write(df, csv_file)

def fetch(orc_class):
    orc = orc_class()
    logging.info(f"fetching data for {orc.name()}")
    df = orc.fetch_all()
    logging.debug(f"sample of {orc.name()}:\n\n{df.head(3).to_string()}\n")
    return df

def get_orchestrators():
    # it's possible to build this dict dynamically (e.g.:
    #    return {k:v for k, v in globals().items() if k.lower().startswith('trans')}
    # but that method doesn't let IDE know that the classes are used.
    return {
        'transfacebook': TransFacebook,
        'transtwitterinfo': TransTwitterInfo,
        'transtwitterremoval': TransTwitterRemoval,
        'transgoogle': TransGoogleInfo,
        'transgoogleremoval': TransGoogleRemoval,
        'translinkedin': TransLinkedin,
        'transsnapinfo': TransSnapInfo,
        'transsnapremoval': TransSnapRemoval,
        'transmanual': TransManual,
    }

if __name__ == '__main__':
    main()
