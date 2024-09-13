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


def filter_datum(fields, redaction, message, separator):
    """
    method definition that returns the log message
    """
    return re.sub(f'({"|".join(fields)})=.*?{separator}',
                  lambda match: f"{match.group(1)}={redaction}{separator}",
                  message)
