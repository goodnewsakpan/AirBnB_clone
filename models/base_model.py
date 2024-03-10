from datetime import datetime
from uuid import uuid4

from . import storage


class BaseModel:
    def __init__(self, *args, **kwargs):
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
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def __repr__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        return self.__dict__ | {
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "__class__": self.__class__.__name__,
        }

    @classmethod
    def all(cls):
        return storage.get_all(cls.__name__)

    @classmethod
    def count(cls):
        return len(cls.all())

    @classmethod
    def show(cls, ids):
        return storage.get(f"{cls.__name__}.{ids}")

    @classmethod
    def destroy(cls, ids):
        storage.delete(f"{cls.__name__}.{ids}")

    @classmethod
    def update(cls, ids, attr=None, value=None):
        obj = cls.show(ids)
        if isinstance(attr, dict):
            for key, value in attr.items():
                setattr(obj, key, value)
        else:
            setattr(obj, attr, value)
        obj.save()
