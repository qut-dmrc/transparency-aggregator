"""
Read data into a DataFrame
"""
from action import Action


class Reader(Action):
    def read(self, filename):
        raise NotImplementedError()
