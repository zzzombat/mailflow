# -*- coding: utf-8 -*-
class StorageError(Exception):
    """
    Base storage-related exception
    """
    pass


class FileSystemError(StorageError):

    def __init__(self, msg, path):
        self.msg = msg
        self.path = path

    def __str__(self):
        return "{msg} on path: {path}".format(
            msg=self.msg,
            path=self.path
        )
