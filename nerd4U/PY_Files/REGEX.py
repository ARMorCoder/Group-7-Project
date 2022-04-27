import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
PHONE_REGEX = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"


def Regex_Input(regex, txt):
    return (re.search(regex, txt)) == "None"


def Regex_Email(txt):
    return Regex_Input(EMAIL_REGEX, txt)


def Regex_Phone(txt):
    return Regex_Input(PHONE_REGEX, txt)
