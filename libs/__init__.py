classes = {}


def get_classes():
    from models.base_model import BaseModel
    from models.user import User
    from models.city import City
    from models.place import Place
    from models.amenity import Amenity
    from models.state import State
    from models.review import Review

    global classes
    classes.update({
        "BaseModel": BaseModel,
        "User": User,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "State": State,
        "Review": Review
    })
