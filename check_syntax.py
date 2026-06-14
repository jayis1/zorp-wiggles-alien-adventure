import ast
with open('game.py', 'r') as f:
    code = f.read()
ast.parse(code)
print('Syntax OK')