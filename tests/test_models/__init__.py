from contextlib import suppress
from os import remove


def clean_up():
    with suppress(IOError, FileNotFoundError):
        remove("file.json")
