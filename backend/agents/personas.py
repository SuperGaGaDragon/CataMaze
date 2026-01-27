"""
Agent Personas - behavior profiles for RL agents
"""

PERSONAS = {
    "aggressive": {
        "description": "Aggressive agent that actively hunts the player",
        "shoot_probability": 0.7,
        "chase_probability": 0.8,
        "explore_probability": 0.2,
    },
    "cautious": {
        "description": "Cautious agent that avoids conflict",
        "shoot_probability": 0.2,
        "chase_probability": 0.3,
        "explore_probability": 0.7,
    },
    "explorer": {
        "description": "Explorer agent that focuses on map exploration",
        "shoot_probability": 0.1,
        "chase_probability": 0.1,
        "explore_probability": 0.9,
    },
}


def get_persona(name: str) -> dict:
    """Get persona configuration by name"""
    if name not in PERSONAS:
        raise ValueError(f"Unknown persona: {name}")
    return PERSONAS[name].copy()


def list_personas() -> list:
    """List all available personas"""
    return list(PERSONAS.keys())
