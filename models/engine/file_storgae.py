import json
from os import path

from libs import classes


class FileStorage:
	__file_path = "file.json"
	__objects = {}

	def all(self):
		return self.__objects

	def new(self, obj):
		self.__objects |= {f"{obj.__class__.__name__}.{obj.id}": obj}

	def save(self):
		with open(self.__file_path, "w") as js:
			ser = {key: value.to_dict() for key, value in self.__objects.items()}
			js.write(json.dumps(ser))

	def reload(self):
		if not path.exists(self.__file_path):
			return
		with open(self.__file_path) as js:
			des = json.loads(js.read())
			self.__objects = {
				key: classes[key.split(".")[0]](**value)
				for key, value in des.items()
			}

	def get(self, key):
		return self.all()[key]

	def get_all(self, key=None):
		if not key:
			return [str(i) for i in self.all().values()]
		return list(filter(
			lambda search_found: key in str(search_found),
			self.all().values()
		))

	def delete(self, key):
		del self.all()[key]
		self.save()
