"""
Read a CSV into a data frame
"""
import logging

import numpy as np
import pandas as pd
from transparency.reader import Reader


class CSVReader(Reader):
    def read(self, filename):
        #try:
        df = pd.read_csv(filename, encoding="UTF-8",
                     dtype=np.object_)  # force dtype to avoid columns changing type because sometimes they have *s in them
        # except UnicodeDecodeError:
        #     logging.debug(f"Failed decoding {filename} with UTF-8. Trying with latin-1.")
        #     df = pd.read_csv(filename, encoding = 'latin-1',
        #                  dtype=np.object_)

        logging.debug("Found {} rows.".format(df.shape[0]))
        return df
