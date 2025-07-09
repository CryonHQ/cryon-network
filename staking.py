import json
import os
from datetime import datetime

STAKING_FILE = "data/staking.json"

def _load_staking_data():
    if not os.path.exists(STAKING_FILE):
        return {}
    with open(STAKING_FILE, "r") as f:
        return json.load(f)

def _save_staking_data(data):
    with open(STAKING_FILE, "w") as f:
        json.dump(data, f, indent=4)

def stake_tokens(address, amount):
    data = _load_staking_data()
    now = datetime.utcnow().isoformat()
    if address not in data:
        data[address] = {"staked": 0, "rewards": 0, "last_action": now}
    data[address]["staked"] += amount
    data[address]["last_action"] = now
    _save_staking_data(data)

def claim_rewards(address):
    data = _load_staking_data()
    if address not in data:
        return 0
    claimed = data[address]["rewards"]
    data[address]["rewards"] = 0
    data[address]["last_action"] = datetime.utcnow().isoformat()
    _save_staking_data(data)
    return claimed

def unstake_tokens(address):
    data = _load_staking_data()
    if address not in data:
        return 0
    unstaked = data[address]["staked"]
    data[address]["staked"] = 0
    data[address]["last_action"] = datetime.utcnow().isoformat()
    _save_staking_data(data)
    return unstaked

def get_staking_info(address):
    data = _load_staking_data()
    return data.get(address, {"staked": 0, "rewards": 0, "last_action": None})