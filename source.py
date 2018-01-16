"""
Get source data pointing to readable files/urls
"""
from action import Action


class Source(Action):
    def get(self):
        raise NotImplementedError()
