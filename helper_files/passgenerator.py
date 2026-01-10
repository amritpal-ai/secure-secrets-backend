import random
import string

def generate_password(length=12):
    # Make sure the password is at least 4 characters long to fit all categories


    # Lists of characters from each category
    uppercase_letters = string.ascii_uppercase  # A-Z
    lowercase_letters = string.ascii_lowercase  # a-z
    digits = string.digits                      # 0-9
    symbols = "!#$*+-_.?"               # Special characters like !, @, #

    # Pick one character from each category to guarantee inclusion
    password_chars = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Now fill the rest of the password length with random choices from all allowed chars
    all_chars = uppercase_letters + lowercase_letters + digits + symbols

    # Calculate how many more characters we need to fill after the 4 guaranteed ones
    remaining_length = length - 4

    # Pick random characters one by one and add them to the password list
    for _ in range(remaining_length):
        password_chars.append(random.choice(all_chars))

    # Shuffle the list so the guaranteed characters are not always at the start
    random.shuffle(password_chars)

    # Join the list into a string to create the final password
    password = ''.join(password_chars)
    return password
