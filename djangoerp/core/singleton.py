# Inspired by http://stackoverflow.com/a/7469395/1063729

class Singleton(type):
    """Singleton pattern.
    """
    def __init__(cls, name, bases, dicts):
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance
