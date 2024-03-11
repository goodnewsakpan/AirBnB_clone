from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.review import Review
from tests.test_models import clean_up


class TestReview(TestCase):
    def test_review_state_id(self):
        review = Review()

        self.assertTrue(hasattr(review, "place_id"))
        self.assertIsInstance(review.place_id, str)

    def test_review_user_id(self):
        review = Review()

        self.assertTrue(hasattr(review, "user_id"))
        self.assertIsInstance(review.user_id, str)

    def test_review_text(self):
        review = Review()

        self.assertTrue(hasattr(review, "text"))
        self.assertIsInstance(review.text, str)

    def test_review_id(self):
        review1 = Review()
        review2 = Review()

        self.assertTrue(hasattr(review1, "id"))
        self.assertNotEqual(review1, review2)
        self.assertIsInstance(UUID(review1.id), UUID)
        self.assertIsInstance(review1.id, str)

    def test_review_created_at(self):
        review1 = Review()

        self.assertTrue(hasattr(review1, "created_at"))
        self.assertIsInstance(review1.created_at, datetime)

    def test_review_updated_at(self):
        review1 = Review()

        self.assertTrue(hasattr(review1, "updated_at"))
        self.assertIsInstance(review1.created_at, datetime)

    def test_two_models_unique_ids(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_two_models_different_created_at(self):
        review1 = Review()
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_two_models_different_updated_at(self):
        review1 = Review()
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        review_str = review.__str__()
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + dt_repr, review_str)
        self.assertIn("'updated_at': " + dt_repr, review_str)

    def test_args_unused(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_review__str__(self):
        review = Review()

        string = (f"[{review.__class__.__name__}] "
                  f"({review.id}) {review.__dict__}")
        self.assertEqual(str(review), string)

    def test_review__repr__(self):
        review = Review()

        string = (f"[{review.__class__.__name__}] "
                  f"({review.id}) {review.__dict__}")
        self.assertEqual(review.__repr__(), string)

    def test_review_save(self):
        review = Review()
        review.save()
        storage.reload()
        new = [str(i) for i in storage.all().values()]
        self.assertIn(str(review), new)
        clean_up()

    def test_to_dict_type(self):
        review = Review()
        self.assertTrue(dict, type(review.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        review = Review()
        review.name = "Holberton"
        review.my_number = 98
        self.assertIn("name", review.to_dict())
        self.assertIn("my_number", review.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        dct = {
            "id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
            "created_at": "2024-03-08T19:07:48.367387",
            "updated_at": "2024-03-08T19:09:34.997818",
            "name": "hello",
            "__class__": "Review"
        }
        review = Review(**dct)
        self.assertDictEqual(review.to_dict(), dct)

    def test_contrast_to_dict_dunder_dict(self):
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)
