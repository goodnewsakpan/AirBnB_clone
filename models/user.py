from models.base_model import BaseModel

"""Base Model"""


class User(BaseModel):
    """A class rperesenting the user information"""
    first_name = ""
    last_name = ""
    email = ""
    password = ""
