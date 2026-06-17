import ast
with open('game.py', 'r') as f:
    source = f.read()
tree = ast.parse(source, filename='game.py')

# Verify all new features are present
checks = {
    'PulseWaveRing class': any(isinstance(n, ast.ClassDef) and n.name == 'PulseWaveRing' for n in ast.walk(tree)),
    'Achievement class': any(isinstance(n, ast.ClassDef) and n.name == 'Achievement' for n in ast.walk(tree)),
    'PULSE_WAVE_COOLDOWN constant': 'PULSE_WAVE_COOLDOWN' in source,
    'SPAWN_HEAL_RADIUS constant': 'SPAWN_HEAL_RADIUS' in source,
    'COLLECT_RADIUS_PER_LEVEL constant': 'COLLECT_RADIUS_PER_LEVEL' in source,
    'Q key handler': "held_keys['q']" in source,
    'F key handler': "held_keys['f']" in source,
    '_check_achievements call': 'game._check_achievements()' in source,
    '_activate_pulse_wave call': 'game._activate_pulse_wave()' in source,
    'pulse_wave_cooldown in Game init': 'self.pulse_wave_cooldown = 0.0' in source,
    'achievements in Game init': 'self.achievements' in source,
    'spawn_heal_ring in Game init': 'self.spawn_heal_ring' in source,
    'total_kills tracking': 'game.total_kills += 1' in source,
    'total_items_collected tracking': 'game.total_items_collected += 1' in source,
    'traded_once flag': 'game.traded_once = True' in source,
    'level_collect_bonus': 'level_collect_bonus' in source,
    'level_pull_bonus': 'level_pull_bonus' in source,
    'SPAWN_HEAL_HP_PER_SECOND': 'SPAWN_HEAL_HP_PER_SECOND' in source,
}

all_ok = True
for name, found in checks.items():
    status = 'OK' if found else 'MISSING!'
    if not found:
        all_ok = False
    print(f'  [{status}] {name}')

if all_ok:
    print('\nAll features verified!')
else:
    print('\nSome features are MISSING!')