"""
Get static source data pointing to readable files/urls from the config
"""

from transparency.source import Source


class StaticSource(Source):
    def get(self):
        return self.config['data']
