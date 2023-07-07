# Conditions for a valid password are:
#
# Should have at least one number.
# Should have at least one uppercase and one lowercase character.
# Should have at least one special symbol.
# Should be between 6 to 20 characters long.

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True
    if len(passwd) < 6:
        print('length should be at least 6')
        val = False
    if len(passwd) > 20:
        print('length should be not be greater than 8')
        val = False

    # Check if password contains at least one digit, uppercase letter, lowercase letter, and special symbol
    has_digit = False
    has_upper = False
    has_lower = False
    has_sym = False
    for char in passwd:
        if 48 <= ord(char) <= 57:
            has_digit = True
        elif 65 <= ord(char) <= 90:
            has_upper = True
        elif 97 <= ord(char) <= 122:
            has_lower = True
        elif char in SpecialSym:
            has_sym = True

    if not has_digit:
        print('Password should have at least one numeral')
        val = False
    if not has_upper:
        print('Password should have at least one uppercase letter')
        val = False
    if not has_lower:
        print('Password should have at least one lowercase letter')
        val = False
    if not has_sym:
        print('Password should have at least one of the symbols $@#')
        val = False

    return val


# print(password_check('Geek12@'))  # should return True
# print(password_check('asd123'))  # should return False
# print(password_check('HELLOworld'))  # should return False
# print(password_check('helloWORLD123@'))  # should return True
# print(password_check('HelloWORLD123'))  # should return False