import hashlib
import secrets
import json
from pathlib import Path

class CryonWallet:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = private_key
        else:
            self.private_key = secrets.token_hex(32)
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()
        self.address = self.public_key[:32]

    def sign(self, message: str) -> str:
        return hashlib.sha256((self.private_key + message).encode()).hexdigest()

    def __repr__(self):
        return f"Address: {self.address}\nPublic Key: {self.public_key}"

    def save_to_file(self, filename):
        Path("wallets").mkdir(exist_ok=True)
        data = {"private_key": self.private_key}
        with open(f"wallets/{filename}.wallet", "w") as f:
            json.dump(data, f)
        print(f"Wallet saved to wallets/{filename}.wallet")

    @staticmethod
    def load_from_file(filename):
        try:
            with open(f"wallets/{filename}.wallet", "r") as f:
                data = json.load(f)
                return CryonWallet(data["private_key"])
        except FileNotFoundError:
            print(f"No wallet file found for {filename}")
            return None
