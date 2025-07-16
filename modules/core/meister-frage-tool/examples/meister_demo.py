#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEISTER FRAGE Tool - Demo Script
================================

Zeigt verschiedene Verwendungsmöglichkeiten
Stand: 12. Tammus 5785
"""

from meister_frage_tool import MeisterFrageTool, ParadoxTyp, FrageTyp
import yaml
from datetime import datetime

def demo_basis():
    """Basis-Verwendung des Tools"""
    print("=== DEMO 1: Basis-Verwendung ===\n")
    
    tool = MeisterFrageTool()
    
    # Einfacher Text
    text = "Die Liebe entsteht nur durch Zwang."
    print(f"Text: '{text}'")
    
    # Analyse
    ergebnis = tool.verarbeite_text(text)
    
    print(f"\nParadoxe gefunden: {len(ergebnis['paradoxe'])}")
    for p in ergebnis['paradoxe']:
        print(f"  - {p.element1} {p.beziehung} {p.element2} (Typ: {p.typ.value})")
    
    print(f"\nBeste Frage: {ergebnis['beste_frage'].frage}")
    print(f"Scores: {ergebnis['beste_frage'].scores}")
    
    print("\n" + "-"*50 + "\n")

def demo_rabash_integration():
    """Integration mit Rabash-Texten"""
    print("=== DEMO 2: Rabash-Integration ===\n")
    
    tool = MeisterFrageTool()
    
    # Typischer Rabash-Text (Artikel 6, 1984)
    rabash_text = """
    Der Mensch muss verstehen, dass im Mangel die Fülle liegt,
    und dass das Licht gerade durch die Dunkelheit scheint.
    Wer empfangen will, muss zuerst geben lernen,
    denn der Empfänger wird zum Gebenden nur durch Einschränkung.
    """
    
    print("Rabash-Text analysieren...")
    ergebnis = tool.verarbeite_text(rabash_text)
    
    print(f"\nTop 3 Fragen für Gruppenarbeit:")
    for i, frage in enumerate(ergebnis['top_5'][:3], 1):
        print(f"\n{i}. {frage.frage}")
        print(f"   Typ: {frage.typ.value}")
        print(f"   Eignung für Anfänger: {'★' * int(frage.scores['kraft'] * 5)}")
        print(f"   Tiefe für Fortgeschrittene: {'★' * int(frage.scores['tiefe'] * 5)}")
    
    print("\n" + "-"*50 + "\n")

def demo_meditation_karten():
    """Erstelle Meditations-Karten"""
    print("=== DEMO 3: Meditations-Karten ===\n")
    
    tool = MeisterFrageTool()
    
    # Verschiedene paradoxe Aussagen
    aussagen = [
        "Oben ist Unten, Innen ist Außen.",
        "Die wahre Freiheit findet sich in der völligen Hingabe.",
        "Im Kleinen liegt das Große verborgen.",
        "Wer alles loslässt, gewinnt alles.",
        "Die Stille spricht lauter als alle Worte."
    ]
    
    karten = []
    
    for aussage in aussagen:
        ergebnis = tool.verarbeite_text(aussage)
        if ergebnis['beste_frage']:
            karten.append({
                'vorderseite': ergebnis['beste_frage'].frage,
                'rückseite': aussage,
                'meditation': f"Sitze mit dieser Frage: {ergebnis['beste_frage'].frage}\n"
                             f"Lass sie in dir wirken ohne zu antworten.",
                'score': ergebnis['beste_frage'].gesamt_score
            })
    
    # Speichere als YAML
    with open('meditation_karten.yaml', 'w', encoding='utf-8') as f:
        yaml.dump({
            'meditation_karten': {
                'erstellt': datetime.now().isoformat(),
                'karten': karten
            }
        }, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✓ {len(karten)} Meditations-Karten erstellt")
    print("  Gespeichert in: meditation_karten.yaml")
    
    # Zeige beste Karte
    beste_karte = max(karten, key=lambda k: k['score'])
    print(f"\nBeste Meditations-Karte:")
    print(f"  Frage: {beste_karte['vorderseite']}")
    print(f"  Score: {beste_karte['score']:.2f}")
    
    print("\n" + "-"*50 + "\n")

def demo_wochen_programm():
    """Erstelle 7-Tage Paradox-Programm"""
    print("=== DEMO 4: 7-Tage Paradox-Programm ===\n")
    
    tool = MeisterFrageTool()
    
    # 7 Themen für 7 Tage
    themen = {
        'Sonntag': "Licht und Dunkelheit tanzen zusammen.",
        'Montag': "Der Gebende wird zum Empfänger.",
        'Dienstag': "Im Mangel offenbart sich die Fülle.",
        'Mittwoch': "Die Einheit enthält die Vielheit.",
        'Donnerstag': "Zwang gebiert wahre Liebe.",
        'Freitag': "Das Ende ist der Anfang.",
        'Schabbat': "In der Ruhe liegt die höchste Bewegung."
    }
    
    programm = {}
    
    for tag, thema in themen.items():
        ergebnis = tool.verarbeite_text(thema)
        
        # Wähle verschiedene Frage-Typen für Abwechslung
        morgen_frage = None
        abend_frage = None
        
        for frage in ergebnis['alle_fragen']:
            if not morgen_frage and frage.typ == FrageTyp.WOZU:
                morgen_frage = frage
            elif not abend_frage and frage.typ in [FrageTyp.ZWISCHEN, FrageTyp.META]:
                abend_frage = frage
            
            if morgen_frage and abend_frage:
                break
        
        programm[tag] = {
            'thema': thema,
            'morgen': {
                'frage': morgen_frage.frage if morgen_frage else ergebnis['beste_frage'].frage,
                'fokus': 'Beginne den Tag mit dieser Frage'
            },
            'abend': {
                'frage': abend_frage.frage if abend_frage else ergebnis['alle_fragen'][1].frage if len(ergebnis['alle_fragen']) > 1 else "Was hast du heute erkannt?",
                'fokus': 'Reflektiere vor dem Schlaf'
            }
        }
    
    # Ausgabe als strukturiertes Programm
    print("7-TAGE PARADOX-PROGRAMM")
    print("="*40)
    
    for tag, inhalt in programm.items():
        print(f"\n{tag.upper()}")
        print(f"Thema: {inhalt['thema']}")
        print(f"Morgen: {inhalt['morgen']['frage']}")
        print(f"Abend: {inhalt['abend']['frage']}")
    
    # Speichere als Markdown
    with open('wochen_programm.md', 'w', encoding='utf-8') as f:
        f.write("# 7-Tage Paradox-Programm\n")
        f.write(f"Erstellt: {datetime.now().strftime('%d.%m.%Y')}\n\n")
        
        for tag, inhalt in programm.items():
            f.write(f"## {tag}\n\n")
            f.write(f"**Thema**: {inhalt['thema']}\n\n")
            f.write(f"### Morgen-Meditation\n")
            f.write(f"> {inhalt['morgen']['frage']}\n\n")
            f.write(f"*{inhalt['morgen']['fokus']}*\n\n")
            f.write(f"### Abend-Reflexion\n")
            f.write(f"> {inhalt['abend']['frage']}\n\n")
            f.write(f"*{inhalt['abend']['fokus']}*\n\n")
            f.write("---\n\n")
        
        f.write("Q! = Die Frage ist der Weg!\n")
    
    print("\n✓ Programm gespeichert in: wochen_programm.md")
    
    print("\n" + "-"*50 + "\n")

def demo_batch_analyse():
    """Batch-Analyse mehrerer Texte"""
    print("=== DEMO 5: Batch-Analyse ===\n")
    
    tool = MeisterFrageTool()
    
    # Sammlung spiritueller Paradoxe
    texte = [
        "Je mehr du gibst, desto mehr empfängst du.",
        "Stärke zeigt sich in der Schwäche.",
        "Der kürzeste Weg führt durch den längsten Umweg.",
        "Wissen bedeutet zu wissen, dass man nichts weiß.",
        "In der Stille hört man am meisten."
    ]
    
    alle_fragen = []
    statistik = {
        'total_paradoxe': 0,
        'total_fragen': 0,
        'typen': {}
    }
    
    for text in texte:
        ergebnis = tool.verarbeite_text(text)
        
        statistik['total_paradoxe'] += len(ergebnis['paradoxe'])
        statistik['total_fragen'] += len(ergebnis['alle_fragen'])
        
        # Sammle beste Frage
        if ergebnis['beste_frage']:
            alle_fragen.append({
                'original': text,
                'frage': ergebnis['beste_frage'].frage,
                'score': ergebnis['beste_frage'].gesamt_score,
                'typ': ergebnis['beste_frage'].typ.value
            })
            
            # Zähle Typen
            typ = ergebnis['beste_frage'].typ.value
            statistik['typen'][typ] = statistik['typen'].get(typ, 0) + 1
    
    # Sortiere nach Score
    alle_fragen.sort(key=lambda x: x['score'], reverse=True)
    
    print("BATCH-ANALYSE ERGEBNIS")
    print(f"Texte analysiert: {len(texte)}")
    print(f"Paradoxe gefunden: {statistik['total_paradoxe']}")
    print(f"Fragen generiert: {statistik['total_fragen']}")
    print(f"\nFrage-Typen Verteilung:")
    for typ, count in statistik['typen'].items():
        print(f"  {typ}: {count}")
    
    print(f"\nTOP 3 FRAGEN:")
    for i, item in enumerate(alle_fragen[:3], 1):
        print(f"\n{i}. {item['frage']}")
        print(f"   Aus: '{item['original']}'")
        print(f"   Score: {item['score']:.2f}")
    
    print("\n" + "-"*50 + "\n")

def demo_custom_paradox():
    """Demo mit benutzerdefinierten Paradox-Typen"""
    print("=== DEMO 6: Eigene Paradox-Definitionen ===\n")
    
    tool = MeisterFrageTool()
    
    # Füge eigene Paradox-Paare hinzu
    tool.PARADOX_PAARE.update({
        ('schöpfer', 'geschöpf'): ParadoxTyp.HIERARCHIE,
        ('lehrer', 'schüler'): ParadoxTyp.REZIPROK,
        ('frage', 'antwort'): ParadoxTyp.IDENTITÄT,
        ('schweigen', 'sprechen'): ParadoxTyp.KLASSISCH
    })
    
    text = """
    Der Schöpfer wird zum Geschöpf, um erkannt zu werden.
    Der Lehrer lernt vom Schüler mehr als er lehrt.
    In jeder Frage liegt bereits die Antwort verborgen.
    Das tiefste Schweigen spricht die klarste Wahrheit.
    """
    
    ergebnis = tool.verarbeite_text(text)
    
    print("Erweiterte Paradox-Erkennung:")
    print(f"Paradoxe gefunden: {len(ergebnis['paradoxe'])}")
    
    # Gruppiere nach Typ
    nach_typ = {}
    for p in ergebnis['paradoxe']:
        typ = p.typ.value
        if typ not in nach_typ:
            nach_typ[typ] = []
        nach_typ[typ].append(f"{p.element1} {p.beziehung} {p.element2}")
    
    for typ, paradoxe in nach_typ.items():
        print(f"\n{typ}:")
        for p in paradoxe:
            print(f"  - {p}")
    
    print(f"\nMächtigste Frage: {ergebnis['beste_frage'].frage}")

# Hauptprogramm
if __name__ == "__main__":
    print("MEISTER FRAGE TOOL - Demonstrationen")
    print("="*50)
    print("Stand: 12. Tammus 5785")
    print("WWAK-konform\n")
    
    # Führe alle Demos aus
    demo_basis()
    demo_rabash_integration()
    demo_meditation_karten()
    demo_wochen_programm()
    demo_batch_analyse()
    demo_custom_paradox()
    
    print("\n✨ Alle Demonstrationen abgeschlossen!")
    print("\nErstelle Dateien:")
    print("  - meditation_karten.yaml")
    print("  - wochen_programm.md")
    print("  - meister_analyse.yaml")
    print("  - meister_analyse.md")
    print("  - meister_analyse.json")
    
    print("\nQ! = Die Frage öffnet, was keine Antwort öffnen kann!")
