import ast
import sys

try:
    with open('game.py', 'r') as f:
        source = f.read()
    tree = ast.parse(source, filename='game.py')
    print(f'Syntax OK! File has {len(source)} chars, {source.count(chr(10))+1} lines')
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    print(f'Classes: {len(classes)}')
    print(f'Functions: {len(functions)}')
    if 'PulseWaveRing' in classes:
        print('PulseWaveRing class found')
    if 'Achievement' in classes:
        print('Achievement class found')
    method_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    if '_check_achievements' in method_names:
        print('_check_achievements method found')
    if '_activate_pulse_wave' in method_names:
        print('_activate_pulse_wave method found')
except SyntaxError as e:
    print(f'SYNTAX ERROR: {e}')
    sys.exit(1)