#!python3

"""
Dictionary schema for logging.config
"""

# Standard Library Imports
import os
import sys
import logging


########################################################################
# Define the name of the tool
TOOLNAME = "template-pyqt5"

# Define the maximum number of files that should be rotated per log type.
MAX_LOG_COUNT = 3

# Define the maximum size of a file before being rotated.
MAX_FILE_SIZE = 1024*1024*5  # bytes


########################################################################
# Determine root directory
if sys.platform.lower().startswith('win'):
    ROOT = os.path.normpath("C:/Bboxx/.eventLogs")
else:
    ROOT = os.path.normpath(os.path.join(os.path.expanduser("~"), ".bboxxEventLogs"))

# Create a location to store the logs in
PATH = os.path.join(ROOT, TOOLNAME)
if not os.path.exists(PATH):
    os.makedirs(PATH)


########################################################################
config = {
    "version": 1,

    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s | %(thread)6d | %(levelname)8s | %(name)s.%(funcName)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "streamFormatter": {
            "format": "%(asctime)s | %(levelname)7s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "debugFileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "fileFormatter",
            "level": "DEBUG",
            "filename": "{}".format(os.path.join(PATH, "debug.log")),
            "mode": "a",
            "maxBytes": MAX_FILE_SIZE,
            "backupCount": MAX_LOG_COUNT - 1
        },
        "consoleFileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "fileFormatter",
            "level": "INFO",
            "filename": "{}".format(os.path.join(PATH, "console.log")),
            "mode": "a",
            "maxBytes": MAX_FILE_SIZE,
            "backupCount": MAX_LOG_COUNT - 1
        },
        "errorFileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "fileFormatter",
            "level": "ERROR",
            "filename": "{}".format(os.path.join(PATH, "error.log")),
            "mode": "a",
            "maxBytes": MAX_FILE_SIZE,
            "backupCount": MAX_LOG_COUNT - 1
        },
        "streamHandler": {
            "class": "logging.StreamHandler",
            "formatter": "streamFormatter",
            "level": "INFO",
            "stream": sys.stdout
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["debugFileHandler", "consoleFileHandler", "errorFileHandler", "streamHandler"]
    }
}
