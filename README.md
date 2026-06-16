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
| **E** | Trade with Wandering Trader |
| **M** | Toggle minimap |
| **TAB** | Toggle missions panel |
| **P** | Pause |
| **ESC** | Quit |
| **R** | Restart (on Game Over) |

## Features (v2.7.1 — 3D!)

- Full 3D open world with third-person camera
- Procedurally generated terrain with **11 biomes**: Grass, Desert, Water, Lava, Forest, Crystal, Snow, Swamp, Alien Mushroom Forest, Floating Islands, **Toxic Bog**
- **14 collectible item types** — including **8 power-ups**: Health Potion, Speed Boost, Shield Crystal, Weapon Upgrade (Spread Shot), Magnet Core, Time Warp, Star Fruit (walk on water/lava!), **XP Orb** (bonus XP scaled by distance!)
- **15 enemy types** — including **Phase Shifter** (teleports!), **Spore Spitter** (fires back!), **Swarm Mite** (fast & tiny), **Void Bomber** (kamikaze explosions!), **Nebula Phantom** (flying orbit + dive attack!), **Starburst Sentinel** (stationary turret firing shockwave rings!), **Cosmic Leech** (drain DoT!), **Void Stalker** (stealth cloak + ambush!), **Plasma Serpent** (segmented snake that splits into mini-enemies when killed!)
- **Critical Hit system** — 15% chance per shot to deal 2x damage with golden particles, screen shake, and **hit-stop freeze** for satisfying impact!
- **Dash ability** — press Space to dodge in your movement direction (2s cooldown)
- Tentacle laser shooting with particle effects
- **Spread Shot weapon upgrade** — pick up a Weapon Upgrade to fire 3 lasers in a fan pattern for 8 seconds!
- **Shield power-up** — blocks all damage for 5 seconds
- **Speed Boost** — 1.8x speed for 6 seconds
- **Health Potion** — restores 55 HP instantly
- **Magnet Core** — boosts item pull radius 2.5x and pull speed 2x for 6 seconds!
- **Time Warp** — slows ALL enemies to 30% speed for 6 seconds! Enemies tint blue while affected
- **Star Fruit** — walk over water and lava for 6 seconds! Golden shimmer ring appears beneath you
- **XP Orb** — grants bonus XP that scales with distance from spawn! Up to 300 XP in distant regions
- **Combo system** — chain kills within 4.5 seconds for XP and score multipliers! +15% XP and +8% score per combo tier
- **Portal system** — 4 pairs of linked portals scattered across the world for fast travel!
- **Wandering Traders** — friendly alien NPCs that wander the world! Trade 5 Space Gloop for rare items
- **Alien Monoliths** — mysterious ancient structures in crystal and snow biomes that grant random buffs when approached! Speed Surge (1.5x speed), Power Surge (1.4x damage), or Wisdom Aura (2x XP) for 10 seconds
- **Weather effects** — rain in grass/forest/swamp biomes, snowfall in snow biomes, rising embers in lava biomes, toxic spore drift in Toxic Bog
- **Biome indicator HUD** — shows your current biome name with color-matching text
- Mission system with collection and kill objectives (16 missions!)
- XP and leveling system (get stronger over time — +12 HP, +0.4 speed, and a heal per level!)
- Distance-based difficulty scaling (harder enemies farther from spawn)
- **Per-enemy loot drops** — tougher enemies drop more items! Plasma Drake drops 4–6 items, Slime Blobs drop 1–2
- Minimap with player tracking and enemy dots
- Enemy HP bars with green→yellow→red color gradient
- 3D trees in forests, crystal spires in crystal biomes, alien mushrooms in mushroom biomes
- **Floating Islands biome** — raised platforms with purple crystals and shadow projections
- **Alien Ruins** — stone pillars and broken walls in desert biomes
- **Toxic Bog biome** — toxic pools, fungal stalks, and drifting spores
- **Alien Monoliths** — tall ancient crystal-topped structures in crystal and snow biomes that activate when you approach, granting random temporary buffs with visual feedback
- Atmospheric fog and lighting with nebula starfield sky
- Smooth camera follow with screen shake on hits, kills, and crits
- Enemy death animations (pop upward, shrink, flash, and dissolve)
- Level-up flash effect and scale pulse
- Satisfying collectible pickup burst particles with magnetic pull snap
- **Critical hit damage numbers** — gold text with ★ prefix for crits
- Floating damage numbers on enemy hits and kills
- Detailed death screen with survival stats (time, KPM, inventory breakdown)
- Distinct enemy shapes and decorations (wings, auras, spikes, shards)
- Invincibility frames on damage
- Enemy respawning and loot drops
- Particle system for hits, kills, and pickups
- Dash cooldown indicator on HUD
- Active power-up timers displayed on HUD (including monolith buff timers)
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
- **Kill feed** — rolling top-right corner display shows recent enemy kills with fade-out animation
- **Cosmic Leech enemy** — small, fast enemy that applies a damage-over-time drain debuff on contact (shown as purple flash on player)
- **Drain DoT system** — Cosmic Leech's drain deals damage over time for 4 seconds; blocked by Shield
- **Void Stalker enemy** — stealth predator that cloaks (nearly invisible) and decloaks to ambush! First hit from stealth deals 50% bonus damage
- **Plasma Serpent enemy** — segmented snake-like creature with 4 body segments that smoothly follow the head. When killed, each segment scatters into a Swarm Mite! Screen shake and particle burst on split
- **XP Orb collectible** — golden-blue glowing orbs that grant bonus XP scaling with distance from spawn (50–300 XP). Perfect for risk/reward exploration!

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
| Crystal | Cyan | Yes | Crystal spires, **alien monoliths** |
| Snow | White | Yes | Icy terrain, snowfall weather, **alien monoliths** |
| Swamp | Murky Green | Yes | Squishy ground, rain weather |
| Mushroom | Alien Green | Yes | Colorful alien mushrooms with spore glow |
| **Floating Islands** | Lavender | Yes | Raised platforms with purple crystals and ground shadows |
| **Toxic Bog** | Sickly Green | Yes | Toxic pools, fungal stalks, drifting spore particles |

## Collectibles

| Item | Value | Effect | Rarity |
|------|-------|--------|--------|
| Space Gloop | 10 pts | Score only | Common |
| Meteor Shard | 25 pts | Score only | Uncommon |
| Quantum Fuzz | 50 pts | Score only | Rare |
| Nebula Dust | 100 pts | Score only | Very Rare |
| Cosmic Jelly | 200 pts | Score only | Legendary |
| Plasma Core | 350 pts | Score only | Mythic |
| **Health Potion** | 15 pts | Restores 55 HP | Common |
| **Speed Boost** | 15 pts | 1.8x speed for 6s | Uncommon |
| **Shield Crystal** | 15 pts | Blocks all damage for 5s | Rare |
| **Weapon Upgrade** | 20 pts | Spread shot (3 lasers) for 8s | Rare |
| **Magnet Core** | 20 pts | 2.5x pull radius + 2x pull speed for 6s | Uncommon |
| **Time Warp** | 25 pts | Slows ALL enemies to 30% speed for 6s | Rare |
| **Star Fruit** | 20 pts | Walk over water/lava for 6s | Uncommon |
| **XP Orb** | 25 pts | Bonus XP (50–300) scaled by distance from spawn | Uncommon |

## Enemies

| Enemy | HP | Speed | Damage | Special | Notes |
|-------|----|-------|--------|---------|-------|
| Slime Blob | 25 | Slow | 8 | — | Common, easy |
| Swarm Mite | 12 | Very Fast | 3 | — | Tiny & fast, spawns in groups |
| Space Beetle | 45 | Medium | 12 | — | Aggressive |
| Phase Shifter | 60 | Medium | 18 | **Teleports** | Warps near player periodically |
| **Starburst Sentinel** | 60 | Stationary | 12 | **Shockwave Rings** | Immobile turret that fires expanding energy rings |
| **Void Bomber** | 50 | Medium | 15 | **Kamikaze!** | Explodes near player, also damages other enemies |
| **Nebula Phantom** | 90 | Fast | 25 | **Orbit + Dive** | Circles player in the air, then dive-attacks! |
| Void Wraith | 70 | Medium | 22 | — | Spooky |
| Spore Spitter | 80 | Slow | 12 | **Shoots back** | Fires projectiles at player |
| **Cosmic Leech** | 30 | Fast | 4 | **Drain DoT** | Small & fast, applies damage-over-time |
| **Void Stalker** | 55 | Fast | 15 | **Stealth Cloak** | Nearly invisible when cloaked, decloaks to ambush for 50% bonus damage |
| **Plasma Serpent** | 120 | Medium | 20 | **Segmented + Splits** | Snake with 4 body segments; splits into Swarm Mites on death |
| Lava Crawler | 100 | Medium | 28 | — | Hot-headed |
| Crystal Guardian | 180 | Slow | 38 | — | Tough |
| Plasma Drake | 350 | Fast | 45 | — | Endgame boss |

## Combo System

Chain kills within 4.5 seconds to build combos! Each combo tier grants:
- **+15% XP bonus** per tier (up to 10 tiers)
- **+8% score bonus** per tier (up to 10 tiers)
- HUD display with escalating colors: yellow → orange → red
- Combo counter scales up visually as it grows

## Critical Hits

Every projectile hit has a **15% chance** to be a critical hit, dealing **2x damage**! Critical hits feature:
- Golden particle burst at impact point
- Extra screen shake for impact
- Enemy flashes yellow briefly
- Larger floating damage number showing the critical damage

## Portals

- **4 pairs of linked portals** scattered across the world
- Step into a portal to teleport to its partner (opposite side of the map)
- 3-second cooldown prevents rapid back-and-forth teleportation
- Portals glow cyan/purple and spin with pulsing ground markers
- Use portals for fast travel and escaping dangerous situations!

## Wandering Traders

- **Friendly alien NPCs** wander the world, wearing purple hats
- Approach a trader and press **E** to trade 5 Space Gloop for a random rare item
- Possible trade rewards: Meteor Shard, Quantum Fuzz, Shield Crystal, Weapon Upgrade, Nebula Dust, Magnet Core, Time Warp, Star Fruit
- New traders spawn periodically if fewer than 3 are alive
- Trader names: Zix, Glip, Orbix, Fweem

## Alien Monoliths

- **Mysterious ancient structures** found in crystal and snow biomes
- Tall pillar topped with a glowing crystal, rotating ring, and pulsing ground glow
- Approach within range to activate — grants a random buff:
  - **Speed Surge**: 1.5x movement speed for 10 seconds (green glow)
  - **Power Surge**: 1.4x projectile damage for 10 seconds (orange glow)
  - **Wisdom Aura**: 2x XP gain for 10 seconds (blue glow)
- 45-second cooldown between activations per monolith
- Colored ring appears around Zorp when a buff is active
- Buff timers shown on HUD alongside other power-ups

## World Features

- **Alien Ruins** in desert biomes — scattered stone pillars (1–4 per ruin) and broken wall segments, giving the desert a mysterious ancient civilization feel
- **Floating Islands** — elevated platforms hovering 3–6 units above the ground with purple crystals on top and shadow projections below
- **Toxic Bog** — murky green terrain with bubbling toxic pools, twisted fungal stalks with glowing caps, and drifting toxic spore particles
- **Portal Pairs** — 4 linked portal pairs for fast travel across the map
- **Alien Monoliths** — tall ancient crystal-topped structures that grant temporary buffs when approached

## Tech Stack

- **Ursina** (Panda3D-based Python game engine)
- **Python 3** — no other dependencies
- Pure Python — no assets needed, all procedural

## License

MIT — Zorp is free to wiggle wherever it wants.