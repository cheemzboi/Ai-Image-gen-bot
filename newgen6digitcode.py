from random import choice
from string import ascii_uppercase, digits


ALPHA = ascii_uppercase = digits


class Key:
    
    def __init__(self, key=None):
        self.key = key
        if key is None:
            self.key = self.generate()
    
    def verify(self):
        # change this to suit your needs, but simplify it!!!
        if len(self.key) != 24:
            return False
        if self.key.count('-') != 4:
            return False
        ksplit = self.key.split('-')
        if len(ksplit) != 5:
            return False
        for chunk in ksplit:
            if len(chunk) != 4:
                return False
            if any(ch not in ALPHA for ch in chunk):
                return False
        return True
    
    def generate(self):
        # only generate valid keys!!!
        # change this to suit your rules
        key = []
        for _ in range(5):
            chunk = []
            for _ in range(4):
                chunk.append(choice(ALPHA))
            key.append(''.join(chunk))
        return '-'.join(key)
    
    def __str__(self):
        valid = 'Valid' if self.verify() else 'Invalid'
        return self.key + ' : ' + valid


p = Key()
print(p)
p = Key('1302-8456-2202-0192-9782')
print(p)