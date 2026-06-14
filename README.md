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
| **Space** | Dash (dodge in movement direction) |
| **M** | Toggle minimap |
| **TAB** | Toggle missions panel |
| **P** | Pause |
| **ESC** | Quit |
| **R** | Restart (on Game Over) |

## Features (v2.3.2 — 3D!)

- Full 3D open world with third-person camera
- Procedurally generated terrain with **10 biomes**: Grass, Desert, Water, Lava, Forest, Crystal, Snow, Swamp, Alien Mushroom Forest, **Floating Islands**
- 11 collectible item types — including **5 power-ups**: Health Potion, Speed Boost, Shield Crystal, Weapon Upgrade (Spread Shot), **Magnet Core**
- **11 enemy types** — including **Phase Shifter** (teleports!), **Spore Spitter** (fires back!), **Swarm Mite** (fast & tiny), **Void Bomber** (kamikaze explosions!), **Nebula Phantom** (flying orbit + dive attack!)
- **Dash ability** — press Space to dodge in your movement direction (2s cooldown)
- Tentacle laser shooting with particle effects
- **Spread Shot weapon upgrade** — pick up a Weapon Upgrade to fire 3 lasers in a fan pattern for 8 seconds!
- **Shield power-up** — blocks all damage for 4 seconds
- **Speed Boost** — 1.8x speed for 5 seconds
- **Health Potion** — restores 30 HP instantly
- **Magnet Core** — boosts item pull radius 2.5x and pull speed 2x for 6 seconds!
- **Combo system** — chain kills within 4 seconds for XP and score multipliers! Combo counter displayed on HUD with escalating colors
- **Weather effects** — rain in grass/forest/swamp biomes, snowfall in snow biomes, rising embers in lava biomes
- Mission system with collection and kill objectives
- XP and leveling system (get stronger over time!)
- Distance-based difficulty scaling (harder enemies farther from spawn)
- Minimap with player tracking
- Enemy HP bars with green→yellow→red color gradient
- 3D trees in forests, crystal spires in crystal biomes, **colorful alien mushrooms** in mushroom biomes
- **Floating Islands biome** — raised platforms hovering above the ground with purple crystals and shadow projections
- **Alien Ruins** — stone pillars and broken walls spawning in desert biomes
- Atmospheric fog and lighting with starfield sky
- Smooth camera follow with screen shake on hits and kills
- Enemy death animations (pop upward, shrink, flash, and dissolve)
- Level-up flash effect and scale pulse
- Satisfying collectible pickup burst particles
- Magnetic item pull (items are drawn toward you when nearby)
- Floating damage numbers on enemy hits and kills
- Detailed death screen with survival stats
- Distinct enemy shapes (spheres, cubes, diamonds) and decorations (wings, auras, spikes, shards)
- Invincibility frames on damage
- Enemy respawning and loot drops
- Particle system for hits, kills, and pickups
- Dash cooldown indicator on HUD
- Active power-up timers displayed on HUD
- **Hit-stop freeze frames** on kills for satisfying impact
- **Collectible pop animation** — items scale up and spin before disappearing
- **Biome-aware fog** — fog color and density smoothly transition as you walk between biomes
- **Twinkling starfield** — stars pulse in brightness for an immersive alien sky
- **Enemy knockback** — enemies get pushed back when hit by projectiles for satisfying combat feel
- **Elastic collectible pop** — items flash white and scale up with a bouncy overshoot before disappearing
- **Player-level difficulty scaling** — newly spawned enemies gain HP and damage as you level up, keeping the challenge fresh
- **Per-type enemy detection ranges** — Swarm Mites detect from further away (swarm behavior), others tuned for fairer encounters
- **Weighted collectible spawning** — common items (Space Gloop) drop more often; rare items (Plasma Core) are truly rare finds
- **Terrain-colored minimap with enemy dots** — see biomes and enemy positions at a glance, refreshes in real time
- **Nebula clouds** — drifting translucent colored clouds in the sky for atmospheric depth
- **Collectible glow pulsing** — items pulse their glow ring to act as beacons, making them easier to spot
- **Dynamic enemy spawn rate** — enemies spawn faster as you level up, keeping pressure on
- **Enhanced death screen** — shows kills per minute and full inventory breakdown
- **Projectile laser trails** — tentacle laser shots leave fading, shrinking cyan trail dots for satisfying visual feedback
- **Player squish/stretch** — Zorp squishes and stretches when moving, making the alien feel more squishy and alive
- **Smoother camera tracking** — faster camera lerp for tighter, more responsive following
- **Dash FOV zoom** — camera field of view widens during dash for a satisfying speed rush effect
- **Enemy alert flash** — enemies flash yellow when they first detect the player, giving you a visual warning before the chase starts

## The Self-Improving Game

This repo is maintained by an AI agent that:

- **Every 10 hours**: Reviews the code, adds new features, improves gameplay, enhances graphics, balances mechanics, and makes things more awesome
- **Daily at 12:00**: Goes on a bug hunt — finds and fixes bugs, edge cases, crashes, and logic errors

Each enhancement is committed and pushed. Check the commit history to watch the game evolve!

## World Biomes

| Biome | Color | Walkable | Features |
|-------|-------|----------|----------|
| Grass | Green | Yes | Safe starting zone, rain weather |
| Desert | Sandy | Yes | Open and exposed, **alien ruins** |
| Water | Blue | No | Blocks movement |
| Lava | Red | No | Blocks movement, rising ember particles |
| Forest | Dark Green | Yes | 3D trees, rain weather |
| Crystal | Cyan | Yes | Crystal spires |
| Snow | White | Yes | Icy terrain, snowfall weather |
| Swamp | Murky Green | Yes | Squishy ground, rain weather |
| Mushroom | Alien Green | Yes | Colorful alien mushrooms with spore glow |
| **Floating Islands** | Lavender | Yes | Raised platforms with purple crystals and ground shadows |

## Collectibles

| Item | Value | Effect | Rarity |
|------|-------|--------|--------|
| Space Gloop | 10 pts | Score only | Common |
| Meteor Shard | 25 pts | Score only | Uncommon |
| Quantum Fuzz | 50 pts | Score only | Rare |
| Nebula Dust | 100 pts | Score only | Very Rare |
| Cosmic Jelly | 200 pts | Score only | Legendary |
| Plasma Core | 350 pts | Score only | Mythic |
| **Health Potion** | 15 pts | Restores 30 HP | Uncommon |
| **Speed Boost** | 15 pts | 1.8x speed for 5s | Uncommon |
| **Shield Crystal** | 15 pts | Blocks all damage for 4s | Rare |
| **Weapon Upgrade** | 20 pts | Spread shot (3 lasers) for 8s | Rare |
| **Magnet Core** | 20 pts | 2.5x pull radius + 2x pull speed for 6s | Uncommon |

## Enemies

| Enemy | HP | Speed | Damage | Special | Notes |
|-------|----|-------|--------|---------|-------|
| Slime Blob | 30 | Slow | 10 | — | Common, easy |
| Swarm Mite | 15 | Very Fast | 5 | — | Tiny & fast, spawns in groups |
| Space Beetle | 50 | Medium | 15 | — | Aggressive |
| Phase Shifter | 70 | Medium | 20 | **Teleports** | Warps near player periodically |
| **Void Bomber** | 60 | Medium | 20 | **Kamikaze!** | Explodes near player, also damages other enemies |
| **Nebula Phantom** | 100 | Fast | 30 | **Orbit + Dive** | Circles player in the air, then dive-attacks! |
| Void Wraith | 80 | Medium | 25 | — | Spooky |
| Spore Spitter | 90 | Medium | 15 | **Shoots back** | Fires projectiles at player |
| Lava Crawler | 120 | Fast | 30 | — | Hot-headed |
| Crystal Guardian | 200 | Slow | 40 | — | Tough |
| Plasma Drake | 400 | Very Fast | 50 | — | Endgame boss |

## Combo System

Chain kills within 4.5 seconds to build combos! Each combo tier grants:
- **+12% XP bonus** per tier (up to 10 tiers)
- **+6% score bonus** per tier (up to 10 tiers)
- HUD display with escalating colors: yellow → orange → red
- Combo counter scales up visually as it grows

## World Features

- **Alien Ruins** in desert biomes — scattered stone pillars (1–4 per ruin) and broken wall segments, giving the desert a mysterious ancient civilization feel
- **Floating Islands** — elevated platforms hovering 3–6 units above the ground with purple crystals on top and shadow projections below

## Tech Stack

- **Ursina** (Panda3D-based Python game engine)
- **Python 3** — no other dependencies
- Pure Python — no assets needed, all procedural

## License

MIT — Zorp is free to wiggle wherever it wants.