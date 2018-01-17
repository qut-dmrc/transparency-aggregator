"""
Write data from a DataFrame
"""
from transparency.action import Action


class Writer(Action):
    def write(self, df, filename):
        raise NotImplementedError()
