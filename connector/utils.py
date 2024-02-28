import logging
import os
from dotenv import load_dotenv

from .custom_errors import EnvironmentVariableNotFoundError


def load_dotenv_file(file_path: str) -> bool:
    """
    Load environment variables from a specified .env file.

    This function logs the action of loading environment variables and then
    attempts to load them using the given file path to the .env file. If the
    specified .env file does not exist, it raises a FileNotFoundError. It's
    designed to be used at the start of an application to initialize
    configuration settings from an environment file.

    Parameters:
    - file_path (str): The path to the .env file containing environment variables.

    Returns:
    - bool: True if the environment variables were loaded successfully.

    Raises:
    - FileNotFoundError: If the specified .env file does not exist.

    Side effects:
    - Reads from the filesystem based on the given file_path.
    - Calls logging.info, which can write to stdout or a log file depending on the logging configuration.
    - Modifies the environment variables of the running process according to the contents of the .env file.
    """
    logging.info("Loading environment variable file")

    if not os.path.exists(file_path):
        logging.info("Loading environment variable file failed!")
        raise FileNotFoundError(f"The specified .env file does not exist: {file_path}")

    load_dotenv(dotenv_path=file_path)
    logging.info("Loading environment variable file success!")
    return True


def load_env_var(variable: str) -> str:
    """
    Retrieve an environment variable by its name.

    Attempts to retrieve the value of an environment variable specified by
    'variable'. If the environment variable is not found, raises a
    EnvironmentVariableNotFoundError.

    Parameters:
    - variable (str): The name of the environment variable to retrieve.

    Returns:
    - str: The value of the environment variable.

    Raises:
    - EnvironmentVariableNotFoundError: If the specified environment variable is not found.
    """
    logging.info("Loading environment variable")
    env_var = os.getenv(variable)
    if env_var is None:
        logging.info(f"Environment variable '{variable}' not found")
        raise EnvironmentVariableNotFoundError(f"Environment variable '{variable}' not found")
    logging.info(f"Environment variable '{variable}' loaded")
    return env_var