import ast
import sys

with open('game.py', 'r') as f:
    source = f.read()
tree = ast.parse(source, filename='game.py')

# Find all methods (FunctionDef inside ClassDef)
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef) and node.name == 'Game':
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        print(f"Game class has {len(methods)} methods")
        if '_check_achievements' in methods:
            print('_check_achievements found in Game class')
        if '_activate_pulse_wave' in methods:
            print('_activate_pulse_wave found in Game class')
        if '_check_achievements' not in methods:
            print('WARNING: _check_achievements NOT in Game class')
        if '_activate_pulse_wave' not in methods:
            print('WARNING: _activate_pulse_wave NOT in Game class')
        break