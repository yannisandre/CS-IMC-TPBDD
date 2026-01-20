#!/usr/bin/env python3

"""
Script de test pour vérifier la syntaxe du programme export-neo4j.py
"""

import ast
import sys

def check_syntax(filename):
    # on essaie de parser le fichier pour vérifier la syntaxe
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✓ {filename}: Syntaxe valide")
        return True
    except SyntaxError as e:
        print(f"✗ Erreur de syntaxe dans {filename}:")
        print(f"  Ligne {e.lineno}: {e.msg}")
        print(f"  {e.text}")
        return False

if __name__ == "__main__":
    success = check_syntax("export-neo4j.py")
    sys.exit(0 if success else 1)
