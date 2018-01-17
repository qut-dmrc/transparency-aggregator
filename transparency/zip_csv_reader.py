"""
Read a CSV into a data frame
"""
import logging
from zipfile import ZipFile

import numpy as np
import pandas as pd
from transparency.reader import Reader


class ZipCSVReader(Reader):
    def read(self, filename):
        internal_filename = self.config['internal_filename']
        with ZipFile(filename) as zipf:
            with zipf.open(internal_filename) as data_file:
                df = pd.read_csv(data_file, encoding="UTF-8",
                                 dtype=np.object_)  # force dtype to avoid columns changing type because sometimes they have *s in them
                logging.debug("Found {} rows.".format(df.shape[0]))
                return df
