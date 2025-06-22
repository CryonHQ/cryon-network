class Ledger:
    def __init__(self):
        self.balances = {}

    def mint(self, address, amount):
        self.balances[address] = self.balances.get(address, 0) + amount

    def transfer(self, from_addr, to_addr, amount):
        if self.balances.get(from_addr, 0) >= amount:
            self.balances[from_addr] -= amount
            self.balances[to_addr] = self.balances.get(to_addr, 0) + amount
            return True
        return False

    def balance_of(self, address):
        return self.balances.get(address, 0)
