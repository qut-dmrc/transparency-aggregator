"""
Read data into a DataFrame
"""
from transparency.action import Action


class Reader(Action):
    def read(self, filename):
        raise NotImplementedError()
