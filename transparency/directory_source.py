"""
Get directory source data pointing to csv files in a directory specified in the config
"""
import glob

import os

from transparency.source import Source


class DirectorySource(Source):
    def get(self):
        directory = self.config['directory']
        return [{'url': file} for file in glob.glob(os.path.join(directory, '*.csv'))]
