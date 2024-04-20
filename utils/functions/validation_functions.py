import re
from datetime import datetime
 
def validate_alphanumeric(input_str):
    """Validate string to contain only alphanumeric characters and underscores."""
    pattern = re.compile(r'^\w+$')
    return bool(pattern.match(input_str))

def validate_height(input_str):
    """Validate string to be a valid height format, e.g., 5'2"."""
    pattern = re.compile(r"^\d+'\d+\"$")
    return bool(pattern.match(input_str))

def validate_age(input_str):
    """Validate string to be a valid age (integer)."""
    return input_str.isdigit()

def validate_date(input_str):
    """Validate string to be a valid date."""
    try:
        datetime.strptime(input_str, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def validate_text(input_str):
    """Validate string to be a valid text without special characters."""
    pattern = re.compile(r"^[a-zA-Z0-9.,'\"!? ]+$")
    return bool(pattern.match(input_str))

def validate_level(input_str):
    """Validate string to be a valid level (integer) and non-negative."""
    return input_str.isdigit() and int(input_str) >= 0