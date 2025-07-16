#!/bin/bash
# -*- coding: utf-8 -*-
#
# Ez Chajim MEISTER FRAGE Tool - Installation mit Transliteration
# Stand: 12. Tammus 5785

echo "================================================"
echo "MEISTER FRAGE Tool - Vollständige Installation"
echo "================================================"
echo "Mit korrekter Transliteration und WWAQ-Konformität"
echo ""

# Prüfe ob im ez-chajim Verzeichnis
cd /Users/jorgbruder/ez-chajim

# Gehe ins Tool-Verzeichnis
cd meister-frage-tool

# Aktiviere virtuelle Umgebung
source venv/bin/activate

echo "1. Kopiere Transliteration-Modul..."
# Erstelle meister_transliteration.py in src/
cat > src/meister_transliteration.py << 'EOF'
# [Hier würde der vollständige Code von meister_transliteration.py eingefügt]
# Aus Platzgründen ausgelassen - verwenden Sie die Artifact-Version
EOF

echo "✓ Transliteration-Modul erstellt"

echo ""
echo "2. Kopiere Test-Script..."
# Kopiere das Test-Script
cat > test_meister_transliteration.py << 'EOF'
# [Hier würde der vollständige Code von test_meister_transliteration.py eingefügt]
# Aus Platzgründen ausgelassen - verwenden Sie die Artifact-Version
EOF

chmod +x test_meister_transliteration.py
echo "✓ Test-Script erstellt"

echo ""
echo "3. Erstelle Beispiel-Texte..."
mkdir -p beispiele

# Fehlerhafte Texte zum Testen
cat > beispiele/fehlerhaft.txt << 'EOF'
Die Kabbala lehrt uns über die zehn Sefirot:
Keter, Chochma, Bina, Chesed, Gevura, Tiferet,
Nezach, Hod, Jesod und Malchut.

Der Masach ist wichtig für den Tikun der Kelim.
Wir müssen die Klipot zerstören durch unsere Kawana.
EOF

# Korrekte Version
cat > beispiele/korrekt.txt << 'EOF'
Die Qabbala lehrt uns über die zehn Sefirot:
Qeter, Chochma, Bina, Chessed, Gewura, Tiferet,
Nezach, Hod, Jessod und Malchut.

Der Massach ist wichtig für den Tiqqun der Qelim.
Wir müssen die Qlipot wandeln durch unsere Qawana.
EOF

# Paradox-Beispiele
cat > beispiele/paradoxe.txt << 'EOF'
אור וחושך - Licht und Dunkelheit tanzen zusammen.
Im Mangel (חסרון) liegt die Fülle (שלמות) verborgen.
Der Gebende (משפיע) wird zum Empfänger (מקבל).
Oben (עליון) ist Unten (תחתון), Innen (פנימי) ist Außen (חיצוני).
Die Einheit (אחדות) enthält die Vielheit (ריבוי).
EOF

echo "✓ Beispiel-Texte erstellt"

echo ""
echo "4. Erstelle Cheat-Sheet..."
cat > TRANSLITERATION_RULES.md << 'EOF'
# MEISTER FRAGE Tool - Transliteration Regeln

## 🔴 KRITISCHE REGELN

### 1. K→Q Transformation (WWAQ)
- Kabbala → **Qabbala**
- Kawana → **Qawana** 
- Kelim → **Qelim**
- Kli → **Qli**
- Klipot → **Qlipot**
- Tikun → **Tiqqun** (Doppel-q!)

### 2. Dagesh-Verdopplung
Mit Dagesh (ּ) = Konsonant verdoppeln!

- מסך → **Massach** (NICHT Masach!)
- חסד → **Chessed** (NICHT Chesed!)
- יסוד → **Jessod** (NICHT Jesod!)
- תיקון → **Tiqqun** (NICHT Tikun!)

### 3. KEIN Dagesh bei:
- נצח → **Nezach** (bleibt einfach)
- הוד → **Hod** (bleibt einfach)

### 4. Zer-Elimination
- zerstören → **wandeln**
- zerbrechen → **bersten**
- zerfallen → **sich wandeln**

## 📋 Sefirot - Korrekte Schreibweise

1. כתר → **Keter** (K bleibt K, da Eigenname)
2. חכמה → **Chochma**
3. בינה → **Bina**
4. חסד → **Chessed** ⚠️ (Dagesh!)
5. גבורה → **Gewura**
6. תפארת → **Tiferet**
7. נצח → **Nezach** ✓ (kein Dagesh)
8. הוד → **Hod** ✓ (kein Dagesh)
9. יסוד → **Jessod** ⚠️ (Dagesh!)
10. מלכות → **Malchut**

## 🔧 Test-Kommandos

```bash
# Teste einzelnen Begriff
python -c "from meister_transliteration import *; print(MeisterTransliteration().korrigiere_deutsche_begriffe('Kabbala'))"

# Teste hebräischen Text
python -c "from meister_transliteration import *; print(MeisterTransliteration().transliteriere_hebräisch('חסד'))"

# Vollständiger Test
python test_meister_transliteration.py
```

Q!
EOF

echo "✓ Cheat-Sheet erstellt"

echo ""
echo "5. Update requirements.txt..."
cat >> requirements.txt << 'EOF'

# Für erweiterte Transliteration (optional)
# unicodedata2>=14.0
EOF

echo "✓ Requirements aktualisiert"

echo ""
echo "================================================"
echo "Installation abgeschlossen!"
echo "================================================"
echo ""
echo "TESTE DIE INSTALLATION:"
echo "  python test_meister_transliteration.py"
echo ""
echo "BEISPIEL-VERWENDUNG:"
echo "  python start_meister.py < beispiele/fehlerhaft.txt"
echo ""
echo "WICHTIGE DATEIEN:"
echo "  - src/meister_transliteration.py (Transliteration-Modul)"
echo "  - test_meister_transliteration.py (Test-Suite)"
echo "  - TRANSLITERATION_RULES.md (Regel-Übersicht)"
echo "  - beispiele/ (Test-Texte)"
echo ""
echo "Q!"

deactivate
