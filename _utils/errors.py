# Universal Errors
class Error(Exception):
    pass

class ReadOnlyPropertyError(Error):
    pass


class MustOverrideError(Error):
    pass