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

# ─── Constants ────────────────────────────────────────────────────────────────
VERSION = "2.0.0"
WORLD_SIZE = 80        # world grid dimensions (tiles)
TILE_SCALE = 4         # size of each terrain tile
PLAYER_SPEED = 12
ENEMY_DETECT_RANGE = 40
ENEMY_ATTACK_RANGE = 2.5
SHOOT_COOLDOWN = 0.15
COLLECT_RADIUS = 2.5

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

BIOME_COLORS = {
    'grass':   C_GRASS,
    'desert':  C_DESERT,
    'water':   C_WATER,
    'lava':    C_LAVA,
    'forest':  C_FOREST,
    'crystal': C_CRYSTAL,
    'snow':    C_SNOW,
    'swamp':   C_SWAMP,
}

WALKABLE = {'grass', 'desert', 'forest', 'crystal', 'snow', 'swamp'}

# ─── World Generation ─────────────────────────────────────────────────────────
class WorldGenerator:
    """Procedural terrain generation for a 3D open world."""

    @staticmethod
    def generate(size, seed=None):
        if seed is not None:
            random.seed(seed)
        grid = [['grass' for _ in range(size)] for _ in range(size)]

        # Place biome blobs
        biomes = ['desert', 'water', 'lava', 'forest', 'crystal', 'snow', 'swamp']
        num_blobs = 50
        for _ in range(num_blobs):
            bx = random.randint(0, size - 1)
            by = random.randint(0, size - 1)
            btype = random.choice(biomes)
            radius = random.randint(3, 10)
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = bx + dx, by + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist <= radius + random.uniform(-1.5, 1.5):
                            # Keep spawn area clear
                            spawn = size // 2
                            if abs(nx - spawn) < 5 and abs(ny - spawn) < 5:
                                continue
                            grid[ny][nx] = btype

        # Ensure spawn area is grass
        spawn = size // 2
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                grid[spawn + dy][spawn + dx] = 'grass'

        return grid


# ─── Player ───────────────────────────────────────────────────────────────────
class Player(Entity):
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=C_ALIEN,
            scale=1.2,
            position=position,
            collider='sphere',
        )
        self.hp = 100
        self.max_hp = 100
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

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.5)
            self.max_hp += 10
            self.hp = min(self.hp + 20, self.max_hp)
            self.speed += 0.3

    def take_damage(self, amount):
        if self.invuln_timer > 0:
            return False
        self.hp -= amount
        self.invuln_timer = 0.5
        # Flash red
        self.color = color.rgb(255, 100, 100)
        invoke(setattr, self, 'color', C_ALIEN, delay=0.15)
        if self.hp <= 0:
            self.hp = 0
            return True  # dead
        return False

    def add_item(self, name, count=1):
        self.inventory[name] = self.inventory.get(name, 0) + count

    def add_kill(self, name):
        self.kills[name] = self.kills.get(name, 0) + 1

    def update_tentacles(self, t):
        for i, tent in enumerate(self.tentacles):
            angle_offset = (i - 1.5) * 0.5
            wave = math.sin(t * 5 + i * 1.5) * 0.3
            tent.rotation_x = wave * 40
            tent.rotation_y = angle_offset * 30 + math.sin(t * 3 + i) * 10

    def animate_bob(self, t):
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
    TYPES = {
        'Slime Blob':      {'color': color.lime,         'hp': 30,  'speed': 3,  'damage': 10, 'scale': 1.0},
        'Space Beetle':    {'color': color.brown,         'hp': 50,  'speed': 5,  'damage': 15, 'scale': 1.2},
        'Void Wraith':     {'color': color.violet,        'hp': 80,  'speed': 4,  'damage': 25, 'scale': 1.4},
        'Lava Crawler':    {'color': color.orange,         'hp': 120, 'speed': 6,  'damage': 30, 'scale': 1.1},
        'Crystal Guardian': {'color': color.cyan,          'hp': 200, 'speed': 3,  'damage': 40, 'scale': 1.8},
        'Plasma Drake':    {'color': color.magenta,        'hp': 350, 'speed': 7,  'damage': 50, 'scale': 2.2},
    }

    def __init__(self, position, enemy_type=None):
        if enemy_type is None:
            enemy_type = random.choice(list(self.TYPES.keys()))
        info = self.TYPES[enemy_type]
        super().__init__(
            model='sphere',
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
        self.attack_cd = 0
        self.wander_dir = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        self.wander_timer = random.uniform(1, 3)
        self.hit_flash = 0

        # Eyes for all enemies
        self.eye_l = Entity(model='sphere', color=color.red, scale=0.3, parent=self, position=(-0.25, 0.3, -0.5))
        self.eye_r = Entity(model='sphere', color=color.red, scale=0.3, parent=self, position=(0.25, 0.3, -0.5))

        # HP bar
        self.hp_bar_bg = Entity(model='quad', color=color.red, scale=(2, 0.15), parent=self, position=(0, 1.5, 0), billboard=True)
        self.hp_bar = Entity(model='quad', color=color.green, scale=(2, 0.15), parent=self, position=(0, 1.5, -0.01), billboard=True)

    def take_damage(self, amount):
        self.hp -= amount
        self.hit_flash = 0.1
        self.color = color.white
        invoke(setattr, self, 'color', self.TYPES[self.name]['color'], delay=0.1)
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def update_hp_bar(self):
        ratio = max(0, self.hp / self.max_hp)
        self.hp_bar.scale_x = 2 * ratio
        self.hp_bar.x = -1 * (1 - ratio)


# ─── Collectible ───────────────────────────────────────────────────────────────
class Collectible(Entity):
    ITEMS = {
        'Space Gloop':    {'color': C_PURPLE, 'value': 10,  'model': 'sphere'},
        'Meteor Shard':   {'color': color.orange, 'value': 25,  'model': 'diamond'},
        'Quantum Fuzz':   {'color': color.cyan,   'value': 50,  'model': 'sphere'},
        'Nebula Dust':    {'color': C_PINK,       'value': 100, 'model': 'diamond'},
        'Cosmic Jelly':   {'color': C_GOLD,       'value': 200, 'model': 'diamond'},
        'Plasma Core':    {'color': color.magenta, 'value': 350, 'model': 'diamond'},
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
        # Glow ring
        self.glow = Entity(model='quad', color=color.rgba(info['color'].r, info['color'].g, info['color'].b, 80),
                           scale=3, parent=self, rotation_x=90, position=(0, -0.3, 0))

    def animate(self, t):
        self.y = 1.0 + math.sin(t * 2 + self.bob_offset) * 0.4
        self.rotation_y += 60 * time.dt


# ─── Projectile ────────────────────────────────────────────────────────────────
class Projectile(Entity):
    def __init__(self, position, direction, damage=20, speed=50):
        super().__init__(
            model='sphere',
            color=C_LASER,
            scale=0.3,
            position=position,
        )
        self.direction = direction.normalized()
        self.damage = damage
        self.speed = speed
        self.lifetime = 2.0

        # Trail
        self.trail = []

    def move(self, dt):
        self.position += self.direction * self.speed * dt
        self.lifetime -= dt
        return self.lifetime > 0


# ─── Mission ───────────────────────────────────────────────────────────────────
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
    def __init__(self):
        self.seed = random.randint(0, 999999)
        self.world_grid = WorldGenerator.generate(WORLD_SIZE, self.seed)
        self.terrain_entities = []
        self.tree_entities = []
        self.crystal_entities = []
        self.enemies = []
        self.collectibles = []
        self.projectiles = []
        self.particles = []
        self.missions = []
        self.messages = []
        self.game_over = False
        self.paused = False
        self.t = 0
        self.spawn_timer = 0
        self.mission_timer = 0

        # Build terrain
        self._build_terrain()

        # Player
        spawn = Vec3(WORLD_SIZE // 2 * TILE_SCALE, 2, WORLD_SIZE // 2 * TILE_SCALE)
        self.player = Player(position=spawn)

        # Camera rig: third-person camera
        self.cam_pivot = Entity(position=spawn)
        camera.parent = self.cam_pivot
        camera.position = (0, 18, -22)
        camera.rotation = (30, 0, 0)

        # Populate world
        self._spawn_initial_entities()
        self._assign_missions(count=3)

        # Lighting
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1, -1, 1))
        AmbientLight(color=color.rgba(100, 100, 100, 255))

        # Sky
        Sky(color=color.rgb(40, 0, 80))

        # Fog for atmosphere
        scene.fog_color = color.rgb(40, 0, 80)
        scene.fog_density = 0.008

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

    def _is_walkable(self, world_x, world_z):
        """Check if a world position is on walkable terrain."""
        tx = int(world_x / TILE_SCALE)
        tz = int(world_z / TILE_SCALE)
        if 0 <= tx < WORLD_SIZE and 0 <= tz < WORLD_SIZE:
            return self.world_grid[tz][tx] in WALKABLE
        return False

    def _spawn_initial_entities(self):
        spawn_x = WORLD_SIZE // 2 * TILE_SCALE
        spawn_z = WORLD_SIZE // 2 * TILE_SCALE

        # Spawn collectibles
        for _ in range(200):
            x = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            z = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            if self._is_walkable(x, z):
                dist = math.sqrt((x - spawn_x) ** 2 + (z - spawn_z) ** 2)
                if dist > 15:
                    c = Collectible(position=Vec3(x, 1, z))
                    self.collectibles.append(c)

        # Spawn enemies
        for _ in range(60):
            x = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            z = random.uniform(2, (WORLD_SIZE - 2) * TILE_SCALE)
            if self._is_walkable(x, z):
                dist = math.sqrt((x - spawn_x) ** 2 + (z - spawn_z) ** 2)
                if dist > 30:
                    e = Enemy(position=Vec3(x, 1, z))
                    self.enemies.append(e)

    def _assign_missions(self, count=1):
        templates = list(MISSION_TEMPLATES)
        random.shuffle(templates)
        for template in templates[:count]:
            m = Mission(template[0], template[1], template[2], template[5], template[4], template[3])
            self.missions.append(m)
            self.add_message(f"New Mission: {m.title}")

    def add_message(self, msg):
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
            text='WASD:Move | Click:Shoot | M:Minimap | Tab:Missions | P:Pause',
            position=(0, -0.47), origin=(0, 0), scale=0.8, color=color.gray
        )
        self.version_text = Text(text=f'v{VERSION}', position=(0.88, -0.47), scale=0.7, color=color.gray)
        self.game_over_text = Text(text='', position=(0, 0.05), origin=(0, 0), scale=4, color=color.red, visible=False)
        self.game_over_sub = Text(text='', position=(0, -0.08), origin=(0, 0), scale=2, color=color.white, visible=False)
        self.game_over_restart = Text(text='', position=(0, -0.15), origin=(0, 0), scale=1.5, color=color.yellow, visible=False)

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
        # Simplified: just set base color, overlay will be drawn in update
        pass

    def _spawn_particles(self, pos, col, count=8):
        for _ in range(count):
            vel = Vec3(random.uniform(-3, 3), random.uniform(1, 5), random.uniform(-3, 3))
            p = Entity(model='sphere', color=col, scale=random.uniform(0.1, 0.3),
                       position=pos)
            self.particles.append((p, vel, random.uniform(0.5, 1.5)))

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
            damage=20 + self.player.level * 2,
            speed=50,
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
        self.hp_text.text = f'HP: {p.hp}/{p.max_hp}'

        # XP bar
        xp_ratio = p.xp / p.xp_to_next if p.xp_to_next > 0 else 0
        self.xp_bar.scale_x = 0.4 * xp_ratio
        self.xp_bar.x = -0.55 - 0.2 * (1 - xp_ratio)

        self.level_text.text = f'Lv.{p.level}'
        self.score_text.text = f'Score: {p.score}'

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

    def _update_missions(self):
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

    if move_dir.length() > 0:
        move_dir = move_dir.normalized()
        new_pos = p.position + move_dir * p.speed * time.dt
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
        p.visible = int(game.t * 20) % 2 == 0
    else:
        p.visible = True

    # Shoot cooldown
    if p.shoot_timer > 0:
        p.shoot_timer -= time.dt

    # Shooting
    if mouse.left and not game.game_over:
        game.shoot()

    # ── Camera Follow ──
    game.cam_pivot.position = lerp(game.cam_pivot.position, p.position + Vec3(0, 0, 0), time.dt * 5)

    # ── Update Enemies ──
    for enemy in game.enemies[:]:
        if not enemy.alive:
            destroy(enemy)
            destroy(enemy.eye_l)
            destroy(enemy.eye_r)
            destroy(enemy.hp_bar_bg)
            destroy(enemy.hp_bar)
            game.enemies.remove(enemy)
            continue

        dist_to_player = (enemy.position - p.position).length()

        if dist_to_player < ENEMY_DETECT_RANGE:
            # Chase player
            direction = (p.position - enemy.position).normalized()
            direction.y = 0
            new_pos = enemy.position + direction * enemy.speed * time.dt
            if game._is_walkable(new_pos.x, new_pos.z):
                enemy.position = new_pos
            enemy.look_at_2d(p.position)
        else:
            # Wander
            enemy.wander_timer -= time.dt
            if enemy.wander_timer <= 0:
                enemy.wander_dir = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
                enemy.wander_timer = random.uniform(2, 5)
            new_pos = enemy.position + enemy.wander_dir * enemy.speed * 0.3 * time.dt
            if game._is_walkable(new_pos.x, new_pos.z):
                enemy.position = new_pos
            else:
                enemy.wander_dir = -enemy.wander_dir

        # Attack player
        if dist_to_player < ENEMY_ATTACK_RANGE:
            if enemy.attack_cd <= 0:
                died = p.take_damage(enemy.damage)
                game._spawn_particles(p.position, color.red, count=6)
                enemy.attack_cd = 1.0
                if died:
                    game.game_over = True
                    game.game_over_text.visible = True
                    game.game_over_text.text = 'GAME OVER'
                    game.game_over_sub.visible = True
                    game.game_over_sub.text = f'Score: {p.score}  Level: {p.level}'
                    game.game_over_restart.visible = True
                    game.game_over_restart.text = 'Press R to Restart'
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
            if not enemy.alive:
                continue
            if (proj.position - enemy.position).length() < enemy.scale_x + 0.5:
                killed = enemy.take_damage(proj.damage)
                game._spawn_particles(enemy.position, color.yellow, count=10)
                destroy(proj)
                if proj in game.projectiles:
                    game.projectiles.remove(proj)
                if killed:
                    p.add_kill(enemy.name)
                    p.gain_xp(25 + enemy.max_hp // 10)
                    p.score += enemy.max_hp
                    # Drop loot
                    for _ in range(random.randint(1, 3)):
                        offset = Vec3(random.uniform(-3, 3), 1.5, random.uniform(-3, 3))
                        c = Collectible(position=enemy.position + offset)
                        game.collectibles.append(c)
                    game.add_message(f"Defeated {enemy.name}!")
                break

        # Remove if out of world
        if proj.x < -10 or proj.x > WORLD_SIZE * TILE_SCALE + 10 or proj.z < -10 or proj.z > WORLD_SIZE * TILE_SCALE + 10:
            destroy(proj)
            if proj in game.projectiles:
                game.projectiles.remove(proj)

    # ── Update Collectibles ──
    for col in game.collectibles[:]:
        col.animate(game.t)
        dist = (col.position - p.position).length()
        if dist < COLLECT_RADIUS:
            p.add_item(col.name)
            p.score += col.value
            p.gain_xp(col.value // 10)
            game._spawn_particles(col.position, col.color, count=6)
            game.add_message(f"Found {col.name}! +{col.value} pts")
            destroy(col.glow)
            destroy(col)
            game.collectibles.remove(col)

    # ── Update Particles ──
    for item in game.particles[:]:
        p_ent, vel, lifetime = item
        p_ent.position += vel * time.dt
        vel.y -= 9.8 * time.dt
        lifetime -= time.dt
        p_ent.scale *= 0.97
        if lifetime <= 0:
            destroy(p_ent)
            game.particles.remove(item)

    # ── Spawn Timer ──
    game.spawn_timer += time.dt
    if game.spawn_timer >= 10:
        game.spawn_timer = 0
        alive = len([e for e in game.enemies if e.alive])
        if alive < 40:
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(30, 60)
            ex = p.x + math.cos(angle) * dist
            ez = p.z + math.sin(angle) * dist
            ex = max(5, min(ex, (WORLD_SIZE - 5) * TILE_SCALE))
            ez = max(5, min(ez, (WORLD_SIZE - 5) * TILE_SCALE))
            if game._is_walkable(ex, ez):
                e = Enemy(position=Vec3(ex, 1, ez))
                game.enemies.append(e)

    # Respawn collectibles
    if len(game.collectibles) < 120 and random.random() < 0.01:
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