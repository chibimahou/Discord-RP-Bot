import re
from datetime import datetime
 
def validate_alphanumeric(input_str):
    pattern = re.compile(r'^\w+$')
    return bool(pattern.match(input_str))

def validate_height(input_str):
    pattern = re.compile(r"^\d+'\d+\"$")
    return bool(pattern.match(input_str))

def validate_age(input_str):
    return input_str.isdigit()

def validate_date(input_str):
    date_formats = [
        '%m/%d/%Y',  # 12/25/2022
        '%d/%b/%Y',  # 25/DEC/2022
        '%d-%b-%Y',  # 25-DEC-2022
        '%Y-%m-%d',  # 2022-12-25
        '%d %B %Y',  # 25 December 2022
        '%d %b %Y',  # 25 Dec 2022
        '%d/%m/%Y',  # 25/12/2022
        '%d-%m-%Y',  # 25-12-2022
    ]
    
    for date_format in date_formats:
        try:
            return datetime.strptime(input_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{input_str}' is not supported.")


def validate_text(input_str):
    pattern = re.compile(r"^[a-zA-Z0-9.,'\"!? ]+$")
    return bool(pattern.match(input_str))

def validate_level(input_str):
    return input_str.isdigit() and int(input_str) >= 0