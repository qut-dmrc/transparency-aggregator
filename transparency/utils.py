import logging
import math
import os
from datetime import datetime, date
from logging.handlers import RotatingFileHandler
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
import regex as re


class AssumptionError(Exception):
    pass


def check_assumption(assumption, assumption_description):
    """ensure that assumption is True.  If it isn't, log a message and throw an AssuptionError"""
    if assumption:
        pass
    else:
        logging.error(f'Assumption failed: {assumption_description}')
        raise AssumptionError(assumption_description)


def str_to_date(date_in, format_str='%Y-%m-%d'):
    """ Simple method to convert a string to a date. If passed a date, leave as is. """
    if isinstance(date_in, str):
        if date_in == '':
            return None
        return datetime.strptime(date_in, format_str)
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
    #df.columns = df.columns.str.lower()
    df.columns = [strip_punctuation(x.lower()) for x in df.columns.values]

def df_percentage_to_count(df, percent_col, total_col, output_col):

    df[output_col] = df[percent_col] * df[total_col] / 100.0
    df[output_col] = df[output_col].astype(float).apply(np.round)

def df_strip_char(df, col, char):
    df[col] = df[col].str.rstrip(char)


def df_create_missing_columns(df, cols):
    for col in cols:
        if col not in df.columns:
            df[col] = None


def df_convert_to_int(df, cols):
    def convert(v):
        if v is None:
            return None
        if type(v) is float and math.isnan(v):
            return None
        return int(v)

    for col in cols:
        df[col] = df[col].astype(object)
        df[col] = df[col].apply(convert, convert_dtype=False)


# TODO Remove default None
def df_convert_to_numeric(df, numeric_cols):
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = None
        elif not is_numeric_dtype(df[col]):
            # replace formatting commas
            df[col] = df[col].str.replace(',', '')

            # replace ranges with the lower bound of the range
            df[col] = df[col].str.replace(r"(\d+)( - )(\d+)", r'\1')

            # discard additional information in cell
            # (e.g. https://transparency.twitter.com/en/removal-requests.html#removal-requests-jul-dec-2015
            #       shows total withheld tweets = "3,353 (2,440)"
            #       This means 3353 tweets withheld from a total of 2440 accounts. We are only interested in the first.
            df[col] = df[col].str.replace(r"(\d+)( )\(\d+\)", r'\1')

            # remove asterisks and percentages
            df[col] = df[col].str.rstrip('*')
            df[col] = df[col].str.rstrip('%')

            df[col] = pd.to_numeric(df[col], errors='raise')


def df_convert_to_lower(df, string_cols):
    for col in string_cols:
        df[col] = df[col].apply(str.lower)


def df_convert_from_percentage(df, pc_col, total_col, dest_col):
    df[dest_col] = df[total_col] * df[pc_col] / 100.0
    df[dest_col] = df[dest_col].astype(float).round()


def make_path(sub_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", sub_path))


def strip_punctuation(s):
    s = re.sub(r"\p{P}+", "", s) # strip all punctuation
    s = re.sub(r"\s\s+", " ", s) # replace multiple whitespace characters with single space
    s = re.sub(r"\s\Z", "", s) # remove trailing whitespace
    return s
