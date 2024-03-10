from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.city import City
from tests.test_models import clean_up


class TestCity(TestCase):
	def test_city_state_id(self):
		city = City()

		self.assertTrue(hasattr(city, "state_id"))
		self.assertIsInstance(city.state_id, str)

	def test_city_name(self):
		city = City()

		self.assertTrue(hasattr(city, "name"))
		self.assertIsInstance(city.name, str)

	def test_city_id(self):
		city1 = City()
		city2 = City()

		self.assertTrue(hasattr(city1, "id"))
		self.assertNotEqual(city1, city2)
		self.assertIsInstance(UUID(city1.id), UUID)
		self.assertIsInstance(city1.id, str)

	def test_city_created_at(self):
		city1 = City()

		self.assertTrue(hasattr(city1, "created_at"))
		self.assertIsInstance(city1.created_at, datetime)

	def test_city_updated_at(self):
		city1 = City()

		self.assertTrue(hasattr(city1, "updated_at"))
		self.assertIsInstance(city1.created_at, datetime)

	def test_two_models_unique_ids(self):
		city1 = City()
		city2 = City()
		self.assertNotEqual(city1.id, city2.id)

	def test_two_models_different_created_at(self):
		city1 = City()
		city2 = City()
		self.assertLess(city1.created_at, city2.created_at)

	def test_two_models_different_updated_at(self):
		city1 = City()
		city2 = City()
		self.assertLess(city1.updated_at, city2.updated_at)

	def test_str_representation(self):
		dt = datetime.today()
		dt_repr = repr(dt)
		city = City()
		city.id = "123456"
		city.created_at = city.updated_at = dt
		city_str = city.__str__()
		self.assertIn("[City] (123456)", city_str)
		self.assertIn("'id': '123456'", city_str)
		self.assertIn("'created_at': " + dt_repr, city_str)
		self.assertIn("'updated_at': " + dt_repr, city_str)

	def test_args_unused(self):
		city = City(None)
		self.assertNotIn(None, city.__dict__.values())

	def test_instantiation_with_kwargs(self):
		dt = datetime.today()
		dt_iso = dt.isoformat()
		city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
		self.assertEqual(city.id, "345")
		self.assertEqual(city.created_at, dt)
		self.assertEqual(city.updated_at, dt)

	def test_instantiation_with_None_kwargs(self):
		with self.assertRaises(TypeError):
			City(id=None, created_at=None, updated_at=None)

	def test_instantiation_with_args_and_kwargs(self):
		dt = datetime.today()
		dt_iso = dt.isoformat()
		city = City("12", id="345", created_at=dt_iso, updated_at=dt_iso)
		self.assertEqual(city.id, "345")
		self.assertEqual(city.created_at, dt)
		self.assertEqual(city.updated_at, dt)

	def test_city__str__(self):
		city = City()

		string = f"[{city.__class__.__name__}] ({city.id}) {city.__dict__}"
		self.assertEqual(str(city), string)

	def test_city__repr__(self):
		city = City()

		string = f"[{city.__class__.__name__}] ({city.id}) {city.__dict__}"
		self.assertEqual(city.__repr__(), string)

	def test_city_save(self):
		city = City()
		city.save()
		storage.reload()
		new = [str(i) for i in storage.all().values()]
		self.assertIn(str(city), new)
		clean_up()

	def test_to_dict_type(self):
		city = City()
		self.assertTrue(dict, type(city.to_dict()))

	def test_to_dict_contains_correct_keys(self):
		city = City()
		self.assertIn("id", city.to_dict())
		self.assertIn("created_at", city.to_dict())
		self.assertIn("updated_at", city.to_dict())
		self.assertIn("__class__", city.to_dict())

	def test_to_dict_contains_added_attributes(self):
		city = City()
		city.name = "Holberton"
		city.my_number = 98
		self.assertIn("name", city.to_dict())
		self.assertIn("my_number", city.to_dict())

	def test_to_dict_datetime_attributes_are_strs(self):
		city = City()
		city_dict = city.to_dict()
		self.assertEqual(str, type(city_dict["created_at"]))
		self.assertEqual(str, type(city_dict["updated_at"]))

	def test_to_dict_output(self):
		dct = {
			"id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
			"created_at": "2024-03-08T19:07:48.367387",
			"updated_at": "2024-03-08T19:09:34.997818",
			"name": "hello",
			"__class__": "City"
		}
		city = City(**dct)
		self.assertDictEqual(city.to_dict(), dct)

	def test_contrast_to_dict_dunder_dict(self):
		city = City()
		self.assertNotEqual(city.to_dict(), city.__dict__)
