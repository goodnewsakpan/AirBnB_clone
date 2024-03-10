from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.place import Place
from tests.test_models import clean_up


class TestPlace(TestCase):
    def test_place_city_id(self):
        place = Place()

        self.assertTrue(hasattr(place, "city_id"))
        self.assertIsInstance(place.city_id, str)

    def test_place_user_id(self):
        place = Place()

        self.assertTrue(hasattr(place, "user_id"))
        self.assertIsInstance(place.user_id, str)

    def test_place_name(self):
        place = Place()

        self.assertTrue(hasattr(place, "name"))
        self.assertIsInstance(place.name, str)

    def test_place_description(self):
        place = Place()

        self.assertTrue(hasattr(place, "description"))
        self.assertIsInstance(place.description, str)

    def test_place_number_rooms(self):
        place = Place()

        self.assertTrue(hasattr(place, "number_rooms"))
        self.assertIsInstance(place.number_rooms, int)

    def test_place_number_bathrooms(self):
        place = Place()

        self.assertTrue(hasattr(place, "number_bathrooms"))
        self.assertIsInstance(place.number_bathrooms, int)

    def test_place_max_guest(self):
        place = Place()

        self.assertTrue(hasattr(place, "max_guest"))
        self.assertIsInstance(place.max_guest, int)

    def test_place_price_by_night(self):
        place = Place()

        self.assertTrue(hasattr(place, "price_by_night"))
        self.assertIsInstance(place.price_by_night, int)

    def test_place_latitude(self):
        place = Place()

        self.assertTrue(hasattr(place, "latitude"))
        self.assertIsInstance(place.latitude, float)

    def test_place_longitude(self):
        place = Place()

        self.assertTrue(hasattr(place, "longitude"))
        self.assertIsInstance(place.longitude, float)

    def test_place_amenity_ids(self):
        place = Place()

        self.assertTrue(hasattr(place, "amenity_ids"))
        self.assertIsInstance(place.amenity_ids, list)

    def test_place_id(self):
        place1 = Place()
        place2 = Place()

        self.assertTrue(hasattr(place1, "id"))
        self.assertNotEqual(place1, place2)
        self.assertIsInstance(UUID(place1.id), UUID)
        self.assertIsInstance(place1.id, str)

    def test_place_created_at(self):
        place1 = Place()

        self.assertTrue(hasattr(place1, "created_at"))
        self.assertIsInstance(place1.created_at, datetime)

    def test_place_updated_at(self):
        place1 = Place()

        self.assertTrue(hasattr(place1, "updated_at"))
        self.assertIsInstance(place1.created_at, datetime)

    def test_two_models_unique_ids(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_two_models_different_created_at(self):
        place1 = Place()
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_two_models_different_updated_at(self):
        place1 = Place()
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        place_str = place.__str__()
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + dt_repr, place_str)
        self.assertIn("'updated_at': " + dt_repr, place_str)

    def test_args_unused(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_place__str__(self):
        place = Place()

        string = f"[{place.__class__.__name__}] ({place.id}) {place.__dict__}"
        self.assertEqual(str(place), string)

    def test_place__repr__(self):
        place = Place()

        string = f"[{place.__class__.__name__}] ({place.id}) {place.__dict__}"
        self.assertEqual(place.__repr__(), string)

    def test_place_save(self):
        place = Place()
        place.save()
        storage.reload()
        new = [str(i) for i in storage.all().values()]
        self.assertIn(str(place), new)
        clean_up()

    def test_to_dict_type(self):
        place = Place()
        self.assertTrue(dict, type(place.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        place = Place()
        place.name = "Holberton"
        place.my_number = 98
        self.assertIn("name", place.to_dict())
        self.assertIn("my_number", place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        dct = {
            "id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
            "created_at": "2024-03-08T19:07:48.367387",
            "updated_at": "2024-03-08T19:09:34.997818",
            "name": "hello",
            "__class__": "Place"
        }
        place = Place(**dct)
        self.assertDictEqual(place.to_dict(), dct)

    def test_contrast_to_dict_dunder_dict(self):
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)
