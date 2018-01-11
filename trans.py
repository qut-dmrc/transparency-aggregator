from docopt import docopt
from trans_facebook import FB
from trans_writer_csv import TransparencyWriterCSV 
import pandas as pd
from utils import setup_logging
import logging

def main():
		""" Fetch transparency reports for different platforms and convert to a common format

    Usage:
      transparency_aggregator.py [-vl] --output=FILE (--get=SOURCE | --get-all)
      transparency_aggregator.py --version

    Options:
      -h --help     Show this screen.
      -v --verbose  Increase verbosity for debugging.
      -l --nolog    Don't save log to file -- for debugging only.
      -o FILE, --output=FILE     Save results to FILE in CSV format.
      --version  Show version.
      --get-all     Fetch all available transparency reports
      --get=SOURCE  Fetch data from SOURCE (e.g. facebook)

		"""

		args = docopt(main.__doc__, version='Transparency Aggregator v0.1')

		get_from = args['--get']
		get_all = args['--get-all']
		csv_file = args['--output']  #TODO: change to --csv-output


		setup_logging("transparency.log", verbose=args['--verbose'],
									interactive_only=args['--nolog'])

		if not csv_file:
			logging.warn("no output file specified, results will be discarded")

		logging.info("Starting complete run, collecting historical data.")
		df = pd.DataFrame()

		if get_from == 'facebook' or get_all:
			df = df.append(fetch_facebook())
	
		logging.info("Finished complete run. Found {} rows total.".format(df.shape[0]))

		if csv_file:
				logging.info('writing to' + csv_file)
				writer = TransparencyWriterCSV()
				writer.write(df, csv_file)

def fetch_facebook():
		fb = FB()
		df = fb.fetch_all()
		return df


if __name__ == '__main__':
		main()
