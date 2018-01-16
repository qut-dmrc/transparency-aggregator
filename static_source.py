""" 
"""

from source import Source


class StaticSource(Source):
    def get(self):
        return self.config['data']
