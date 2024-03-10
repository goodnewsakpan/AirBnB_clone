#!/usr/bin/python3
"""
Import modules with functions related to
JSON file handling files and classes
"""
import json
from os import path

from libs import classes


class FileStorage:
    """A class for handling storage operations using JSON files"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Retrieve all objects stored in the file storage"""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the file storage"""
        self.__objects |= {f"{obj.__class__.__name__}.{obj.id}": obj}

    def save(self):
        """saves the objects in the file storage to the JSON file"""
        with open(self.__file_path, "w") as js:
            ser = {
                key: value.to_dict()
                for key, value in self.__objects.items()
            }
            js.write(json.dumps(ser))

    def reload(self):
        """Reloads objects from the JSON file into the file storage"""
        if not path.exists(self.__file_path):
            return
        with open(self.__file_path) as js:
            des = json.loads(js.read())
            self.__objects = {
                key: classes[key.split(".")[0]](**value)
                for key, value in des.items()
            }

    def get(self, key):
        """Gets an object from the file storage by its key"""
        return self.all()[key]

    def get_all(self, key=None):
        """Gets all objects from the storage optionally filtered by the key"""
        if not key:
            return [str(i) for i in self.all().values()]
        return list(filter(
            lambda search_found: key in str(search_found),
            self.all().values()
        ))

    def delete(self, key):
        """Deletes an object from tje file storage by its key"""
        del self.all()[key]
        self.save()
