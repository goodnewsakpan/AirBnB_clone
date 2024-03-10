from datetime import datetime
from unittest import TestCase
from uuid import UUID

from models import storage
from models.state import State
from tests.test_models import clean_up


class TestState(TestCase):
	def test_state_name(self):
		state = State()

		self.assertTrue(hasattr(state, "name"))
		self.assertIsInstance(state.name, str)

	def test_state_id(self):
		state1 = State()
		state2 = State()

		self.assertTrue(hasattr(state1, "id"))
		self.assertNotEqual(state1, state2)
		self.assertIsInstance(UUID(state1.id), UUID)
		self.assertIsInstance(state1.id, str)

	def test_state_created_at(self):
		state1 = State()

		self.assertTrue(hasattr(state1, "created_at"))
		self.assertIsInstance(state1.created_at, datetime)

	def test_state_updated_at(self):
		state1 = State()

		self.assertTrue(hasattr(state1, "updated_at"))
		self.assertIsInstance(state1.created_at, datetime)

	def test_two_models_unique_ids(self):
		state1 = State()
		state2 = State()
		self.assertNotEqual(state1.id, state2.id)

	def test_two_models_different_created_at(self):
		state1 = State()
		state2 = State()
		self.assertLess(state1.created_at, state2.created_at)

	def test_two_models_different_updated_at(self):
		state1 = State()
		state2 = State()
		self.assertLess(state1.updated_at, state2.updated_at)

	def test_str_representation(self):
		dt = datetime.today()
		dt_repr = repr(dt)
		state = State()
		state.id = "123456"
		state.created_at = state.updated_at = dt
		state_str = state.__str__()
		self.assertIn("[State] (123456)", state_str)
		self.assertIn("'id': '123456'", state_str)
		self.assertIn("'created_at': " + dt_repr, state_str)
		self.assertIn("'updated_at': " + dt_repr, state_str)

	def test_args_unused(self):
		state = State(None)
		self.assertNotIn(None, state.__dict__.values())

	def test_instantiation_with_kwargs(self):
		dt = datetime.today()
		dt_iso = dt.isoformat()
		state = State(id="345", created_at=dt_iso, updated_at=dt_iso)
		self.assertEqual(state.id, "345")
		self.assertEqual(state.created_at, dt)
		self.assertEqual(state.updated_at, dt)

	def test_instantiation_with_None_kwargs(self):
		with self.assertRaises(TypeError):
			State(id=None, created_at=None, updated_at=None)

	def test_instantiation_with_args_and_kwargs(self):
		dt = datetime.today()
		dt_iso = dt.isoformat()
		state = State("12", id="345", created_at=dt_iso, updated_at=dt_iso)
		self.assertEqual(state.id, "345")
		self.assertEqual(state.created_at, dt)
		self.assertEqual(state.updated_at, dt)

	def test_state__str__(self):
		state = State()

		string = f"[{state.__class__.__name__}] ({state.id}) {state.__dict__}"
		self.assertEqual(str(state), string)

	def test_state__repr__(self):
		state = State()

		string = f"[{state.__class__.__name__}] ({state.id}) {state.__dict__}"
		self.assertEqual(state.__repr__(), string)

	def test_state_save(self):
		state = State()
		state.save()
		storage.reload()
		new = [str(i) for i in storage.all().values()]
		self.assertIn(str(state), new)
		clean_up()

	def test_to_dict_type(self):
		state = State()
		self.assertTrue(dict, type(state.to_dict()))

	def test_to_dict_contains_correct_keys(self):
		state = State()
		self.assertIn("id", state.to_dict())
		self.assertIn("created_at", state.to_dict())
		self.assertIn("updated_at", state.to_dict())
		self.assertIn("__class__", state.to_dict())

	def test_to_dict_contains_added_attributes(self):
		state = State()
		state.name = "Holberton"
		state.my_number = 98
		self.assertIn("name", state.to_dict())
		self.assertIn("my_number", state.to_dict())

	def test_to_dict_datetime_attributes_are_strs(self):
		state = State()
		state_dict = state.to_dict()
		self.assertEqual(str, type(state_dict["created_at"]))
		self.assertEqual(str, type(state_dict["updated_at"]))

	def test_to_dict_output(self):
		dct = {
			"id": "d17d6b56-2c95-4c50-96d3-e4e14c47f45b",
			"created_at": "2024-03-08T19:07:48.367387",
			"updated_at": "2024-03-08T19:09:34.997818",
			"name": "hello",
			"__class__": "State"
		}
		state = State(**dct)
		self.assertDictEqual(state.to_dict(), dct)

	def test_contrast_to_dict_dunder_dict(self):
		state = State()
		self.assertNotEqual(state.to_dict(), state.__dict__)
