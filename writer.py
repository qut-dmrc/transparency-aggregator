"""
Write data from a DataFrame
"""
from action import Action


class Writer(Action):
    def write(self, df, filename):
        raise NotImplementedError()
