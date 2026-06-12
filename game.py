"""
Zorp Wiggles: Alien Adventure
An open-world game where you play as Zorp, a squishy alien,
running around collecting weird stuff, completing missions, and blasting enemies.
"""

import pygame
import random
import math
import sys
import json
import os

# ─── Constants ────────────────────────────────────────────────────────────────
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 64
WORLD_WIDTH = 200  # tiles
WORLD_HEIGHT = 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
BROWN = (139, 69, 19)
SAND = (210, 180, 140)
WATER_BLUE = (30, 144, 255)
LAVA_RED = (207, 16, 32)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Biome types
BIOME_GRASS = 0
BIOME_DESERT = 1
BIOME_WATER = 2
BIOME_LAVA = 3
BIOME_FOREST = 4
BIOME_CRYSTAL = 5

# ─── World Generation ────────────────────────────────────────────────────────
class WorldGenerator:
    """Procedural world generation using simple noise."""

    @staticmethod
    def generate(width, height, seed=None):
        if seed is not None:
            random.seed(seed)
        world = [[BIOME_GRASS for _ in range(width)] for _ in range(height)]
        # Place biome regions using random walk clusters
        biome_centers = []
        num_biomes = 40
        for _ in range(num_biomes):
            bx = random.randint(0, width - 1)
            by = random.randint(0, height - 1)
            btype = random.choice([BIOME_GRASS, BIOME_DESERT, BIOME_WATER,
                                   BIOME_LAVA, BIOME_FOREST, BIOME_CRYSTAL])
            biome_centers.append((bx, by, btype))
            radius = random.randint(5, 20)
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = bx + dx, by + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist <= radius + random.randint(-2, 2):
                            if btype == BIOME_WATER or world[ny][nx] != BIOME_WATER:
                                if not (0 <= nx < 5 or 0 <= ny < 5 or nx >= width - 5 or ny >= height - 5):
                                    world[ny][nx] = btype
        # Ensure spawn area is grass
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                world[100 + dy][100 + dx] = BIOME_GRASS
        return world

    @staticmethod
    def get_tile_color(biome):
        return {
            BIOME_GRASS: GREEN,
            BIOME_DESERT: SAND,
            BIOME_WATER: WATER_BLUE,
            BIOME_LAVA: LAVA_RED,
            BIOME_FOREST: DARK_GREEN,
            BIOME_CRYSTAL: CYAN,
        }.get(biome, GREEN)

    @staticmethod
    def is_walkable(biome):
        return biome not in (BIOME_WATER, BIOME_LAVA)


# ─── Entities ─────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, vx=0, vy=0, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx + random.uniform(-1, 1)
        self.vy = vy + random.uniform(-1, 1)
        self.x = float(self.x)
        self.y = float(self.y)
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface, cam_x, cam_y):
        alpha = self.lifetime / self.max_lifetime
        size = max(2, int(6 * alpha))
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        if 0 <= sx < SCREEN_WIDTH and 0 <= sy < SCREEN_HEIGHT:
            pygame.draw.circle(surface, self.color, (sx, sy), size)


class Collectible:
    TYPES = [
        ("Space Gloop", PURPLE, 10),
        ("Meteor Shard", ORANGE, 25),
        ("Quantum Fuzz", CYAN, 50),
        ("Nebula Dust", PINK, 100),
        ("Cosmic Jelly", YELLOW, 200),
    ]

    def __init__(self, x, y, item_type=None):
        if item_type is None:
            item_type = random.choice(self.TYPES)
        self.name, self.color, self.value = item_type
        self.x = x
        self.y = y
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.collected = False
        self.radius = 10

    def update(self, tick):
        pass

    def draw(self, surface, cam_x, cam_y, tick):
        if self.collected:
            return
        bob = math.sin(tick * 0.05 + self.bob_offset) * 4
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y + bob)
        if -20 < sx < SCREEN_WIDTH + 20 and -20 < sy < SCREEN_HEIGHT + 20:
            # Glow
            glow_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color, 80), (15, 15), 15)
            surface.blit(glow_surf, (sx - 15, sy - 15))
            pygame.draw.circle(surface, self.color, (sx, sy), self.radius)
            pygame.draw.circle(surface, WHITE, (sx, sy), self.radius, 2)
            # Sparkle
            angle = tick * 0.1 + self.bob_offset
            for i in range(3):
                a = angle + i * 2.094
                px = sx + int(math.cos(a) * 14)
                py = sy + int(math.sin(a) * 14)
                pygame.draw.circle(surface, WHITE, (px, py), 2)


class Enemy:
    TYPES = [
        ("Slime Blob", GREEN, 30, 1.5, 15),
        ("Space Beetle", BROWN, 50, 2.0, 20),
        ("Void Wraith", PURPLE, 80, 1.0, 30),
        ("Lava Crawler", ORANGE, 120, 2.5, 35),
        ("Crystal Guardian", CYAN, 200, 1.2, 50),
    ]

    def __init__(self, x, y, enemy_type=None):
        if enemy_type is None:
            enemy_type = random.choice(self.TYPES)
        self.name, self.color, self.hp, self.speed, self.damage = enemy_type
        self.max_hp = self.hp
        self.x = x
        self.y = y
        self.radius = 18
        self.alive = True
        self.hit_flash = 0
        self.attack_cooldown = 0
        self.direction = random.uniform(0, math.pi * 2)
        self.wander_timer = random.randint(30, 120)

    def update(self, player_x, player_y, world):
        if not self.alive:
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        dist_to_player = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)

        if dist_to_player < 400:
            # Chase player
            dx = player_x - self.x
            dy = player_y - self.y
            dist = max(1, math.sqrt(dx * dx + dy * dy))
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        else:
            # Wander
            self.wander_timer -= 1
            if self.wander_timer <= 0:
                self.direction = random.uniform(0, math.pi * 2)
                self.wander_timer = random.randint(30, 120)
            self.x += math.cos(self.direction) * self.speed * 0.5
            self.y += math.sin(self.direction) * self.speed * 0.5

        # Keep in world bounds
        self.x = max(0, min(self.x, WORLD_WIDTH * TILE_SIZE - 10))
        self.y = max(0, min(self.y, WORLD_HEIGHT * TILE_SIZE - 10))

    def take_damage(self, amount):
        self.hp -= amount
        self.hit_flash = 8
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def can_attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 60
            return True
        return False

    def draw(self, surface, cam_x, cam_y, tick):
        if not self.alive:
            return
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        if -30 < sx < SCREEN_WIDTH + 30 and -30 < sy < SCREEN_HEIGHT + 30:
            color = WHITE if self.hit_flash > 0 else self.color
            # Body
            pygame.draw.circle(surface, color, (sx, sy), self.radius)
            pygame.draw.circle(surface, WHITE, (sx, sy), self.radius, 2)
            # Eyes
            eye_offset_x = int(math.cos(0) * 6)
            pygame.draw.circle(surface, RED, (sx - 5, sy - 4), 4)
            pygame.draw.circle(surface, RED, (sx + 5, sy - 4), 4)
            pygame.draw.circle(surface, WHITE, (sx - 4, sy - 5), 2)
            pygame.draw.circle(surface, WHITE, (sx + 6, sy - 5), 2)
            # HP bar
            bar_w = 30
            bar_h = 4
            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, RED, (sx - bar_w // 2, sy - self.radius - 10, bar_w, bar_h))
            pygame.draw.rect(surface, GREEN, (sx - bar_w // 2, sy - self.radius - 10, int(bar_w * hp_ratio), bar_h))


class Projectile:
    def __init__(self, x, y, angle, speed=10, damage=20, color=CYAN, owner="player"):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.damage = damage
        self.color = color
        self.owner = owner
        self.lifetime = 120
        self.radius = 5

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface, cam_x, cam_y):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        if 0 <= sx < SCREEN_WIDTH and 0 <= sy < SCREEN_HEIGHT:
            pygame.draw.circle(surface, self.color, (sx, sy), self.radius)
            pygame.draw.circle(surface, WHITE, (sx, sy), self.radius, 1)


# ─── Missions ──────────────────────────────────────────────────────────────────
class Mission:
    def __init__(self, title, description, target, reward, mission_type="collect", target_count=1):
        self.title = title
        self.description = description
        self.target = target
        self.reward = reward
        self.mission_type = mission_type
        self.target_count = target_count
        self.progress = 0
        self.completed = False
        self.turned_in = False

    def check_completion(self, player):
        if self.completed:
            return
        if self.mission_type == "collect":
            self.progress = player.inventory.get(self.target, 0)
            if self.progress >= self.target_count:
                self.completed = True
        elif self.mission_type == "kill":
            self.progress = player.kills.get(self.target, 0)
            if self.progress >= self.target_count:
                self.completed = True
        elif self.mission_type == "explore":
            self.progress = 1 if getattr(player, self.target, False) else 0
            if self.progress >= self.target_count:
                self.completed = True


MISSION_TEMPLATES = [
    ("Gloop Harvest", "Collect Space Gloop for the Mothership", "Space Gloop", 5, "collect", 100),
    ("Beetle B Gone", "Defeat Space Beetles invading the sector", "Space Beetle", 3, "kill", 200),
    ("Shard Collection", "Gather Meteor Shards for the Lab", "Meteor Shard", 5, "collect", 150),
    ("Wraith Hunter", "Eliminate Void Wraiths from the dark zones", "Void Wraith", 2, "kill", 300),
    ("Fuzz Finder", "Find Quantum Fuzz in the wild", "Quantum Fuzz", 3, "collect", 250),
    ("Jelly Jam", "Collect Cosmic Jelly — it's delicious", "Cosmic Jelly", 2, "collect", 400),
    ("Crawler Crisis", "Take out Lava Crawlers near volcanic zones", "Lava Crawler", 3, "kill", 350),
    ("Crystal Clear", "Defeat Crystal Guardians in crystal biomes", "Crystal Guardian", 2, "kill", 500),
]


# ─── Player ───────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4.0
        self.hp = 100
        self.max_hp = 100
        self.radius = 16
        self.inventory = {}
        self.kills = {}
        self.score = 0
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.shoot_cooldown = 0
        self.invincible_timer = 0
        self.facing_angle = 0
        self.tentacle_anim = 0
        self.missions = []
        self.completed_missions = 0

    def add_item(self, name, count=1):
        self.inventory[name] = self.inventory.get(name, 0) + count

    def add_kill(self, name):
        self.kills[name] = self.kills.get(name, 0) + 1

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.5)
            self.max_hp += 10
            self.hp = min(self.hp + 20, self.max_hp)
            self.speed += 0.1

    def take_damage(self, amount):
        if self.invincible_timer > 0:
            return False
        self.hp -= amount
        self.invincible_timer = 30
        if self.hp <= 0:
            self.hp = 0
            return True  # Dead
        return False

    def update(self, keys, world):
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        # Diagonal normalization
        if dx != 0 and dy != 0:
            factor = self.speed / math.sqrt(dx * dx + dy * dy)
            dx *= factor
            dy *= factor

        if dx != 0 or dy != 0:
            self.facing_angle = math.atan2(dy, dx)

        # Try move with collision
        new_x = self.x + dx
        new_y = self.y + dy
        tile_x = int(new_x // TILE_SIZE)
        tile_y = int(new_y // TILE_SIZE)
        if 0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT:
            if WorldGenerator.is_walkable(world[tile_y][tile_x]):
                self.x = max(self.radius, min(new_x, WORLD_WIDTH * TILE_SIZE - self.radius))
                self.y = max(self.radius, min(new_y, WORLD_HEIGHT * TILE_SIZE - self.radius))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        self.tentacle_anim += 1

    def draw(self, surface, cam_x, cam_y, tick):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)

        if self.invincible_timer > 0 and self.invincible_timer % 4 < 2:
            return  # Blink when invincible

        # Glow aura
        glow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (0, 255, 100, 40), (40, 40), 35)
        surface.blit(glow_surf, (sx - 40, sy - 40))

        # Tentacles (4 wiggly)
        for i in range(4):
            angle = self.facing_angle + (i - 1.5) * 0.4
            wave = math.sin(tick * 0.15 + i * 1.5) * 6
            tx = sx + int(math.cos(angle) * (20 + wave))
            ty = sy + int(math.sin(angle) * (20 + wave))
            pygame.draw.line(surface, GREEN, (sx, sy), (tx, ty), 3)
            pygame.draw.circle(surface, (0, 255, 150), (tx, ty), 4)

        # Body
        body_pulse = math.sin(tick * 0.08) * 2
        pygame.draw.circle(surface, (0, 220, 0), (sx, sy), int(self.radius + body_pulse))
        pygame.draw.circle(surface, (0, 255, 100), (sx, sy), int(self.radius + body_pulse), 2)

        # Eyes (big alien eyes)
        eye_angle = self.facing_angle
        ex1 = sx + int(math.cos(eye_angle - 0.4) * 7)
        ey1 = sy + int(math.sin(eye_angle - 0.4) * 7)
        ex2 = sx + int(math.cos(eye_angle + 0.4) * 7)
        ey2 = sy + int(math.sin(eye_angle + 0.4) * 7)
        pygame.draw.circle(surface, WHITE, (ex1, ey1), 6)
        pygame.draw.circle(surface, WHITE, (ex2, ey2), 6)
        # Pupils
        px = int(math.cos(eye_angle) * 2)
        py = int(math.sin(eye_angle) * 2)
        pygame.draw.circle(surface, BLACK, (ex1 + px, ey1 + py), 3)
        pygame.draw.circle(surface, BLACK, (ex2 + px, ey2 + py), 3)

        # Mouth
        mouth_x = sx + int(math.cos(eye_angle) * 10)
        mouth_y = sy + int(math.sin(eye_angle) * 10)
        pygame.draw.circle(surface, (0, 100, 0), (mouth_x, mouth_y), 3)


# ─── Main Game ────────────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zorp Wiggles: Alien Adventure v1.0")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self.big_font = pygame.font.SysFont("monospace", 24, bold=True)
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)

        # World
        self.seed = random.randint(0, 999999)
        self.world = WorldGenerator.generate(WORLD_WIDTH, WORLD_HEIGHT, self.seed)

        # Player
        spawn_x = 100 * TILE_SIZE + TILE_SIZE // 2
        spawn_y = 100 * TILE_SIZE + TILE_SIZE // 2
        self.player = Player(spawn_x, spawn_y)

        # Entities
        self.enemies = []
        self.collectibles = []
        self.projectiles = []
        self.particles = []
        self.missions = []

        # Populate
        self._spawn_initial_entities()

        # Camera
        self.cam_x = spawn_x - SCREEN_WIDTH // 2
        self.cam_y = spawn_y - SCREEN_HEIGHT // 2

        # Game state
        self.tick = 0
        self.show_minimap = True
        self.show_missions = False
        self.game_over = False
        self.paused = False
        self.message_log = []
        self.spawn_timer = 0

        # Version tracking
        self.version = "1.0.0"

    def _spawn_initial_entities(self):
        # Spawn collectibles
        for _ in range(150):
            x = random.randint(5, WORLD_WIDTH * TILE_SIZE - 5)
            y = random.randint(5, WORLD_HEIGHT * TILE_SIZE - 5)
            self.collectibles.append(Collectible(x, y))

        # Spawn enemies
        for _ in range(50):
            x = random.randint(5, WORLD_WIDTH * TILE_SIZE - 5)
            y = random.randint(5, WORLD_HEIGHT * TILE_SIZE - 5)
            # Don't spawn too close to player
            if math.sqrt((x - self.player.x) ** 2 + (y - self.player.y) ** 2) > 300:
                self.enemies.append(Enemy(x, y))

        # Assign initial missions
        templates = list(MISSION_TEMPLATES)
        random.shuffle(templates)
        for template in templates[:3]:
            m = Mission(template[0], template[1], template[2], template[5], template[4])
            if template[4] == "collect":
                m.target_count = template[3]
            elif template[4] == "kill":
                m.target_count = template[3]
            else:
                m.target_count = 1
            self.missions.append(m)

    def add_message(self, msg):
        self.message_log.append((self.tick, msg))
        if len(self.message_log) > 50:
            self.message_log = self.message_log[-50:]

    def spawn_particles(self, x, y, color, count=10, speed=3):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            spd = random.uniform(1, speed)
            self.particles.append(
                Particle(x, y, color, math.cos(angle) * spd, math.sin(angle) * spd, random.randint(15, 40))
            )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_m:
                    self.show_minimap = not self.show_minimap
                if event.key == pygame.K_TAB:
                    self.show_missions = not self.show_missions
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()
                    return True
                if event.key == pygame.K_p:
                    self.paused = not self.paused
        return True

    def update(self):
        if self.game_over or self.paused:
            return

        self.tick += 1
        keys = pygame.key.get_pressed()

        # Player movement
        self.player.update(keys, self.world)

        # Shooting
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.player.shoot_cooldown <= 0:
            mx, my = pygame.mouse.get_pos()
            world_mx = mx + self.cam_x
            world_my = my + self.cam_y
            angle = math.atan2(world_my - self.player.y, world_mx - self.player.x)
            self.projectiles.append(
                Projectile(self.player.x, self.player.y, angle, speed=12, damage=20, color=CYAN)
            )
            self.player.shoot_cooldown = 10
            self.spawn_particles(self.player.x, self.player.y, CYAN, count=3, speed=2)

        # Update projectiles
        alive_projectiles = []
        for proj in self.projectiles:
            if proj.update():
                alive_projectiles.append(proj)
        self.projectiles = alive_projectiles

        # Update enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self.player.x, self.player.y, self.world)
                # Enemy attack
                dist = math.sqrt((enemy.x - self.player.x) ** 2 + (enemy.y - self.player.y) ** 2)
                if dist < enemy.radius + self.player.radius + 5:
                    if enemy.can_attack():
                        died = self.player.take_damage(enemy.damage)
                        self.spawn_particles(self.player.x, self.player.y, RED, count=5, speed=4)
                        if died:
                            self.game_over = True

        # Projectile-enemy collisions
        for proj in self.projectiles:
            if proj.owner != "player":
                continue
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                dist = math.sqrt((proj.x - enemy.x) ** 2 + (proj.y - enemy.y) ** 2)
                if dist < enemy.radius + proj.radius:
                    killed = enemy.take_damage(proj.damage)
                    self.spawn_particles(enemy.x, enemy.y, enemy.color, count=8, speed=4)
                    proj.lifetime = 0
                    if killed:
                        self.player.add_kill(enemy.name)
                        self.player.gain_xp(25)
                        self.player.score += enemy.max_hp
                        # Drop loot
                        for _ in range(random.randint(1, 3)):
                            ox = random.uniform(-20, 20)
                            oy = random.uniform(-20, 20)
                            self.collectibles.append(Collectible(enemy.x + ox, enemy.y + oy))
                        self.spawn_particles(enemy.x, enemy.y, YELLOW, count=15, speed=5)
                        self.add_message(f"Defeated {enemy.name}! +25 XP")
                    break

        # Collectible pickup
        for col in self.collectibles:
            if col.collected:
                continue
            dist = math.sqrt((col.x - self.player.x) ** 2 + (col.y - self.player.y) ** 2)
            if dist < col.radius + self.player.radius + 10:
                col.collected = True
                self.player.add_item(col.name)
                self.player.score += col.value
                self.player.gain_xp(col.value // 10)
                self.spawn_particles(col.x, col.y, col.color, count=8, speed=3)
                self.add_message(f"Found {col.name}! +{col.value} pts")

        # Remove collected
        self.collectibles = [c for c in self.collectibles if not c.collected]

        # Check missions
        for m in self.missions:
            if not m.completed and not m.turned_in:
                old_progress = m.progress
                if m.mission_type == "collect":
                    m.progress = self.player.inventory.get(m.target, 0)
                elif m.mission_type == "kill":
                    m.progress = self.player.kills.get(m.target, 0)
                if m.progress >= m.target_count and not m.completed:
                    m.completed = True
                    self.add_message(f"Mission Complete: {m.title}!")

        # Turn in completed missions (auto)
        for m in self.missions:
            if m.completed and not m.turned_in:
                m.turned_in = True
                self.player.gain_xp(m.reward)
                self.player.score += m.reward
                self.player.completed_missions += 1
                self.add_message(f"Turned in: {m.title}! +{m.reward} XP")

        # Respawn enemies periodically
        self.spawn_timer += 1
        if self.spawn_timer >= 600:  # Every 10 seconds
            self.spawn_timer = 0
            alive_enemies = sum(1 for e in self.enemies if e.alive)
            if alive_enemies < 30:
                angle = random.uniform(0, math.pi * 2)
                dist = random.randint(500, 800)
                ex = self.player.x + math.cos(angle) * dist
                ey = self.player.y + math.sin(angle) * dist
                ex = max(0, min(ex, WORLD_WIDTH * TILE_SIZE - 10))
                ey = max(0, min(ey, WORLD_HEIGHT * TILE_SIZE - 10))
                self.enemies.append(Enemy(ex, ey))

        # Respawn collectibles
        if len(self.collectibles) < 80 and self.tick % 300 == 0:
            angle = random.uniform(0, math.pi * 2)
            dist = random.randint(200, 600)
            cx = self.player.x + math.cos(angle) * dist
            cy = self.player.y + math.sin(angle) * dist
            cx = max(0, min(cx, WORLD_WIDTH * TILE_SIZE - 10))
            cy = max(0, min(cy, WORLD_HEIGHT * TILE_SIZE - 10))
            self.collectibles.append(Collectible(cx, cy))

        # New missions
        active_missions = sum(1 for m in self.missions if not m.turned_in)
        if active_missions < 3 and self.tick % 600 == 0:
            template = random.choice(MISSION_TEMPLATES)
            m = Mission(template[0], template[1], template[2], template[5], template[4])
            if template[4] == "collect":
                m.target_count = template[3]
            elif template[4] == "kill":
                m.target_count = template[3]
            else:
                m.target_count = 1
            self.missions.append(m)
            self.add_message(f"New Mission: {m.title}")

        # Update particles
        self.particles = [p for p in self.particles if p.update()]

        # Remove dead enemies (cleanup)
        if self.tick % 300 == 0:
            self.enemies = [e for e in self.enemies if e.alive]

        # Camera follow
        target_cam_x = self.player.x - SCREEN_WIDTH // 2
        target_cam_y = self.player.y - SCREEN_HEIGHT // 2
        self.cam_x += (target_cam_x - self.cam_x) * 0.1
        self.cam_y += (target_cam_y - self.cam_y) * 0.1

    def draw_world(self):
        # Only draw visible tiles
        start_tx = max(0, int(self.cam_x // TILE_SIZE) - 1)
        start_ty = max(0, int(self.cam_y // TILE_SIZE) - 1)
        end_tx = min(WORLD_WIDTH, start_tx + SCREEN_WIDTH // TILE_SIZE + 3)
        end_ty = min(WORLD_HEIGHT, start_ty + SCREEN_HEIGHT // TILE_SIZE + 3)

        for ty in range(start_ty, end_ty):
            for tx in range(start_tx, end_tx):
                biome = self.world[ty][tx]
                color = WorldGenerator.get_tile_color(biome)
                sx = tx * TILE_SIZE - int(self.cam_x)
                sy = ty * TILE_SIZE - int(self.cam_y)
                pygame.draw.rect(self.screen, color, (sx, sy, TILE_SIZE, TILE_SIZE))

                # Add detail based on biome
                if biome == BIOME_FOREST and (tx + ty) % 3 == 0:
                    # Draw a little tree
                    pygame.draw.rect(self.screen, BROWN, (sx + 28, sy + 32, 8, 20))
                    pygame.draw.circle(self.screen, (0, 150, 0), (sx + 32, sy + 26), 14)
                elif biome == BIOME_CRYSTAL and (tx + ty) % 4 == 0:
                    # Crystal spire
                    points = [(sx + 32, sy + 10), (sx + 20, sy + 50), (sx + 44, sy + 50)]
                    pygame.draw.polygon(self.screen, (100, 200, 255), points)
                elif biome == BIOME_WATER:
                    # Water shimmer
                    if (tx + ty + self.tick // 30) % 5 == 0:
                        pygame.draw.line(self.screen, (100, 200, 255),
                                         (sx + 10, sy + 32), (sx + 54, sy + 32), 1)

    def draw_hud(self):
        # HP bar
        bar_x, bar_y = 20, 20
        bar_w, bar_h = 200, 20
        hp_ratio = self.player.hp / self.player.max_hp
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4))
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
        hp_text = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + 5, bar_y + 2))

        # XP bar
        xp_y = bar_y + bar_h + 5
        xp_ratio = self.player.xp / self.player.xp_to_next
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x - 2, xp_y - 2, bar_w + 4, 12))
        pygame.draw.rect(self.screen, (80, 0, 120), (bar_x, xp_y, bar_w, 8))
        pygame.draw.rect(self.screen, PURPLE, (bar_x, xp_y, int(bar_w * xp_ratio), 8))

        # Level & Score
        lvl_text = self.font.render(f"Lv.{self.player.level}", True, YELLOW)
        self.screen.blit(lvl_text, (bar_x + bar_w + 10, bar_y))
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (bar_x + bar_w + 10, bar_y + 20))

        # Speed
        speed_text = self.font.render(f"Speed: {self.player.speed:.1f}", True, CYAN)
        self.screen.blit(speed_text, (bar_x + bar_w + 10, bar_y + 40))

        # Messages
        visible_messages = self.message_log[-5:]
        for i, (tick, msg) in enumerate(visible_messages):
            alpha = max(0, 255 - (self.tick - tick) * 3)
            if alpha > 0:
                msg_surf = self.font.render(msg, True, YELLOW)
                self.screen.blit(msg_surf, (20, SCREEN_HEIGHT - 100 + i * 18))

        # Controls hint
        hint = self.font.render("WASD:Move  Click:Shoot  M:Minimap  TAB:Missions  P:Pause", True, GRAY)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 25))

    def draw_minimap(self):
        if not self.show_minimap:
            return
        mm_size = 160
        mm_x = SCREEN_WIDTH - mm_size - 10
        mm_y = 10
        mm_surface = pygame.Surface((mm_size, mm_size))
        mm_surface.fill(BLACK)

        scale_x = mm_size / (WORLD_WIDTH * TILE_SIZE)
        scale_y = mm_size / (WORLD_HEIGHT * TILE_SIZE)

        # Simplified minimap - just draw biome dots sparsely
        for ty in range(0, WORLD_HEIGHT, 4):
            for tx in range(0, WORLD_WIDTH, 4):
                biome = self.world[ty][tx]
                color = WorldGenerator.get_tile_color(biome)
                mx = int(tx * TILE_SIZE * scale_x)
                my = int(ty * TILE_SIZE * scale_y)
                pygame.draw.rect(mm_surface, color, (mx, my, max(1, int(4 * TILE_SIZE * scale_x)), max(1, int(4 * TILE_SIZE * scale_y))))

        # Player dot
        px = int(self.player.x * scale_x)
        py = int(self.player.y * scale_y)
        pygame.draw.circle(mm_surface, WHITE, (px, py), 3)

        # Enemy dots
        for e in self.enemies:
            if e.alive:
                ex = int(e.x * scale_x)
                ey = int(e.y * scale_y)
                pygame.draw.circle(mm_surface, RED, (ex, ey), 2)

        # Collectible dots
        for c in self.collectibles:
            cx = int(c.x * scale_x)
            cy = int(c.y * scale_y)
            pygame.draw.circle(mm_surface, YELLOW, (cx, cy), 1)

        pygame.draw.rect(mm_surface, WHITE, (0, 0, mm_size, mm_size), 2)
        self.screen.blit(mm_surface, (mm_x, mm_y))

    def draw_missions_panel(self):
        if not self.show_missions:
            return
        panel_w, panel_h = 400, 300
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))
        self.screen.blit(panel, (panel_x, panel_y))
        pygame.draw.rect(self.screen, CYAN, (panel_x, panel_y, panel_w, panel_h), 2)

        title = self.big_font.render("MISSIONS", True, CYAN)
        self.screen.blit(title, (panel_x + panel_w // 2 - title.get_width() // 2, panel_y + 10))

        y = panel_y + 45
        for m in self.missions:
            if m.turned_in:
                continue
            status = "[DONE]" if m.completed else f"[{m.progress}/{m.target_count}]"
            color = YELLOW if m.completed else WHITE
            text = self.font.render(f"{status} {m.title}", True, color)
            self.screen.blit(text, (panel_x + 15, y))
            desc = self.font.render(f"  {m.description}", True, GRAY)
            self.screen.blit(desc, (panel_x + 15, y + 16))
            reward = self.font.render(f"  Reward: {m.reward} XP", True, GREEN)
            self.screen.blit(reward, (panel_x + 15, y + 32))
            y += 55

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        go_text = self.title_font.render("GAME OVER", True, RED)
        self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        score_text = self.big_font.render(f"Final Score: {self.player.score}  Level: {self.player.level}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

        restart_text = self.font.render("Press R to Restart", True, YELLOW)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_world()

        # Draw collectibles
        for col in self.collectibles:
            col.draw(self.screen, self.cam_x, self.cam_y, self.tick)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.cam_x, self.cam_y, self.tick)

        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(self.screen, self.cam_x, self.cam_y)

        # Draw particles
        for p in self.particles:
            p.draw(self.screen, self.cam_x, self.cam_y)

        # Draw player
        self.player.draw(self.screen, self.cam_x, self.cam_y, self.tick)

        # HUD
        self.draw_hud()
        self.draw_minimap()
        self.draw_missions_panel()

        if self.game_over:
            self.draw_game_over()

        # Version watermark
        ver_text = self.font.render(f"v{self.version}", True, DARK_GRAY)
        self.screen.blit(ver_text, (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()