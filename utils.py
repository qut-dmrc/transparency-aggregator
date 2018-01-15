import logging
from logging.handlers import RotatingFileHandler
from dateutil.parser import parse
from datetime import datetime, date
import numpy as np
import pandas as pd

def check_assumption(assumption, assumption_description):
	if assumption:
		pass
	else:
		logging.error(f'Assumption failed: {assumption_description}')

def str_to_date(date_in):
	""" Simple method to convert a string to a date. If passed a date, leave as is. """
	## TODO Make this locale independant
	if isinstance(date_in, str):
		if date_in == '':
			return None
		return parse(date_in)
	elif isinstance(date_in, (datetime, date)):
		return date_in
	else:
		raise ValueError("Input not in a string or date format. Got: {}".format(date_in))

def setup_logging(log_file_name, verbose=False, interactive_only=False):
	if not verbose:
		# Quieten other loggers down a bit (particularly requests and google api client)
		for logger_str in logging.Logger.manager.loggerDict:
			try:
				logging.getLogger(logger_str).setLevel(logging.WARNING)
			except:
				pass

	log_formatter = logging.Formatter(
		"%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-20.20s() [%(threadName)-12.12s] [%(levelname)-8.8s]  %(message).5000s")
	logger = logging.getLogger()

	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(log_formatter)
	logger.addHandler(consoleHandler)
	if verbose:
		consoleHandler.setLevel(logging.DEBUG)
	else:
		consoleHandler.setLevel(logging.INFO)

	if not interactive_only:
		fileHandler = RotatingFileHandler(log_file_name, maxBytes=20000000, backupCount=20)
		fileHandler.setFormatter(log_formatter)

		if verbose:
			fileHandler.setLevel(logging.DEBUG)
		else:
			fileHandler.setLevel(logging.INFO)

		logger.addHandler(fileHandler)

	if verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	return logger


def df_fix_columns(df):
	df.columns = df.columns.str.lower()

def df_strip_char(df, col, char):
	df[col] = df[col].str.rstrip(char)

def df_convert_to_numeric(df, numeric_cols):
	for col in numeric_cols:
		if col not in df.columns:
			df[col] = None
		else:
			# replace formatting commas
			df[col] = df[col].str.replace(',', '')

			# replace ranges with the lower bound of the range
			df[col] = df[col].str.replace(r"(\d+)( - )(\d+)", r'\1')

			df[col] = pd.to_numeric(df[col], errors='raise')

def df_convert_from_percentage(df, pc_col, total_col, dest_col):
		df[dest_col] = df[total_col] * df[pc_col] / 100.0
		df[dest_col] = df[dest_col].round()
