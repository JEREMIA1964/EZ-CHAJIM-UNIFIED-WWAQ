#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimierte Rabash-Analyse mit expliziten Paradoxen
Stand: 12. Tammus 5785
"""

import sys
sys.path.insert(0, 'src')

from meister_frage_tool import MeisterFrageTool, ParadoxTyp

# Initialisiere Tool
tool = MeisterFrageTool()

# Erweitere die Paradox-Paare für Rabash-Begriffe
tool.PARADOX_PAARE.update({
    ('zwang', 'gesetz'): ParadoxTyp.WANDLUNG,
    ('zwang', 'liebe'): ParadoxTyp.WANDLUNG,
    ('wille zu empfangen', 'wille zu geben'): ParadoxTyp.WANDLUNG,
    ('empfangen', 'geben'): ParadoxTyp.REZIPROK,
    ('verstand', 'glaube'): ParadoxTyp.KLASSISCH,
    ('verstand', 'über dem verstand'): ParadoxTyp.HIERARCHIE,
    ('körper', 'seele'): ParadoxTyp.KLASSISCH,
    ('arbeit', 'freude'): ParadoxTyp.WANDLUNG,
    ('ochse', 'joch'): ParadoxTyp.EINSCHLUSS,
    ('esel', 'last'): ParadoxTyp.EINSCHLUSS,
    ('frage', 'keine antwort'): ParadoxTyp.KLASSISCH,
    ('reinigung', 'gefäße'): ParadoxTyp.WANDLUNG
})

# Analysiere drei Kern-Paradoxe aus dem Text
print("=== RABASH ARTIKEL 37 - TIEFENANALYSE ===\n")

# 1. Hauptparadox: Zwang wird zu Gesetz
text1 = "Die Arbeit unter Zwang wird zum Gesetz der spirituellen Entwicklung."
ergebnis1 = tool.verarbeite_text(text1)

print("1. ZWANG → GESETZ")
if ergebnis1['beste_frage']:
    print(f"   Frage: {ergebnis1['beste_frage'].frage}")
    print(f"   Score: {ergebnis1['beste_frage'].gesamt_score:.2f}")

# 2. Verstand vs. Über dem Verstand
text2 = "Der Verstand fragt, aber die Antwort liegt über dem Verstand im Glauben."
ergebnis2 = tool.verarbeite_text(text2)

print("\n2. VERSTAND ↔ ÜBER DEM VERSTAND")
if ergebnis2['beste_frage']:
    print(f"   Frage: {ergebnis2['beste_frage'].frage}")
    print(f"   Score: {ergebnis2['beste_frage'].gesamt_score:.2f}")

# 3. Wille zu empfangen vs. Wille zu geben
text3 = "Der Wille zu empfangen muss zum Willen zu geben werden durch bewusste Arbeit."
ergebnis3 = tool.verarbeite_text(text3)

print("\n3. EMPFANGEN → GEBEN")
if ergebnis3['beste_frage']:
    print(f"   Frage: {ergebnis3['beste_frage'].frage}")
    print(f"   Score: {ergebnis3['beste_frage'].gesamt_score:.2f}")

# 4. Der volle Rabash-Text in Segmenten
print("\n=== VOLLTEXT-ANALYSE IN SEGMENTEN ===\n")

segmente = [
    "Bevor der Mensch die Reinigung der Gefäße erlangt hat, ist seine Arbeit unter Zwang.",
    "Wenn der Körper fragt, antwortet man nicht innerhalb des Verstandes.",
    "Ich will nicht für den Willen zu empfangen arbeiten.",
    "Man muss zum Nutzen des Ewigen über dem Verstand arbeiten.",
    "Ich nehme diese Arbeit an als Ochse zum Joch und Esel zur Last."
]

alle_fragen = []

for i, segment in enumerate(segmente, 1):
    print(f"Segment {i}: {segment[:50]}...")
    ergebnis = tool.verarbeite_text(segment)
    
    if ergebnis['paradoxe']:
        print(f"   Paradoxe: {len(ergebnis['paradoxe'])}")
        for p in ergebnis['paradoxe']:
            print(f"   - {p.element1} {p.beziehung} {p.element2}")
    
    if ergebnis['beste_frage']:
        alle_fragen.append(ergebnis['beste_frage'])
        print(f"   Beste Frage: {ergebnis['beste_frage'].frage}")
    print()

# Wähle die ultimative Frage
if alle_fragen:
    ultimative_frage = max(alle_fragen, key=lambda f: f.gesamt_score)
    print("\n🏆 ULTIMATIVE FRAGE FÜR GRUPPENARBEIT:")
    print(f"   {ultimative_frage.frage}")
    print(f"   Typ: {ultimative_frage.typ.value}")
    print(f"   Score: {ultimative_frage.gesamt_score:.2f}")

# Generiere spezielle Rabash-Fragen
print("\n=== SPEZIELLE RABASH-FRAGEN ===\n")

rabash_fragen = [
    "WOZU muss die Arbeit unter Zwang sein, bevor die Gefäße gereinigt sind?",
    "WIE wird der Wille zu empfangen zum Willen zu geben?",
    "Was liegt ZWISCHEN Verstand und Glaube?",
    "WENN der Körper fragt → DANN schweigt die Seele?",
    "Zwang + Gesetz = ?",
    "IST 'über dem Verstand' wirklich jenseits des Verstandes?"
]

for frage in rabash_fragen:
    print(f"• {frage}")

# Export
print("\n=== EXPORT ===")

# Erstelle Gesamt-Analyse
gesamt_analyse = {
    'artikel': 'Rabash Artikel 37 (1991)',
    'kern_paradoxe': [
        'Zwang → Gesetz',
        'Verstand ↔ Über dem Verstand',
        'Wille zu empfangen → Wille zu geben',
        'Körper ↔ Seele',
        'Frage → Keine Antwort'
    ],
    'beste_fragen': [f.frage for f in alle_fragen[:3]] if alle_fragen else [],
    'gruppen_fragen': rabash_fragen[:3],
    'meditation': "Sitze mit der Frage: 'Zwang + Liebe = ?' ohne zu antworten."
}

import yaml
with open('output/rabash_37_optimiert.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(gesamt_analyse, f, allow_unicode=True, default_flow_style=False)

print("✓ Optimierte Analyse exportiert nach: output/rabash_37_optimiert.yaml")

# Markdown für Gruppenarbeit
with open('output/rabash_37_gruppenarbeit.md', 'w', encoding='utf-8') as f:
    f.write("""# Rabash Artikel 37 (1991) - Gruppenarbeit

## Zentrale Paradoxe

1. **Zwang → Gesetz**: Die Arbeit beginnt unter Zwang und wird zum spirituellen Gesetz
2. **Verstand ↔ Glaube**: Der Verstand fragt, aber die Antwort liegt darüber
3. **Empfangen → Geben**: Der Wille muss transformiert werden

## Diskussionsfragen

### Für Anfänger
- Was bedeutet "Arbeit unter Zwang"?
- Warum antwortet man dem Körper nicht mit Verstand?

### Für Fortgeschrittene
- WOZU muss die Arbeit unter Zwang sein, bevor die Gefäße gereinigt sind?
- WIE wird der Wille zu empfangen zum Willen zu geben?

### Für die Gruppe
- Zwang + Liebe = ?
- Was liegt ZWISCHEN Verstand und Glaube?

## Meditation
Sitze 10 Minuten mit dieser Frage:
> "IST 'über dem Verstand' wirklich jenseits des Verstandes?"

Lass die Frage in dir wirken ohne zu antworten.

---
Q! = Die Frage ist der Weg!
""")

print("✓ Gruppenarbeits-Blatt exportiert nach: output/rabash_37_gruppenarbeit.md")

print("\nQ!")
