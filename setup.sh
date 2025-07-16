#!/bin/bash
# Ez Chajim Unified Setup Script
# Stand: 20. Tammus 5785 (16. Juli 2025)
# WWAQ-konform

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    Ez Chajim Unified Setup                          ║"
echo "║                     עץ חיים - Baum des Lebens                      ║"
echo "║                    WWAQ-konform implementiert                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Farben für Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# GitHub Token direkt setzen
GITHUB_TOKEN="ghp_62BgW6u5aKRb7"
echo -e "${GREEN}✓ GitHub Token gesetzt${NC}"

# Arbeitsverzeichnis ist das aktuelle
WORK_DIR=$(pwd)
REPO_NAME="EZ-CHAJIM-UNIFIED-WWAQ"
GITHUB_ORG="JEREMIA1964"

echo -e "${YELLOW}📁 Arbeite in: $WORK_DIR${NC}"

# Git initialisieren (falls noch nicht geschehen)
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}🔧 Initialisiere Git...${NC}"
    git init
fi

# Erstelle Projektstruktur
echo -e "${YELLOW}📂 Erstelle Projektstruktur...${NC}"
mkdir -p {lib,src,manuscripts,yaml-schemas,output}
mkdir -p {modules/core,processing/translation,original-texts/{chunks-hebr,chunks-de}}
mkdir -p {tests,docs,scripts}

# Erstelle README
echo -e "${YELLOW}📝 Erstelle README...${NC}"
cat > README.md << 'EOF'
# EZ CHAJIM UNIFIED - עץ חיים

## ⚠️ DIES IST DAS EINZIGE AKTIVE REPOSITORY ⚠️

Alle anderen Ez Chajim Repositories wurden archiviert und sind DEPRECATED.

### 📚 Inhalt
- **1342 hebräische Chunks** des originalen Ez Chajim von Chajim Vital
- **Alle Module** konsolidiert in einer Struktur
- **HNS10-Spiralsystem** mit Drei-Kalender-Integration
- **Claude Batches** für Übersetzungsprozess
- **WWAQ-konform** mit Q-Schreibweise

### 🌳 Struktur### ⚡ Wichtige Konzepte
- **Lurianische Qabbala** - LiSchma (לשמה)
- **Q-Schreibweise** durchgängig (Qabbala, nicht Kabbala)
- **WWAQ** - Wissenschaft der Weisheit der Authentischen Qabbala
- **HNS10** - Hebräisches Numeral-System mit Null-Tabu (Grad 0 verboten)
- **Spiralzeit** - Jahr.Monat.Tag.Stunde Format

### 📅 Stand
20. Tammus 5785 (16. Juli 2025)

**Q! = Qawana! + DWEKUT!**
EOF

# Erstelle requirements.txt
echo -e "${YELLOW}📦 Erstelle requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
PyYAML>=6.0.1
python-dateutil>=2.8.2
pyluach>=2.0.0
hijri-converter>=2.2.0
click>=8.1.7
jsonschema>=4.19.0
regex>=2023.8.8
pytest>=7.4.0
EOF

# Erstelle .gitignore
echo -e "${YELLOW}🚫 Erstelle .gitignore...${NC}"
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
output/temp/
*.log
.cache/
EOF

# Erstelle Basis-Testdatei
echo -e "${YELLOW}🧪 Erstelle Test-Struktur...${NC}"
cat > test_integration.py << 'EOF'
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
EOF

# Erstelle Platzhalter für Bibliotheksdateien
echo -e "${YELLOW}📚 Erstelle Bibliotheks-Platzhalter...${NC}"
touch lib/__init__.py
touch src/__init__.py
touch modules/__init__.py

# Git konfigurieren
echo -e "${YELLOW}🔐 Konfiguriere Git...${NC}"
git config user.name "JEREMIA1964"
git config user.email "jeremiagottlieb@gmail.com"

# Alles zu Git hinzufügen
echo -e "${YELLOW}📦 Füge Dateien zu Git hinzu...${NC}"
git add .

# Initial Commit
echo -e "${YELLOW}💾 Erstelle Initial Commit...${NC}"
git commit -m "feat: Initial Ez Chajim Unified Setup

- Vollständige Projektstruktur
- HNS10-Spiralsystem Vorbereitung
- WWAQ-konforme Implementation
- 1342 Chunks Struktur

Hebrew Date: 20. Tammus 5785
Spiralzeit: 5785.5.20
Q!"

# Remote hinzufügen (falls noch nicht vorhanden)
if ! git remote | grep -q "origin"; then
    echo -e "${YELLOW}🔗 Verbinde mit GitHub...${NC}"
    git remote add origin "https://github.com/$GITHUB_ORG/$REPO_NAME.git"
else
    echo -e "${GREEN}✅ Remote 'origin' bereits konfiguriert${NC}"
fi

# Branch umbenennen
git branch -M main

# Push zum Remote mit Token
echo -e "${YELLOW}🚀 Push zu GitHub...${NC}"
git push -u origin main

echo -e "${GREEN}✅ Setup erfolgreich abgeschlossen!${NC}"
echo ""
echo "Nächste Schritte:"
echo "1. Kopieren Sie die Bibliotheksdateien nach lib/"
echo "2. python3 -m venv venv && source venv/bin/activate"
echo "3. pip install -r requirements.txt"
echo "4. python test_integration.py"
echo ""
echo "Q! = Qawana! + DWEKUT!"
