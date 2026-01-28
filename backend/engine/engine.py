"""
Core game engine.
Handles tick execution, action processing, and state updates.
"""
from typing import List, Dict, Tuple, Optional
from backend.engine.state import WorldState, EntityState, BulletState
from backend.engine.actions import (
    is_move_action, is_shoot_action, is_wait_action,
    get_direction_vector, get_direction_name, WAIT
)
from backend.engine.position import get_next_position, add_vector
from backend.engine.hp import take_damage, is_dead
from backend.engine.bullet import consume_ammo, recover_ammo, simulate_shot
from backend.engine.observation import generate_observation, generate_sound_for_entity


class GameEngine:
    """
    Core game engine managing world state and tick execution.
    """

    def __init__(self, world: WorldState, agents: Optional[Dict[str, any]] = None):
        """
        Initialize engine with a world state and agents.

        Args:
            world: Initial world state
            agents: Dict mapping entity_id to Agent instance (for AI agents)
        """
        self.world = world
        self.agents = agents or {}
        self.events: List[str] = []

    def log_event(self, event: str):
        """Add event to event log."""
        self.events.append(event)

    def tick(self) -> Dict[str, any]:
        """
        Execute one game tick.
        - Let AI agents decide actions
        - Pop one action from each entity's queue
        - Execute all actions
        - Resolve bullets
        - Recover ammo
        - Check win/loss conditions
        - Generate observations

        Returns:
            Dict with events and observations
        """
        self.events = []  # Clear events from last tick

        # Record shot positions for sound generation
        shot_positions = []

        # Phase 0: Let AI agents decide actions and queue them
        for entity_id, agent in self.agents.items():
            entity = self.world.entities.get(entity_id)
            if entity and entity.alive and not self.world.game_over:
                try:
                    # Generate observation for this agent
                    obs = generate_observation(self.world, entity_id)
                    # Let agent decide action
                    action = agent.decide_action(obs)
                    # Queue the action
                    entity.action_queue.append(action)
                    print(f"DEBUG: {entity_id} decided action: {action}")
                except Exception as e:
                    print(f"ERROR: Agent {entity_id} failed to decide action: {e}")
                    import traceback
                    traceback.print_exc()

        # Phase 1: Pop actions from queues
        entity_actions = {}
        for entity_id, entity in self.world.entities.items():
            if not entity.alive:
                continue

            if len(entity.action_queue) > 0:
                action = entity.action_queue.pop(0)
            else:
                action = WAIT

            entity_actions[entity_id] = action

        # Phase 2: Execute actions
        for entity_id, action in entity_actions.items():
            entity = self.world.entities[entity_id]

            if is_move_action(action):
                self._execute_move(entity, action)

            elif is_shoot_action(action):
                shot_pos = (entity.x, entity.y)
                shot_positions.append(shot_pos)
                self._execute_shoot(entity, action)

        # Phase 3: Recover ammo
        for entity in self.world.entities.values():
            if entity.alive:
                self._recover_entity_ammo(entity)

        # Phase 4: Check win conditions
        self._check_win_conditions()

        # Phase 5: Increment tick
        self.world.tick += 1

        # Phase 6: Generate observations for all entities
        observations = {}
        for entity_id, entity in self.world.entities.items():
            if entity.alive:
                sound = generate_sound_for_entity(
                    (entity.x, entity.y),
                    shot_positions
                )
                obs = generate_observation(self.world, entity_id, sound)
                observations[entity_id] = obs

        return {
            "tick": self.world.tick,
            "events": self.events,
            "observations": observations
        }

    def _execute_move(self, entity: EntityState, action: str):
        """Execute a move action for an entity."""
        direction_vector = get_direction_vector(action)
        new_pos = get_next_position(
            self.world.map_grid,
            (entity.x, entity.y),
            direction_vector
        )

        if (new_pos[0], new_pos[1]) != (entity.x, entity.y):
            # Movement succeeded
            entity.x, entity.y = new_pos
            entity.visited_positions.add((entity.x, entity.y))
            self.log_event(f"{entity.entity_id} moved to ({entity.x}, {entity.y})")
        else:
            # Hit a wall
            self.log_event(f"{entity.entity_id} tried to move but hit a wall")

    def _execute_shoot(self, entity: EntityState, action: str):
        """Execute a shoot action for an entity."""
        if entity.ammo <= 0:
            self.log_event(f"{entity.entity_id} tried to shoot but out of ammo")
            return

        # Consume ammo
        entity.ammo = consume_ammo(entity.ammo)
        entity.last_bullet_tick = self.world.tick

        direction_vector = get_direction_vector(action)
        direction_name = get_direction_name(action)

        # Get all alive entity positions as targets
        target_positions = [
            (e.x, e.y) for eid, e in self.world.entities.items()
            if e.alive and eid != entity.entity_id
        ]

        # Simulate shot
        hit_pos = simulate_shot(
            (entity.x, entity.y),
            direction_vector,
            self.world.map_grid,
            target_positions
        )

        if hit_pos:
            # Find which entity was hit
            for target_id, target in self.world.entities.items():
                if target.alive and (target.x, target.y) == hit_pos:
                    target.hp = take_damage(target.hp)
                    self.log_event(
                        f"{entity.entity_id} shot {target_id} at {hit_pos}. "
                        f"{target_id} HP: {target.hp}"
                    )

                    if is_dead(target.hp):
                        target.alive = False
                        self.log_event(f"{target_id} died")
                    break
        else:
            self.log_event(f"{entity.entity_id} shot {direction_name} but missed")

    def _recover_entity_ammo(self, entity: EntityState):
        """Recover ammo for an entity if conditions met."""
        new_ammo, new_last_shot_tick = recover_ammo(
            entity.ammo,
            self.world.tick,
            entity.last_bullet_tick
        )

        if new_ammo > entity.ammo:
            entity.ammo = new_ammo
            entity.last_bullet_tick = new_last_shot_tick
            self.log_event(f"{entity.entity_id} recovered 1 ammo (total: {entity.ammo})")

    def _check_win_conditions(self):
        """Check if any entity has won or if game is over."""
        player = self.world.entities.get("player")

        if player:
            # Check if player reached exit
            if player.alive and player.x == self.world.exit_x and player.y == self.world.exit_y:
                player.won = True
                self.world.game_over = True
                self.world.winner_id = "player"
                self.log_event("Player reached the exit and won!")

            # Check if player died
            elif not player.alive:
                self.world.game_over = True
                self.log_event("Player died. Game over.")
