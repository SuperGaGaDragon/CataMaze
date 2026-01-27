"""
Agent Registry - register and load agents
"""
from typing import Dict, Type, Optional
from backend.agents.base import Agent
from backend.agents.human import HumanAgent


# Agent registry
_AGENT_REGISTRY: Dict[str, Type[Agent]] = {
    "human": HumanAgent,
}


def register_agent(name: str, agent_class: Type[Agent]):
    """Register a new agent type"""
    _AGENT_REGISTRY[name] = agent_class


def create_agent(agent_type: str, entity_id: str, persona: Optional[str] = None) -> Agent:
    """
    Create an agent instance.

    Args:
        agent_type: Type of agent (e.g., "human", "rl", "random")
        entity_id: Unique ID for this agent
        persona: Optional persona (e.g., "aggressive", "cautious", "explorer")

    Returns:
        Agent instance
    """
    if agent_type not in _AGENT_REGISTRY:
        raise ValueError(f"Unknown agent type: {agent_type}")

    agent_class = _AGENT_REGISTRY[agent_type]

    if persona:
        return agent_class(entity_id, persona)
    else:
        return agent_class(entity_id)


def list_agents() -> list:
    """List all registered agent types"""
    return list(_AGENT_REGISTRY.keys())
