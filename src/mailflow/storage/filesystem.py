import os.path
from base import BaseStorage
from exceptions import FileSystemError


class FileSystemStorage(BaseStorage):

    def __init__(self, location=None):
        self.base_location = location
        self.location = os.path.abspath(self.base_location)
        if not os.path.exists(self.location):
            raise FileSystemError("Location doesn't exist", path=self.location)

    def __str__(self):
        return "<FlieSystemStorage at location {0}".format(self.location)

    def _open(self, name, mode):
        return open(self._get_absolute_path(name), mode)

    def _save(self, name, content):
        file = self.open(name, mode='w')
        file.write(content)
        file.close()

    def _get_absolute_path(self, name):
        return os.path.join(self.location, name)
