from dateutil import parser
import jdatetime
import locale
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


def datetime_converter(date_utc):
    locale.setlocale(locale.LC_ALL, "fa_IR")
    date = parser.parse(date_utc)
    persian_date = jdatetime.date.fromgregorian(date=date).strftime("%a, %d %b %Y")
    persian_time = date.time()
    tup = (persian_date, persian_time)
    return tup
