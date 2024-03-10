#!/usr/bin/python3

"""Import modules datetime, uuid4 and storage"""
from datetime import datetime
from uuid import uuid4

from . import storage


class BaseModel:
    """A base class for other models in the system"""

    def __init__(self, *args, **kwargs):
        """instance of a new basemodel"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.fromisoformat(value))
                    continue
                setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            storage.new(self)

    def __str__(self):
        """return a string representation of BaseModel instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def __repr__(self):
        """returns an instance of a string representation"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """saves the instance"""
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        """converts the instnace to a dictionary"""
        dt = self.__dict__.copy()
        dt.update({
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "__class__": self.__class__.__name__,
        })
        return dt

    @classmethod
    def all(cls):
        """gets all instances of the class"""
        return storage.get_all(cls.__name__)

    @classmethod
    def count(cls):
        """Gets the counts of the instance"""
        return len(cls.all())

    @classmethod
    def show(cls, ids):
        """Shows the instance by its ID"""
        return storage.get(f"{cls.__name__}.{ids}")

    @classmethod
    def destroy(cls, ids):
        """Destroys an instance by its ID"""
        storage.delete(f"{cls.__name__}.{ids}")

    @classmethod
    def update(cls, ids, attr=None, value=None):
        """Updates the instance or attributes by its ID"""
        obj = cls.show(ids)
        if isinstance(attr, dict):
            for key, value in attr.items():
                setattr(obj, key, value)
        else:
            setattr(obj, attr, value)
        obj.save()
