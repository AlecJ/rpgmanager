import random
import string

def generate_random_string(chars=None, length=4):
    """
    Used by various services to create easy to remember
    room codes.

    :param chars: List of string, Characters to use if provided, otherwise just upper and lower case
    :param length: Integer, The length the generated string should be
    :return: String, the randomly generated string
    """
     # Allow upper and lower case characters
    letters = string.ascii_lowercase + string.ascii_uppercase
   
    # remove exceptions
    exceptions = ['I', 'l']
    [letters.replace(c, "") for c in exceptions]

    # Use specific character pool if provided
    if chars:
        letters = chars

    return ''.join(random.choice(letters) for i in range(length))