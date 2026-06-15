import ast
with open('game.py', 'r') as f:
    source = f.read()
try:
    ast.parse(source)
    print("SYNTAX OK")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")