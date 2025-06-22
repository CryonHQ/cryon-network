import hashlib
import secrets

class CryonWallet:
    def __init__(self):
        self.private_key = secrets.token_hex(32)
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()
        self.address = self.public_key[:32]

    def sign(self, message: str) -> str:
        return hashlib.sha256((self.private_key + message).encode()).hexdigest()

    def __repr__(self):
        return f"Address: {self.address}\nPublic Key: {self.public_key}"
