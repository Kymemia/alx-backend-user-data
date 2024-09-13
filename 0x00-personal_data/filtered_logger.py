#!/usr/bin/env python3

"""
this is a function that returns the log message obfuscated
Args:
    fields:  a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing
    by which character is separating all fields
    in the log line (message)
"""
import re
import logging
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """
    method definition that returns the log message
    """
    return re.sub(f'({"|".join(fields)})=.*?{separator}',
                  lambda match: f"{match.group(1)}={redaction}{separator}",
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        pattern = "|".join(self.fields)
        record.msg = re.sub(fr'({pattern})=([^;]+)',
                            fr'\1={self.REDACTION}',
                            record.msg
                            )
        return super().format(record)
