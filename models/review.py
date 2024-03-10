from .base_model import BaseModel

"""Base Model"""


class Review(BaseModel):
    """A class to show review in the system"""
    place_id = ""
    user_id = ""
    text = ""
