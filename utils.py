import logging
from logging.handlers import RotatingFileHandler
from dateutil.parser import parse
from datetime import datetime, date

def c_to_date(date_in):
    """ Simple method to convert a string to a date. If passed a date, leave as is. """
    if isinstance(date_in, str):
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
