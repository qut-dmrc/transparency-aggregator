import logging
from datetime import datetime, date
from logging.handlers import RotatingFileHandler

import math
import pandas as pd


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
    df.columns = df.columns.str.lower()


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
        else:
            # replace formatting commas
            df[col] = df[col].str.replace(',', '')

            # replace ranges with the lower bound of the range
            df[col] = df[col].str.replace(r"(\d+)( - )(\d+)", r'\1')

            df[col] = pd.to_numeric(df[col], errors='raise')


def df_convert_to_lower(df, string_cols):
    for col in string_cols:
        df[col] = df[col].apply(str.lower)


def df_convert_from_percentage(df, pc_col, total_col, dest_col):
    df[dest_col] = df[total_col] * df[pc_col] / 100.0
    df[dest_col] = df[dest_col].round()

