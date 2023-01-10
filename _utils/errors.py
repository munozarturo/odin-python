"""
Module to define custom exceptions in this module.    
"""

# Universal Errors

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ReadOnlyPropertyError(Error):
    """Base class for errors coming from read only property deletions."""
    pass


class RequiredOverwrite(Error):
    """Base class for errors coming from methods that must be overridden."""
    pass