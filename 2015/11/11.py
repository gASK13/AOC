import common

# Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
# Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
# Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.

straights = [chr(ord('a') + i) + chr(ord('a') + i + 1) + chr(ord('a') + i + 2) for i in range(24)]


def validate_password(password):
    if 'i' in password or 'o' in password or 'l' in password:
        return False
    if not any([straight in password for straight in straights]):
        return False
    cnt = 0
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i + 1]:
            cnt += 1
            i += 1
        i += 1
    if cnt < 2:
        return False

    return True


def increment_password(password):
    if password[-1] == 'z':
        return increment_password(password[:-1]) + 'a'
    return password[:-1] + chr(ord(password[-1]) + 1)


def increment_password_until_valid(password):
    password = increment_password(password)
    while not validate_password(password):
        password = increment_password(password)
    return password


assert not validate_password('hijklmmn')
assert not validate_password('abbceffg')
assert not validate_password('abcdefgh')
assert not validate_password('abbcegjk')
assert not validate_password('ghijklmn')
assert validate_password('abcdffaa')
assert validate_password('ghjaabcc')
assert not validate_password('ghjaaaaa')
assert not validate_password('abcdeggg')

assert increment_password('xx') == 'xy'
assert increment_password('xz') == 'ya'
assert increment_password('abzzz') == 'acaaa'

assert increment_password_until_valid('abcdefgh') == 'abcdffaa'
assert increment_password_until_valid('ghijklmn') == 'ghjaabcc'

print(f'Part 1: {increment_password_until_valid(common.Loader.load_lines()[0])}')
print(f'Part 2: {increment_password_until_valid(increment_password_until_valid(common.Loader.load_lines()[0]))}')