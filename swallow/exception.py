class SwallowException(Exception):
    pass


class StopImport(SwallowException):
    """Stop current builder import"""
    pass


class BuilderException(SwallowException):
    pass


class StoppedImport(BuilderException):
    pass

class PopulationError(BuilderException):
    pass
