"""
Read a LinkedIn html file into a data frame.

LinkedIn has the transparency data as json embedded in a html page.
The json does not include dates - presumably linkedin generates the dates based on a known start date, just as we do
here.
"""
import json
import logging

import pandas as pd
from bs4 import BeautifulSoup, Comment

from transparency.reader import Reader


class LinkedinReader(Reader):
    def read(self, filename):
        with open(filename) as file:
            soup = BeautifulSoup(file, 'html.parser')

        parent = soup.find('code', {"id": "templates/legal/transparency-content"})
        comments = parent.findAll(text=lambda text: isinstance(text, Comment))

        final_json = comments[0]

        # the contract for Reader is that all elements of the dataframe are strings
        # parse_int=str uses 'str' to read in ints, which casts them to strings
        linked_in = json.loads(final_json, parse_int=str)

        gov_reqs = linked_in['governmentRequestsTable']
        bigdata = []
        for (i, dat) in enumerate(gov_reqs):
            (report_start, report_end) = self.linkedin_data_index_to_dates(i)
            for row in dat['countries']:
                bigdata.append({"i": i, "report_start": report_start, "report_end": report_end, **row})

        df = pd.DataFrame(bigdata)

        logging.debug("Found {} rows.".format(df.shape[0]))

        # TODO Add assumption check in trans_linkedin

        return df

    def linkedin_data_index_to_dates(self, i):
        """
        calculate start and end dates based on the index of a block of data.
        Data starts at 2011-07 and increases 6 months each time
        """
        year = int((i + 1) / 2) + 2011
        period_i = (i + 1) % 2
        month = [1, 7][period_i]
        start = pd.Timestamp(year, month, 1)
        end = start + pd.DateOffset(months=6) - pd.DateOffset(seconds=1)
        return (str(start), str(end))
