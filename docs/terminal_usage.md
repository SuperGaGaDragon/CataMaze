# CataMaze Terminal Usage Guide

## Quick Start

### 1. Start the Terminal
The terminal launches with a retro DOS-style interface. Use the `>_` button in the bottom-right corner or press `F12` / `Ctrl+\`` to toggle visibility.

### 2. Create a New Game
```bash
> catamaze new
```

This creates a new game and displays:
- Your Game ID
- Initial HP (5) and Ammo (3)
- Your starting position
- Your 5x5 vision area
- Current status (Alive/Dead, Playing/Won)

### 3. Queue Actions
```bash
# Single action
> catamaze action w

# Multiple actions (batch queue)
> catamaze action wasd

# Mix movements and shots
> catamaze action wwii
```

**Available Keys:**
- **Movement**: `w` (up), `a` (left), `s` (down), `d` (right)
- **Shooting**: `i` (up), `j` (left), `k` (down), `l` (right)
- **Wait**: `space` or `.`

### 4. Execute Tick
```bash
> catamaze tick
```

Each tick:
- Consumes **1 action** from your queue
- Moves/shoots based on that action
- Shows event log (what happened)
- Updates your vision
- Displays HP, Ammo, Position

### 5. View Current State
```bash
> catamaze observe
```

Shows current game state without advancing the game.

### 6. Check Queue
```bash
> catamaze queue
```

Displays how many actions are queued.

## Complete Command Reference

### Game Management

#### `catamaze new`
Start a new game.
- Generates random player and agent positions
- Returns game ID for resuming later

#### `catamaze resume <game_id>`
Resume a saved game.
```bash
> catamaze resume abc-123-def-456
```

### Action Commands

#### `catamaze action <keys>`
Queue one or more actions.
```bash
> catamaze action w       # Queue 1 move up
> catamaze action wasd    # Queue 4 moves
> catamaze action wwii    # Queue 2 moves up, 2 shoots up
```

**Aliases**: `cm action`, `cata a`

#### `catamaze tick`
Execute one game tick (consumes 1 queued action).
```bash
> catamaze tick
```

Shows:
- Tick number
- HP and Ammo bars (♥●)
- Position (x, y)
- Event log (what happened this tick)
- Sound (if any)
- Updated 5x5 vision

**Aliases**: `cm tick`, `cata t`

#### `catamaze clear`
Clear all queued actions (like pressing ESC).
```bash
> catamaze clear
```

**Aliases**: `cm clear`, `cata esc`

### Information Commands

#### `catamaze observe`
View current game state without executing a tick.
```bash
> catamaze observe
```

**Aliases**: `cm observe`, `cata obs`, `cata o`

#### `catamaze queue`
View action queue status.
```bash
> catamaze queue
```

**Aliases**: `cm queue`, `cata q`

#### `catamaze help`
Display help panel.
```bash
> catamaze help
```

## Game Flow Example

### Complete Game Session
```bash
# 1. Start a new game
> catamaze new
=== NEW GAME STARTED ===
Game ID: abc-123-def-456
HP: ♥♥♥♥♥  Ammo: ●●●

# 2. Queue some movements
> catamaze action www
3 action(s) queued
Queue size: 3

# 3. Execute first move
> catamaze tick
=== TICK 1 ===
HP: ♥♥♥♥♥  Ammo: ●●●  Queue: 2
Events:
  1. player moved UP

# 4. Continue executing
> catamaze tick
=== TICK 2 ===
HP: ♥♥♥♥♥  Ammo: ●●●  Queue: 1

# 5. Check state
> catamaze observe
HP: ♥♥♥♥♥  Ammo: ●●●  Tick: 2
Position: (10, 13)

# 6. Queue more actions
> catamaze action di
2 action(s) queued
Queue size: 3

# 7. Check queue
> catamaze queue
Queue size: 3
3 action(s) pending

# 8. Clear queue if needed
> catamaze clear
Queue cleared.

# 9. Continue playing...
> catamaze action wasd
> catamaze tick
...
```

## Vision Symbols

The 5x5 vision grid uses these symbols:

- `█` - Wall (impassable)
- `·` - Empty floor (walkable)
- `@` - You (player)
- `P` - AI Agent (enemy)
- `S` - Start position
- `E` - Exit (reach to win!)
- `A` - Ammo pickup
- `o` - Bullet in flight

## Game Mechanics

### HP System
- Start with **5 HP** (♥♥♥♥♥)
- Lose 1 HP when hit by bullet
- Die at 0 HP (✗)

### Ammo System
- Start with **3 Ammo** (●●●)
- Use 1 ammo per shot
- Cannot shoot at 0 ammo
- Recover 1 ammo every **2 ticks** (passive regeneration)

### Movement
- 4-directional movement (up/down/left/right)
- Cannot move through walls (`█`)
- Cannot move onto other entities

### Shooting
- 4-directional shooting
- Bullets travel until hitting wall or entity
- Uses 1 ammo per shot
- Deals 1 damage on hit

### Sound System
- Hear sounds from nearby actions
- Displayed as `Sound: *click*` or `Sound: *bang*`
- Use to detect nearby agents

### Win Condition
Reach the exit tile (`E`) to win (★).

### Loss Condition
Die (HP = 0) before reaching exit (✗).

## Error Messages

### No Active Game
```bash
> catamaze action w
No active game. Use "catamaze new" to start.
```

**Solution**: Run `catamaze new` first.

### Invalid Keys
```bash
> catamaze action xyz
Invalid keys: x, y, z
Valid keys: w/a/s/d, i/j/k/l, space
```

**Solution**: Use only valid action keys.

### Game Over
```bash
> catamaze tick
╔════════════════════════════════════╗
║         ✗ GAME OVER ✗              ║
║   You died in the maze...          ║
╚════════════════════════════════════╝
Type "catamaze new" to play again.
```

### Server Error
```bash
> catamaze new
Error: Server at capacity (50 concurrent games). Try again later.
```

**Solution**: Wait for server capacity to free up.

## Tips & Strategies

### 1. Queue Multiple Actions
Instead of:
```bash
> catamaze action w
> catamaze tick
> catamaze action w
> catamaze tick
```

Do this:
```bash
> catamaze action ww
> catamaze tick
> catamaze tick
```

### 2. Check Your Queue
Before queuing more actions, check what's already queued:
```bash
> catamaze queue
```

### 3. Clear Queue When Needed
If you queued wrong actions:
```bash
> catamaze clear
> catamaze action [correct actions]
```

### 4. Use Observe Without Wasting Ticks
Want to see current state without advancing time?
```bash
> catamaze observe
```

### 5. Watch Your Ammo
- Shooting uses ammo (●)
- Ammo regenerates every 2 ticks
- Don't spam shots when empty

### 6. Listen for Sounds
Sound indicates nearby activity:
- `*click*` - Someone moved nearby
- `*bang*` - Someone shot nearby

### 7. Find the Exit
Look for `E` in your vision. Navigate towards it to win!

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `F12` | Toggle terminal |
| `Ctrl+\`` | Toggle terminal |
| `↑` / `↓` | Navigate command history |
| `Ctrl+C` | Cancel current input |
| `Ctrl+L` | Clear screen |
| `clear` / `cls` | Clear screen (command) |

## Command Aliases

Short aliases for faster typing:

| Full Command | Short Alias |
|--------------|-------------|
| `catamaze` | `cm` or `cata` |
| `catamaze action` | `cm a` or `cata a` |
| `catamaze tick` | `cm t` or `cata t` |
| `catamaze observe` | `cm obs` or `cata o` |
| `catamaze queue` | `cm q` or `cata q` |
| `catamaze resume` | `cm r` or `cata r` |

Example:
```bash
> cm new
> cm a wasd
> cm t
> cm obs
```

## Troubleshooting

### Terminal Won't Open
- Check browser console for errors
- Ensure backend is running on `localhost:8000`
- Try `F12` or `Ctrl+\`` to toggle

### Commands Not Working
- Ensure you type `catamaze` before subcommand
- Use `catamaze help` to see all commands
- Check for typos in command names

### Game State Not Updating
- Run `catamaze observe` to refresh
- Check backend server is running
- Verify network connection

### Vision Not Rendering
- Clear terminal with `clear` or `Ctrl+L`
- Run `catamaze observe` to re-render
- Check browser console for errors

## Backend API

The terminal communicates with backend API at:
```
http://localhost:8000
```

**Environment Variable**:
```bash
REACT_APP_API_URL=http://localhost:8000
```

Change this to point to a different backend server.

## Advanced Usage

### Resume Game Later
Save your Game ID to resume later:
```bash
> catamaze new
Game ID: abc-123-def-456

# Later...
> catamaze resume abc-123-def-456
```

### Watch Mode (Developer Only)
View full map in god mode:
```bash
GET /game/watch?game_id=abc-123-def-456-watch
```

Note: Requires `-watch` suffix. Not available in terminal UI.

## Need Help?

- Type `catamaze help` for command list
- Type `help` for general terminal commands
- Press `F12` to close terminal
- Visit GitHub repository for issues

---

**Version**: 1.0.0
**Last Updated**: 2026-01-27
