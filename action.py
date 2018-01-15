"""
Actions are objects that have take a config when created
"""
import re
import urllib
import urllib.request
import os.path
import logging

class Action:
	def __init__(self, config):
		self.config = config
