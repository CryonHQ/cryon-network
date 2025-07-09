from fastapi import FastAPI, HTTPException
from src.ledger import get_balance, get_history, append_to_ledger
from src.bounty import add_bounty_points, get_bounty_points
from src.stats import get_testnet_stats
from src.staking import stake_tokens, claim_rewards, unstake_tokens, get_staking_info

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Cryon backend działa"}

@app.post("/transfer")
def transfer(from_addr: str, to_addr: str, amount: int):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    append_to_ledger(from_addr, to_addr, amount)
    add_bounty_points(from_addr, 5)
    return {"status": "success", "amount": amount}

@app.get("/balance/{address}")
def balance(address: str):
    return {"address": address, "balance": get_balance(address)}

@app.get("/history/{address}")
def history(address: str):
    return {"address": address, "history": get_history(address)}

@app.post("/mint")
def mint(address: str, amount: int):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    append_to_ledger("MINT", address, amount)
    add_bounty_points(address, 10)
    return {"status": "success", "amount": amount}

@app.get("/bounty/{address}")
def bounty(address: str):
    points = get_bounty_points(address)
    return {"address": address, "bounty_points": points}

@app.get("/leaderboard")
def leaderboard():
    import os, json
    all_addresses = {}
    for filename in ["data/bounty.json"]:
        if os.path.exists(filename):
            with open(filename) as f:
                data = json.load(f)
                all_addresses.update(data)
    top = sorted(all_addresses.items(), key=lambda x: x[1], reverse=True)[:10]
    return [{"address": addr, "bounty_points": pts} for addr, pts in top]

@app.get("/stats")
def stats():
    return get_testnet_stats()

@app.post("/stake")
def stake(address: str, amount: int):
    stake_tokens(address, amount)
    return {"status": "success", "staked": amount}

@app.post("/claim")
def claim(address: str):
    claimed = claim_rewards(address)
    return {"status": "success", "claimed": claimed}

@app.post("/unstake")
def unstake(address: str):
    unstaked = unstake_tokens(address)
    return {"status": "success", "unstaked": unstaked}

@app.get("/staked/{address}")
def staked(address: str):
    return get_staking_info(address)