from passgen import passgen


def generate_one_time_password():
    """passgen modules used to generate one time password"""
    value = passgen(length=6, case='both', digits=True, letters=True, punctuation=False)
    return value
