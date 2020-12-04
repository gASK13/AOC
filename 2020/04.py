import re

mandatory_fields = {'byr' : '^(19[2-9][0-9]|200[0-2])$',
                    'iyr' : '^20(1[0-9]|20)$',
                    'eyr' : '^20(2[0-9]|30)$',
                    'hgt' : '^(1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-6]in)$',
                    'hcl' : '^#[0-9a-f]{6}$',
                    'ecl' : '^(amb|blu|brn|gry|grn|hzl|oth)$',
                    'pid' : '^[0-9]{9}$'}

class Passport:
    def __init__(self, lines):
        self.fields = {}
        for line in lines:
            for field in line.split(" "):
                self.fields[(field.split(':')[0])] = field.split(':')[1].strip()
    def isValid(self):
        for field in mandatory_fields.keys():
            if field not in self.fields.keys():
                return False
            if not re.compile(mandatory_fields[field]).match(self.fields[field]):
                print("Does not match " + field + ": " + self.fields[field])
                return False
        return True



buffer = []
passports = []
for line in open('04.txt', 'r').readlines():
    if len(line.strip()) == 0:
        passports.append(Passport(buffer))
        buffer = []
    else:
        buffer.append(line)
passports.append(Passport(buffer))

valid = 0
for passport in passports:
    if passport.isValid():
        valid += 1

print(str(valid) + " OUT OF " + str(len(passports)))