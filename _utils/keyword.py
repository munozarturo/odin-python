"""
Module used to define the `iskeyword` and `issofkeyword` functions;
used to check if a string is a python keyword.
"""

# list of python keywords
from _utils.validation import val_instance


kwlist = [
    'False',
    'None',
    'True',
    'and',
    'as',
    'assert',
    'async',
    'await',
    'break',
    'class',
    'continue',
    'def',
    'del',
    'elif',
    'else',
    'except',
    'finally',
    'for',
    'from',
    'global',
    'if',
    'import',
    'in',
    'is',
    'lambda',
    'nonlocal',
    'not',
    'or',
    'pass',
    'raise',
    'return',
    'try',
    'while',
    'with',
    'yield'
]

# list of python soft keywords
softkwlist = [
    '_',
    'case',
    'match'
]


def iskeyword(s: str) -> bool:
    """
    Check if a string is a python keyword.

    Args:
        s (str): String to be checked.

    Returns:
        bool: True if the string is a python keyword, False otherwise.
    """
    
    # check if the input object is a string
    val_instance(s, str)

    return s in kwlist


def issofkeyword(s: str) -> bool:
    """
    Check if a string is a soft python keyword.

    Args:
        s (str): String to be checked.

    Returns:
        bool: True if the string is a python keyword, False otherwise.
    """
    
    # check if input object is a string
    val_instance(s, str)
    
    return s in softkwlist