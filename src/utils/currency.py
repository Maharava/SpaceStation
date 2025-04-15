# src/utils/currency.py
import os
import json
from utils.resource_loader import DATA_DIR

CURRENCIES_PATH = os.path.join(DATA_DIR, "player", "currencies.json")
CAPS = {
    "essence": 50000,
    "upgrade_tokens": {
        "gear": 50,
        "augment": 50,
        "stim": 50
    },
    "neural_patterns": 100
}

def init_currencies():
    """Initialize currencies file if it doesn't exist"""
    if os.path.exists(CURRENCIES_PATH):
        return
        
    default_currencies = {
        "essence": 1000,
        "upgrade_tokens": {
            "gear": 4,
            "augment": 4,
            "stim": 4
        },
        "neural_patterns": 0
    }
    
    os.makedirs(os.path.dirname(CURRENCIES_PATH), exist_ok=True)
    with open(CURRENCIES_PATH, 'w') as f:
        json.dump(default_currencies, f, indent=2)

def get_currencies():
    """Get current currencies"""
    init_currencies()
    with open(CURRENCIES_PATH, 'r') as f:
        return json.load(f)

def save_currencies(currencies):
    """Save currencies to file"""
    with open(CURRENCIES_PATH, 'w') as f:
        json.dump(currencies, f, indent=2)

def add_currency(currency_type, amount, token_type=None):
    """Add currency to player's total"""
    currencies = get_currencies()
    
    if currency_type == "upgrade_tokens" and token_type:
        current = currencies["upgrade_tokens"][token_type]
        currencies["upgrade_tokens"][token_type] = min(current + amount, CAPS["upgrade_tokens"][token_type])
    else:
        current = currencies[currency_type]
        currencies[currency_type] = min(current + amount, CAPS[currency_type])
    
    save_currencies(currencies)
    return True

def remove_currency(currency_type, amount, token_type=None):
    """Remove currency if player has enough"""
    currencies = get_currencies()
    
    if currency_type == "upgrade_tokens" and token_type:
        current = currencies["upgrade_tokens"][token_type]
        if current < amount:
            return False
        currencies["upgrade_tokens"][token_type] = current - amount
    else:
        current = currencies[currency_type]
        if current < amount:
            return False
        currencies[currency_type] = current - amount
    
    save_currencies(currencies)
    return True

def check_amount(currency_type, amount, token_type=None):
    """Check if player has enough of a currency"""
    currencies = get_currencies()
    
    if currency_type == "upgrade_tokens" and token_type:
        return currencies["upgrade_tokens"][token_type] >= amount
    
    return currencies[currency_type] >= amount