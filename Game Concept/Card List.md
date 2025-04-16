### Fields Explanation:
- `id`: A unique identifier for the card.
- `name`: The name of the card, displayed in the UI.
- `image`: The filename of the card's image, located in `data/assets/cards`.
- `text`: The description of the card's effect, shown as a tooltip.
- `abilities`: A list of abilities the card has. Each ability includes:
    - `type`: The type of ability (e.g., `Attack`, `Defend`).
    - `value`: The value or reference for the ability. For `Attack` and `Defend`, this references the hero's stats (`hero_attack` or `hero_armour`).



[
    {
        "id": "attack_base",
        "name": "Attack",
        "image": "attack_base.png",
        "text": "x1 Attack",
        "abilities": [
            {
                "type": "Attack",
                "value": "hero_attack"
            }
        ],
        "upgrade": {
            "id": "attack_upgraded",
            "name": "Attack+",
            "image": "attack_upgraded.png",
            "text": "x2 Attack",
            "abilities": [
                {
                    "type": "Attack",
                    "value": "hero_attack * 2"
                }
            ]
        }
    },
    {
        "id": "defend_base",
        "name": "Defend",
        "image": "defend_base.png",
        "text": "x1 Defend",
        "abilities": [
            {
                "type": "Defend",
                "value": "hero_defend"
            }
        ],
        "upgrade": {
            "id": "defend_upgraded",
            "name": "Defend+",
            "image": "defend_upgraded.png",
            "text": "x2 Defend",
            "abilities": [
                {
                    "type": "Defend",
                    "value": "hero_defend * 2"
                }
            ]
        }
    },
    {
        "id": "rapid_attack_base",
        "name": "Rapid Attack",
        "image": "rapid_attack_base.png",
        "text": "x2 Attack",
        "abilities": [
            {
                "type": "Attack",
                "value": "hero_attack * 2"
            }
        ],
        "upgrade": {
            "id": "rapid_attack_upgraded",
            "name": "Rapid Attack+",
            "image": "rapid_attack_upgraded.png",
            "text": "x3 Attack",
            "abilities": [
                {
                    "type": "Attack",
                    "value": "hero_attack * 3"
                }
            ]
        }
    },
    {
        "id": "target_lock_base",
        "name": "Target Lock",
        "image": "target_lock_base.png",
        "text": "x1 Targeted",
        "abilities": [
            {
                "type": "ApplyStatus",
                "status": "Targeted",
                "value": 1
            }
        ],
        "upgrade": {
            "id": "target_lock_upgraded",
            "name": "Target Lock+",
            "image": "target_lock_upgraded.png",
            "text": "x3 Targeted",
            "abilities": [
                {
                    "type": "ApplyStatus",
                    "status": "Targeted",
                    "value": 3
                }
            ]
        }
    },
    {
        "id": "dodge_base",
        "name": "Dodge",
        "image": "dodge_base.png",
        "text": "Defend once and gain haste buff",
        "abilities": [
            {
                "type": "Defend",
                "value": "hero_defend"
            },
            {
                "type": "ApplyStatus",
                "status": "Haste",
                "value": 1
            }
        ],
        "upgrade": {
            "id": "dodge_upgraded",
            "name": "Dodge+",
            "image": "dodge_upgraded.png",
            "text": "Defend twice and gain 2 haste buff",
            "abilities": [
                {
                    "type": "Defend",
                    "value": "hero_defend * 2"
                },
                {
                    "type": "ApplyStatus",
                    "status": "Haste",
                    "value": 2
                }
            ]
        }
    },
    {
        "id": "med_kit_base",
        "name": "Med Kit",
        "image": "med_kit_base.png",
        "text": "x1 Hypo-spray, +1 energy",
        "abilities": [
            {
                "type": "ApplyStatus",
                "status": "Hypo-spray",
                "value": 1
            },
            {
                "type": "GainEnergy",
                "value": 1
            }
        ],
        "upgrade": {
            "id": "med_kit_upgraded",
            "name": "Med Kit+",
            "image": "med_kit_upgraded.png",
            "text": "x3 Hypo-spray, +1 energy",
            "abilities": [
                {
                    "type": "ApplyStatus",
                    "status": "Hypo-spray",
                    "value": 3
                },
                {
                    "type": "GainEnergy",
                    "value": 1
                }
            ]
        }
    },
    {
        "id": "raging_strike_base",
        "name": "Raging Strike",
        "image": "raging_strike_base.png",
        "text": "x1 Attack, x1 Adrenaline",
        "abilities": [
            {
                "type": "Attack",
                "value": "hero_attack"
            },
            {
                "type": "ApplyStatus",
                "status": "Adrenaline",
                "value": 1
            }
        ],
        "upgrade": {
            "id": "raging_strike_upgraded",
            "name": "Raging Strike+",
            "image": "raging_strike_upgraded.png",
            "text": "x1 Attack, x2 Adrenaline, x1 Injury on target",
            "abilities": [
                {
                    "type": "Attack",
                    "value": "hero_attack"
                },
                {
                    "type": "ApplyStatus",
                    "status": "Adrenaline",
                    "value": 2
                },
                {
                    "type": "ApplyStatus",
                    "status": "Injury",
                    "target": "enemy",
                    "value": 1
                }
            ]
        }
    },
    {
        "id": "hunker_down_base",
        "name": "Hunker Down",
        "image": "hunker_down_base.png",
        "text": "x2 Defence",
        "abilities": [
            {
                "type": "Defend",
                "value": "hero_defend * 2"
            }
        ],
        "upgrade": {
            "id": "hunker_down_upgraded",
            "name": "Hunker Down+",
            "image": "hunker_down_upgraded.png",
            "text": "x2 Defence, x2 Shield",
            "abilities": [
                {
                    "type": "Defend",
                    "value": "hero_defend * 2"
                },
                {
                    "type": "ApplyStatus",
                    "status": "Shield",
                    "value": 2
                }
            ]
        }
    },
    {
        "id": "bunker_down_base",
        "name": "Bunker Down",
        "image": "bunker_down_base.png",
        "text": "x1 Defence, x2 Lash Out",
        "abilities": [
            {
                "type": "Defend",
                "value": "hero_defend"
            },
            {
                "type": "ApplyStatus",
                "status": "Lash Out",
                "value": 2
            }
        ],
        "upgrade": {
            "id": "bunker_down_upgraded",
            "name": "Bunker Down+",
            "image": "bunker_down_upgraded.png",
            "text": "x2 Defence, x3 Lash Out",
            "abilities": [
                {
                    "type": "Defend",
                    "value": "hero_defend * 2"
                },
                {
                    "type": "ApplyStatus",
                    "status": "Lash Out",
                    "value": 3
                }
            ]
        }
    },
    {
        "id": "crippling_shot_base",
        "name": "Crippling Shot",
        "image": "crippling_shot_base.png",
        "text": "x1 Attack, x2 Injury on target",
        "abilities": [
            {
                "type": "Attack",
                "value": "hero_attack"
            },
            {
                "type": "ApplyStatus",
                "status": "Injury",
                "target": "enemy",
                "value": 2
            }
        ],
        "upgrade": {
            "id": "crippling_shot_upgraded",
            "name": "Crippling Shot+",
            "image": "crippling_shot_upgraded.png",
            "text": "x2 Attack, x3 Injury on target",
            "abilities": [
                {
                    "type": "Attack",
                    "value": "hero_attack * 2"
                },
                {
                    "type": "ApplyStatus",
                    "status": "Injury",
                    "target": "enemy",
                    "value": 3
                }
            ]
        }
    },
    {
        "id": "flashbang_base",
        "name": "Flashbang",
        "image": "flashbang_base.png",
        "text": "x1 Shellshock, x1 Stunned, x1 Blinded",
        "abilities": [
            {
                "type": "ApplyStatus",
                "status": "Shellshock",
                "target": "enemy",
                "value": 1
            },
            {
                "type": "ApplyStatus",
                "status": "Stunned",
                "target": "enemy",
                "value": 1
            },
            {
                "type": "ApplyStatus",
                "status": "Blinded",
                "target": "enemy",
                "value": 1
            }
        ],
        "upgrade": {
            "id": "flashbang_upgraded",
            "name": "Flashbang+",
            "image": "flashbang_upgraded.png",
            "text": "x1 Shellshock, x1 Stunned, x1 Blinded, +1 energy",
            "abilities": [
                {
                    "type": "ApplyStatus",
                    "status": "Shellshock",
                    "target": "enemy",
                    "value": 1
                },
                {
                    "type": "ApplyStatus",
                    "status": "Stunned",
                    "target": "enemy",
                    "value": 1
                },
                {
                    "type": "ApplyStatus",
                    "status": "Blinded",
                    "target": "enemy",
                    "value": 1
                },
                {
                    "type": "GainEnergy",
                    "value": 1
                }
            ]
        }
    },
    {
        "id": "shield_overcharge_base",
        "name": "Shield Overcharge",
        "image": "shield_overcharge_base.png",
        "text": "x2 Shield, +1 energy",
        "abilities": [
            {
                "type": "ApplyStatus",
                "status": "Shield",
                "value": 2
            },
            {
                "type": "GainEnergy",
                "value": 1
            }
        ],
        "upgrade": {
            "id": "shield_overcharge_upgraded",
            "name": "Shield Overcharge+",
            "image": "shield_overcharge_upgraded.png",
            "text": "x1 Defence, x2 Shield, +1 energy",
            "abilities": [
                {
                    "type": "Defend",
                    "value": "hero_defend"
                },
                {
                    "type": "ApplyStatus",
                    "status": "Shield",
                    "value": 2
                },
                {
                    "type": "GainEnergy",
                    "value": 1
                }
            ]
        }
    }
]