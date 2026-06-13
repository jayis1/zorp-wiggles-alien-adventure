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
VERSION = "2.1.0"

# ─── World Generation ─────────────────────────────────────────────────────────
WORLD_SIZE = 80
TILE_SCALE = 4

# ─── Player ───────────────────────────────────────────────────────────────────
PLAYER_SPEED = 12
PLAYER_INVULN_DURATION = 0.5
PLAYER_BLINK_RATE = 20
PLAYER_START_HP = 100

# ─── Combat ───────────────────────────────────────────────────────────────────
SHOOT_COOLDOWN = 0.15
COLLECT_RADIUS = 2.5
COLLECT_PULL_RADIUS = 5.0
COLLECT_PULL_SPEED = 12.0
PROJECTILE_BASE_DAMAGE = 20
PROJECTILE_LEVEL_DAMAGE_BONUS = 2
PROJECTILE_SPEED = 50
PROJECTILE_LIFETIME = 2.0
ENEMY_DETECT_RANGE = 40
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
ENEMY_SPAWN_DISTANCE_MIN = 30
ENEMY_SPAWN_DISTANCE_MAX = 60
LOOT_DROP_MIN = 1
LOOT_DROP_MAX = 3
INITIAL_COLLECTIBLES = 200
INITIAL_ENEMIES = 60
SPAWN_SAFE_RADIUS = 15
ENEMY_SPAWN_SAFE_RADIUS = 30

# ─── Leveling ─────────────────────────────────────────────────────────────────
LEVEL_UP_HEAL_AMOUNT = 20
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
CAMERA_LERP_SPEED = 5.0
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

# ─── Difficulty Scaling ──────────────────────────────────────────────────────
EASY_ENEMY_TYPES = ['Slime Blob', 'Space Beetle', 'Swarm Mite']
MEDIUM_ENEMY_TYPES = ['Space Beetle', 'Void Wraith', 'Phase Shifter']
HARD_ENEMY_TYPES = ['Void Wraith', 'Lava Crawler', 'Crystal Guardian', 'Plasma Drake', 'Spore Spitter']
DIFFICULTY_SCALE_DISTANCE = 100  # world units per difficulty tier

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
}

WALKABLE = {'grass', 'desert', 'forest', 'crystal', 'snow', 'swamp', 'mushroom'}

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
        biomes = ['desert', 'water', 'lava', 'forest', 'crystal', 'snow', 'swamp', 'mushroom']
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
        """Apply vertical bob animation to the player."""
        self.y = 1.2 + math.sin(t * 3) * 0.15

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
        'Crystal Guardian': {'color': color.cyan,         'hp': 200, 'speed': 3,  'damage': 40, 'scale': 1.8,  'model': 'diamond', 'decor': 'shards'},
        'Plasma Drake':    {'color': color.magenta,       'hp': 350, 'speed': 7,  'damage': 50, 'scale': 2.2,  'model': 'diamond', 'decor': 'wings'},
        'Phase Shifter':   {'color': color.rgba(180, 0, 255, 200), 'hp': 70,  'speed': 5,  'damage': 20, 'scale': 1.3,  'model': 'diamond', 'decor': 'aura'},
        'Spore Spitter':   {'color': color.rgb(200, 100, 0),       'hp': 90,  'speed': 3.5,'damage': 15, 'scale': 1.4,  'model': 'sphere', 'decor': 'spikes'},
        'Swarm Mite':      {'color': color.rgb(150, 200, 50),      'hp': 15,  'speed': 8,  'damage': 5,  'scale': 0.5,  'model': 'sphere', 'decor': 'none'},
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
        self.wander_dir = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        self.wander_timer = random.uniform(ENEMY_WANDER_INTERVAL_MIN, ENEMY_WANDER_INTERVAL_MAX)
        self.hit_flash = 0
        self.decor_entities = []

        # Type-specific special behaviors
        self.is_phase_shifter = (enemy_type == 'Phase Shifter')
        self.phase_timer = random.uniform(4, 8) if self.is_phase_shifter else 0
        self.is_spore_spitter = (enemy_type == 'Spore Spitter')
        self.spit_timer = random.uniform(2, 4) if self.is_spore_spitter else 0
        self.is_swarm_mite = (enemy_type == 'Swarm Mite')

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

    def take_damage(self, amount):
        """Apply damage to the enemy. Returns True if killed."""
        self.hp -= amount
        self.hit_flash = 0.1
        self.color = color.white
        invoke(setattr, self, 'color', self.original_color, delay=0.1)
        if self.hp <= 0:
            self.alive = False
            self.dying = True
            self.death_timer = DEATH_ANIM_DURATION
            return True
        return False

    def update_hp_bar(self):
        """Update the HP bar scale and color based on current health ratio."""
        ratio = max(0, self.hp / self.max_hp)
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
    }

    def __init__(self, position, item_type=None):
        if item_type is None:
            item_type = random.choice(list(self.ITEMS.keys()))
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
        # Glow ring
        self.glow = Entity(model='quad', color=color.rgba(info['color'].r, info['color'].g, info['color'].b, 80),
                           scale=3, parent=self, rotation_x=90, position=(0, -0.3, 0))

    def animate(self, t):
        """Bob and spin the collectible each frame."""
        self.y = 1.0 + math.sin(t * 2 + self.bob_offset) * 0.4
        self.rotation_y += 60 * time.dt


# ─── Projectile ────────────────────────────────────────────────────────────────
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

        # Trail
        self.trail = []

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
        # Fade out
        alpha = max(0, self.lifetime / self.max_lifetime)
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
            star = Entity(
                model='quad',
                color=color.rgba(255, 255, 255, int(255 * brightness)),
                scale=star_size,
                position=(sx, sy, sz),
                billboard=True,
            )
            self.stars.append(star)

        # Fog for atmosphere
        scene.fog_color = color.rgb(25, 0, 60)
        scene.fog_density = 0.007

        # HUD
        self._create_hud()

        # Crosshair
        self.crosshair = Entity(parent=camera.ui, model='quad', color=color.rgba(255, 255, 255, 128),
                                scale=(0.003, 0.04), position=(0, 0))
        self.crosshair2 = Entity(parent=camera.ui, model='quad', color=color.rgba(255, 255, 255, 128),
                                 scale=(0.04, 0.003), position=(0, 0))

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

    def _is_walkable(self, world_x, world_z):
        """Check if a world position is on walkable terrain."""
        tx = int(world_x / TILE_SCALE)
        tz = int(world_z / TILE_SCALE)
        if 0 <= tx < WORLD_SIZE and 0 <= tz < WORLD_SIZE:
            return self.world_grid[tz][tx] in WALKABLE
        return False

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

        # Minimap
        self.minimap_shown = True
        self.minimap_entity = None
        self.minimap_player_dot = None
        self.minimap_enemy_dots = []
        self._build_minimap()

    def _build_minimap(self):
        """Create minimap as a UI texture."""
        self.minimap_entity = Entity(parent=camera.ui, model='quad',
                                     color=color.black, scale=(0.22, 0.22),
                                     position=(0.72, 0.37))
        # Player dot on minimap
        self.minimap_player_dot = Entity(parent=camera.ui, model='quad',
                                          color=color.white, scale=(0.005, 0.005),
                                          position=(0.72, 0.37))
        self._update_minimap_colors()

    def _update_minimap_colors(self):
        """Color-code minimap terrain."""
        pass

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
        """Fire tentacle laser toward mouse."""
        if self.player.shoot_timer > 0 or self.game_over:
            return
        self.player.shoot_timer = SHOOT_COOLDOWN

        # Get shooting direction from mouse world point
        hit = mouse.world_point
        if hit:
            direction = Vec3(hit.x - self.player.x, 0, hit.z - self.player.z).normalized()
        else:
            direction = self.player.facing

        proj = Projectile(
            position=self.player.position + Vec3(0, 1, 0) + self.player.facing * 1.5,
            direction=direction,
            damage=PROJECTILE_BASE_DAMAGE + self.player.level * PROJECTILE_LEVEL_DAMAGE_BONUS,
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

        # XP bar
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

        # Messages
        visible = self.messages[-5:]
        for i, (tick, msg) in enumerate(visible):
            age = self.t - tick
            if age < 5:
                self.msg_texts[i].text = msg
                self.msg_texts[i].color = color.rgba(255, 255, 0, max(0, 255 - int(age * 50)))
            else:
                self.msg_texts[i].text = ''

        # Minimap player dot
        mm_cx = 0.72
        mm_cy = 0.37
        mm_scale = 0.22 / (WORLD_SIZE * TILE_SCALE)
        px = mm_cx + (p.x * mm_scale) - 0.11
        pz = mm_cy + (p.z * mm_scale) - 0.11
        self.minimap_player_dot.position = (px, pz)

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
        self.powerup_text.text = '  |  '.join(pu_lines)
        self.powerup_text.color = color.green if pu_lines else color.gray

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

        # Assign new missions if needed
        active = sum(1 for m in self.missions if not m.turned_in)
        if active < 3:
            self._assign_missions(count=1)


def game_update():
    """Main update loop — called every frame."""
    global game

    if game.game_over:
        # Check for restart
        if held_keys['r']:
            for e in scene.entities[:]:
                destroy(e)
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
        # Brief scale pulse on player
        p.scale = 1.8
        invoke(setattr, p, 'scale', 1.2, delay=0.3)
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

        # Skip AI updates for very distant enemies (performance)
        if dist_to_player < ENEMY_DETECT_RANGE:
            # Chase player
            direction = (p.position - enemy.position).normalized()
            direction.y = 0
            new_pos = enemy.position + direction * enemy.speed * time.dt
            if game._is_walkable(new_pos.x, new_pos.z):
                enemy.position = new_pos
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
                        speed=18,
                    )
                    game.enemy_projectiles.append(ep)
                    game._spawn_particles(enemy.position, color.rgb(200, 100, 0), count=4)
                    enemy.spit_timer = random.uniform(2.5, 4.5)
        else:
            # Wander
            enemy.wander_timer -= time.dt
            if enemy.wander_timer <= 0:
                enemy.wander_dir = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
                enemy.wander_timer = random.uniform(ENEMY_WANDER_INTERVAL_MIN, ENEMY_WANDER_INTERVAL_MAX)
            new_pos = enemy.position + enemy.wander_dir * enemy.speed * ENEMY_WANDER_SPEED_FACTOR * time.dt
            if game._is_walkable(new_pos.x, new_pos.z):
                enemy.position = new_pos
            else:
                enemy.wander_dir = -enemy.wander_dir

        # Attack player (shield blocks damage)
        if dist_to_player < ENEMY_ATTACK_RANGE:
            if enemy.attack_cd <= 0:
                if p.shield_timer > 0:
                    # Shield absorbs the hit
                    game._spawn_particles(p.position + Vec3(0, 1, 0), color.rgb(100, 200, 255), count=10)
                    game.add_message("Shield blocked!")
                else:
                    died = p.take_damage(enemy.damage)
                    game.screen_shake = SCREEN_SHAKE_DAMAGE
                    game._spawn_particles(p.position, color.red, count=PARTICLE_DAMAGE_COUNT)
                    if died:
                        game.game_over = True
                        game.game_over_text.visible = True
                        game.game_over_text.text = 'GAME OVER'
                        game.game_over_sub.visible = True
                        game.game_over_sub.text = f'Score: {p.score}  Level: {p.level}'
                        # Build detailed death stats
                        total_kills = sum(p.kills.values())
                        total_items = sum(p.inventory.values())
                        time_alive = int(game.t)
                        minutes = time_alive // 60
                        seconds = time_alive % 60
                        kill_details = '  '.join(f'{k}:{v}' for k, v in p.kills.items()) if p.kills else 'None'
                        stats_lines = [
                            f'Time Survived: {minutes}m {seconds}s',
                            f'Total Kills: {total_kills}   Items Collected: {total_items}',
                            f'Missions Completed: {p.completed_missions}',
                            f'Enemies Defeated: {kill_details}',
                        ]
                        game.game_over_stats.visible = True
                        game.game_over_stats.text = '\n'.join(stats_lines)
                        game.game_over_restart.visible = True
                        game.game_over_restart.text = 'Press R to Restart'
                enemy.attack_cd = ENEMY_ATTACK_COOLDOWN
        else:
            enemy.attack_cd = max(0, enemy.attack_cd - time.dt)

        # Float enemies
        enemy.y = 1 + math.sin(game.t * 2 + id(enemy) % 100) * 0.2
        enemy.update_hp_bar()

    # ── Update Projectiles ──
    for proj in game.projectiles[:]:
        alive = proj.move(time.dt)
        if not alive:
            destroy(proj)
            game.projectiles.remove(proj)
            continue

        # Check collision with enemies
        for enemy in game.enemies:
            if not enemy.alive or enemy.dying:
                continue
            if (proj.position - enemy.position).length() < enemy.scale_x + 0.5:
                killed = enemy.take_damage(proj.damage)
                game._spawn_particles(enemy.position, color.yellow, count=PARTICLE_HIT_COUNT)
                game.screen_shake = max(game.screen_shake, 0.15)
                # Floating damage number
                game.damage_numbers.append(DamageNumber(enemy.position, proj.damage, is_kill=False))
                destroy(proj)
                if proj in game.projectiles:
                    game.projectiles.remove(proj)
                if killed:
                    p.add_kill(enemy.name)
                    xp_gain = BASE_KILL_XP + enemy.max_hp // KILL_XP_HP_DIVISOR
                    p.gain_xp(xp_gain)
                    p.score += enemy.max_hp
                    game.screen_shake = SCREEN_SHAKE_KILL
                    # Kill damage number (bigger, yellow)
                    game.damage_numbers.append(DamageNumber(enemy.position, proj.damage, is_kill=True))
                    # Drop loot
                    for _ in range(random.randint(LOOT_DROP_MIN, LOOT_DROP_MAX)):
                        offset = Vec3(random.uniform(-3, 3), 1.5, random.uniform(-3, 3))
                        c = Collectible(position=enemy.position + offset)
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
                    game.game_over = True
                    game.game_over_text.visible = True
                    game.game_over_text.text = 'GAME OVER'
                    game.game_over_sub.visible = True
                    game.game_over_sub.text = f'Score: {p.score}  Level: {p.level}'
                    total_kills = sum(p.kills.values())
                    total_items = sum(p.inventory.values())
                    time_alive = int(game.t)
                    minutes = time_alive // 60
                    seconds = time_alive % 60
                    kill_details = '  '.join(f'{k}:{v}' for k, v in p.kills.items()) if p.kills else 'None'
                    stats_lines = [
                        f'Time Survived: {minutes}m {seconds}s',
                        f'Total Kills: {total_kills}   Items Collected: {total_items}',
                        f'Missions Completed: {p.completed_missions}',
                        f'Enemies Defeated: {kill_details}',
                    ]
                    game.game_over_stats.visible = True
                    game.game_over_stats.text = '\n'.join(stats_lines)
                    game.game_over_restart.visible = True
                    game.game_over_restart.text = 'Press R to Restart'
            destroy(eproj)
            game.enemy_projectiles.remove(eproj)
            continue
        # Remove if out of world
        if eproj.x < -10 or eproj.x > WORLD_SIZE * TILE_SCALE + 10 or eproj.z < -10 or eproj.z > WORLD_SIZE * TILE_SCALE + 10:
            destroy(eproj)
            game.enemy_projectiles.remove(eproj)

    # ── Update Collectibles ──
    for col in game.collectibles[:]:
        col.animate(game.t)
        dist = (col.position - p.position).length()
        # Magnetic pull: items are drawn toward player when close
        if dist < COLLECT_PULL_RADIUS and dist > 0.1:
            pull_dir = (p.position - col.position).normalized()
            pull_strength = 1.0 - (dist / COLLECT_PULL_RADIUS)  # stronger when closer
            col.position += pull_dir * COLLECT_PULL_SPEED * pull_strength * time.dt
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
            else:
                p.add_item(col.name)
                p.score += col.value
                p.gain_xp(col.value // 10)
                game._spawn_collect_burst(col.position, col.item_color)
                game.add_message(f"Found {col.name}! +{col.value} pts")
            # For power-ups, also give points
            if col.name in ('Health Potion', 'Speed Boost', 'Shield Crystal'):
                p.score += col.value
                p.gain_xp(col.value // 10)
            destroy(col.glow)
            destroy(col)
            game.collectibles.remove(col)

    # ── Update Particles ──
    for item in game.particles[:]:
        p_ent, vel, lifetime = item
        p_ent.position += vel * time.dt
        vel = Vec3(vel.x, vel.y - PARTICLE_GRAVITY * time.dt, vel.z)
        lifetime -= time.dt
        p_ent.scale *= PARTICLE_SCALE_DECAY
        if lifetime <= 0:
            destroy(p_ent)
            game.particles.remove(item)

    # ── Update Damage Numbers ──
    for dmg_num in game.damage_numbers[:]:
        if dmg_num.update(time.dt):
            dmg_num.destroy()
            game.damage_numbers.remove(dmg_num)

    # ── Spawn Timer ──
    game.spawn_timer += time.dt
    if game.spawn_timer >= ENEMY_SPAWN_INTERVAL:
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
        game._m_held = True
    elif not held_keys['m']:
        game._m_held = False

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
    if key == 'p' and not game.game_over:
        game.paused = not game.paused

app.update = game_update
app.run()