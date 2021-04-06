"""
Custom exceptions
"""


class UnknownMoveTypeError(TypeError):
    """Unknown move type"""

    pass


class UnknownGameStatusError(ValueError):
    """Unknown game status"""

    pass
