import random
import string

class RedeemCodeGenerator:
    def __init__(self, length=10):
        self.length = length
        self.codes = set()

    def generate_code(self):
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.length))
        while code in self.codes:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.length))
        self.codes.add(code)
        return code

    def verify_code(self, code):
        return code in self.codes

if __name__ == "__main__":
    generator = RedeemCodeGenerator()
    new_code = generator.generate_code()
    new_code="0EB3LUNGNX"
    print(f"New code: {new_code}")
    print(f"Verify code: {generator.verify_code(new_code)}")
