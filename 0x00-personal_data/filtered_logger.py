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
    conn = mysql.connector.connect(
                                   host=host,
                                   database=database,
                                   user=username,
                                   password=password
                                   )
    return conn


def main() -> None:
    """retrieve all rows in the users table"""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users;")
    for item in cur:
        ms = f'name={item[0]};email={item[1]};phone={item[2]};'\
             f'ssn={item[3]};password={item[4]};ip={item[5]};'\
             f'last_login={item[6]};user_agent={item[7]};'
        log_record = logging.LogRecord("my_logger",
                                       logging.INFO, None, None,
                                       ms, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        print(formatter.format(log_record))


if __name__ == '__main__':
    main()
