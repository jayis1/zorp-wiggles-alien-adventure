"""
Zorp Wiggles: Alien Adventure — 3D Open World
You are Zorp, a squishy green alien exploring a 3D procedurally-generated planet.
Collect weird stuff, complete missions, blast enemies with your tentacle laser.
Built with Ursina engine (Panda3D).
"""

from ursina import *
import math
import random
import json

app = Ursina(title='Zorp Wiggles: Alien Adventure', borderless=False, fullscreen=False)

# ─── Version ──────────────────────────────────────────────────────────────────
VERSION = "2.3.1"

# ─── World Generation ─────────────────────────────────────────────────────────
WORLD_SIZE = 80
TILE_SCALE = 4

# ─── Player ───────────────────────────────────────────────────────────────────
PLAYER_SPEED = 12
PLAYER_INVULN_DURATION = 0.5
PLAYER_BLINK_RATE = 20
PLAYER_START_HP = 100

# ─── Combat ───────────────────────────────────────────────────────────────────
SHOOT_COOLDOWN = 0.12
COLLECT_RADIUS = 2.5
COLLECT_PULL_RADIUS = 5.0
COLLECT_PULL_SPEED = 12.0
PROJECTILE_BASE_DAMAGE = 20
PROJECTILE_LEVEL_DAMAGE_BONUS = 2
PROJECTILE_SPEED = 55
PROJECTILE_LIFETIME = 2.0
ENEMY_DETECT_RANGE = 35
ENEMY_ATTACK_RANGE = 2.5
ENEMY_ATTACK_COOLDOWN = 1.0

# ─── Enemy Behavior ───────────────────────────────────────────────────────────
ENEMY_WANDER_SPEED_FACTOR = 0.3
ENEMY_WANDER_INTERVAL_MIN = 2.0
ENEMY_WANDER_INTERVAL_MAX = 5.0
ENEMY_WANDER_DIR_JITTER = 1.5

# ─── Spawning ─────────────────────────────────────────────────────────────────
MAX_ACTIVE_ENEMIES = 40
MIN_COLLECTIBLES = 120
COLLECTIBLE_RESPAWN_CHANCE = 0.01
ENEMY_SPAWN_INTERVAL = 10
ENEMY_SPAWN_INTERVAL_LEVEL_DECAY = 0.5   # seconds faster per player level tier
ENEMY_SPAWN_DISTANCE_MIN = 30
ENEMY_SPAWN_DISTANCE_MAX = 60
LOOT_DROP_MIN = 1
LOOT_DROP_MAX = 3
INITIAL_COLLECTIBLES = 200
INITIAL_ENEMIES = 60
SPAWN_SAFE_RADIUS = 15
ENEMY_SPAWN_SAFE_RADIUS = 30

# ─── Leveling ─────────────────────────────────────────────────────────────────
LEVEL_UP_HEAL_AMOUNT = 25
LEVEL_UP_HP_BONUS = 10
LEVEL_UP_SPEED_BONUS = 0.3
XP_SCALE_FACTOR = 1.5
BASE_KILL_XP = 25
KILL_XP_HP_DIVISOR = 10

# ─── Visual Effects ───────────────────────────────────────────────────────────
DEATH_ANIM_DURATION = 0.4
SCREEN_SHAKE_DAMAGE = 0.35
SCREEN_SHAKE_KILL = 0.6
SCREEN_SHAKE_DECAY = 10.0
LEVEL_UP_FLASH_DURATION = 1.5
CAMERA_LERP_SPEED = 6.0
CAMERA_HEIGHT = 18
CAMERA_DISTANCE = 22
CAMERA_ANGLE = 30

# ─── Particles ────────────────────────────────────────────────────────────────
PARTICLE_GRAVITY = 9.8
PARTICLE_SCALE_DECAY = 0.97
MAX_PARTICLES = 150
PARTICLE_HIT_COUNT = 8
PARTICLE_KILL_COUNT = 14
PARTICLE_DAMAGE_COUNT = 6
PARTICLE_COLLECT_COUNT = 10
PARTICLE_LEVELUP_COUNT = 20

# ─── Projectile Trail ────────────────────────────────────────────────────────
PROJECTILE_TRAIL_INTERVAL = 0.03  # Seconds between trail dot spawns
PROJECTILE_TRAIL_LIFETIME = 0.25  # How long each trail dot lives
PROJECTILE_TRAIL_START_SCALE = 0.22  # Initial scale of trail dot
PROJECTILE_TRAIL_END_SCALE = 0.02   # Scale at end of trail dot life (shrinks away)

# ─── Player Squish/Stretch ───────────────────────────────────────────────────
PLAYER_SQUISH_AMOUNT = 0.18   # How much the player squishes on landing/moving
PLAYER_SQUISH_SPEED = 8.0     # How fast the squish animation runs
PLAYER_STRETCH_FACTOR = 1.14  # Y stretch when moving (elongated alien look)
PLAYER_SQUASH_FACTOR = 0.86   # X/Z squish when moving (compressed look)

# ─── Hit-Stop ────────────────────────────────────────────────────────────────
HIT_STOP_KILL_DURATION = 0.06  # Brief freeze on kills for impact feel

# ─── Enemy Knockback ──────────────────────────────────────────────────────────
ENEMY_KNOCKBACK_FORCE = 4.0    # How far enemies get pushed on hit
ENEMY_KNOCKBACK_UP = 2.0       # Upward component of knockback

# ─── Collectible Pop ──────────────────────────────────────────────────────────
COLLECT_POP_DURATION = 0.18    # Seconds for the scale-up animation before destruction
COLLECT_POP_MAX_SCALE = 2.2    # Peak scale multiplier during pop (elastic overshoot)

# ─── Player-Level Difficulty Scaling ──────────────────────────────────────────
PLAYER_LEVEL_DIFFICULTY_INTERVAL = 5   # Player levels per difficulty tier increase
ENEMY_HP_SCALE_PER_TIER = 0.15        # +15% enemy HP per difficulty tier above base
ENEMY_DAMAGE_SCALE_PER_TIER = 0.10    # +10% enemy damage per difficulty tier above base

# ─── Damage Numbers ──────────────────────────────────────────────────────────
DMG_NUMBER_LIFETIME = 1.0
DMG_NUMBER_RISE_SPEED = 3.0
DMG_NUMBER_SCALE = 1.2

# ─── Death Screen ────────────────────────────────────────────────────────────
DEATH_SCREEN_STATS_COLOR = color.white
DEATH_SCREEN_TITLE_COLOR = color.red

# ─── Stars ────────────────────────────────────────────────────────────────────
STAR_COUNT = 50
STAR_HEIGHT_MIN = 80
STAR_HEIGHT_MAX = 150
STAR_SPREAD = 200

# ─── Biome Fog ────────────────────────────────────────────────────────────────
BIOME_FOG = {
    'grass':   {'color': color.rgb(25, 0, 60),   'density': 0.007},
    'desert':  {'color': color.rgb(60, 40, 20),   'density': 0.012},
    'water':   {'color': color.rgb(10, 30, 80),   'density': 0.009},
    'lava':    {'color': color.rgb(60, 10, 10),   'density': 0.015},
    'forest':  {'color': color.rgb(10, 30, 10),   'density': 0.010},
    'crystal': {'color': color.rgb(15, 30, 50),   'density': 0.008},
    'snow':    {'color': color.rgb(40, 40, 55),    'density': 0.006},
    'swamp':   {'color': color.rgb(25, 35, 15),    'density': 0.014},
    'mushroom': {'color': color.rgb(20, 10, 40),   'density': 0.011},
    'floating_islands': {'color': color.rgb(30, 20, 50),   'density': 0.006},
}

# ─── Biome Generation ─────────────────────────────────────────────────────────
BIOME_BLOB_COUNT = 50
BIOME_BLOB_RADIUS_MIN = 3
BIOME_BLOB_RADIUS_MAX = 10
BIOME_BLOB_JITTER = 1.5
SPAWN_CLEAR_RADIUS = 5
SPAWN_PAD_RADIUS = 3

# ─── Dash ─────────────────────────────────────────────────────────────────────
DASH_COOLDOWN = 2.0
DASH_SPEED = 60
DASH_DURATION = 0.2
DASH_TRAIL_PARTICLES = 6

# ─── Power-Up Durations ───────────────────────────────────────────────────────
SPEED_BOOST_DURATION = 5.0
SPEED_BOOST_MULTIPLIER = 1.8
SHIELD_DURATION = 4.0
HEALTH_POTION_HEAL = 30

# ─── Combo System ────────────────────────────────────────────────────────────
COMBO_TIMEOUT = 5.0        # seconds before combo resets
COMBO_XP_BONUS_PER_TIER = 0.1  # +10% XP per combo tier
COMBO_SCORE_BONUS_PER_TIER = 0.05  # +5% score per combo tier
COMBO_DISPLAY_LIFETIME = 2.5

# ─── Weapon Upgrade (Spread Shot) ────────────────────────────────────────────
WEAPON_UPGRADE_DURATION = 8.0
SPREAD_ANGLE = 12  # degrees between spread shot projectiles

# ─── Weather ────────────────────────────────────────────────────────────────
WEATHER_PARTICLE_COUNT = 60
WEATHER_SNOW_COUNT = 40
WEATHER_EMBER_COUNT = 30
WEATHER_FALL_SPEED_RAIN = 25
WEATHER_FALL_SPEED_SNOW = 5
WEATHER_FALL_SPEED_EMBER = 3
WEATHER_DRIFT_SNOW = 2
WEATHER_DRIFT_EMBER = 4

# ─── Void Bomber (New Enemy) ────────────────────────────────────────────────
VOID_BOMBER_DETECT_RANGE = 30
VOID_BOMBER_FUSE_RANGE = 6
VOID_BOMBER_FUSE_TIME = 1.2
VOID_BOMBER_EXPLOSION_RADIUS = 5.5
VOID_BOMBER_EXPLOSION_DAMAGE = 40

# ─── Difficulty Scaling ──────────────────────────────────────────────────────
EASY_ENEMY_TYPES = ['Slime Blob', 'Space Beetle', 'Swarm Mite']
MEDIUM_ENEMY_TYPES = ['Space Beetle', 'Void Wraith', 'Phase Shifter', 'Void Bomber']
HARD_ENEMY_TYPES = ['Void Wraith', 'Lava Crawler', 'Crystal Guardian', 'Plasma Drake', 'Spore Spitter', 'Void Bomber', 'Nebula Phantom']
DIFFICULTY_SCALE_DISTANCE = 100  # world units per difficulty tier

# ─── Nebula Phantom (New Enemy) ────────────────────────────────────────────
NEBULA_PHANTOM_ORBIT_RADIUS = 12
NEBULA_PHANTOM_ORBIT_SPEED = 2.0
NEBULA_PHANTOM_DIVE_SPEED = 25
NEBULA_PHANTOM_DIVE_COOLDOWN_MIN = 4.0
NEBULA_PHANTOM_DIVE_COOLDOWN_MAX = 7.0

# ─── Magnet Core (New Collectible) ────────────────────────────────────────
MAGNET_DURATION = 6.0
MAGNET_PULL_RADIUS_MULT = 2.5
MAGNET_PULL_SPEED_MULT = 2.0

# ─── Floating Islands Biome ──────────────────────────────────────────────
FLOATING_ISLAND_HEIGHT_MIN = 3
FLOATING_ISLAND_HEIGHT_MAX = 6
FLOATING_ISLAND_SPAWN_CHANCE = 0.15
FLOATING_ISLAND_CRYSTAL_CHANCE = 0.4

# ─── Alien Ruins ──────────────────────────────────────────────────────────
RUINS_PILLAR_CHANCE = 0.08
RUINS_WALL_CHANCE = 0.05

# ─── Collectible Weighted Spawn ─────────────────────────────────────────────
COLLECTIBLE_WEIGHTS = {
    'Space Gloop':    30,   # Common
    'Health Potion':  18,   # Common-ish (useful early game)
    'Meteor Shard':   15,   # Uncommon
    'Speed Boost':    10,   # Uncommon
    'Quantum Fuzz':   8,    # Rare
    'Shield Crystal': 5,   # Rare
    'Weapon Upgrade': 4,   # Rare
    'Magnet Core':    7,    # Uncommon
    'Nebula Dust':    4,    # Very Rare
    'Cosmic Jelly':   3,    # Legendary
    'Plasma Core':    3,    # Mythic
}

# ─── Minimap ─────────────────────────────────────────────────────────────────
MINIMAP_SIZE = 0.22
MINIMAP_POSITION = (0.72, 0.37)
MINIMAP_RESOLUTION = 80  # pixels per side for terrain texture
MINIMAP_ENEMY_DOT_SIZE = 0.006
MINIMAP_ENEMY_DOT_RGB = (255, 60, 60)
MINIMAP_PLAYER_DOT_SIZE = 0.008
MINIMAP_PLAYER_DOT_RGB = (255, 255, 255)
MINIMAP_REFRESH_INTERVAL = 0.25  # seconds between minimap redraws

# ─── Collectible Glow Pulse ──────────────────────────────────────────────────
GLOW_PULSE_SPEED = 3.5        # how fast the glow ring pulses
GLOW_PULSE_MIN_SCALE = 2.8     # minimum glow scale
GLOW_PULSE_MAX_SCALE = 3.8     # maximum glow scale

# ─── Sky Nebula ──────────────────────────────────────────────────────────────
NEBULA_CLOUD_COUNT = 8
NEBULA_SPREAD = 250
NEBULA_HEIGHT_MIN = 100
NEBULA_HEIGHT_MAX = 180

# ─── Colors ───────────────────────────────────────────────────────────────────
C_GRASS    = color.rgb(34, 139, 34)
C_DESERT   = color.rgb(210, 180, 100)
C_WATER    = color.rgb(30, 100, 200)
C_LAVA     = color.rgb(200, 30, 30)
C_FOREST   = color.rgb(0, 80, 0)
C_CRYSTAL  = color.rgb(0, 200, 210)
C_SNOW     = color.rgb(220, 220, 240)
C_SWAMP    = color.rgb(60, 90, 40)
C_ALIEN    = color.rgb(0, 230, 70)
C_ENEMY    = color.rgb(200, 30, 30)
C_LASER    = color.rgb(0, 255, 255)
C_GOLD     = color.rgb(255, 215, 0)
C_PURPLE   = color.rgb(170, 0, 255)
C_PINK     = color.rgb(255, 80, 180)
C_MUSHROOM = color.rgb(50, 180, 90)
C_FLOATING_ISLANDS = color.rgb(180, 140, 220)

BIOME_COLORS = {
    'grass':   C_GRASS,
    'desert':  C_DESERT,
    'water':   C_WATER,
    'lava':    C_LAVA,
    'forest':  C_FOREST,
    'crystal': C_CRYSTAL,
    'snow':    C_SNOW,
    'swamp':   C_SWAMP,
    'mushroom': C_MUSHROOM,
    'floating_islands': C_FLOATING_ISLANDS,
}

WALKABLE = {'grass', 'desert', 'forest', 'crystal', 'snow', 'swamp', 'mushroom', 'floating_islands'}

# ─── World Generation ─────────────────────────────────────────────────────────
class WorldGenerator:
    """Procedural terrain generation for a 3D open world."""

    @staticmethod
    def generate(size, seed=None):
        """Generate a 2D grid of biome names for the world.

        Args:
            size: World grid dimensions (tiles per side).
            seed: Optional random seed for reproducibility.

        Returns:
            2D list of biome name strings.
        """
        if seed is not None:
            random.seed(seed)
        grid = [['grass' for _ in range(size)] for _ in range(size)]

        # Place biome blobs
        biomes = ['desert', 'water', 'lava', 'forest', 'crystal', 'snow', 'swamp', 'mushroom', 'floating_islands']
        for _ in range(BIOME_BLOB_COUNT):
            bx = random.randint(0, size - 1)
            by = random.randint(0, size - 1)
            btype = random.choice(biomes)
            radius = random.randint(BIOME_BLOB_RADIUS_MIN, BIOME_BLOB_RADIUS_MAX)
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = bx + dx, by + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist <= radius + random.uniform(-BIOME_BLOB_JITTER, BIOME_BLOB_JITTER):
                            # Keep spawn area clear
                            spawn = size // 2
                            if abs(nx - spawn) < SPAWN_CLEAR_RADIUS and abs(ny - spawn) < SPAWN_CLEAR_RADIUS:
                                continue
                            grid[ny][nx] = btype

        # Ensure spawn area is grass
        spawn = size // 2
        for dy in range(-SPAWN_PAD_RADIUS, SPAWN_PAD_RADIUS + 1):
            for dx in range(-SPAWN_PAD_RADIUS, SPAWN_PAD_RADIUS + 1):
                grid[spawn + dy][spawn + dx] = 'grass'

        return grid


# ─── Player ───────────────────────────────────────────────────────────────────
class Player(Entity):
    """The player-controlled alien character with HP, XP, and tentacle aesthetics."""

    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=C_ALIEN,
            scale=1.2,
            position=position,
            collider='sphere',
        )
        self.hp = PLAYER_START_HP
        self.max_hp = PLAYER_START_HP
        self.speed = PLAYER_SPEED
        self.score = 0
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.shoot_timer = 0
        self.invuln_timer = 0
        self.inventory = {}
        self.kills = {}
        self.completed_missions = 0
        self.facing = Vec3(0, 0, 1)
        self.level_up_pending = False

        # Dash ability
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_direction = Vec3(0, 0, 0)

        # Power-up timers
        self.speed_boost_timer = 0
        self.shield_timer = 0
        self.weapon_upgrade_timer = 0  # Spread shot duration
        self.magnet_timer = 0  # Magnet Core pull boost

        # Tentacle entities
        self.tentacles = []
        for i in range(4):
            t = Entity(
                model='cube',
                color=color.rgb(0, 200, 80),
                scale=(0.15, 0.15, 1.2),
                parent=self,
            )
            self.tentacles.append(t)

        # Eyes
        self.eye_l = Entity(model='sphere', color=color.white, scale=(0.4, 0.5, 0.4),
                            parent=self, position=(-0.3, 0.4, -0.6))
        self.eye_r = Entity(model='sphere', color=color.white, scale=(0.4, 0.5, 0.4),
                            parent=self, position=(0.3, 0.4, -0.6))
        self.pupil_l = Entity(model='sphere', color=color.black, scale=(0.2, 0.25, 0.2),
                              parent=self.eye_l, position=(0, 0, -0.3))
        self.pupil_r = Entity(model='sphere', color=color.black, scale=(0.2, 0.25, 0.2),
                              parent=self.eye_r, position=(0, 0, -0.3))

        # Shield visual (invisible by default)
        self.shield_visual = Entity(model='sphere', color=color.rgba(100, 200, 255, 60),
                                    scale=1.6, parent=self, visible=False)

        # Squish/stretch animation state
        self.squish_current = 1.0  # Current Y scale (1.0 = normal)
        self.is_moving = False

    def gain_xp(self, amount):
        """Add XP and level up if threshold reached. Sets level_up_pending flag."""
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * XP_SCALE_FACTOR)
            self.max_hp += LEVEL_UP_HP_BONUS
            self.hp = min(self.hp + LEVEL_UP_HEAL_AMOUNT, self.max_hp)
            self.speed += LEVEL_UP_SPEED_BONUS
            self.level_up_pending = True

    def take_damage(self, amount):
        """Apply damage to the player. Returns True if player died.

        Args:
            amount: Damage points to subtract from HP.

        Returns:
            True if HP dropped to 0 (player is dead), False otherwise.
        """
        if self.invuln_timer > 0:
            return False
        self.hp -= amount
        self.invuln_timer = PLAYER_INVULN_DURATION
        # Flash red
        self.color = color.rgb(255, 100, 100)
        invoke(setattr, self, 'color', C_ALIEN, delay=0.15)
        if self.hp <= 0:
            self.hp = 0
            return True  # dead
        return False

    def add_item(self, name, count=1):
        """Add an item to the player's inventory."""
        self.inventory[name] = self.inventory.get(name, 0) + count

    def add_kill(self, name):
        """Record an enemy kill in the player's kill log."""
        self.kills[name] = self.kills.get(name, 0) + 1

    def update_tentacles(self, t):
        """Animate tentacles with a sinusoidal wave pattern."""
        for i, tent in enumerate(self.tentacles):
            angle_offset = (i - 1.5) * 0.5
            wave = math.sin(t * 5 + i * 1.5) * 0.3
            tent.rotation_x = wave * 40
            tent.rotation_y = angle_offset * 30 + math.sin(t * 3 + i) * 10

    def animate_bob(self, t):
        """Apply vertical bob and squish/stretch animation to the player."""
        self.y = 1.2 + math.sin(t * 3) * 0.15
        # Squish/stretch: stretch Y and squish XZ when moving, compress Y and bulge XZ when idle
        if self.is_moving:
            target_squish = PLAYER_STRETCH_FACTOR
        else:
            target_squish = 1.0
        self.squish_current += (target_squish - self.squish_current) * min(1.0, PLAYER_SQUISH_SPEED * time.dt)
        y_scale = 1.2 * self.squish_current
        xz_scale = 1.0 / self.squish_current  # Inverse for XZ to preserve volume
        self.scale = Vec3(xz_scale, y_scale, xz_scale)

    def set_facing_from_mouse(self, cam_pivot):
        """Point the alien toward where the mouse ray hits the ground."""
        hit_info = mouse.world_point
        if hit_info:
            direction = Vec3(hit_info.x - self.x, 0, hit_info.z - self.z)
            if direction.length() > 0.1:
                self.facing = direction.normalized()
                self.look_at_2d(Vec3(hit_info.x, self.y, hit_info.z))


# ─── Enemy ─────────────────────────────────────────────────────────────────────
class Enemy(Entity):
    """An enemy entity that chases the player when in detection range."""

    TYPES = {
        'Slime Blob':      {'color': color.lime,         'hp': 30,  'speed': 3,  'damage': 10, 'scale': 1.0,  'model': 'sphere', 'decor': 'none'},
        'Space Beetle':    {'color': color.brown,         'hp': 50,  'speed': 5,  'damage': 15, 'scale': 1.2,  'model': 'cube',    'decor': 'wings'},
        'Void Wraith':     {'color': color.violet,        'hp': 80,  'speed': 4,  'damage': 25, 'scale': 1.4,  'model': 'diamond', 'decor': 'aura'},
        'Lava Crawler':    {'color': color.orange,        'hp': 120, 'speed': 6,  'damage': 30, 'scale': 1.1,  'model': 'cube',    'decor': 'spikes'},
        'Crystal Guardian': {'color': color.cyan,         'hp': 200,  'speed': 2.5,  'damage': 40, 'scale': 1.8,  'model': 'diamond', 'decor': 'shards'},
        'Plasma Drake':    {'color': color.magenta,       'hp': 350, 'speed': 7,  'damage': 50, 'scale': 2.2,  'model': 'diamond', 'decor': 'wings'},
        'Phase Shifter':   {'color': color.rgba(180, 0, 255, 200), 'hp': 70,  'speed': 5,  'damage': 20, 'scale': 1.3,  'model': 'diamond', 'decor': 'aura'},
        'Spore Spitter':   {'color': color.rgb(200, 100, 0),       'hp': 90,  'speed': 3.5,'damage': 15, 'scale': 1.4,  'model': 'sphere', 'decor': 'spikes'},
        'Swarm Mite':      {'color': color.rgb(150, 200, 50),      'hp': 15,  'speed': 8,  'damage': 5,  'scale': 0.5,  'model': 'sphere', 'decor': 'none', 'detect': 45},
        'Void Bomber':     {'color': color.rgb(80, 0, 40),        'hp': 60,  'speed': 4,  'damage': 20, 'scale': 1.1,  'model': 'sphere', 'decor': 'spikes', 'detect': 30},
        'Nebula Phantom':  {'color': color.rgba(100, 150, 255, 150), 'hp': 100, 'speed': 6,  'damage': 30, 'scale': 1.3,  'model': 'sphere', 'decor': 'aura', 'detect': 40},
    }

    def __init__(self, position, enemy_type=None):
        if enemy_type is None:
            enemy_type = random.choice(list(self.TYPES.keys()))
        info = self.TYPES[enemy_type]
        super().__init__(
            model=info['model'],
            color=info['color'],
            scale=info['scale'],
            position=position,
            collider='sphere',
        )
        self.name = enemy_type
        self.hp = info['hp']
        self.max_hp = info['hp']
        self.speed = info['speed']
        self.damage = info['damage']
        self.alive = True
        self.dying = False
        self.death_timer = 0.0
        self.original_scale = info['scale']
        self.original_color = info['color']
        self.attack_cd = 0
        self.detect_range = info.get('detect', ENEMY_DETECT_RANGE)
        self.wander_dir = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        self.wander_timer = random.uniform(ENEMY_WANDER_INTERVAL_MIN, ENEMY_WANDER_INTERVAL_MAX)
        self.hit_flash = 0
        self.decor_entities = []
        self.knockback_vel = Vec3(0, 0, 0)  # Knockback velocity from being hit

        # Type-specific special behaviors
        self.is_phase_shifter = (enemy_type == 'Phase Shifter')
        self.phase_timer = random.uniform(4, 8) if self.is_phase_shifter else 0
        self.is_spore_spitter = (enemy_type == 'Spore Spitter')
        self.spit_timer = random.uniform(2, 4) if self.is_spore_spitter else 0
        self.is_swarm_mite = (enemy_type == 'Swarm Mite')

        # Void Bomber: kamikaze that explodes near player
        self.is_void_bomber = (enemy_type == 'Void Bomber')
        self.fuse_timer = 0
        self.fuse_active = False
        self.pulse_speed = 0

        # Nebula Phantom: flying enemy that orbits and dive-attacks
        self.is_nebula_phantom = (enemy_type == 'Nebula Phantom')
        self.orbit_angle = random.uniform(0, math.pi * 2) if self.is_nebula_phantom else 0
        self.orbit_state = 'orbit' if self.is_nebula_phantom else None  # 'orbit' or 'dive'
        self.dive_timer = random.uniform(NEBULA_PHANTOM_DIVE_COOLDOWN_MIN, NEBULA_PHANTOM_DIVE_COOLDOWN_MAX) if self.is_nebula_phantom else 0
        self.dive_target = Vec3(0, 0, 0) if self.is_nebula_phantom else None

        # Eyes for all enemies
        eye_y = 0.3 if info['model'] == 'sphere' else 0.4
        self.eye_l = Entity(model='sphere', color=color.red, scale=0.3, parent=self, position=(-0.25, eye_y, -0.5))
        self.eye_r = Entity(model='sphere', color=color.red, scale=0.3, parent=self, position=(0.25, eye_y, -0.5))

        # Type-specific decorations
        decor = info['decor']
        if decor == 'wings':
            wing_l = Entity(model='quad', color=color.rgba(int(info['color'][0]*255), int(info['color'][1]*255), int(info['color'][2]*255), 180),
                            scale=(1.0, 0.5), parent=self, position=(-0.8, 0.2, 0.2), rotation_y=-30)
            wing_r = Entity(model='quad', color=color.rgba(int(info['color'][0]*255), int(info['color'][1]*255), int(info['color'][2]*255), 180),
                            scale=(1.0, 0.5), parent=self, position=(0.8, 0.2, 0.2), rotation_y=30)
            self.decor_entities.extend([wing_l, wing_r])
        elif decor == 'aura':
            aura = Entity(model='sphere', color=color.rgba(int(info['color'][0]*255), int(info['color'][1]*255), int(info['color'][2]*255), 60),
                          scale=1.5, parent=self)
            self.decor_entities.append(aura)
        elif decor == 'spikes':
            for angle in [0, 72, 144, 216, 288]:
                rad = math.radians(angle)
                spike = Entity(model='cube', color=color.rgb(255, 100, 0),
                               scale=(0.15, 0.6, 0.15), parent=self,
                               position=(math.cos(rad) * 0.5, 0.5, math.sin(rad) * 0.5))
                self.decor_entities.append(spike)
        elif decor == 'shards':
            for angle in [0, 90, 180, 270]:
                rad = math.radians(angle)
                shard = Entity(model='cube', color=color.rgb(0, 255, 255),
                               scale=(0.1, 1.0, 0.1), parent=self,
                               position=(math.cos(rad) * 0.7, 0.7, math.sin(rad) * 0.7))
                self.decor_entities.append(shard)

        # HP bar
        self.hp_bar_bg = Entity(model='quad', color=color.red, scale=(2, 0.15), parent=self, position=(0, 1.5, 0), billboard=True)
        self.hp_bar = Entity(model='quad', color=color.green, scale=(2, 0.15), parent=self, position=(0, 1.5, -0.01), billboard=True)

    def take_damage(self, amount, hit_direction=None):
        """Apply damage to the enemy. Returns True if killed.

        Args:
            amount: Damage points to subtract from HP.
            hit_direction: Optional direction vector for knockback (from projectile source).
        """
        self.hp -= amount
        self.hit_flash = 0.1
        self.color = color.white
        invoke(setattr, self, 'color', self.original_color, delay=0.1)
        # Apply knockback if a direction is provided
        if hit_direction and hit_direction.length() > 0.01:
            kb_dir = hit_direction.normalized()
            self.knockback_vel = Vec3(
                kb_dir.x * ENEMY_KNOCKBACK_FORCE,
                ENEMY_KNOCKBACK_UP,
                kb_dir.z * ENEMY_KNOCKBACK_FORCE,
            )
        if self.hp <= 0:
            self.alive = False
            self.dying = True
            self.death_timer = DEATH_ANIM_DURATION
            return True
        return False

    def update_hp_bar(self):
        """Update the HP bar scale and color based on current health ratio."""
        # Defensive: guard against division by zero if max_hp is somehow 0
        ratio = max(0, self.hp / self.max_hp) if self.max_hp > 0 else 0
        self.hp_bar.scale_x = 2 * ratio
        self.hp_bar.x = -1 * (1 - ratio)
        # Color gradient: green → yellow → red
        if ratio > 0.5:
            t = (ratio - 0.5) * 2  # 1.0 at full, 0.0 at half
            self.hp_bar.color = color.rgb(int(255 * (1 - t)), 255, 0)
        else:
            t = ratio * 2  # 1.0 at half, 0.0 at empty
            self.hp_bar.color = color.rgb(255, int(255 * t), 0)

    def update_death_animation(self, dt):
        """Animate enemy death: pop upward, shrink, flash, and dissolve. Returns True when done."""
        if not self.dying:
            return True
        self.death_timer -= dt
        progress = 1.0 - (self.death_timer / DEATH_ANIM_DURATION)
        # Pop upward at start, then fall
        if progress < 0.3:
            pop_height = math.sin(progress / 0.3 * math.pi) * 1.5
        else:
            pop_height = max(0, 1.5 * (1.0 - (progress - 0.3) / 0.7))
        self.y = 1 + pop_height
        # Shrink with easing (fast start, slow end)
        ease_progress = 1.0 - (1.0 - progress) ** 2
        shrink = max(0.01, self.original_scale * (1.0 - ease_progress))
        self.scale = shrink
        # Flash between white and original color, dissolving at end
        if progress < 0.7:
            if int(self.death_timer * 15) % 2 == 0:
                self.color = color.white
            else:
                self.color = self.original_color
        else:
            # Dissolve to faded color
            fade = max(0, 1.0 - (progress - 0.7) / 0.3)
            self.color = color.rgba(
                int(self.original_color[0] * 255 * fade),
                int(self.original_color[1] * 255 * fade),
                int(self.original_color[2] * 255 * fade),
                int(255 * fade),
            )
        # Hide HP bar during death
        self.hp_bar_bg.visible = False
        self.hp_bar.visible = False
        return self.death_timer <= 0


# ─── Collectible ───────────────────────────────────────────────────────────────

def _weighted_random_collectible():
    """Pick a random collectible type using weighted probabilities.

    Common items like Space Gloop appear more often, while rare items
    like Plasma Core and Cosmic Jelly appear infrequently. This makes
    exploration more rewarding and power-ups a pleasant surprise.
    """
    names = list(COLLECTIBLE_WEIGHTS.keys())
    weights = list(COLLECTIBLE_WEIGHTS.values())
    return random.choices(names, weights=weights, k=1)[0]


class Collectible(Entity):
    """A collectible item that bobs and spins in the world."""

    ITEMS = {
        'Space Gloop':    {'color': C_PURPLE, 'value': 10,  'model': 'sphere'},
        'Meteor Shard':   {'color': color.orange, 'value': 25,  'model': 'diamond'},
        'Quantum Fuzz':   {'color': color.cyan,   'value': 50,  'model': 'sphere'},
        'Nebula Dust':    {'color': C_PINK,       'value': 100, 'model': 'diamond'},
        'Cosmic Jelly':   {'color': C_GOLD,       'value': 200, 'model': 'diamond'},
        'Plasma Core':    {'color': color.magenta, 'value': 350, 'model': 'diamond'},
        'Health Potion':  {'color': color.rgb(255, 50, 50),  'value': 15,  'model': 'sphere'},
        'Speed Boost':    {'color': color.rgb(50, 255, 50),  'value': 15,  'model': 'diamond'},
        'Shield Crystal': {'color': color.rgb(100, 200, 255),'value': 15,  'model': 'diamond'},
        'Weapon Upgrade': {'color': color.rgb(255, 150, 0),  'value': 20,  'model': 'diamond'},
        'Magnet Core':    {'color': color.rgb(200, 50, 255), 'value': 20,  'model': 'sphere'},
    }

    def __init__(self, position, item_type=None):
        if item_type is None:
            item_type = _weighted_random_collectible()
        info = self.ITEMS[item_type]
        super().__init__(
            model=info['model'],
            color=info['color'],
            scale=0.6,
            position=position,
            collider='sphere',
        )
        self.name = item_type
        self.value = info['value']
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.item_color = info['color']
        self.popping = False
        self.pop_timer = 0.0
        # Glow ring
        self.glow = Entity(model='quad', color=color.rgba(info['color'].r, info['color'].g, info['color'].b, 80),
                           scale=3, parent=self, rotation_x=90, position=(0, -0.3, 0))

    def animate(self, t):
        """Bob, spin, and pulse glow on the collectible each frame."""
        self.y = 1.0 + math.sin(t * 2 + self.bob_offset) * 0.4
        self.rotation_y += 60 * time.dt
        # Pulsing glow ring — scales between min and max for a beacon effect
        pulse = GLOW_PULSE_MIN_SCALE + (GLOW_PULSE_MAX_SCALE - GLOW_PULSE_MIN_SCALE) * (0.5 + 0.5 * math.sin(t * GLOW_PULSE_SPEED + self.bob_offset))
        self.glow.scale = pulse


# ─── Projectile ────────────────────────────────────────────────────────────────
class ProjectileTrail(Entity):
    """A fading trail dot spawned behind a projectile for a satisfying laser streak effect.

    Each trail dot shrinks and fades over its lifetime, creating a smooth
    comet-tail visual behind the player's tentacle laser.
    """

    def __init__(self, position, col):
        """Initialize a trail dot at the given position with the projectile's color."""
        super().__init__(
            model='sphere',
            color=col,
            scale=PROJECTILE_TRAIL_START_SCALE,
            position=position,
        )
        self.lifetime = PROJECTILE_TRAIL_LIFETIME
        self.max_lifetime = PROJECTILE_TRAIL_LIFETIME

    def update_trail(self, dt):
        """Advance the trail animation. Returns True when expired and should be removed.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if the trail dot has expired and should be destroyed.
        """
        self.lifetime -= dt
        if self.lifetime <= 0:
            return True
        progress = 1.0 - (self.lifetime / self.max_lifetime)
        # Smoothly shrink from start scale to end scale
        current_scale = PROJECTILE_TRAIL_START_SCALE + (PROJECTILE_TRAIL_END_SCALE - PROJECTILE_TRAIL_START_SCALE) * progress
        self.scale = current_scale
        # Fade alpha out over lifetime
        alpha = max(0, int(200 * (1.0 - progress)))
        r, g, b = int(self.color[0] * 255), int(self.color[1] * 255), int(self.color[2] * 255)
        self.color = color.rgba(r, g, b, alpha)
        return False


class Projectile(Entity):
    """A laser projectile fired by the player."""

    def __init__(self, position, direction, damage=PROJECTILE_BASE_DAMAGE, speed=PROJECTILE_SPEED):
        super().__init__(
            model='sphere',
            color=C_LASER,
            scale=0.3,
            position=position,
        )
        self.direction = direction.normalized()
        self.damage = damage
        self.speed = speed
        self.lifetime = PROJECTILE_LIFETIME

        # Trail spawning timer
        self.trail_timer = 0.0

    def move(self, dt):
        """Move the projectile forward. Returns False when lifetime expires."""
        self.position += self.direction * self.speed * dt
        self.lifetime -= dt
        return self.lifetime > 0


class EnemyProjectile(Entity):
    """A projectile fired by Spore Spitter enemies toward the player."""

    def __init__(self, position, direction, damage=10, speed=20):
        super().__init__(
            model='sphere',
            color=color.rgb(200, 100, 0),
            scale=0.25,
            position=position,
        )
        self.direction = direction.normalized()
        self.damage = damage
        self.speed = speed
        self.lifetime = 3.0

    def move(self, dt):
        """Move the enemy projectile forward. Returns False when lifetime expires."""
        self.position += self.direction * self.speed * dt
        self.lifetime -= dt
        return self.lifetime > 0


class DamageNumber:
    """A floating damage number that rises from an enemy on hit and fades out.

    Uses a 3D billboard entity with a text overlay for visibility.
    Tracks its own lifetime and handles cleanup.
    """

    def __init__(self, position, amount, is_kill=False):
        col = color.yellow if is_kill else color.white
        text_str = str(amount) if not is_kill else f"{amount} KILL!"
        scale_factor = 1.4 if is_kill else 1.0

        # 3D billboard quad as a glowing background dot behind the number
        self.bg_dot = Entity(
            model='quad',
            color=color.rgba(col.r, col.g, col.b, 120),
            scale=0.6 * scale_factor,
            position=Vec3(position.x, position.y + 2.0, position.z),
            billboard=True,
        )
        # UI Text anchored to the camera for crisp rendering
        self.text_ent = Text(
            parent=camera.ui,
            text=text_str,
            scale=DMG_NUMBER_SCALE * scale_factor * 0.7,
            color=col,
            origin=(0, 0),
            background=False,
        )
        self.lifetime = DMG_NUMBER_LIFETIME
        self.max_lifetime = DMG_NUMBER_LIFETIME
        self.world_pos = Vec3(position.x, position.y + 2.0, position.z)
        self.is_kill = is_kill
        self.alive = True

    def update(self, dt):
        """Advance the damage number animation. Returns True when expired."""
        self.lifetime -= dt
        self.world_pos += Vec3(0, DMG_NUMBER_RISE_SPEED * dt, 0)
        self.bg_dot.position = self.world_pos
        # Project world position to UI screen coordinates
        cam = camera
        cam_pos = cam.get_world_position()
        diff = self.world_pos - cam_pos
        # Simple projection to screen space using camera's view
        screen_pos = camera.screen_point(self.world_pos)
        self.text_ent.position = (screen_pos[0], screen_pos[1])
        # Fade out — defensive: clamp alpha to prevent negative values
        alpha = max(0, min(1, self.lifetime / self.max_lifetime))
        r, g, b = int(self.text_ent.color[0] * 255), int(self.text_ent.color[1] * 255), int(self.text_ent.color[2] * 255)
        if self.is_kill:
            self.text_ent.color = color.rgba(255, 255, 0, int(255 * alpha))
        else:
            self.text_ent.color = color.rgba(255, 255, 255, int(255 * alpha))
        self.bg_dot.color = color.rgba(255, 255, 255, int(80 * alpha))
        if self.lifetime <= 0:
            self.alive = False
            return True
        return False

    def destroy(self):
        """Clean up all owned entities."""
        destroy(self.bg_dot)
        destroy(self.text_ent)
MISSION_TEMPLATES = [
    ("Gloop Harvest",        "Collect Space Gloop for the Mothership",     "Space Gloop",    5, "collect", 100),
    ("Beetle B Gone",        "Defeat Space Beetles invading the sector",  "Space Beetle",   3, "kill",    200),
    ("Shard Collection",     "Gather Meteor Shards for the Lab",           "Meteor Shard",   5, "collect", 150),
    ("Wraith Hunter",        "Eliminate Void Wraiths from the dark zones","Void Wraith",    2, "kill",    300),
    ("Fuzz Finder",          "Find Quantum Fuzz in the wild",             "Quantum Fuzz",   3, "collect", 250),
    ("Jelly Jam",            "Collect Cosmic Jelly — it's delicious",      "Cosmic Jelly",   2, "collect", 400),
    ("Crawler Crisis",       "Take out Lava Crawlers near volcanic zones", "Lava Crawler",  3, "kill",    350),
    ("Crystal Clear",        "Defeat Crystal Guardians in crystal biomes", "Crystal Guardian",2,"kill",    500),
    ("Plasma Pursuit",       "Hunt down the elusive Plasma Drakes",        "Plasma Drake",  1, "kill",    700),
    ("Phantom Purge",       "Banish Nebula Phantoms from the skies",     "Nebula Phantom",2, "kill",    450),
    ("Core Collector",       "Gather Plasma Cores for the warp drive",     "Plasma Core",    2, "collect", 600),
]

class Mission:
    """A mission objective with progress tracking."""
    def __init__(self, title, description, target, reward, mission_type, target_count):
        self.title = title
        self.description = description
        self.target = target
        self.reward = reward
        self.mission_type = mission_type
        self.target_count = target_count
        self.progress = 0
        self.completed = False
        self.turned_in = False


# ─── Game ──────────────────────────────────────────────────────────────────────
class Game:
    """Main game controller: manages world, entities, HUD, and game state."""

    def __init__(self):
        self.seed = random.randint(0, 999999)
        self.world_grid = WorldGenerator.generate(WORLD_SIZE, self.seed)
        self.terrain_entities = []
        self.tree_entities = []
        self.crystal_entities = []
        self.enemies = []
        self.collectibles = []
        self.projectiles = []
        self.projectile_trails = []
        self.enemy_projectiles = []
        self.particles = []
        self.damage_numbers = []
        self.missions = []
        self.messages = []
        self.game_over = False
        self.paused = False
        self.t = 0
        self.game_start_time = 0
        self.spawn_timer = 0
        self.mission_timer = 0

        # Visual effects state
        self.screen_shake = 0.0
        self.level_up_timer = 0.0
        self.hit_stop_timer = 0.0
        self.current_biome = 'grass'

        # Combo system
        self.combo_count = 0
        self.combo_timer = 0.0
        self.combo_display_timer = 0.0

        # Weather particles
        self.weather_particles = []

        # Build terrain
        self._build_terrain()

        # Player
        spawn = Vec3(WORLD_SIZE // 2 * TILE_SCALE, 2, WORLD_SIZE // 2 * TILE_SCALE)
        self.player = Player(position=spawn)

        # Camera rig: third-person camera
        self.cam_pivot = Entity(position=spawn)
        camera.parent = self.cam_pivot
        camera.position = (0, CAMERA_HEIGHT, -CAMERA_DISTANCE)
        camera.rotation = (CAMERA_ANGLE, 0, 0)

        # Populate world
        self._spawn_initial_entities()
        self._assign_missions(count=3)

        # Lighting
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1, -1, 1))
        AmbientLight(color=color.rgba(100, 100, 100, 255))

        # Sky
        Sky(color=color.rgb(25, 0, 60))

        # Stars in the sky
        self.stars = []
        for _ in range(STAR_COUNT):
            angle_h = random.uniform(0, math.pi * 2)
            angle_v = random.uniform(0.15, math.pi * 0.45)
            dist = random.uniform(STAR_HEIGHT_MIN, STAR_HEIGHT_MAX)
            sx = math.cos(angle_h) * math.cos(angle_v) * STAR_SPREAD
            sy = abs(math.sin(angle_v)) * dist + STAR_HEIGHT_MIN
            sz = math.sin(angle_h) * math.cos(angle_v) * STAR_SPREAD
            brightness = random.uniform(0.5, 1.0)
            star_size = random.uniform(1, 3)
            twinkle_speed = random.uniform(2.0, 6.0)
            twinkle_offset = random.uniform(0, math.pi * 2)
            star = Entity(
                model='quad',
                color=color.rgba(255, 255, 255, int(255 * brightness)),
                scale=star_size,
                position=(sx, sy, sz),
                billboard=True,
            )
            star.base_brightness = brightness
            star.twinkle_speed = twinkle_speed
            star.twinkle_offset = twinkle_offset
            self.stars.append(star)

        # Nebula clouds — large translucent colored quads for atmospheric depth
        self.nebula_clouds = []
        nebula_palette = [
            color.rgb(120, 40, 180),   # deep purple
            color.rgb(40, 80, 180),    # deep blue
            color.rgb(180, 40, 80),    # crimson
            color.rgb(40, 160, 120),   # teal
            color.rgb(180, 100, 40),   # amber
            color.rgb(80, 40, 160),    # indigo
            color.rgb(60, 120, 180),   # sky blue
            color.rgb(160, 60, 120),   # rose
        ]
        for i in range(NEBULA_CLOUD_COUNT):
            angle_h = random.uniform(0, math.pi * 2)
            ny = random.uniform(NEBULA_HEIGHT_MIN, NEBULA_HEIGHT_MAX)
            nx = random.uniform(-NEBULA_SPREAD, NEBULA_SPREAD)
            nz = random.uniform(-NEBULA_SPREAD, NEBULA_SPREAD)
            nebula_size = random.uniform(30, 80)
            nebula_color = nebula_palette[i % len(nebula_palette)]
            cloud = Entity(
                model='quad',
                color=color.rgba(int(nebula_color[0] * 255), int(nebula_color[1] * 255),
                                 int(nebula_color[2] * 255), 25),
                scale=nebula_size,
                position=(nx, ny, nz),
                billboard=True,
            )
            cloud.drift_speed = random.uniform(0.1, 0.4)
            cloud.drift_phase = random.uniform(0, math.pi * 2)
            self.nebula_clouds.append(cloud)

        # Fog for atmosphere
        scene.fog_color = color.rgb(25, 0, 60)
        scene.fog_density = 0.007

        # Weather particles (rain, snow, embers)
        self._init_weather()

        # HUD
        self._create_hud()

        # Crosshair
        self.crosshair = Entity(parent=camera.ui, model='quad', color=color.rgba(255, 255, 255, 128),
                                scale=(0.003, 0.04), position=(0, 0))
        self.crosshair2 = Entity(parent=camera.ui, model='quad', color=color.rgba(255, 255, 255, 128),
                                 scale=(0.04, 0.003), position=(0, 0))

    def _cleanup(self):
        """Clean up all game entities for a restart. Destroys terrain, enemies,
        collectibles, projectiles, particles, HUD, and player — but NOT camera,
        scene, or lighting which Ursina manages globally."""
        # Destroy enemies and their sub-entities
        for e in self.enemies:
            if e and e.enabled:
                for d in e.decor_entities:
                    destroy(d)
                destroy(e.eye_l)
                destroy(e.eye_r)
                destroy(e.hp_bar_bg)
                destroy(e.hp_bar)
                destroy(e)
        self.enemies.clear()

        # Destroy collectibles
        for c in self.collectibles:
            if c and c.enabled:
                destroy(c.glow)
                destroy(c)
        self.collectibles.clear()

        # Destroy projectiles
        for p in self.projectiles:
            if p and p.enabled:
                destroy(p)
        self.projectiles.clear()

        # Destroy projectile trails
        for t in self.projectile_trails:
            if t and t.enabled:
                destroy(t)
        self.projectile_trails.clear()

        for ep in self.enemy_projectiles:
            if ep and ep.enabled:
                destroy(ep)
        self.enemy_projectiles.clear()

        # Destroy particles
        for p_ent, vel, lifetime in self.particles:
            if p_ent and p_ent.enabled:
                destroy(p_ent)
        self.particles.clear()

        # Destroy damage numbers
        for dn in self.damage_numbers:
            dn.destroy()
        self.damage_numbers.clear()

        # Destroy terrain and decoration entities
        for t in self.terrain_entities:
            if t and t.enabled:
                destroy(t)
        self.terrain_entities.clear()

        for t in self.tree_entities:
            if t and t.enabled:
                destroy(t)
        self.tree_entities.clear()

        for c in self.crystal_entities:
            if c and c.enabled:
                destroy(c)
        self.crystal_entities.clear()

        # Destroy stars
        for s in self.stars:
            if s and s.enabled:
                destroy(s)
        self.stars.clear()

        # Destroy nebula clouds
        for c in self.nebula_clouds:
            if c and c.enabled:
                destroy(c)
        self.nebula_clouds.clear()

        # Destroy player and sub-entities (player's children: tentacles, eyes, shield)
        if self.player and self.player.enabled:
            destroy(self.player)
        # Player's children cascade-destroy: tentacles, eyes, pupils, shield_visual

        # Destroy HUD entities
        for attr in ('hp_bar_bg', 'hp_bar', 'xp_bar_bg', 'xp_bar',
                      'level_text', 'score_text', 'hp_text',
                      'mission_text', 'controls_text', 'version_text',
                      'game_over_text', 'game_over_sub', 'game_over_stats',
                      'game_over_restart', 'level_up_text', 'dash_text',
                      'powerup_text', 'crosshair', 'crosshair2',
                      'combo_text', 'weapon_text'):
            ent = getattr(self, attr, None)
            if ent and hasattr(ent, 'enabled'):
                destroy(ent)
        for t in self.msg_texts:
            if t:
                destroy(t)
        self.msg_texts.clear()

        # Destroy minimap entities
        if self.minimap_entity and hasattr(self.minimap_entity, 'enabled'):
            destroy(self.minimap_entity)
        if self.minimap_player_dot and hasattr(self.minimap_player_dot, 'enabled'):
            destroy(self.minimap_player_dot)
        for dot in self.minimap_enemy_dots:
            if dot and hasattr(dot, 'enabled'):
                destroy(dot)
        self.minimap_enemy_dots.clear()

        # Destroy camera pivot (player follow rig)
        if self.cam_pivot and hasattr(self.cam_pivot, 'enabled'):
            destroy(self.cam_pivot)

        # Destroy lights
        if hasattr(self, 'sun') and self.sun:
            destroy(self.sun)

        # Destroy weather particles
        for wp in self.weather_particles:
            if wp and hasattr(wp, 'enabled'):
                destroy(wp)
        self.weather_particles.clear()

        # BUG FIX: clear missions and messages on restart so stale data
        # doesn't carry over to the new game session.
        self.missions.clear()
        self.messages.clear()

        # Destroy Sky (Ursina's Sky is a special entity)
        for e in scene.entities[:]:
            if hasattr(e, 'model') and e.model and 'sky' in str(e.model).lower():
                destroy(e)

    def _build_terrain(self):
        """Build the 3D terrain from the world grid."""
        for y in range(WORLD_SIZE):
            for x in range(WORLD_SIZE):
                biome = self.world_grid[y][x]
                c = BIOME_COLORS.get(biome, C_GRASS)
                tile = Entity(
                    model='cube',
                    color=c,
                    position=(x * TILE_SCALE, 0, y * TILE_SCALE),
                    scale=(TILE_SCALE, 1, TILE_SCALE),
                    collider='box',
                )
                self.terrain_entities.append(tile)

                # Decorations
                if biome == 'forest' and random.random() < 0.3:
                    tree = Entity(
                        model='cube',
                        color=color.rgb(80, 50, 20),
                        position=(x * TILE_SCALE, 3, y * TILE_SCALE),
                        scale=(0.6, 6, 0.6),
                    )
                    canopy = Entity(
                        model='sphere',
                        color=color.rgb(0, 130, 0),
                        position=(x * TILE_SCALE, 7, y * TILE_SCALE),
                        scale=3,
                    )
                    self.tree_entities.extend([tree, canopy])

                elif biome == 'crystal' and random.random() < 0.2:
                    height = random.uniform(3, 8)
                    crystal = Entity(
                        model='cube',
                        color=color.rgb(0, 220, 230),
                        position=(x * TILE_SCALE, height / 2 + 0.5, y * TILE_SCALE),
                        scale=(0.5, height, 0.5),
                    )
                    self.crystal_entities.append(crystal)

                elif biome == 'mushroom' and random.random() < 0.25:
                    # Alien mushroom: stem + cap with glow
                    stem_h = random.uniform(1.5, 4.5)
                    stem = Entity(
                        model='cube',
                        color=color.rgb(180, 170, 160),
                        position=(x * TILE_SCALE, stem_h / 2 + 0.5, y * TILE_SCALE),
                        scale=(0.4, stem_h, 0.4),
                    )
                    cap_r = random.uniform(1.0, 2.5)
                    cap_color_choices = [
                        color.rgb(255, 50, 120),   # neon pink
                        color.rgb(80, 255, 80),    # bright green
                        color.rgb(200, 50, 255),   # purple
                        color.rgb(255, 200, 0),    # golden
                    ]
                    cap = Entity(
                        model='sphere',
                        color=random.choice(cap_color_choices),
                        position=(x * TILE_SCALE, stem_h + 1.0, y * TILE_SCALE),
                        scale=cap_r,
                    )
                    # Spore glow ring under cap
                    glow = Entity(
                        model='quad',
                        color=color.rgba(255, 100, 255, 50),
                        position=(x * TILE_SCALE, stem_h + 0.5, y * TILE_SCALE),
                        scale=cap_r * 1.5,
                        rotation_x=90,
                    )
                    self.crystal_entities.extend([stem, cap, glow])

                elif biome == 'floating_islands' and random.random() < FLOATING_ISLAND_SPAWN_CHANCE:
                    # Floating island: raised platform with crystals
                    island_h = random.uniform(FLOATING_ISLAND_HEIGHT_MIN, FLOATING_ISLAND_HEIGHT_MAX)
                    island_size = random.uniform(1.5, 3.0)
                    # The floating platform itself
                    island = Entity(
                        model='cube',
                        color=color.rgb(160, 120, 200),
                        position=(x * TILE_SCALE, island_h, y * TILE_SCALE),
                        scale=(island_size, 0.5, island_size),
                    )
                    # Shadow beneath
                    shadow = Entity(
                        model='quad',
                        color=color.rgba(0, 0, 0, 40),
                        position=(x * TILE_SCALE, 0.05, y * TILE_SCALE),
                        scale=island_size * 1.5,
                        rotation_x=90,
                    )
                    self.crystal_entities.extend([island, shadow])
                    # Crystal on top of island
                    if random.random() < FLOATING_ISLAND_CRYSTAL_CHANCE:
                        crystal_h = random.uniform(1.5, 4.0)
                        crystal_top = Entity(
                            model='cube',
                            color=color.rgb(200, 180, 255),
                            position=(x * TILE_SCALE, island_h + crystal_h / 2 + 0.25, y * TILE_SCALE),
                            scale=(0.3, crystal_h, 0.3),
                        )
                        self.crystal_entities.append(crystal_top)

                elif biome == 'desert' and random.random() < RUINS_PILLAR_CHANCE:
                    # Alien ruins: ancient stone pillars
                    pillar_count = random.randint(1, 4)
                    for pi in range(pillar_count):
                        offset_x = random.uniform(-2, 2)
                        offset_z = random.uniform(-2, 2)
                        pillar_h = random.uniform(2, 6)
                        pillar = Entity(
                            model='cube',
                            color=color.rgb(160, 140, 100),
                            position=(x * TILE_SCALE + offset_x, pillar_h / 2 + 0.5, y * TILE_SCALE + offset_z),
                            scale=(0.4, pillar_h, 0.4),
                        )
                        self.crystal_entities.append(pillar)
                    # Broken wall segment
                    if random.random() < 0.5:
                        wall_w = random.uniform(1, 3)
                        wall_h = random.uniform(1.5, 3)
                        wall = Entity(
                            model='cube',
                            color=color.rgb(140, 120, 80),
                            position=(x * TILE_SCALE, wall_h / 2 + 0.5, y * TILE_SCALE),
                            scale=(wall_w, wall_h, 0.3),
                        )
                        self.crystal_entities.append(wall)

    def _is_walkable(self, world_x, world_z):
        """Check if a world position is on walkable terrain."""
        tx = int(world_x / TILE_SCALE)
        tz = int(world_z / TILE_SCALE)
        if 0 <= tx < WORLD_SIZE and 0 <= tz < WORLD_SIZE:
            return self.world_grid[tz][tx] in WALKABLE
        return False  # Out of bounds is not walkable

    def _get_biome_at(self, world_x, world_z):
        """Return the biome name at a world position."""
        tx = int(world_x / TILE_SCALE)
        tz = int(world_z / TILE_SCALE)
        tx = max(0, min(tx, WORLD_SIZE - 1))
        tz = max(0, min(tz, WORLD_SIZE - 1))
        return self.world_grid[tz][tx]

    def _show_death_screen(self, p):
        """Display the game over screen with detailed survival stats."""
        self.game_over = True
        self.game_over_text.visible = True
        self.game_over_text.text = 'GAME OVER'
        self.game_over_sub.visible = True
        self.game_over_sub.text = f'Score: {p.score}  Level: {p.level}'
        total_kills = sum(p.kills.values())
        total_items = sum(p.inventory.values())
        time_alive = int(self.t)
        minutes = time_alive // 60
        seconds = time_alive % 60
        kill_details = '  '.join(f'{k}:{v}' for k, v in p.kills.items()) if p.kills else 'None'
        item_details = '  '.join(f'{k}:{v}' for k, v in p.inventory.items()) if p.inventory else 'None'
        kpm = f'{total_kills / max(1, time_alive / 60):.1f}' if time_alive > 0 else '0'
        stats_lines = [
            f'Time Survived: {minutes}m {seconds}s',
            f'Total Kills: {total_kills}   Items Collected: {total_items}',
            f'Kills Per Minute: {kpm}',
            f'Missions Completed: {p.completed_missions}',
            f'Enemies Defeated: {kill_details}',
            f'Inventory: {item_details}',
        ]
        self.game_over_stats.visible = True
        self.game_over_stats.text = '\n'.join(stats_lines)
        self.game_over_restart.visible = True
        self.game_over_restart.text = 'Press R to Restart'

    def _spawn_initial_entities(self):
        """Populate the world with initial collectibles and enemies."""
        spawn_x = WORLD_SIZE // 2 * TILE_SCALE
        spawn_z = WORLD_SIZE // 2 * TILE_SCALE

        # Spawn collectibles
        for _ in range(INITIAL_COLLECTIBLES):
            x = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            z = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            if self._is_walkable(x, z):
                dist = math.sqrt((x - spawn_x) ** 2 + (z - spawn_z) ** 2)
                if dist > SPAWN_SAFE_RADIUS:
                    c = Collectible(position=Vec3(x, 1, z))
                    self.collectibles.append(c)

        # Spawn enemies
        for _ in range(INITIAL_ENEMIES):
            x = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            z = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            if self._is_walkable(x, z):
                dist = math.sqrt((x - spawn_x) ** 2 + (z - spawn_z) ** 2)
                if dist > ENEMY_SPAWN_SAFE_RADIUS:
                    # Distance-based difficulty scaling for initial spawn
                    enemy_type = self._pick_enemy_type(dist)
                    e = Enemy(position=Vec3(x, 1, z), enemy_type=enemy_type)
                    self.enemies.append(e)

    def _pick_enemy_type(self, distance_from_spawn):
        """Pick an enemy type based on distance from spawn (farther = harder)."""
        tier = min(int(distance_from_spawn / DIFFICULTY_SCALE_DISTANCE), 2)
        if tier == 0:
            return random.choice(EASY_ENEMY_TYPES)
        elif tier == 1:
            return random.choice(MEDIUM_ENEMY_TYPES)
        else:
            return random.choice(HARD_ENEMY_TYPES)

    def _scale_enemy_to_player_level(self, enemy):
        """Scale enemy HP and damage based on player level for balanced difficulty.

        Higher-level players face tougher variants of the same enemy type,
        keeping early enemies relevant while making the game progressively harder.
        """
        p = self.player
        tier_above_base = max(0, (p.level - 1) // PLAYER_LEVEL_DIFFICULTY_INTERVAL)
        if tier_above_base > 0:
            hp_mult = 1.0 + tier_above_base * ENEMY_HP_SCALE_PER_TIER
            dmg_mult = 1.0 + tier_above_base * ENEMY_DAMAGE_SCALE_PER_TIER
            enemy.hp = int(enemy.hp * hp_mult)
            enemy.max_hp = enemy.hp
            enemy.damage = int(enemy.damage * dmg_mult)

    def _assign_missions(self, count=1):
        """Assign new random missions from templates."""
        templates = list(MISSION_TEMPLATES)
        random.shuffle(templates)
        for template in templates[:count]:
            m = Mission(template[0], template[1], template[2], template[5], template[4], template[3])
            self.missions.append(m)
            self.add_message(f"New Mission: {m.title}")

    def add_message(self, msg):
        """Add a timed message to the HUD message queue."""
        self.messages.append((self.t, msg))
        if len(self.messages) > 50:
            self.messages = self.messages[-50:]

    def _create_hud(self):
        """Create HUD elements as UI entities."""
        self.hp_bar_bg = Entity(parent=camera.ui, model='quad', color=color.dark_gray,
                                scale=(0.4, 0.03), position=(-0.55, 0.46))
        self.hp_bar = Entity(parent=camera.ui, model='quad', color=color.green,
                             scale=(0.4, 0.03), position=(-0.55, 0.46), origin=(-0.5, 0))

        self.xp_bar_bg = Entity(parent=camera.ui, model='quad', color=color.dark_gray,
                                scale=(0.4, 0.015), position=(-0.55, 0.43))
        self.xp_bar = Entity(parent=camera.ui, model='quad', color=C_PURPLE,
                             scale=(0.4, 0.015), position=(-0.55, 0.43), origin=(-0.5, 0))

        self.level_text = Text(text='Lv.1', position=(-0.75, 0.46), scale=1.5, color=color.yellow)
        self.score_text = Text(text='Score: 0', position=(-0.75, 0.41), scale=1.2, color=color.white)
        self.hp_text = Text(text='HP: 100/100', position=(-0.37, 0.46), scale=1.0, color=color.white)

        self.msg_texts = []
        for i in range(5):
            t = Text(text='', position=(-0.85, -0.3 - i * 0.04), scale=0.9, color=color.yellow)
            self.msg_texts.append(t)

        self.mission_panel_shown = False
        self.mission_text = Text(text='', position=(-0.15, 0.35), scale=1.0, color=color.cyan, visible=False)
        self.controls_text = Text(
            text='WASD:Move | Click:Shoot | Space:Dash | M:Minimap | Tab:Missions | P:Pause',
            position=(0, -0.47), origin=(0, 0), scale=0.8, color=color.gray
        )
        self.version_text = Text(text=f'v{VERSION}', position=(0.88, -0.47), scale=0.7, color=color.gray)
        self.game_over_text = Text(text='', position=(0, 0.15), origin=(0, 0), scale=4, color=color.red, visible=False)
        self.game_over_sub = Text(text='', position=(0, 0.05), origin=(0, 0), scale=2, color=color.white, visible=False)
        self.game_over_stats = Text(text='', position=(0, -0.05), origin=(0, 0), scale=1.3, color=color.rgba(200, 200, 255, 255), visible=False)
        self.game_over_restart = Text(text='', position=(0, -0.25), origin=(0, 0), scale=1.5, color=color.yellow, visible=False)

        # Level-up popup
        self.level_up_text = Text(text='', position=(0, 0.2), origin=(0, 0), scale=3, color=color.yellow, visible=False)

        # Dash cooldown indicator & power-up status
        self.dash_text = Text(text='DASH READY', position=(-0.75, 0.37), scale=0.9, color=color.cyan)
        self.powerup_text = Text(text='', position=(-0.75, 0.33), scale=0.85, color=color.green)

        # Combo counter display
        self.combo_text = Text(text='', position=(0.35, 0.3), scale=2.0, color=color.yellow, visible=False, origin=(0, 0))

        # Weapon upgrade indicator
        self.weapon_text = Text(text='', position=(-0.75, 0.29), scale=0.85, color=color.orange)

        # Minimap
        self.minimap_shown = True
        self.minimap_entity = None
        self.minimap_player_dot = None
        self.minimap_enemy_dots = []
        self.minimap_refresh_timer = 0.0
        self._build_minimap()

    def _build_minimap(self):
        """Create a minimap with terrain-color texture and enemy dot tracking.

        Renders the biome grid as a colored pixel texture on a quad,
        then overlays a white player dot and red enemy dots that update
        each refresh interval.
        """
        size = MINIMAP_RESOLUTION
        # Build a pixel image from the world grid biome colors
        pixels = []
        for gz in range(WORLD_SIZE):
            for gx in range(WORLD_SIZE):
                biome = self.world_grid[gz][gx]
                c = BIOME_COLORS.get(biome, C_GRASS)
                pixels.append((int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)))

        # Downsample to minimap resolution
        scale_factor = WORLD_SIZE / size
        img = [[(0, 0, 0)] * size for _ in range(size)]
        for my in range(size):
            for mx in range(size):
                wx = int(mx * scale_factor)
                wy = int(my * scale_factor)
                wx = min(wx, WORLD_SIZE - 1)
                wy = min(wy, WORLD_SIZE - 1)
                img[my][mx] = pixels[wy * WORLD_SIZE + wx]

        # Flatten for Ursina Texture
        flat_pixels = []
        for row in img:
            for r, g, b in row:
                flat_pixels.extend([r, g, b])

        tex_data = bytes(flat_pixels)
        minimap_texture = Texture()
        minimap_texture.setup2d_texture(size, size, Texture.T_unsigned_byte, Texture.F_rgb8)
        minimap_texture.set_ram_image(tex_data)

        self.minimap_entity = Entity(
            parent=camera.ui,
            model='quad',
            texture=minimap_texture,
            scale=(MINIMAP_SIZE, MINIMAP_SIZE),
            position=MINIMAP_POSITION,
        )
        # Player dot on minimap
        self.minimap_player_dot = Entity(
            parent=camera.ui,
            model='quad',
            color=color.white,
            scale=(MINIMAP_PLAYER_DOT_SIZE, MINIMAP_PLAYER_DOT_SIZE),
            position=MINIMAP_POSITION,
        )
        # Pre-allocate enemy dot pool (max 40 enemies)
        self.minimap_enemy_dots = []
        for _ in range(MAX_ACTIVE_ENEMIES):
            dot = Entity(
                parent=camera.ui,
                model='quad',
                color=color.rgb(*MINIMAP_ENEMY_DOT_RGB),
                scale=(MINIMAP_ENEMY_DOT_SIZE, MINIMAP_ENEMY_DOT_SIZE),
                position=(-1, -1),  # offscreen initially
                visible=False,
            )
            self.minimap_enemy_dots.append(dot)

    def _update_minimap_colors(self):
        """Refresh enemy dots on the minimap to reflect live positions."""
        p = self.player
        mm_cx, mm_cy = MINIMAP_POSITION
        mm_half = MINIMAP_SIZE / 2
        world_size = WORLD_SIZE * TILE_SCALE

        # Player dot position
        px_norm = (p.x / world_size) - 0.5
        pz_norm = (p.z / world_size) - 0.5
        self.minimap_player_dot.position = (mm_cx + px_norm * MINIMAP_SIZE, mm_cy + pz_norm * MINIMAP_SIZE)

        # Update enemy dots from pool
        visible_enemies = [e for e in self.enemies if e.alive and not e.dying]
        for i, dot in enumerate(self.minimap_enemy_dots):
            if i < len(visible_enemies):
                e = visible_enemies[i]
                ex_norm = (e.x / world_size) - 0.5
                ez_norm = (e.z / world_size) - 0.5
                dot.position = (mm_cx + ex_norm * MINIMAP_SIZE, mm_cy + ez_norm * MINIMAP_SIZE)
                dot.visible = True
            else:
                dot.visible = False

    def _init_weather(self):
        """Create weather particle entities that appear based on current biome."""
        self.weather_particles = []
        # Rain particles (used in grass, forest, swamp biomes)
        for _ in range(WEATHER_PARTICLE_COUNT):
            p = Entity(
                model='cube',
                color=color.rgba(100, 150, 255, 80),
                scale=(0.03, 0.4, 0.03),
                position=Vec3(0, -100, 0),  # hidden below world
                visible=False,
            )
            p.fall_speed = WEATHER_FALL_SPEED_RAIN + random.uniform(-3, 3)
            p.drift = random.uniform(-0.5, 0.5)
            p.weather_type = 'rain'
            self.weather_particles.append(p)

        # Snow particles (used in snow biome)
        for _ in range(WEATHER_SNOW_COUNT):
            p = Entity(
                model='sphere',
                color=color.rgba(240, 240, 255, 120),
                scale=0.12,
                position=Vec3(0, -100, 0),
                visible=False,
            )
            p.fall_speed = WEATHER_FALL_SPEED_SNOW + random.uniform(-1, 1)
            p.drift = random.uniform(-WEATHER_DRIFT_SNOW, WEATHER_DRIFT_SNOW)
            p.drift_phase = random.uniform(0, math.pi * 2)
            p.weather_type = 'snow'
            self.weather_particles.append(p)

        # Ember particles (used in lava biome)
        for _ in range(WEATHER_EMBER_COUNT):
            p = Entity(
                model='sphere',
                color=color.rgba(255, 120, 30, 150),
                scale=random.uniform(0.05, 0.15),
                position=Vec3(0, -100, 0),
                visible=False,
            )
            p.fall_speed = WEATHER_FALL_SPEED_EMBER + random.uniform(-1, 1)
            p.drift = random.uniform(-WEATHER_DRIFT_EMBER, WEATHER_DRIFT_EMBER)
            p.rise_speed = random.uniform(2, 6)
            p.weather_type = 'ember'
            self.weather_particles.append(p)

    def _update_weather(self, dt, player_pos):
        """Update weather particles based on current biome."""
        biome = self.current_biome
        # Determine which weather type is active
        if biome == 'snow':
            active_type = 'snow'
        elif biome == 'lava':
            active_type = 'ember'
        elif biome in ('grass', 'forest', 'swamp'):
            active_type = 'rain'
        else:
            active_type = None

        for wp in self.weather_particles:
            if wp.weather_type == active_type:
                wp.visible = True
                if wp.weather_type == 'rain':
                    # Rain: falls straight down in a column around the player
                    if wp.y < 0:
                        # Respawn above player
                        wp.x = player_pos.x + random.uniform(-30, 30)
                        wp.z = player_pos.z + random.uniform(-30, 30)
                        wp.y = player_pos.y + random.uniform(15, 30)
                    wp.y -= wp.fall_speed * dt
                    wp.x += wp.drift * dt
                    # Hide if fell below ground
                    if wp.y < 0:
                        wp.visible = False
                elif wp.weather_type == 'snow':
                    # Snow: falls slowly with lateral drift
                    if wp.y < 0:
                        wp.x = player_pos.x + random.uniform(-35, 35)
                        wp.z = player_pos.z + random.uniform(-35, 35)
                        wp.y = player_pos.y + random.uniform(10, 25)
                    wp.y -= wp.fall_speed * dt
                    wp.drift_phase += dt * 2
                    wp.x += math.sin(wp.drift_phase) * wp.drift * dt
                    wp.z += wp.drift * 0.3 * dt
                    if wp.y < 0:
                        wp.visible = False
                elif wp.weather_type == 'ember':
                    # Embers: rise upward from ground
                    if wp.y < 0:
                        wp.x = player_pos.x + random.uniform(-25, 25)
                        wp.z = player_pos.z + random.uniform(-25, 25)
                        wp.y = random.uniform(0, 2)
                    wp.y += wp.rise_speed * dt
                    wp.x += math.sin(self.t * 2 + wp.drift_phase) * wp.drift * dt
                    wp.z += wp.drift * 0.5 * dt
                    # Fade and respawn after rising too high
                    if wp.y > player_pos.y + 20:
                        wp.visible = False
            else:
                wp.visible = False

    def _spawn_particles(self, pos, col, count=8):
        """Spawn burst particles at a position. Respects MAX_PARTICLES limit."""
        count = min(count, MAX_PARTICLES - len(self.particles))
        if count <= 0:
            return
        for _ in range(count):
            vel = Vec3(random.uniform(-3, 3), random.uniform(1, 5), random.uniform(-3, 3))
            p = Entity(model='sphere', color=col, scale=random.uniform(0.1, 0.3),
                       position=pos)
            self.particles.append((p, vel, random.uniform(0.5, 1.5)))

    def _spawn_collect_burst(self, pos, col):
        """Spawn a ring burst effect when collecting an item."""
        count = min(PARTICLE_COLLECT_COUNT, MAX_PARTICLES - len(self.particles))
        for i in range(count):
            angle = (i / count) * math.pi * 2
            spread = random.uniform(1.5, 3.5)
            vel = Vec3(math.cos(angle) * spread, random.uniform(2, 5), math.sin(angle) * spread)
            p = Entity(model='sphere', color=col, scale=random.uniform(0.15, 0.35),
                       position=pos)
            self.particles.append((p, vel, random.uniform(0.4, 1.0)))

    def shoot(self):
        """Fire tentacle laser toward mouse. Supports spread shot when weapon upgrade active."""
        if self.player.shoot_timer > 0 or self.game_over:
            return
        self.player.shoot_timer = SHOOT_COOLDOWN

        # Get shooting direction from mouse world point
        hit = mouse.world_point
        if hit:
            direction = Vec3(hit.x - self.player.x, 0, hit.z - self.player.z).normalized()
        else:
            direction = self.player.facing

        base_damage = PROJECTILE_BASE_DAMAGE + self.player.level * PROJECTILE_LEVEL_DAMAGE_BONUS

        if self.player.weapon_upgrade_timer > 0:
            # Spread shot: fire 3 projectiles in a fan pattern
            base_angle = math.atan2(direction.x, direction.z)
            for offset in [-SPREAD_ANGLE, 0, SPREAD_ANGLE]:
                angle = base_angle + math.radians(offset)
                spread_dir = Vec3(math.sin(angle), 0, math.cos(angle)).normalized()
                proj = Projectile(
                    position=self.player.position + Vec3(0, 1, 0) + self.player.facing * 1.5,
                    direction=spread_dir,
                    damage=base_damage,
                    speed=PROJECTILE_SPEED,
                )
                self.projectiles.append(proj)
            self._spawn_particles(self.player.position + Vec3(0, 1, 0), color.rgb(255, 150, 0), count=5)
        else:
            # Normal single shot
            proj = Projectile(
                position=self.player.position + Vec3(0, 1, 0) + self.player.facing * 1.5,
                direction=direction,
                damage=base_damage,
                speed=PROJECTILE_SPEED,
            )
            self.projectiles.append(proj)
            self._spawn_particles(proj.position, C_LASER, count=3)

    def _update_hud(self):
        """Update HUD elements each frame."""
        p = self.player
        # HP bar
        hp_ratio = max(0, p.hp / p.max_hp)
        self.hp_bar.scale_x = 0.4 * hp_ratio
        self.hp_bar.x = -0.55 - 0.2 * (1 - hp_ratio)
        # HP bar color gradient: green → yellow → red
        if hp_ratio > 0.5:
            t = (hp_ratio - 0.5) * 2
            self.hp_bar.color = color.rgb(int(255 * (1 - t)), 255, 0)
        else:
            t = hp_ratio * 2
            self.hp_bar.color = color.rgb(255, int(255 * t), 0)
        self.hp_text.text = f'HP: {p.hp}/{p.max_hp}'

        # XP bar — defensive: guard against division by zero
        xp_ratio = p.xp / p.xp_to_next if p.xp_to_next > 0 else 0
        self.xp_bar.scale_x = 0.4 * xp_ratio
        self.xp_bar.x = -0.55 - 0.2 * (1 - xp_ratio)

        self.level_text.text = f'Lv.{p.level}'
        self.score_text.text = f'Score: {p.score}'

        # Level-up flash
        if self.level_up_timer > 0:
            self.level_up_text.visible = True
            alpha = min(1.0, self.level_up_timer / 0.5)
            self.level_up_text.color = color.rgba(255, 255, 0, int(255 * alpha))
        else:
            self.level_up_text.visible = False

        # Messages — clear all slots first to avoid stale text from previous frames
        for i in range(len(self.msg_texts)):
            self.msg_texts[i].text = ''
        visible = self.messages[-5:]
        for i, (tick, msg) in enumerate(visible):
            age = self.t - tick
            if age < 5:
                self.msg_texts[i].text = msg
                self.msg_texts[i].color = color.rgba(255, 255, 0, max(0, 255 - int(age * 50)))

        # Minimap player dot
        # Minimap player dot — position is also refreshed by _update_minimap_colors
        # at MINIMAP_REFRESH_INTERVAL, but we update every frame for smooth tracking
        world_size = WORLD_SIZE * TILE_SCALE
        mm_cx, mm_cy = MINIMAP_POSITION
        px_norm = (p.x / world_size) - 0.5
        pz_norm = (p.z / world_size) - 0.5
        self.minimap_player_dot.position = (mm_cx + px_norm * MINIMAP_SIZE, mm_cy + pz_norm * MINIMAP_SIZE)

        # Dash cooldown indicator
        if p.dash_cooldown > 0:
            self.dash_text.text = f'DASH: {p.dash_cooldown:.1f}s'
            self.dash_text.color = color.gray
        else:
            self.dash_text.text = 'DASH READY'
            self.dash_text.color = color.cyan

        # Power-up status
        pu_lines = []
        if p.speed_boost_timer > 0:
            pu_lines.append(f'SPEED BOOST: {p.speed_boost_timer:.1f}s')
        if p.shield_timer > 0:
            pu_lines.append(f'SHIELD: {p.shield_timer:.1f}s')
        if p.magnet_timer > 0:
            pu_lines.append(f'MAGNET: {p.magnet_timer:.1f}s')
        self.powerup_text.text = '  |  '.join(pu_lines)
        self.powerup_text.color = color.green if pu_lines else color.gray

        # Combo display — BUG FIX: _update_hud no longer decrements combo_display_timer
        # here; that was causing a double-decrement since game_update() also
        # decrements it. Now _update_hud only reads the timer for display purposes.
        if self.combo_display_timer > 0:
            if self.combo_count >= 2:
                self.combo_text.visible = True
                tier = min(self.combo_count, 10)
                alpha = min(1.0, self.combo_display_timer / 0.5)
                # Color shifts from yellow to orange to red as combo grows
                if tier < 4:
                    self.combo_text.color = color.rgba(255, 255, 0, int(255 * alpha))
                elif tier < 7:
                    self.combo_text.color = color.rgba(255, 150, 0, int(255 * alpha))
                else:
                    self.combo_text.color = color.rgba(255, 50, 50, int(255 * alpha))
                scale_bonus = 1.0 + min(self.combo_count * 0.15, 1.5)
                self.combo_text.scale = 2.0 * scale_bonus
                self.combo_text.text = f'COMBO x{self.combo_count}'
            else:
                self.combo_text.visible = False
        else:
            self.combo_text.visible = False
            if self.combo_count > 0:
                self.combo_count = 0

        # Weapon upgrade indicator
        if p.weapon_upgrade_timer > 0:
            self.weapon_text.text = f'SPREAD SHOT: {p.weapon_upgrade_timer:.1f}s'
            self.weapon_text.color = color.orange
        else:
            self.weapon_text.text = ''
            self.weapon_text.color = color.gray

    def _update_missions(self):
        """Check and update mission progress for all active missions."""
        p = self.player
        for m in self.missions:
            if m.completed and not m.turned_in:
                continue
            if m.turned_in:
                continue
            if m.mission_type == 'collect':
                m.progress = p.inventory.get(m.target, 0)
            elif m.mission_type == 'kill':
                m.progress = p.kills.get(m.target, 0)
            if m.progress >= m.target_count and not m.completed:
                m.completed = True
                self.add_message(f"Mission Complete: {m.title}!")

        # Auto-turn-in
        for m in self.missions:
            if m.completed and not m.turned_in:
                m.turned_in = True
                p.gain_xp(m.reward)
                p.score += m.reward
                p.completed_missions += 1
                self.add_message(f"Turned in: {m.title}! +{m.reward} XP")

        # BUG FIX: prune turned-in missions to prevent the list from growing
        # forever and slowing down iteration. Keep only active missions.
        self.missions = [m for m in self.missions if not m.turned_in]

        # Assign new missions if needed
        # After pruning, all missions in the list are active (not turned_in)
        if len(self.missions) < 3:
            self._assign_missions(count=1)


def game_update():
    """Main update loop — called every frame."""
    global game

    if game.game_over:
        # Check for restart
        if held_keys['r']:
            # Bug fix: instead of destroying ALL scene entities (which kills camera,
            # sky, lighting etc.), properly clean up only the game's own entities.
            # Ursina's destroy() on parent cascades to children, so we destroy
            # top-level game entities and let the new Game() recreate everything.
            game._cleanup()
            game = Game()
            return
        return

    if game.paused:
        if held_keys['p'] and not hasattr(game, '_p_held'):
            game.paused = False
            game._p_held = True
        elif not held_keys['p']:
            game._p_held = False
        return
    else:
        if held_keys['p'] and not hasattr(game, '_p_held'):
            game.paused = True
            game._p_held = True
            return
        elif not held_keys['p']:
            game._p_held = False

    game.t += time.dt
    p = game.player

    # ── Hit-Stop: Brief freeze on kills for impact ──
    if game.hit_stop_timer > 0:
        game.hit_stop_timer -= time.dt
        # During hit-stop, only update camera, HUD, particles, and damage numbers
        # (visual cleanup continues, but gameplay is frozen)
        if game.level_up_timer > 0:
            game.level_up_timer -= time.dt
            if game.level_up_timer <= 0:
                game.level_up_text.visible = False
        target_pos = p.position + Vec3(0, 0, 0)
        shake_offset = Vec3(0, 0, 0)
        if game.screen_shake > 0.01:
            shake_offset = Vec3(
                random.uniform(-1, 1) * game.screen_shake,
                random.uniform(-1, 1) * game.screen_shake,
                random.uniform(-0.5, 0.5) * game.screen_shake,
            )
            game.screen_shake -= game.screen_shake * SCREEN_SHAKE_DECAY * time.dt
        else:
            game.screen_shake = 0
        game.cam_pivot.position = lerp(game.cam_pivot.position, target_pos, time.dt * CAMERA_LERP_SPEED) + shake_offset
        # Still update particles and damage numbers during freeze
        i = 0
        while i < len(game.particles):
            p_ent, vel, lifetime = game.particles[i]
            p_ent.position += vel * time.dt
            new_vel = Vec3(vel.x, vel.y - PARTICLE_GRAVITY * time.dt, vel.z)
            new_lifetime = lifetime - time.dt
            p_ent.scale *= PARTICLE_SCALE_DECAY
            if new_lifetime <= 0:
                destroy(p_ent)
                game.particles.pop(i)
            else:
                game.particles[i] = (p_ent, new_vel, new_lifetime)
                i += 1
        for dmg_num in game.damage_numbers[:]:
            if dmg_num.update(time.dt):
                dmg_num.destroy()
                game.damage_numbers.remove(dmg_num)
        # Update projectile trails during freeze (visual only)
        for trail in game.projectile_trails[:]:
            if trail.update_trail(time.dt):
                destroy(trail)
                game.projectile_trails.remove(trail)
        # Star twinkling
        for star in game.stars:
            twinkle = 0.5 + 0.5 * math.sin(game.t * star.twinkle_speed + star.twinkle_offset)
            alpha = int(255 * max(0.1, min(1.0, star.base_brightness * twinkle)))
            star.color = color.rgba(255, 255, 255, alpha)
        game._update_hud()
        return

    # ── Player Movement ──
    move_dir = Vec3(0, 0, 0)
    if held_keys['w'] or held_keys['up arrow']:
        move_dir += Vec3(0, 0, 1)
    if held_keys['s'] or held_keys['down arrow']:
        move_dir += Vec3(0, 0, -1)
    if held_keys['a'] or held_keys['left arrow']:
        move_dir += Vec3(-1, 0, 0)
    if held_keys['d'] or held_keys['right arrow']:
        move_dir += Vec3(1, 0, 0)

    # Effective speed (apply speed boost power-up)
    effective_speed = p.speed
    if p.speed_boost_timer > 0:
        effective_speed *= SPEED_BOOST_MULTIPLIER
        p.speed_boost_timer -= time.dt

    # ── Dash Ability ──
    if p.dash_cooldown > 0:
        p.dash_cooldown -= time.dt
    if p.dash_timer > 0:
        # Currently dashing
        p.dash_timer -= time.dt
        dash_pos = p.position + p.dash_direction * DASH_SPEED * time.dt
        if game._is_walkable(dash_pos.x, dash_pos.z):
            p.x = max(1, min(dash_pos.x, (WORLD_SIZE - 1) * TILE_SCALE))
            p.z = max(1, min(dash_pos.z, (WORLD_SIZE - 1) * TILE_SCALE))
        # Dash trail particles
        if int(game.t * 30) % 2 == 0:
            game._spawn_particles(p.position + Vec3(0, 0.5, 0), color.rgba(0, 230, 70, 180), count=DASH_TRAIL_PARTICLES)
    elif held_keys['space'] and p.dash_cooldown <= 0 and move_dir.length() > 0:
        # Initiate dash
        p.dash_direction = move_dir.normalized()
        p.dash_timer = DASH_DURATION
        p.dash_cooldown = DASH_COOLDOWN
        game.add_message("DASH!")
        game._spawn_particles(p.position, color.cyan, count=5)

    # Shield visual update
    p.shield_visual.visible = p.shield_timer > 0
    if p.shield_timer > 0:
        p.shield_timer -= time.dt
        # Pulsing shield effect
        p.shield_visual.scale = 1.6 + math.sin(game.t * 8) * 0.1

    # Weapon upgrade timer
    if p.weapon_upgrade_timer > 0:
        p.weapon_upgrade_timer -= time.dt

    # Magnet Core timer
    if p.magnet_timer > 0:
        p.magnet_timer -= time.dt

    # Combo timer
    if game.combo_timer > 0:
        game.combo_timer -= time.dt
        if game.combo_timer <= 0:
            game.combo_count = 0
    # BUG FIX: combo_display_timer was decremented in both _update_hud() and
    # (implicitly via game global references), causing a double-decrement per frame.
    # Now it's only decremented here in game_update().
    if game.combo_display_timer > 0:
        game.combo_display_timer -= time.dt

    # Track whether player is actually moving (for squish/stretch animation)
    p.is_moving = move_dir.length() > 0 and p.dash_timer <= 0

    if move_dir.length() > 0 and p.dash_timer <= 0:
        move_dir = move_dir.normalized()
        new_pos = p.position + move_dir * effective_speed * time.dt
        if game._is_walkable(new_pos.x, new_pos.z):
            p.x = max(1, min(new_pos.x, (WORLD_SIZE - 1) * TILE_SCALE))
            p.z = max(1, min(new_pos.z, (WORLD_SIZE - 1) * TILE_SCALE))
            p.facing = move_dir

    # Face mouse
    hit = mouse.world_point
    if hit:
        face_dir = Vec3(hit.x - p.x, 0, hit.z - p.z)
        if face_dir.length() > 0.1:
            p.facing = face_dir.normalized()
            p.look_at_2d(Vec3(hit.x, p.y, hit.z))

    # Bob animation
    p.animate_bob(game.t)
    p.update_tentacles(game.t)

    # Invulnerability timer
    if p.invuln_timer > 0:
        p.invuln_timer -= time.dt
        # Blink
        p.visible = int(game.t * PLAYER_BLINK_RATE) % 2 == 0
    else:
        p.visible = True

    # Shoot cooldown
    if p.shoot_timer > 0:
        p.shoot_timer -= time.dt

    # Shooting
    if mouse.left and not game.game_over:
        game.shoot()

    # ── Level-up visual feedback ──
    if p.level_up_pending:
        p.level_up_pending = False
        game.level_up_timer = LEVEL_UP_FLASH_DURATION
        game.level_up_text.text = f'LEVEL UP! Lv.{p.level}'
        game.level_up_text.visible = True
        game._spawn_particles(p.position, color.yellow, count=PARTICLE_LEVELUP_COUNT)
        # BUG FIX: removed p.scale = 1.8 / invoke(setattr) because animate_bob()
        # continuously overrides p.scale every frame, making the level-up pulse
        # invisible. Instead, use a brief color flash on the player model.
        p.color = color.yellow
        invoke(setattr, p, 'color', C_ALIEN, delay=0.4)
        game.add_message(f"Level Up! Now Lv.{p.level}!")

    if game.level_up_timer > 0:
        game.level_up_timer -= time.dt
        if game.level_up_timer <= 0:
            game.level_up_text.visible = False

    # ── Camera Follow with Screen Shake ──
    target_pos = p.position + Vec3(0, 0, 0)
    shake_offset = Vec3(0, 0, 0)
    if game.screen_shake > 0.01:
        shake_offset = Vec3(
            random.uniform(-1, 1) * game.screen_shake,
            random.uniform(-1, 1) * game.screen_shake,
            random.uniform(-0.5, 0.5) * game.screen_shake,
        )
        game.screen_shake -= game.screen_shake * SCREEN_SHAKE_DECAY * time.dt
    else:
        game.screen_shake = 0
    game.cam_pivot.position = lerp(game.cam_pivot.position, target_pos, time.dt * CAMERA_LERP_SPEED) + shake_offset

    # ── Update Enemies ──
    for enemy in game.enemies[:]:
        # Handle death animation
        if enemy.dying:
            if enemy.update_death_animation(time.dt):
                # Death animation complete, remove enemy
                for d in enemy.decor_entities:
                    destroy(d)
                destroy(enemy)
                destroy(enemy.eye_l)
                destroy(enemy.eye_r)
                destroy(enemy.hp_bar_bg)
                destroy(enemy.hp_bar)
                game.enemies.remove(enemy)
            continue

        if not enemy.alive:
            for d in enemy.decor_entities:
                destroy(d)
            destroy(enemy)
            destroy(enemy.eye_l)
            destroy(enemy.eye_r)
            destroy(enemy.hp_bar_bg)
            destroy(enemy.hp_bar)
            game.enemies.remove(enemy)
            continue

        dist_to_player = (enemy.position - p.position).length()

        # ── Process knockback velocity ──
        if enemy.knockback_vel.length() > 0.1:
            kb_pos = enemy.position + enemy.knockback_vel * time.dt
            if game._is_walkable(kb_pos.x, kb_pos.z):
                enemy.x = kb_pos.x
                enemy.z = kb_pos.z
            # Gravity on the vertical component
            enemy.knockback_vel = Vec3(
                enemy.knockback_vel.x * 0.9,
                enemy.knockback_vel.y - PARTICLE_GRAVITY * time.dt,
                enemy.knockback_vel.z * 0.9,
            )
            # If vertical velocity pulls below ground, reset
            if enemy.knockback_vel.y < 0 and enemy.y <= 1:
                enemy.knockback_vel = Vec3(0, 0, 0)
            # Decay horizontal knockback quickly
            if abs(enemy.knockback_vel.x) < 0.1 and abs(enemy.knockback_vel.z) < 0.1:
                enemy.knockback_vel = Vec3(0, enemy.knockback_vel.y, 0)

        # Skip AI updates for very distant enemies (performance)
        if dist_to_player < enemy.detect_range:
            # Chase player
            direction = (p.position - enemy.position).normalized()
            direction.y = 0
            new_pos = enemy.position + direction * enemy.speed * time.dt
            if game._is_walkable(new_pos.x, new_pos.z):
                enemy.position = new_pos
            else:
                # BUG FIX: if the direct path is blocked (e.g., water/lava between
                # enemy and player), try moving along each axis independently so
                # the enemy slides along the obstacle instead of freezing in place.
                move_step = direction * enemy.speed * time.dt
                # Try X axis only
                if game._is_walkable(enemy.x + move_step.x, enemy.z):
                    enemy.x += move_step.x
                # Try Z axis only
                if game._is_walkable(enemy.x, enemy.z + move_step.z):
                    enemy.z += move_step.z
            enemy.look_at_2d(p.position)

            # ── Phase Shifter: Teleport near player periodically ──
            if enemy.is_phase_shifter:
                enemy.phase_timer -= time.dt
                if enemy.phase_timer <= 0:
                    # Teleport to a random position near the player
                    angle = random.uniform(0, math.pi * 2)
                    tp_dist = random.uniform(5, 10)
                    tp_x = p.x + math.cos(angle) * tp_dist
                    tp_z = p.z + math.sin(angle) * tp_dist
                    if game._is_walkable(tp_x, tp_z):
                        # Poof particles at old position
                        game._spawn_particles(enemy.position, color.violet, count=8)
                        enemy.x = tp_x
                        enemy.z = tp_z
                        # Poof particles at new position
                        game._spawn_particles(enemy.position, color.rgba(180, 0, 255, 200), count=8)
                        game.add_message(f"Phase Shifter teleported!")
                    enemy.phase_timer = random.uniform(4, 8)

            # ── Spore Spitter: Shoot projectiles at player ──
            if enemy.is_spore_spitter:
                enemy.spit_timer -= time.dt
                if enemy.spit_timer <= 0 and dist_to_player < 25:
                    spit_dir = (p.position - enemy.position).normalized()
                    spit_dir.y = 0
                    spit_dir = spit_dir.normalized()
                    ep = EnemyProjectile(
                        position=enemy.position + Vec3(0, 1, 0) + spit_dir * 1.2,
                        direction=spit_dir,
                        damage=enemy.damage,
                        speed=15,
                    )
                    game.enemy_projectiles.append(ep)
                    game._spawn_particles(enemy.position, color.rgb(200, 100, 0), count=4)
                    enemy.spit_timer = random.uniform(2.5, 4.5)

            # ── Void Bomber: Kamikaze explosion near player ──
            if enemy.is_void_bomber:
                if dist_to_player < VOID_BOMBER_FUSE_RANGE and not enemy.fuse_active:
                    # Start fuse countdown
                    enemy.fuse_active = True
                    enemy.fuse_timer = VOID_BOMBER_FUSE_TIME
                    game.add_message("Void Bomber is about to explode!")
                if enemy.fuse_active:
                    enemy.fuse_timer -= time.dt
                    # Pulsing red glow as fuse counts down
                    pulse = 1.0 - (enemy.fuse_timer / VOID_BOMBER_FUSE_TIME)
                    # BUG FIX: pulse_speed used += which accumulated forever, causing
                    # the pulsing to become so fast it appeared constant. Now use game.t
                    # directly for a smooth, time-based pulse effect.
                    pulse_rate = 8 + pulse * 20  # accelerates as fuse runs down
                    if int(game.t * pulse_rate) % 2 == 0:
                        enemy.color = color.rgb(255, int(50 * (1 - pulse)), 0)
                    else:
                        enemy.color = color.rgb(200, 0, 0)
                    enemy.scale = enemy.original_scale * (1.0 + pulse * 0.4)
                    if enemy.fuse_timer <= 0:
                        # EXPLODE!
                        game._spawn_particles(enemy.position, color.rgb(255, 100, 0), count=20)
                        game._spawn_particles(enemy.position, color.yellow, count=10)
                        game.screen_shake = max(game.screen_shake, 1.0)
                        # Damage player if in range
                        if dist_to_player < VOID_BOMBER_EXPLOSION_RADIUS:
                            if p.shield_timer > 0:
                                game._spawn_particles(p.position + Vec3(0, 1, 0), color.rgb(100, 200, 255), count=10)
                                game.add_message("Shield absorbed explosion!")
                            else:
                                died = p.take_damage(VOID_BOMBER_EXPLOSION_DAMAGE)
                                game._spawn_particles(p.position, color.red, count=PARTICLE_DAMAGE_COUNT)
                                game.damage_numbers.append(DamageNumber(p.position, VOID_BOMBER_EXPLOSION_DAMAGE, is_kill=False))
                                if died:
                                    game._show_death_screen(p)
                        # Damage other nearby enemies too (friendly fire!)
                        for other_enemy in game.enemies:
                            if other_enemy is enemy or not other_enemy.alive or other_enemy.dying:
                                continue
                            edist = (other_enemy.position - enemy.position).length()
                            if edist < VOID_BOMBER_EXPLOSION_RADIUS:
                                other_killed = other_enemy.take_damage(VOID_BOMBER_EXPLOSION_DAMAGE // 2)
                                if other_killed:
                                    p.add_kill(other_enemy.name)
                                    xp_gain = BASE_KILL_XP + other_enemy.max_hp // KILL_XP_HP_DIVISOR
                                    p.gain_xp(xp_gain)
                                    p.score += other_enemy.max_hp
                                    game.damage_numbers.append(DamageNumber(other_enemy.position, VOID_BOMBER_EXPLOSION_DAMAGE // 2, is_kill=True))
                        # Kill the bomber
                        enemy.alive = False
                        enemy.dying = True
                        enemy.death_timer = DEATH_ANIM_DURATION

            # ── Nebula Phantom: Flying orbit + dive attack ──
            if enemy.is_nebula_phantom and enemy.alive:
                if enemy.orbit_state == 'orbit':
                    # Circle around the player
                    enemy.orbit_angle += NEBULA_PHANTOM_ORBIT_SPEED * time.dt
                    target_x = p.x + math.cos(enemy.orbit_angle) * NEBULA_PHANTOM_ORBIT_RADIUS
                    target_z = p.z + math.sin(enemy.orbit_angle) * NEBULA_PHANTOM_ORBIT_RADIUS
                    # BUG FIX: Nebula Phantom is a flying enemy and should be able
                    # to move over water/lava tiles. Use bounds check instead of
                    # walkability check so it doesn't get stuck orbiting in place.
                    if 0 <= target_x <= WORLD_SIZE * TILE_SCALE and 0 <= target_z <= WORLD_SIZE * TILE_SCALE:
                        enemy.x = target_x
                        enemy.z = target_z
                    # Float higher than normal enemies
                    enemy.y = 4 + math.sin(game.t * 3 + id(enemy) % 100) * 0.5
                    enemy.look_at_2d(p.position)
                    # Check if should dive
                    enemy.dive_timer -= time.dt
                    if enemy.dive_timer <= 0:
                        enemy.orbit_state = 'dive'
                        enemy.dive_target = Vec3(p.x, 1, p.z)
                        game._spawn_particles(enemy.position, color.rgb(100, 150, 255), count=8)
                        game.add_message("Nebula Phantom diving!")
                elif enemy.orbit_state == 'dive':
                    # Dive toward the player's last known position
                    dive_dir = (enemy.dive_target - enemy.position).normalized()
                    new_dive_pos = enemy.position + dive_dir * NEBULA_PHANTOM_DIVE_SPEED * time.dt
                    # BUG FIX: Same as orbit — flying enemy can dive over any terrain.
                    if 0 <= new_dive_pos.x <= WORLD_SIZE * TILE_SCALE and 0 <= new_dive_pos.z <= WORLD_SIZE * TILE_SCALE:
                        enemy.x = new_dive_pos.x
                        enemy.z = new_dive_pos.z
                    # Descend toward ground level
                    enemy.y = max(1, enemy.y - 15 * time.dt)
                    # Check if reached dive target (close to ground)
                    if enemy.y <= 1.2:
                        # Impact particles and return to orbit
                        game._spawn_particles(enemy.position, color.rgb(100, 150, 255), count=10)
                        enemy.orbit_state = 'orbit'
                        enemy.dive_timer = random.uniform(NEBULA_PHANTOM_DIVE_COOLDOWN_MIN, NEBULA_PHANTOM_DIVE_COOLDOWN_MAX)
                        enemy.y = 4
        else:
            # Wander
            enemy.wander_timer -= time.dt
            if enemy.wander_timer <= 0:
                # Bug fix: guard against zero-length direction producing NaN
                wd = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1))
                enemy.wander_dir = wd.normalized() if wd.length() > 0.01 else Vec3(1, 0, 0)
                enemy.wander_timer = random.uniform(ENEMY_WANDER_INTERVAL_MIN, ENEMY_WANDER_INTERVAL_MAX)
            new_pos = enemy.position + enemy.wander_dir * enemy.speed * ENEMY_WANDER_SPEED_FACTOR * time.dt
            if game._is_walkable(new_pos.x, new_pos.z):
                enemy.position = new_pos
            else:
                enemy.wander_dir = -enemy.wander_dir

        # Attack player (shield blocks damage)
        # Bug fix: cooldown must decrement even when in range, otherwise enemies
        # attack once and then never again while staying next to the player.
        enemy.attack_cd = max(0, enemy.attack_cd - time.dt)
        if dist_to_player < ENEMY_ATTACK_RANGE and enemy.attack_cd <= 0:
            if p.shield_timer > 0:
                # Shield absorbs the hit
                game._spawn_particles(p.position + Vec3(0, 1, 0), color.rgb(100, 200, 255), count=10)
                game.add_message("Shield blocked!")
            else:
                died = p.take_damage(enemy.damage)
                game.screen_shake = SCREEN_SHAKE_DAMAGE
                game._spawn_particles(p.position, color.red, count=PARTICLE_DAMAGE_COUNT)
                if died:
                    game._show_death_screen(p)
            enemy.attack_cd = ENEMY_ATTACK_COOLDOWN

        # Float enemies (except Nebula Phantom which controls its own Y)
        if not enemy.is_nebula_phantom:
            enemy.y = 1 + math.sin(game.t * 2 + id(enemy) % 100) * 0.2
        enemy.update_hp_bar()

    # ── Update Projectiles ──
    for proj in game.projectiles[:]:
        alive = proj.move(time.dt)
        if not alive:
            destroy(proj)
            game.projectiles.remove(proj)
            continue

        # Spawn trail dot behind projectile for visual flair
        proj.trail_timer += time.dt
        if proj.trail_timer >= PROJECTILE_TRAIL_INTERVAL:
            proj.trail_timer = 0.0
            trail = ProjectileTrail(position=Vec3(proj.x, proj.y, proj.z), col=C_LASER)
            game.projectile_trails.append(trail)

        # Check collision with enemies
        for enemy in game.enemies:
            if not enemy.alive or enemy.dying:
                continue
            if (proj.position - enemy.position).length() < enemy.scale_x + 0.5:
                # Pass projectile direction for knockback
                hit_dir = proj.direction
                killed = enemy.take_damage(proj.damage, hit_direction=hit_dir)
                game._spawn_particles(enemy.position, color.yellow, count=PARTICLE_HIT_COUNT)
                game.screen_shake = max(game.screen_shake, 0.15)
                # Floating damage number
                game.damage_numbers.append(DamageNumber(enemy.position, proj.damage, is_kill=False))
                destroy(proj)
                if proj in game.projectiles:
                    game.projectiles.remove(proj)
                if killed:
                    p.add_kill(enemy.name)
                    # Combo system: increment combo and apply bonus
                    game.combo_count += 1
                    game.combo_timer = COMBO_TIMEOUT
                    game.combo_display_timer = COMBO_DISPLAY_LIFETIME
                    combo_xp_mult = 1.0 + (min(game.combo_count, 10) - 1) * COMBO_XP_BONUS_PER_TIER
                    combo_score_mult = 1.0 + (min(game.combo_count, 10) - 1) * COMBO_SCORE_BONUS_PER_TIER
                    xp_gain = int((BASE_KILL_XP + enemy.max_hp // KILL_XP_HP_DIVISOR) * combo_xp_mult)
                    p.gain_xp(xp_gain)
                    p.score += int(enemy.max_hp * combo_score_mult)
                    game.screen_shake = SCREEN_SHAKE_KILL
                    # Hit-stop: brief freeze on kills for satisfying impact
                    game.hit_stop_timer = HIT_STOP_KILL_DURATION
                    # Kill damage number (bigger, yellow)
                    game.damage_numbers.append(DamageNumber(enemy.position, proj.damage, is_kill=True))
                    # Drop loot
                    # BUG FIX: loot drops now check walkability so collectibles don't
                    # spawn in unreachable water/lava tiles.
                    for _ in range(random.randint(LOOT_DROP_MIN, LOOT_DROP_MAX)):
                        offset = Vec3(random.uniform(-3, 3), 1.5, random.uniform(-3, 3))
                        drop_pos = enemy.position + offset
                        if game._is_walkable(drop_pos.x, drop_pos.z):
                            c = Collectible(position=drop_pos)
                            game.collectibles.append(c)
                    game._spawn_particles(enemy.position, enemy.original_color, count=PARTICLE_KILL_COUNT)
                    game.add_message(f"Defeated {enemy.name}!")
                break

        # Remove if out of world
        if proj.x < -10 or proj.x > WORLD_SIZE * TILE_SCALE + 10 or proj.z < -10 or proj.z > WORLD_SIZE * TILE_SCALE + 10:
            destroy(proj)
            if proj in game.projectiles:
                game.projectiles.remove(proj)

    # ── Update Enemy Projectiles ──
    for eproj in game.enemy_projectiles[:]:
        alive = eproj.move(time.dt)
        if not alive:
            destroy(eproj)
            game.enemy_projectiles.remove(eproj)
            continue
        # Check collision with player
        dist = (eproj.position - p.position).length()
        if dist < 1.5:
            if p.shield_timer > 0:
                # Shield blocks enemy projectile
                game._spawn_particles(p.position + Vec3(0, 1, 0), color.rgb(100, 200, 255), count=10)
                game.add_message("Shield blocked!")
            else:
                died = p.take_damage(eproj.damage)
                game.screen_shake = SCREEN_SHAKE_DAMAGE
                game._spawn_particles(p.position, color.rgb(200, 100, 0), count=PARTICLE_DAMAGE_COUNT)
                game.damage_numbers.append(DamageNumber(p.position, eproj.damage, is_kill=False))
                if died:
                    game._show_death_screen(p)
            destroy(eproj)
            game.enemy_projectiles.remove(eproj)
            continue
        # Remove if out of world
        if eproj.x < -10 or eproj.x > WORLD_SIZE * TILE_SCALE + 10 or eproj.z < -10 or eproj.z > WORLD_SIZE * TILE_SCALE + 10:
            destroy(eproj)
            game.enemy_projectiles.remove(eproj)

    # ── Update Collectibles ──
    for col in game.collectibles[:]:
        # Handle pop animation before destruction
        if col.popping:
            col.pop_timer -= time.dt
            progress = 1.0 - max(0, col.pop_timer / COLLECT_POP_DURATION)
            # Elastic overshoot: scale peaks above max then settles
            # Uses a sine-based elastic curve for a bouncy feel
            if progress < 0.6:
                # Scale up with acceleration toward peak
                elastic = (progress / 0.6) ** 0.5  # ease-out quad for initial rise
                col.scale = 0.6 * (1.0 + elastic * (COLLECT_POP_MAX_SCALE - 1.0))
            else:
                # Settle back down with a slight bounce
                settle = (progress - 0.6) / 0.4  # 0 to 1 in settle phase
                col.scale = 0.6 * (COLLECT_POP_MAX_SCALE - (COLLECT_POP_MAX_SCALE - 1.0) * settle)
            # Flash white at the start of pop
            if progress < 0.3:
                col.color = color.white
                col.glow.color = color.rgba(255, 255, 255, 200)
            else:
                col.color = col.item_color
                # Fade out glow
                fade = max(0, 1.0 - (progress - 0.3) / 0.7)
                col.glow.color = color.rgba(col.item_color.r, col.item_color.g, col.item_color.b, int(80 * fade))
            col.rotation_y += 720 * time.dt  # Spin fast during pop
            if col.pop_timer <= 0:
                destroy(col.glow)
                destroy(col)
                game.collectibles.remove(col)
            continue

        col.animate(game.t)
        dist = (col.position - p.position).length()
        # Magnetic pull: items are drawn toward player when close
        # Defensive: skip pull if dist is effectively zero to avoid NaN direction
        pull_radius = COLLECT_PULL_RADIUS * (MAGNET_PULL_RADIUS_MULT if p.magnet_timer > 0 else 1.0)
        pull_speed = COLLECT_PULL_SPEED * (MAGNET_PULL_SPEED_MULT if p.magnet_timer > 0 else 1.0)
        if dist < pull_radius and dist > 0.1:
            pull_dir = (p.position - col.position).normalized()
            pull_strength = 1.0 - (dist / pull_radius)  # stronger when closer
            col.position += pull_dir * pull_speed * pull_strength * time.dt
            # Spin faster as pulled
            col.rotation_y += 200 * pull_strength * time.dt
        if dist < COLLECT_RADIUS:
            # Apply power-up effects for special collectibles
            if col.name == 'Health Potion':
                p.hp = min(p.hp + HEALTH_POTION_HEAL, p.max_hp)
                game.add_message(f"Health Potion! +{HEALTH_POTION_HEAL} HP")
                game._spawn_particles(col.position, color.rgb(255, 50, 50), count=12)
            elif col.name == 'Speed Boost':
                p.speed_boost_timer = SPEED_BOOST_DURATION
                game.add_message(f"Speed Boost! {SPEED_BOOST_DURATION}s of speed!")
                game._spawn_particles(col.position, color.rgb(50, 255, 50), count=12)
            elif col.name == 'Shield Crystal':
                p.shield_timer = SHIELD_DURATION
                game.add_message(f"Shield Crystal! {SHIELD_DURATION}s of protection!")
                game._spawn_particles(col.position, color.rgb(100, 200, 255), count=12)
            elif col.name == 'Weapon Upgrade':
                p.weapon_upgrade_timer = WEAPON_UPGRADE_DURATION
                game.add_message(f"Weapon Upgrade! Spread shot for {WEAPON_UPGRADE_DURATION}s!")
                game._spawn_particles(col.position, color.rgb(255, 150, 0), count=12)
            elif col.name == 'Magnet Core':
                p.magnet_timer = MAGNET_DURATION
                game.add_message(f"Magnet Core! Item pull boosted for {MAGNET_DURATION}s!")
                game._spawn_particles(col.position, color.rgb(200, 50, 255), count=12)
            else:
                p.add_item(col.name)
                p.score += col.value
                p.gain_xp(col.value // 10)
                game._spawn_collect_burst(col.position, col.item_color)
                game.add_message(f"Found {col.name}! +{col.value} pts")
            # For power-ups, also give points
            if col.name in ('Health Potion', 'Speed Boost', 'Shield Crystal', 'Weapon Upgrade', 'Magnet Core'):
                p.score += col.value
                p.gain_xp(col.value // 10)
            # Start pop animation instead of immediate destroy
            col.popping = True
            col.pop_timer = COLLECT_POP_DURATION

    # ── Update Particles ──
    # Bug fix: must update the tuple in-place; Python tuple unpacking creates local copies
    # so modifying `vel` and `lifetime` never updates the list, causing particles to never
    # expire and the list to grow forever (memory leak).
    i = 0
    while i < len(game.particles):
        p_ent, vel, lifetime = game.particles[i]
        p_ent.position += vel * time.dt
        new_vel = Vec3(vel.x, vel.y - PARTICLE_GRAVITY * time.dt, vel.z)
        new_lifetime = lifetime - time.dt
        p_ent.scale *= PARTICLE_SCALE_DECAY
        if new_lifetime <= 0:
            destroy(p_ent)
            game.particles.pop(i)
        else:
            game.particles[i] = (p_ent, new_vel, new_lifetime)
            i += 1

    # ── Update Projectile Trails ──
    for trail in game.projectile_trails[:]:
        if trail.update_trail(time.dt):
            destroy(trail)
            game.projectile_trails.remove(trail)

    # ── Update Damage Numbers ──
    for dmg_num in game.damage_numbers[:]:
        if dmg_num.update(time.dt):
            dmg_num.destroy()
            game.damage_numbers.remove(dmg_num)

    # ── Star Twinkling ──
    for star in game.stars:
        twinkle = 0.5 + 0.5 * math.sin(game.t * star.twinkle_speed + star.twinkle_offset)
        alpha = int(255 * max(0.1, min(1.0, star.base_brightness * twinkle)))
        star.color = color.rgba(255, 255, 255, alpha)

    # ── Nebula Cloud Drift ──
    for cloud in game.nebula_clouds:
        cloud.x += math.sin(game.t * cloud.drift_speed + cloud.drift_phase) * 0.3 * time.dt
        cloud.z += math.cos(game.t * cloud.drift_speed * 0.7 + cloud.drift_phase) * 0.2 * time.dt

    # ── Biome-Aware Fog ──
    current_biome = game._get_biome_at(p.x, p.z)
    if current_biome != game.current_biome:
        game.current_biome = current_biome
    fog_info = BIOME_FOG.get(current_biome, BIOME_FOG['grass'])
    target_fog_color = fog_info['color']
    target_fog_density = fog_info['density']
    # Lerp fog toward target biome's settings
    r = lerp(scene.fog_color[0] * 255, target_fog_color[0] * 255, time.dt * 2)
    g = lerp(scene.fog_color[1] * 255, target_fog_color[1] * 255, time.dt * 2)
    b = lerp(scene.fog_color[2] * 255, target_fog_color[2] * 255, time.dt * 2)
    scene.fog_color = color.rgb(int(r), int(g), int(b))
    scene.fog_density = lerp(scene.fog_density, target_fog_density, time.dt * 2)

    # ── Weather Effects ──
    game._update_weather(time.dt, p.position)

    # ── Spawn Timer ──
    game.spawn_timer += time.dt
    # Dynamic spawn interval: gets faster as player levels up (min 3s)
    spawn_interval = max(3, ENEMY_SPAWN_INTERVAL - (p.level - 1) // PLAYER_LEVEL_DIFFICULTY_INTERVAL * ENEMY_SPAWN_INTERVAL_LEVEL_DECAY)
    if game.spawn_timer >= spawn_interval:
        game.spawn_timer = 0
        alive_count = len([e for e in game.enemies if e.alive or e.dying])
        if alive_count < MAX_ACTIVE_ENEMIES:
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(ENEMY_SPAWN_DISTANCE_MIN, ENEMY_SPAWN_DISTANCE_MAX)
            ex = p.x + math.cos(angle) * dist
            ez = p.z + math.sin(angle) * dist
            ex = max(5, min(ex, (WORLD_SIZE - 5) * TILE_SCALE))
            ez = max(5, min(ez, (WORLD_SIZE - 5) * TILE_SCALE))
            if game._is_walkable(ex, ez):
                # Distance-based difficulty scaling
                spawn_center_x = WORLD_SIZE // 2 * TILE_SCALE
                spawn_center_z = WORLD_SIZE // 2 * TILE_SCALE
                dist_from_spawn = math.sqrt((ex - spawn_center_x) ** 2 + (ez - spawn_center_z) ** 2)
                enemy_type = game._pick_enemy_type(dist_from_spawn)
                e = Enemy(position=Vec3(ex, 1, ez), enemy_type=enemy_type)
                game._scale_enemy_to_player_level(e)
                game.enemies.append(e)

    # Respawn collectibles
    if len(game.collectibles) < MIN_COLLECTIBLES and random.random() < COLLECTIBLE_RESPAWN_CHANCE:
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(20, 50)
        cx = p.x + math.cos(angle) * dist
        cz = p.z + math.sin(angle) * dist
        cx = max(2, min(cx, (WORLD_SIZE - 2) * TILE_SCALE))
        cz = max(2, min(cz, (WORLD_SIZE - 2) * TILE_SCALE))
        if game._is_walkable(cx, cz):
            c = Collectible(position=Vec3(cx, 1, cz))
            game.collectibles.append(c)

    # ── Missions ──
    game._update_missions()

    # ── Toggle minimap ──
    if held_keys['m'] and not hasattr(game, '_m_held'):
        game.minimap_shown = not game.minimap_shown
        game.minimap_entity.visible = game.minimap_shown
        game.minimap_player_dot.visible = game.minimap_shown
        # BUG FIX: when hiding the minimap, don't use 'and dot.visible' which
        # permanently sets all enemy dots to invisible. When showing the minimap
        # again, the dots would stay invisible until the next refresh. Instead,
        # hide/show unconditionally — the refresh cycle will set correct visibility.
        for dot in game.minimap_enemy_dots:
            dot.visible = game.minimap_shown
        game._m_held = True
    elif not held_keys['m']:
        game._m_held = False

    # ── Minimap Refresh ──
    game.minimap_refresh_timer -= time.dt
    if game.minimap_refresh_timer <= 0 and game.minimap_shown:
        game.minimap_refresh_timer = MINIMAP_REFRESH_INTERVAL
        game._update_minimap_colors()

    # ── Toggle mission panel ──
    if held_keys['tab'] and not hasattr(game, '_tab_held'):
        game.mission_panel_shown = not game.mission_panel_shown
        game.mission_text.visible = game.mission_panel_shown
        game._tab_held = True
        if game.mission_panel_shown:
            lines = ["== MISSIONS =="]
            for m in game.missions:
                if m.turned_in:
                    continue
                status = "[DONE]" if m.completed else f"[{m.progress}/{m.target_count}]"
                lines.append(f"{status} {m.title}")
                lines.append(f"  {m.description}")
                lines.append(f"  Reward: {m.reward} XP")
                lines.append("")
            game.mission_text.text = '\n'.join(lines)
    elif not held_keys['tab']:
        game._tab_held = False

    # ── Update HUD ──
    game._update_hud()


# ─── Initialize & Run ─────────────────────────────────────────────────────────
game = Game()

def input(key):
    global game
    if key == 'escape':
        application.quit()
    # Bug fix: 'p' key for pause is handled entirely in game_update() via held_keys
    # to avoid double-toggle race condition where input() toggles ON and then
    # game_update() on the same frame toggles it OFF again.

app.update = game_update
app.run()