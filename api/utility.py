def make_uniform_string(input_string: str) -> str:
    """
    Convert a string to a uniform format by removing leading/trailing whitespace,
    converting to lowercase, and removing spaces.

    Args:
        input_string (str): The string to be converted.

    Returns:
        str: The uniform string.
    """
    return input_string.strip().lower().replace(" ", "")


def translate_special_chars(input_string: str) -> str:
    """
    Translate special characters in the string to their alphabetic equivalents.

    Args:
        input_string (str): The string to be translated.

    Returns:
        str: The translated string.
    """
    return input_string.translate(str.maketrans("@0$1!3#5+7", "aosiieshst"))
