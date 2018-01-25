"""
Read a Snap html file into a data frame.

"""
import logging

import pandas as pd
from bs4 import BeautifulSoup
from dateutil.parser import parse

from transparency.reader import Reader


class SnapReader(Reader):
    def read(self, filename):
        with open(filename) as file:
            soup = BeautifulSoup(file, 'html.parser')

        table_data = soup.find("h2", text="International Government Information Requests").find_next("table")
        df = pd.read_html(str(table_data))[0]

        start_date, end_date = self.parse_date_range(df.iloc[0, 0])

        df['report_start_from_table'] = start_date
        df['report_end_from_table'] = end_date

        # rename first column
        df = df.rename(columns={'Reporting Period': 'country'})

        # drop first row - totals data and reindex in case anyone uses this index
        df = df.drop(0, axis=0).reset_index(drop=True)

        logging.debug("Found {} rows.".format(df.shape[0]))

        return df

    def parse_date_range(self, date_range_string):
        """
        Take a string in the form
        and return start date and end date (modified for last minute of period)
        """

        start_date_str, end_date_str = date_range_string.split('—')  # warning - emdash

        start_date = parse(start_date_str)
        end_date = parse(end_date_str)
        end_date = end_date.replace(hour=23, minute=59, second=59)

        return start_date, end_date
