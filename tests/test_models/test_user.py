from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.user import User
from tests.test_models import clean_up


class TestCity(TestCase):
    def test_user_first_name(self):
        user = User()

        self.assertTrue(hasattr(user, "first_name"))
        self.assertIsInstance(user.first_name, str)

    def test_user_last_name(self):
        user = User()

        self.assertTrue(hasattr(user, "last_name"))
        self.assertIsInstance(user.last_name, str)

    def test_user_email(self):
        user = User()

        self.assertTrue(hasattr(user, "email"))
        self.assertIsInstance(user.email, str)

    def test_user_password(self):
        user = User()

        self.assertTrue(hasattr(user, "password"))
        self.assertIsInstance(user.password, str)

    def test_base_model_id(self):
        bm1 = User()
        bm2 = User()

        self.assertTrue(hasattr(bm1, "id"))
        self.assertNotEqual(bm1, bm2)
        self.assertIsInstance(UUID(bm1.id), UUID)
        self.assertIsInstance(bm1.id, str)

    def test_base_model_created_at(self):
        bm1 = User()

        self.assertTrue(hasattr(bm1, "created_at"))
        self.assertIsInstance(bm1.created_at, datetime)

    def test_base_model_updated_at(self):
        bm1 = User()

        self.assertTrue(hasattr(bm1, "updated_at"))
        self.assertIsInstance(bm1.created_at, datetime)

    def test_two_models_unique_ids(self):
        bm1 = User()
        bm2 = User()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self):
        bm1 = User()
        bm2 = User()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        bm1 = User()
        bm2 = User()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + dt_repr, user_str)
        self.assertIn("'updated_at': " + dt_repr, user_str)

    def test_args_unused(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_base_model__str__(self):
        user = User()

        string = f"[{user.__class__.__name__}] ({user.id}) {user.__dict__}"
        self.assertEqual(str(user), string)

    def test_base_model__repr__(self):
        user = User()

        string = f"[{user.__class__.__name__}] ({user.id}) {user.__dict__}"
        self.assertEqual(user.__repr__(), string)

    def test_base_model_save(self):
        user = User()
        user.save()
        storage.reload()
        new = [str(i) for i in storage.all().values()]
        self.assertIn(str(user), new)
        clean_up()

    def test_to_dict_type(self):
        user = User()
        self.assertTrue(dict, type(user.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def test_to_dict_contains_added_attributes(self):
        user = User()
        user.name = "Holberton"
        user.my_number = 98
        self.assertIn("name", user.to_dict())
        self.assertIn("my_number", user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        user = User()
        bm_dict = user.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dct = {
            "id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
            "created_at": "2024-03-08T19:07:48.367387",
            "updated_at": "2024-03-08T19:09:34.997818",
            "name": "hello",
            "__class__": "User"
        }
        user = User(**dct)
        self.assertDictEqual(user.to_dict(), dct)

    def test_contrast_to_dict_dunder_dict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)
