# Zorp Wiggles: Alien Adventure

You are **Zorp**, a squishy green alien who crash-landed on a bizarre procedurally-generated 3D planet. Run around a 3D open world, collect weird alien gloop, complete bonkers missions, and blast enemies with your tentacle laser!

This game **evolves on its own**. Every 10 hours, an AI enhances the code to make it more awesome. Every day at noon, the AI hunts bugs. It only gets better.

## How to Play

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
python game.py
```

### Controls
| Key | Action |
|-----|--------|
| **WASD / Arrow Keys** | Move Zorp |
| **Mouse** | Aim / Look direction |
| **Left Click** | Shoot tentacle laser |
| **M** | Toggle minimap |
| **TAB** | Toggle missions panel |
| **P** | Pause |
| **ESC** | Quit |
| **R** | Restart (on Game Over) |

## Features (v2.0.0 — 3D!)

- Full 3D open world with third-person camera
- Procedurally generated terrain with 8 biomes: Grass, Desert, Water, Lava, Forest, Crystal, Snow, Swamp
- 6 collectible item types with different point values
- 6 enemy types that chase, attack, and drop loot
- Tentacle laser shooting with particle effects
- Mission system with collection and kill objectives
- XP and leveling system (get stronger over time!)
- Minimap with player tracking
- Enemy HP bars and floating combat effects
- 3D trees in forests, crystal spires in crystal biomes
- Atmospheric fog and lighting
- Smooth camera follow
- Invincibility frames on damage
- Enemy respawning and loot drops
- Particle system for hits, kills, and pickups

## The Self-Improving Game

This repo is maintained by an AI agent that:

- **Every 10 hours**: Reviews the code, adds new features, improves gameplay, enhances graphics, balances mechanics, and makes things more awesome
- **Daily at 12:00**: Goes on a bug hunt — finds and fixes bugs, edge cases, crashes, and logic errors

Each enhancement is committed and pushed. Check the commit history to watch the game evolve!

## World Biomes

| Biome | Color | Walkable | Features |
|-------|-------|----------|----------|
| Grass | Green | Yes | Safe starting zone |
| Desert | Sandy | Yes | Open and exposed |
| Water | Blue | No | Blocks movement |
| Lava | Red | No | Blocks movement |
| Forest | Dark Green | Yes | 3D trees |
| Crystal | Cyan | Yes | Crystal spires |
| Snow | White | Yes | Icy terrain |
| Swamp | Murky Green | Yes | Squishy ground |

## Collectibles

| Item | Value | Rarity |
|------|-------|--------|
| Space Gloop | 10 pts | Common |
| Meteor Shard | 25 pts | Uncommon |
| Quantum Fuzz | 50 pts | Rare |
| Nebula Dust | 100 pts | Very Rare |
| Cosmic Jelly | 200 pts | Legendary |
| Plasma Core | 350 pts | Mythic |

## Enemies

| Enemy | HP | Speed | Damage | Notes |
|-------|----|-------|--------|-------|
| Slime Blob | 30 | Slow | 10 | Common, easy |
| Space Beetle | 50 | Medium | 15 | Aggressive |
| Void Wraith | 80 | Medium | 25 | Spooky |
| Lava Crawler | 120 | Fast | 30 | Hot-headed |
| Crystal Guardian | 200 | Slow | 40 | Tough |
| Plasma Drake | 350 | Very Fast | 50 | Endgame boss |

## Tech Stack

- **Ursina** (Panda3D-based Python game engine)
- **Python 3** — no other dependencies
- Pure Python — no assets needed, all procedural

## License

MIT — Zorp is free to wiggle wherever it wants.