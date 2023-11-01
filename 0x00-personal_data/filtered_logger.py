#!/usr/bin/env python3
"""filtered_logger.py - Regex-ing"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for item in fields:
        message = re.sub(rf"{item}=(.*?)\{separator}",
                         f'{item}={redaction}{separator}', message)
    return message
