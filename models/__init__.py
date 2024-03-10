#!/usr/bin/ python3

"""script to initialize classes and storage for the HBnB clone"""
from libs import get_classes, classes
from .engine.file_storage import FileStorage

__all__ = ("classes", "storage")

storage = FileStorage()
get_classes()
storage.reload()
