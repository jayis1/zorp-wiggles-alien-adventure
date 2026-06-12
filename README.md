# Zorp Wiggles: Alien Adventure

You are **Zorp**, a squishy green alien who crash-landed on a bizarre procedurally-generated planet. Run around an open world, collect weird alien gloop, complete bonkers missions, and blast enemies with your tentacle laser!

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
| **Left Click** | Shoot tentacle laser |
| **M** | Toggle minimap |
| **TAB** | Toggle missions panel |
| **P** | Pause |
| **ESC** | Quit |
| **R** | Restart (on Game Over) |

## Features (v1.0.0)

- Procedurally-generated open world with 6 biomes: Grass, Desert, Water, Lava, Forest, Crystal
- 5 collectible item types with different point values
- 5 enemy types that chase and attack you
- Tentacle laser shooting with particle effects
- Mission system with collection and kill objectives
- XP and leveling system (get stronger over time!)
- Minimap with enemy and collectible tracking
- Enemy respawning and loot drops
- Smooth camera follow
- Invincibility frames and HP system

## The Self-Improving Game

This repo is maintained by an AI agent that:

- **Every 10 hours**: Reviews the code, adds new features, improves gameplay, enhances graphics, balances mechanics, and makes things more awesome
- **Daily at 12:00**: Goes on a bug hunt — finds and fixes bugs, edge cases, crashes, and logic errors

Each enhancement is committed and pushed. Check the commit history to watch the game evolve!

## World Biomes

| Biome | Color | Walkable | Notes |
|-------|-------|----------|-------|
| Grass | Green | Yes | Safe starting zone |
| Desert | Sandy | Yes | Open and exposed |
| Water | Blue | No | Blocks movement |
| Lava | Red | No | Blocks movement |
| Forest | Dark Green | Yes | Has trees |
| Crystal | Cyan | Yes | Crystal spires |

## Collectibles

| Item | Value | Rarity |
|------|-------|--------|
| Space Gloop | 10 pts | Common |
| Meteor Shard | 25 pts | Uncommon |
| Quantum Fuzz | 50 pts | Rare |
| Nebula Dust | 100 pts | Very Rare |
| Cosmic Jelly | 200 pts | Legendary |

## Enemies

| Enemy | HP | Speed | Damage |
|-------|----|-------|--------|
| Slime Blob | 30 | Slow | 15 |
| Space Beetle | 50 | Medium | 20 |
| Void Wraith | 80 | Slow | 30 |
| Lava Crawler | 120 | Fast | 35 |
| Crystal Guardian | 200 | Medium | 50 |

## License

MIT - Zorp is free to wiggle wherever it wants.