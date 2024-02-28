import logging

class EnvironmentVariableNotFoundError(Exception):
    """Exception raised when an expected environment variable is not found."""
    pass