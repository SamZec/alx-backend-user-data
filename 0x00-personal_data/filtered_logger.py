#!/usr/bin/env python3
"""filtered_logger.py - Regex-ing"""


import re
import os
import logging
import mysql.connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for item in fields:
        message = re.sub(rf"{item}=(.*?)\{separator}",
                         f'{item}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Intantiate objects"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """records loggings"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object."""
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(handler)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", 'root')
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", '')
    host = os.getenv("PERSONAL_DATA_DB_HOST", 'localhost')
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   database=database)
    return conn
