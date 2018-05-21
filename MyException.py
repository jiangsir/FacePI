class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class responseError(Error):
    """Exception raised for errors when response error.
    """

    def __init__(self, message):
        self.message = message


