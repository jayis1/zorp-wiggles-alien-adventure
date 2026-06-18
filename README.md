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
| **WASD / Arrow Keys** | Move Zorp (camera-relative) |
| **Right Click + Mouse** | Orbit camera / Look around |
| **Mouse** | Aim at ground |
| **Left Click** | Shoot tentacle laser |
| **Space** | Dash (dodge in movement direction) |
| **Q** | Pulse Wave (push enemies away!) |
| **F** | Toggle achievements panel |
| **E** | Trade with Wandering Trader |
| **M** | Toggle minimap |
| **TAB** | Toggle missions panel |
| **P** | Pause |
| **ESC** | Quit |
| **R** | Restart (on Game Over) |

## Features (v2.13.1 — 3D!)

- Full 3D open world with third-person camera
- Procedurally generated terrain with **11 biomes**: Grass, Desert, Water, Lava, Forest, Crystal, Snow, Swamp, Alien Mushroom Forest, Floating Islands, **Toxic Bog**
- **17 collectible item types** — including **11 power-ups**: Health Potion, Speed Boost, Shield Crystal, Weapon Upgrade (Spread Shot), Magnet Core, Time Warp, Star Fruit (walk on water/lava!), XP Orb (bonus XP scaled by distance!), Fireball Scroll (explosive AOE shots!), Regen Crystal (HP regeneration over time!), **Lucky Clover** (+35% crit chance for 8 seconds!)
- **17 enemy types** — including **Phase Shifter** (teleports!), **Spore Spitter** (fires back!), **Swarm Mite** (fast & tiny), **Void Bomber** (kamikaze explosions!), **Nebula Phantom** (flying orbit + dive attack!), **Starburst Sentinel** (stationary turret firing shockwave rings!), **Cosmic Leech** (drain DoT!), **Void Stalker** (stealth cloak + ambush!), **Plasma Serpent** (segmented snake that splits into mini-enemies when killed!), **Graviton** (gravity pull that drags the player toward it!), **Void Wisp** (tiny, fast, semi-transparent — 50% chance to teleport away when hit!)
- **Critical Hit system** — 15% base chance per shot (boosted to 50% with Lucky Clover!) to deal 2x damage with golden particles, screen shake, and **hit-stop freeze** for satisfying impact!
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
- **Fireball Scroll** — projectiles explode on impact, dealing 50% damage to all enemies within a 4-unit blast radius for 8 seconds! Orange aura visual effect
- **Regen Crystal** — regenerates 8 HP per second for 10 seconds! Green glow visual effect
- **Lucky Clover** — boosts critical hit chance by +35% for 8 seconds (stacks with base 15% for 50% total)! Bright green aura ring and power-up HUD indicator
- **Combo system** — chain kills within 4.5 seconds for XP and score multipliers! +15% XP and +8% score per combo tier. **Visual combo timer bar** shows time remaining before combo resets (green → yellow → red). **Combo milestone fireworks** at x5, x10, x15... — colorful particle bursts erupt around Zorp for hitting kill streak milestones! **At x10+ combo, projectiles gain +25% damage** — a rewards skillful chains with raw firepower
- **Portal system** — 4 pairs of linked portals scattered across the world for fast travel!
- **Wandering Traders** — friendly alien NPCs that wander the world! Trade 5 Space Gloop for rare items
- **Alien Monoliths** — mysterious ancient structures in crystal and snow biomes that grant random buffs when approached! Speed Surge (1.5x speed), Power Surge (1.4x damage), or Wisdom Aura (2x XP) for 10 seconds
- **Weather effects** — rain in grass/forest/swamp biomes, snowfall in snow biomes, rising embers in lava biomes, toxic spore drift in Toxic Bog
- **Biome indicator HUD** — shows your current biome name with color-matching text
- Mission system with collection and kill objectives (19 missions!)
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
- Detailed death screen with survival stats (time, KPM, inventory breakdown, best combo)
- Distinct enemy shapes and decorations (wings, auras, spikes, shards)
- Invincibility frames on damage
- Enemy respawning and loot drops
- Particle system for hits, kills, and pickups
- Dash cooldown indicator on HUD
- **Kill counter** on HUD — shows total kills this run for progression feedback
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
- **Graviton enemy** — floating purple orb that periodically activates a gravity pull, dragging the player toward it! Purple ring visual indicator when pulling, dim warning pulse before activation. Deals continuous damage while pulling. Appears in medium and hard zones
- **Void Wisp enemy** — tiny, semi-transparent, extremely fast enemy that teleports away when hit! 50% chance to blink to a nearby position after taking damage, with teal poof particles at both old and new positions. Spawns in easy and medium zones. Low HP (18) but very evasive
- **Lucky Clover collectible** — uncommon green diamond that boosts critical hit chance by +35% for 8 seconds, stacking with the base 15% for 50% total crit! Bright green power-up aura ring and HUD timer display
- **Kill flash effect** — brief white screen flash on enemy kills for satisfying juice and impact feedback
- **Combo timer bar** — visual progress bar beneath the combo counter showing time remaining before the combo resets. Color shifts from green (full) → yellow (half) → red (almost empty)
- **Boss Health Bar** — prominent health bar appears at the top of the screen when a Plasma Drake (boss) is nearby! Shows boss name and color-coded HP (green → yellow → red)
- **XP Orb collectible** — golden-blue glowing orbs that grant bonus XP scaling with distance from spawn (50–300 XP). Perfect for risk/reward exploration!
- **Hit ripple effect** — expanding ring at enemy hit location for satisfying impact feedback; golden ripple for critical hits, white for normal hits
- **Horizon glow band** — atmospheric colored gradient quads at the horizon line adding depth and alien sky ambiance
- **AI culling for distant enemies** — complex special AI behaviors (teleporting, spitting, orbiting, cloaking) are skipped for enemies beyond 50 units, improving performance with many active enemies
- **Refactored enemy cleanup** — duplicated enemy sub-entity destruction code consolidated into a single `_destroy_enemy_entities()` helper method for cleaner, more maintainable code
- **Low-HP danger vignette** — a pulsing red screen overlay appears when health drops below 30%, with heartbeat-style rhythm that intensifies as HP drops lower — clearer danger feedback than the HP bar alone
- **Low-HP player model pulse** — Zorp's body pulses red when below 30% HP, blending between alien green and danger red in sync with the heartbeat vignette — an in-world visual cue that complements the screen overlay
- **Damage direction indicator** — red directional arrows appear on the HUD pointing toward the source of incoming damage (enemies, projectiles, explosions, shockwaves) — immediately tells you which direction the threat is coming from, with pulsing urgency animation and fade-out
- **Particle color variation** — each burst particle gets a ±20% random color shift for natural, non-uniform effects instead of identical-looking spheres
- **Projectile collision pre-check** — squared-distance pre-check skips expensive sqrt calculations for far-away enemies, improving combat performance with many active enemies
- **Named constants** — magic numbers for shield particles, enemy projectile hit radius, collectible respawn range, and spawn interval extracted into named constants for readability
- **Pulse Wave ability (Q key)** — press Q to emit an expanding teal shockwave that pushes enemies away and deals minor damage! 8-second cooldown. Great for crowd control and creating breathing room when surrounded
- **Achievement system (18 achievements)** — track milestones like First Blood, Warrior, Dragon Slayer, Survivor, and more! Popup notification on unlock with golden particles. Press F to view the full achievements panel
- **Spawn Healing Zone** — a gentle green healing aura surrounds the spawn point, regenerating 5 HP/sec when you're inside it. Pulsing ring visual indicator on the ground. A safe haven to retreat to when low on health
- **Level-scaled collection radius** — both pickup radius and magnetic pull radius grow slightly with each level, rewarding progression with smoother collection
- **Level-up magnet burst** — when you level up, all collectibles within 25 units are vacuumed toward Zorp in a satisfying vortex effect, making level-ups feel powerful and rewarding
- **Enemy Spawn Warning Markers** — a pulsing red ring now appears at enemy spawn locations 1.5 seconds before they materialize! The ring shrinks and pulses faster as the countdown approaches zero, giving you time to react and reposition. No more surprise spawns!
- **Dash Collectible Vacuum** — dashing now pulls nearby collectibles (within 8 units) toward Zorp! Dash through fields of items to vacuum them up, making dash useful for collection as well as dodging
- **Combo Damage Buff** — at combo x10+, your projectiles deal +25% damage! The HUD combo counter displays a ⚔+25% DMG indicator when active, rewarding skillful kill chains with raw firepower
- **Dash Landing Impact** — when a dash ends, Zorp squishes flat with an elastic bounce-back, kicks up a biome-tinted dust burst, and triggers a small camera shake. The dash finally feels like it *lands* instead of just switching off
- **Smooth biome indicator color** — the biome indicator HUD text color smoothly lerps between biomes instead of snapping instantly, for a more polished transition as you explore
- **Dynamic collectible respawn scaling** — when the world is depleted of items (after big combat/loot explosions), the respawn rate ramps up to 4x and spawns in small batches so the world refills faster instead of trickling back one item at a time
- **Projectile glow aura** — tentacle laser shots now have a soft pulsing cyan energy aura around the core, making projectiles look like glowing energy balls instead of flat dots — a visual upgrade that makes shooting feel more powerful
- **Rare collectible pickup flash** — when you pick up a rare-or-better item (rare, very rare, legendary, mythic), the screen edges briefly flash with that item's color, making valuable finds feel special and rewarding instead of identical to common junk
- **Dynamic heartbeat acceleration** — the low-HP danger vignette heartbeat now speeds up as your health drops from 30% to critical, with the pulse rate accelerating from 8 to 14 beats/sec — escalating tension as you near death instead of a flat constant rhythm
- **Enemy idle breathing** — enemies that haven't detected the player gently breathe in and out with a subtle scale oscillation, making the world feel alive instead of populated with frozen statues waiting to aggro
- **Overkill system** — when a kill deals 25+ more damage than the enemy's remaining HP, you get an OVERKILL! Bonus XP, red-orange "OVERKILL" damage number, extra particles, and screen shake reward excessive damage with satisfying feedback
- **HP bar damage shake** — the HP bar on the HUD jitters briefly when you take damage, providing visceral feedback that makes hits feel impactful even when you're not looking at the action
- **Spawn density throttle** — when 8+ enemies are already within 25 units of you, enemy spawning slows down by 50%, preventing overwhelming crowds and keeping combat fair instead of swarming
- **Rare collectible sparkle trail** — rare+ collectibles emit occasional sparkle particles that drift upward in the item's color, making valuable items more visually enticing and easier to spot from a distance

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
| **Fireball Scroll** | 25 pts | Projectiles explode on impact for AOE damage (8s) | Rare |
| **Regen Crystal** | 20 pts | Regenerates 8 HP/sec for 10 seconds | Uncommon |
| **Lucky Clover** | 20 pts | +35% crit chance for 8 seconds | Uncommon |

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
| **Graviton** | 75 | Medium | 10 | **Gravity Pull** | Periodically pulls player toward it; deals DoT while pulling; purple ring indicator |
| **Void Wisp** | 18 | Very Fast | 5 | **Teleport Dodge** | Tiny & semi-transparent; 50% chance to teleport away when hit! |
| Lava Crawler | 100 | Medium | 28 | — | Hot-headed |
| Crystal Guardian | 180 | Slow | 38 | — | Tough |
| Plasma Drake | 350 | Fast | 45 | — | Endgame boss |

## Combo System

Chain kills within 4.5 seconds to build combos! Each combo tier grants:
- **+15% XP bonus** per tier (up to 10 tiers)
- **+8% score bonus** per tier (up to 10 tiers)
- **+25% projectile damage** at combo x10+!
- HUD display with escalating colors: yellow → orange → red
- Combo counter scales up visually as it grows
- **⚔+25% DMG** indicator appears on the combo HUD at x10+

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
- Possible trade rewards: Meteor Shard, Quantum Fuzz, Shield Crystal, Weapon Upgrade, Nebula Dust, Magnet Core, Time Warp, Star Fruit, Fireball Scroll, Regen Crystal, Lucky Clover
- New traders spawn periodically if fewer than 3 are alive
- Trader names: Zix, Glip, Orbix, Fweem

## Pulse Wave Ability

- Press **Q** to emit an expanding teal shockwave from Zorp's position
- The wave **pushes enemies away** with strong knockback and deals 8 damage
- **8-second cooldown** — shown on HUD as "PULSE READY [Q]" or countdown timer
- Great for **crowd control** — use when surrounded to create breathing room
- Visual: expanding teal ring that fades as it spreads outward
- Kills from pulse wave count toward combos and drop loot!

## Spawn Healing Zone

- A **gentle green healing aura** surrounds the world's center (spawn point)
- Regenerates **5 HP per second** while inside the zone
- Pulsing green ring on the ground marks the healing area
- HUD indicator shows "♥ HEALING ZONE" when inside
- Perfect safe haven to retreat to when low on health

## Achievements

Press **F** to view the achievements panel. 18 milestones to unlock:

| Achievement | Requirement | Icon |
|-------------|-------------|------|
| First Blood | Defeat 1 enemy | ☠ |
| Hunter | Defeat 10 enemies | ⚔ |
| Warrior | Defeat 50 enemies | 🗡 |
| Warlord | Defeat 100 enemies | 🔥 |
| Gatherer | Collect 50 items | 💎 |
| Hoarder | Collect 200 items | 💰 |
| Evolver | Reach level 5 | ⬆ |
| Ascended | Reach level 10 | ✦ |
| Chain Killer | Reach a 5x combo | ⚡ |
| Unstoppable | Reach a 10x combo | 💥 |
| Dragon Slayer | Defeat a Plasma Drake | 🐉 |
| Survivor | Survive 5 minutes | 🛡 |
| Veteran | Survive 10 minutes | ⏳ |
| Rich Alien | Reach 1000 score | 🌟 |
| Galactic Tycoon | Reach 5000 score | 👑 |
| Mission Runner | Complete 5 missions | 📋 |
| Shockwave | Use Pulse Wave | 🌀 |
| Trader | Complete a trade | 🤝 |

Golden popup notification appears when an achievement unlocks!

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

## Changelog

### v2.13.1 — Portal Bursts, Smart Monoliths, Trader Glow & Dash Flash
- **Portal Teleport Burst**: Stepping into a portal now triggers dramatic particle bursts at BOTH the departure point (cyan) and arrival point (purple), plus an extra ring burst at the destination. Teleporting feels like a real event instead of a silent blink — you see where you left and where you landed
- **Smart Monolith Activation**: Monoliths no longer waste their 45-second cooldown when you already have all three buffs active (Speed Surge, Power Surge, Wisdom Aura). They wait patiently until at least one buff expires before granting a new one — no more frustrating duplicate buffs
- **Trader Proximity Glow**: Wandering traders now pulse with a warm golden glow when you're within trade range, making it immediately obvious that interaction is available without reading the tiny trade prompt text. The glow brightens and dims rhythmically to draw your eye
- **Dash Readiness Flash**: When the dash cooldown ends, a brief cyan pulse flashes behind the "DASH READY" text on the HUD. This draws your peripheral attention to the fact that dash is available again — no more wondering "is dash off cooldown yet?" while dodging enemies

### v2.13.0 — Overkill, HP Shake, Spawn Balance & Sparkles
- **Overkill System**: When a kill deals 25+ more damage than the enemy's remaining HP, you trigger an OVERKILL! A red-orange "OVERKILL" damage number appears (bigger than even crit numbers), bonus XP is granted (scaled by combo and monolith multipliers), orange particles burst from the enemy, and the screen shakes harder. Makes high-damage crits and high-level shots against weak enemies feel satisfying instead of wasteful
- **HP Bar Damage Shake**: The HP bar on the HUD now jitters briefly (0.4s) when you take damage, with decreasing intensity. This provides visceral, immediate feedback that you've been hit — you feel each damage event even when focused on the action. The shake applies to both the HP bar fill and its background
- **Spawn Density Throttle**: When 8 or more enemies are already within 25 units of the player, enemy spawning slows down by 50% (spawn interval doubled). This prevents unfair overwhelming crowds while still keeping the world populated — combat stays challenging but fair, giving you breathing room to thin the herd before more arrive
- **Rare Collectible Sparkle Trail**: Rare+ collectibles (rare, very rare, legendary, mythic) now emit occasional sparkle particles that drift upward in the item's color. This makes valuable items more visually enticing and easier to spot from a distance — you'll notice that legendary Cosmic Jelly or mythic Plasma Core shimmering in the distance before you even see its glow ring

### v2.12.2 — Visual Polish & Game Feel
- **Projectile Glow Aura**: Tentacle laser shots now feature a soft pulsing cyan energy aura around the core sphere, making projectiles look like glowing energy balls instead of flat dots. The aura gently pulses in brightness as the projectile flies, giving every shot a more powerful, satisfying visual presence
- **Rare Collectible Pickup Flash**: When you pick up a rare-or-better item (rare, very rare, legendary, mythic), the screen edges briefly flash with that item's color — making valuable finds feel special and rewarding instead of identical to picking up common Space Gloop. Mythic Plasma Core pickups now get a dramatic magenta flash!
- **Dynamic Heartbeat Acceleration**: The low-HP danger vignette heartbeat now speeds up as your health drops from 30% toward 0%, with the pulse rate accelerating from 8 to 14 beats/sec. This creates escalating tension as you near death — the heartbeat gets faster and more frantic — instead of a flat constant rhythm. The player model's red pulse syncs with the accelerated heartbeat too
- **Enemy Idle Breathing**: Enemies that haven't detected the player gently breathe in and out with a subtle 4% scale oscillation, making the world feel alive instead of populated with frozen statues waiting to aggro. Once an enemy detects you, the breathing stops and it switches to active combat behavior

### v2.12.1 — Performance, Dash Landing & Polish
- **Collectible Loop Performance**: The collectible update loop (200+ items per frame) now uses squared-distance pre-checks instead of calling `sqrt` for every item. Most distant collectibles skip the expensive square-root call entirely, reducing per-frame overhead when the world is full of loot. Player position is also cached once per loop to avoid repeated Vec3 property access
- **Dash Landing Impact**: Dashing previously ended with zero feedback — Zorp just stopped dead. Now when a dash ends, Zorp squishes flat (recovering with an elastic bounce), kicks up a biome-tinted dust burst, and triggers a small camera shake. The dash finally feels like it *lands* instead of just switching off
- **Smooth Biome Indicator Color**: The biome indicator HUD text used to snap its color instantly when you crossed a biome border. The color now smoothly lerps between biomes for a more polished, less jarring transition as you explore
- **Dynamic Collectible Respawn Scaling**: The collectible respawn rate now scales with how depleted the world is. When the item count drops well below the minimum (e.g., after a big combat/loot explosion), the respawn chance ramps up to 4x the base rate and spawns in small batches, so the world refills faster instead of trickling back one item at a time

### v2.12.0 — Spawn Warnings, Dash Vacuum & Combo Damage
- **Enemy Spawn Warning Markers**: Enemies no longer appear out of thin air! A pulsing red ring now appears at the spawn location 1.5 seconds before the enemy materializes. The ring shrinks and pulses faster as the countdown approaches, giving players time to react and reposition — eliminating unfair surprise spawns
- **Dash Collectible Vacuum**: Dashing through fields of collectibles now vacuums them toward Zorp! Items within 8 units get pulled in and spin rapidly, making dash a versatile tool for both dodging enemies and collecting loot at high speed
- **Combo Damage Buff**: Maintaining a combo of x10 or higher now grants +25% projectile damage! The HUD combo counter displays a ⚔+25% DMG indicator when active, rewarding skilled players who chain kills with raw firepower on top of the existing XP and score bonuses

### v2.11.1 — Kill Impact & Polish
- **Kill Burst Particles**: Enemy deaths now produce a dramatic radial ring of particles that burst outward and upward, making kills feel more explosive and satisfying — a clear visual upgrade from the previous single-direction particle spray
- **Collectible Spawn Animation**: Collectibles no longer pop into existence instantly. They now scale up from tiny with an elastic overshoot over 0.4 seconds, with the glow ring fading in partway through — giving the world a more alive, polished feel when items respawn
- **Dash Afterimage Ghost**: Initiating a dash now leaves a brief green afterimage silhouette at the starting position that fades over 0.25 seconds, making the dash feel faster and more dramatic while clearly communicating the dash direction
- **Enhanced Low-HP Heartbeat Vignette**: The danger vignette now uses a sharper `sin^1.5` heartbeat curve that feels more like an actual heartbeat (sharp thump, quick fade) instead of a smooth sine wave. When HP drops below 15%, a brief bright-red flash appears at the peak of each heartbeat for urgent near-death warning

### v2.10.2 — Movement & Combat Polish
- **Smooth Acceleration/Deceleration**: Player movement now uses velocity-based acceleration (45 units/s²) and deceleration (25 units/s²) instead of instant start/stop. Zorp feels heavier and more responsive — starting has a satisfying ramp-up and stopping has a gentle slide that makes the alien feel more physical
- **Wall Sliding**: Moving diagonally into walls no longer stops Zorp dead. The movement system now tries each axis independently, so you slide along obstacles smoothly — a huge quality-of-life improvement for navigating tight terrain
- **Dash Invincibility**: Dashing now grants 0.3 seconds of invulnerability, making dash a true dodge mechanic rather than just a speed boost. Time your dashes to avoid attacks!
- **Enemy Spawn Grace Period**: Newly spawned enemies no longer aggro instantly. They have a 2-second grace period where they can't detect the player, during which they fade in with a materializing visual effect (scaling up from small, flashing bright before settling to their normal color). This prevents unfair instant-attacks from enemies that just appeared

### v2.10.1 — Game Feel & UX Polish
- **Smooth Enemy Rotation**: Enemies now smoothly rotate toward the player instead of snapping instantly, making movement feel more natural and polished. Traders also turn smoothly at a slower rate for a casual feel
- **Movement Dust Particles**: Subtle dust puffs now appear beneath Zorp while moving, with color that adapts to the current biome (green dust on grass, tan on desert, blue on snow, etc.) — gives movement a more grounded, alive feel
- **Kill Counter HUD**: A persistent "Kills: N" display has been added below the score, providing real-time progression feedback without waiting for the death screen
- **Best Combo Tracker**: The highest combo streak reached during a run is now tracked and displayed on the death screen as "Best Combo: xN" — gives players a satisfying milestone to beat

### v2.9.2 — Game Feel & Visual Polish
- **Camera Kill Zoom**: Brief FOV punch-in effect on enemy kills for cinematic impact, complementing existing hit-stop and screen shake
- **Power-Up Aura Ring**: Pulsing ground ring appears under Zorp when a buff is active (shield=cyan, speed=green, magnet=purple, weapon=orange, fireball=red, regen=green, damage=red, XP=gold) — makes active buffs immediately visible at a glance
- **Game Balance**: XP Orb distance bonus increased from 2 to 3 per 50 units from spawn, making deep exploration more rewarding
- **Code Quality**: Added `_dist2d_coords()` static method for cleaner 2D distance calculations from raw coordinates; replaced two inline `math.sqrt((x1-x2)**2 + (z1-z2)**2)` patterns with the helper

### v2.9.1 — Polish & Performance
- **Game Balance**: Reduced first level-up threshold from 100 to 80 XP for smoother early-game progression; collectible XP now has a floor of 1 (no more 0 XP drops from cheap items)
- **Visual Polish**: Zorp's eye pupils now track the mouse/facing direction, giving the character personality and better aim feedback
- **Performance**: Collectible update loop skips magnetic pull/glow calculations for items >60 units from the player, reducing per-frame overhead with 120+ collectibles
- **Game Feel**: Combo HUD now displays the XP bonus percentage (e.g., "COMBO x3 (+30% XP)"), making the reward system transparent and satisfying