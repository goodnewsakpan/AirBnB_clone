from libs import get_classes, classes
from .engine.file_storgae import FileStorage

__all__ = ("classes", "storage")

storage = FileStorage()
get_classes()
storage.reload()
