#!/bin/bash
# -*- coding: utf-8 -*-
#
# Ez Chajim MEISTER FRAGE Tool - Setup Script
# Stand: 12. Tammus 5785
# 
# Dieses Script installiert das MEISTER FRAGE Tool
# im ez-chajim Verzeichnis

echo "================================================"
echo "Ez Chajim MEISTER FRAGE Tool - Installation"
echo "================================================"
echo "Stand: 12. Tammus 5785"
echo ""

# Farben für Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Prüfe ob wir im richtigen Verzeichnis sind
if [[ ! "$PWD" == */ez-chajim* ]]; then
    echo -e "${YELLOW}Warnung: Sie scheinen nicht im ez-chajim Verzeichnis zu sein.${NC}"
    echo "Aktuelles Verzeichnis: $PWD"
    read -p "Trotzdem fortfahren? (j/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Jj]$ ]]; then
        echo "Installation abgebrochen."
        exit 1
    fi
fi

echo "1. Erstelle Verzeichnisstruktur..."
mkdir -p meister-frage-tool/{src,templates,examples,output,docs}
echo -e "${GREEN}✓ Verzeichnisse erstellt${NC}"

echo ""
echo "2. Prüfe Python-Installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION gefunden${NC}"
else
    echo -e "${RED}✗ Python3 nicht gefunden!${NC}"
    echo "Bitte installieren Sie Python 3.8 oder höher."
    exit 1
fi

echo ""
echo "3. Erstelle virtuelle Umgebung..."
cd meister-frage-tool
python3 -m venv venv
echo -e "${GREEN}✓ Virtuelle Umgebung erstellt${NC}"

echo ""
echo "4. Aktiviere virtuelle Umgebung..."
source venv/bin/activate
echo -e "${GREEN}✓ Umgebung aktiviert${NC}"

echo ""
echo "5. Installiere Abhängigkeiten..."
pip install --upgrade pip > /dev/null 2>&1
pip install PyYAML > /dev/null 2>&1
echo -e "${GREEN}✓ PyYAML installiert${NC}"

echo ""
echo "6. Erstelle requirements.txt..."
cat > requirements.txt << 'EOF'
PyYAML>=6.0
# Optional: Für Web-API
# flask>=2.0
# Optional: Für erweiterte Analyse
# nltk>=3.6
EOF
echo -e "${GREEN}✓ requirements.txt erstellt${NC}"

echo ""
echo "7. Erstelle Beispiel-Konfiguration..."
cat > config.yaml << 'EOF'
# MEISTER FRAGE Tool Konfiguration
# Stand: 12. Tammus 5785

meister_config:
  # Sprach-Einstellungen
  sprache:
    haupt: "de"
    sekundär: "he"
    
  # WWAQ-Transformationen
  wwaq:
    aktiviert: true
    strikt: true
    
  # Export-Einstellungen
  export:
    standard_format: "yaml"
    output_verzeichnis: "output"
    zeitstempel: true
    
  # Bewertungs-Gewichtung
  bewertung:
    kraft_gewicht: 0.33
    tiefe_gewicht: 0.33
    wozu_gewicht: 0.34
    
  # Erweiterte Paradox-Paare
  zusatz_paradoxe:
    - ["anfang", "ende", "SIMULTAN"]
    - ["leere", "fülle", "EINSCHLUSS"]
    - ["sprechen", "schweigen", "KLASSISCH"]
EOF
echo -e "${GREEN}✓ Konfiguration erstellt${NC}"

echo ""
echo "8. Erstelle Starter-Script..."
cat > start_meister.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEISTER FRAGE Tool - Starter Script
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from meister_frage_tool import MeisterFrageTool

def main():
    print("=== MEISTER FRAGE Tool ===")
    print("Stand: 12. Tammus 5785")
    print()
    
    tool = MeisterFrageTool()
    
    print("Geben Sie einen Text ein (Enter + Enter zum Beenden):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    if lines:
        text = " ".join(lines)
        ergebnis = tool.verarbeite_text(text)
        
        if ergebnis['beste_frage']:
            print(f"\n🏆 BESTE FRAGE:")
            print(f"   {ergebnis['beste_frage'].frage}")
            print(f"\n   Kraft: {ergebnis['beste_frage'].scores['kraft']:.2f}")
            print(f"   Tiefe: {ergebnis['beste_frage'].scores['tiefe']:.2f}")
            print(f"   WOZU: {ergebnis['beste_frage'].scores['wozu']:.2f}")
        
        # Export
        tool.export_yaml(ergebnis, "output/letzte_analyse.yaml")
        print(f"\n✓ Analyse exportiert nach: output/letzte_analyse.yaml")
    
    print("\nQ!")

if __name__ == "__main__":
    main()
EOF
chmod +x start_meister.py
echo -e "${GREEN}✓ Starter-Script erstellt${NC}"

echo ""
echo "9. Erstelle Test-Script..."
cat > test_installation.py << 'EOF'
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
EOF
chmod +x test_installation.py
echo -e "${GREEN}✓ Test-Script erstellt${NC}"

echo ""
echo "10. Erstelle README..."
cat > README_QUICK.md << 'EOF'
# MEISTER FRAGE Tool - Schnellstart

## Start
```bash
# Virtuelle Umgebung aktivieren
source venv/bin/activate

# Tool starten
python start_meister.py
```

## Web-Interface
```bash
open templates/meister_frage_ui.html
```

## Demos ausführen
```bash
python examples/meister_demo.py
```

## Deaktivieren
```bash
deactivate
```

Q!
EOF
echo -e "${GREEN}✓ Quick-README erstellt${NC}"

echo ""
echo "================================================"
echo -e "${GREEN}Installation abgeschlossen!${NC}"
echo "================================================"
echo ""
echo "WICHTIG: Kopieren Sie jetzt die Tool-Dateien:"
echo ""
echo "  cp /pfad/zu/meister_frage_tool.py src/"
echo "  cp /pfad/zu/meister_frage_ui.html templates/"
echo "  cp /pfad/zu/meister_demo.py examples/"
echo "  cp /pfad/zu/meister_frage_readme.md docs/"
echo ""
echo "Dann testen Sie die Installation:"
echo "  python test_installation.py"
echo ""
echo "Zum Starten:"
echo "  source venv/bin/activate"
echo "  python start_meister.py"
echo ""
echo "Q!"

# Deaktiviere venv am Ende
deactivate
