from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.base_model import BaseModel
from tests.test_models import clean_up


class TestBaseModel(TestCase):
    def test_base_model_id(self):
        bm1 = BaseModel()
        bm2 = BaseModel()

        self.assertTrue(hasattr(bm1, "id"))
        self.assertNotEqual(bm1, bm2)
        self.assertIsInstance(UUID(bm1.id), UUID)
        self.assertIsInstance(bm1.id, str)

    def test_base_model_created_at(self):
        bm1 = BaseModel()

        self.assertTrue(hasattr(bm1, "created_at"))
        self.assertIsInstance(bm1.created_at, datetime)

    def test_base_model_updated_at(self):
        bm1 = BaseModel()

        self.assertTrue(hasattr(bm1, "updated_at"))
        self.assertIsInstance(bm1.created_at, datetime)

    def test_two_models_unique_ids(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_base_model__str__(self):
        bm = BaseModel()

        string = f"[{bm.__class__.__name__}] ({bm.id}) {bm.__dict__}"
        self.assertEqual(str(bm), string)

    def test_base_model__repr__(self):
        bm = BaseModel()

        string = f"[{bm.__class__.__name__}] ({bm.id}) {bm.__dict__}"
        self.assertEqual(bm.__repr__(), string)

    def test_base_model_save(self):
        bm = BaseModel()
        bm.save()
        storage.reload()
        new = [str(i) for i in storage.all().values()]
        self.assertIn(str(bm), new)
        clean_up()

    def test_to_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bm = BaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dct = {
            "id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
            "created_at": "2024-03-08T19:07:48.367387",
            "updated_at": "2024-03-08T19:09:34.997818",
            "name": "hello",
            "__class__": "BaseModel"
        }
        bm = BaseModel(**dct)
        self.assertDictEqual(bm.to_dict(), dct)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)
