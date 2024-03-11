from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.amenity import Amenity
from tests.test_models import clean_up


class TestAmenity(TestCase):

    def test_amenity_name(self):
        amenity = Amenity()

        self.assertTrue(hasattr(amenity, "name"))
        self.assertIsInstance(amenity.name, str)

    def test_amenity_id(self):
        amenity1 = Amenity()
        amenity2 = Amenity()

        self.assertTrue(hasattr(amenity1, "id"))
        self.assertNotEqual(amenity1, amenity2)
        self.assertIsInstance(UUID(amenity1.id), UUID)
        self.assertIsInstance(amenity1.id, str)

    def test_amenity_created_at(self):
        amenity1 = Amenity()

        self.assertTrue(hasattr(amenity1, "created_at"))
        self.assertIsInstance(amenity1.created_at, datetime)

    def test_amenity_updated_at(self):
        amenity1 = Amenity()

        self.assertTrue(hasattr(amenity1, "updated_at"))
        self.assertIsInstance(amenity1.created_at, datetime)

    def test_two_models_unique_ids(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_two_models_different_created_at(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_two_models_different_updated_at(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        amenity_str = amenity.__str__()
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + dt_repr, amenity_str)
        self.assertIn("'updated_at': " + dt_repr, amenity_str)

    def test_args_unused(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    def test_amenity__str__(self):
        amenity = Amenity()

        string = (f"[{amenity.__class__.__name__}] "
                  f"({amenity.id}) {amenity.__dict__}")
        self.assertEqual(str(amenity), string)

    def test_amenity__repr__(self):
        amenity = Amenity()

        string = (f"[{amenity.__class__.__name__}] "
                  f"({amenity.id}) {amenity.__dict__}")
        self.assertEqual(amenity.__repr__(), string)

    def test_amenity_save(self):
        amenity = Amenity()
        amenity.save()
        storage.reload()
        new = [str(i) for i in storage.all().values()]
        self.assertIn(str(amenity), new)
        clean_up()

    def test_to_dict_type(self):
        amenity = Amenity()
        self.assertTrue(dict, type(amenity.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amenity = Amenity()
        amenity.name = "Holberton"
        amenity.my_number = 98
        self.assertIn("name", amenity.to_dict())
        self.assertIn("my_number", amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        dct = {
            "id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
            "created_at": "2024-03-08T19:07:48.367387",
            "updated_at": "2024-03-08T19:09:34.997818",
            "name": "hello",
            "__class__": "Amenity"
        }
        amenity = Amenity(**dct)
        self.assertDictEqual(amenity.to_dict(), dct)

    def test_contrast_to_dict_dunder_dict(self):
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)
