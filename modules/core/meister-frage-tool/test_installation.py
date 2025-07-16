#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test ob Installation erfolgreich war"""

import sys
import os

print("Teste MEISTER FRAGE Tool Installation...")
print("-" * 40)

# Test 1: Python Version
print("1. Python Version:", sys.version.split()[0])
if sys.version_info >= (3, 8):
    print("   ✓ Python Version OK")
else:
    print("   ✗ Python 3.8+ benötigt!")

# Test 2: PyYAML
try:
    import yaml
    print("2. PyYAML:", yaml.__version__)
    print("   ✓ PyYAML installiert")
except ImportError:
    print("2. ✗ PyYAML nicht gefunden!")

# Test 3: Verzeichnisse
dirs_ok = True
for d in ['src', 'templates', 'examples', 'output']:
    if os.path.exists(d):
        print(f"3. ✓ Verzeichnis '{d}' existiert")
    else:
        print(f"3. ✗ Verzeichnis '{d}' fehlt!")
        dirs_ok = False

# Test 4: Hauptmodul
if os.path.exists('src/meister_frage_tool.py'):
    print("4. ✓ Hauptmodul vorhanden")
    
    # Versuche zu importieren
    sys.path.insert(0, 'src')
    try:
        from meister_frage_tool import MeisterFrageTool
        tool = MeisterFrageTool()
        result = tool.verarbeite_text("Test Paradox")
        print("   ✓ Import und Basis-Test erfolgreich")
    except Exception as e:
        print(f"   ✗ Fehler beim Import: {e}")
else:
    print("4. ✗ Hauptmodul fehlt!")
    print("   Bitte kopieren Sie meister_frage_tool.py nach src/")

print("-" * 40)
print("Q!")
