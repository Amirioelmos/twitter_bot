import re


def arabic_to_eng_number(number):
    number = str(number)
    return number.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


def eng_to_arabic_number(number):
    number = str(number)
    return number.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))


def phone_number_validation(phone_num):
    if re.match(r'^(\+98|0098|0)?9\d{9}$', phone_num):
        return True
    else:
        return False


def standardize_phone_number(number):
    number_str = str(number)
    if number_str.startswith("0098"):
        return "+98" + number_str[4:]
    elif number_str.startswith("0"):
        return "+98" + number_str[1:]
