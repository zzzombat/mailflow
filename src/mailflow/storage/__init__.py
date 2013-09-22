from mailflow.front import app


class FSWrapper(object):
    """
    FS wrapper object for lazy initialization
    """

    __fs = None

    def __init__(self, fs_class_name, fs_kwargs):
        self.fs_class_name = fs_class_name
        self.fs_kwargs = fs_kwargs

    def __getattr__(self, value):
        if self.__fs is None:
            self.__fs = self.initialize_fs()

        return getattr(self.__fs, value)

    def initialize_fs(self):
        fs_class = self.get_class()
        return fs_class(**self.fs_kwargs)

    def get_class(self):
        module_name, class_name = self.fs_class_name.rsplit('.', 1)
        module = __import__(module_name, globals(), locals(), class_name)

        return getattr(module, class_name)

fs = FSWrapper(
    app.config['STORAGE_CLASS'],
    app.config['STORAGE_ARGS']
)
