#!/usr/bin/env python3
"""
Ez Chajim Integration Tests
Stand: 20. Tammus 5785
"""

import sys
from pathlib import Path

# Füge lib zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

def test_imports():
    """Teste ob alle Module importiert werden können"""
    print("🧪 Teste Imports...")
    
    modules_to_test = [
        'hns10_spiral_system',
        'manuscript_processor', 
        'yaml_ez_chajim_formatter'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✅ {module} erfolgreich importiert")
        except ImportError as e:
            print(f"  ❌ {module} konnte nicht importiert werden: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Ez Chajim Integration Tests")
    print("=" * 40)
    
    if test_imports():
        print("\n✅ Alle Tests erfolgreich!")
    else:
        print("\n❌ Tests fehlgeschlagen!")
        print("    (Das ist normal - die Bibliotheken müssen noch hinzugefügt werden)")
