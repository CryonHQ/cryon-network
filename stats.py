import json
from pathlib import Path

def get_testnet_stats():
    ledger_path = Path("data/ledger.json")

    if not ledger_path.exists():
        return {
            "wallets": 0,
            "transactions": 0,
            "total_transferred": 0
        }

    with open(ledger_path, "r") as f:
        try:
            ledger = json.load(f)
        except json.JSONDecodeError:
            return {
                "wallets": 0,
                "transactions": 0,
                "total_transferred": 0
            }

    unique_wallets = set()
    total_transferred = 0

    for tx in ledger:
        sender = tx.get("from")
        receiver = tx.get("to")
        amount = tx.get("amount", 0)

        if sender:
            unique_wallets.add(sender)
        if receiver:
            unique_wallets.add(receiver)

        if isinstance(amount, (int, float)):
            total_transferred += amount

    return {
        "wallets": len(unique_wallets),
        "transactions": len(ledger),
        "total_transferred": total_transferred
    }
