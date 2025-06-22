import sys
from src.cryon_wallet import CryonWallet
from src.ledger import Ledger

ledger = Ledger()
wallets = {}

def create_wallet(name):
    wallet = CryonWallet()
    wallets[name] = wallet
    ledger.mint(wallet.address, 1000)
    print(f"Wallet '{name}' created with address {wallet.address} and 1000 tokens.")

def show_balance(name):
    wallet = wallets.get(name)
    if not wallet:
        print(f"No wallet found with name '{name}'.")
        return
    balance = ledger.balance_of(wallet.address)
    print(f"Wallet '{name}' ({wallet.address}) has {balance} tokens.")

def transfer(from_name, to_name, amount):
    from_wallet = wallets.get(from_name)
    to_wallet = wallets.get(to_name)
    if not from_wallet or not to_wallet:
        print("Invalid wallet names.")
        return
    success = ledger.transfer(from_wallet.address, to_wallet.address, int(amount))
    if success:
        print(f"Transferred {amount} tokens from '{from_name}' to '{to_name}'.")
    else:
        print("Transfer failed. Not enough balance.")

def help():
    print("""
Cryon Wallet CLI
-----------------
Commands:
  create <name>         - Create a new wallet with a given name
  balance <name>        - Show balance of the wallet
  transfer <from> <to> <amount> - Transfer tokens between wallets
  help                  - Show this help message
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
    else:
        cmd = sys.argv[1]
        if cmd == "create" and len(sys.argv) == 3:
            create_wallet(sys.argv[2])
        elif cmd == "balance" and len(sys.argv) == 3:
            show_balance(sys.argv[2])
        elif cmd == "transfer" and len(sys.argv) == 5:
            transfer(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            help()
