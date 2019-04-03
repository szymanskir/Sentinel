import pickle
from datetime import datetime
from typing import Any


def read_pickle(filepath: str):
    with open(filepath, 'rb') as f:
        content = pickle.load(f)

    return content


def write_pickle(obj: Any, filepath: str):
    with open(filepath, 'wb') as save_file:
        pickle.dump(obj, save_file)


def datetime_to_unix_timestamp(dt: str):
    unix_timestamp = round(datetime.strptime(
        dt, '%Y-%m-%d').timestamp())

    return unix_timestamp
