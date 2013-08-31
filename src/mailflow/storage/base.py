from abc import ABCMeta


class BaseStorage(object):
    __metaclass__ = ABCMeta

    def open(self, name, mode='rb'):
        """
        Calls _open method containg actual file retieving.
        """

        return self._open(name, mode)

    def save(self, name, content):
        """
        Validates file name  and calls _save for actual saving
        """
        if name is None:
            name = content.name

        return self._save(name, content)

    def read(self, name):
        file = self.open(name, mode='rb')
        content = file.read()
        file.close()

        return content

    def delete(self, name):
        raise NotImplementedError()

    def exists(self, name):
        raise NotImplementedError()
