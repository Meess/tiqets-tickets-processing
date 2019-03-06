"""
This file contains functions and classes for reading datasets from
files or other artifacts.
"""

import pandas as pd


def csv(data_path, dtype='object'):
    return pd.read_csv(data_path, dtype='object')
