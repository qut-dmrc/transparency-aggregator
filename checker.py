"""
Check that assumptions are valid.

When building this project, we made assumptions about the tranparency data we get from 
companies (e.g. google's transparency reports come out twice yearly).  This class and
its decendents encode those assumptions, so that the user is notified, and check code,
when the assumptions are violated.
"""
import re
import urllib
import urllib.request
import os.path
import logging
from action import Action

class Checker:
	def check(self, df):
		raise NotImplementedError()
