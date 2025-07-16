#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEISTER FRAGE Tool - Paradoxe als Tore zu Meister-Fragen
=======================================================

Findet Paradoxe und generiert die 3 Tiefen der Fragen:
1. Klärung: "X + Y = ?"
2. Essenz: "WOZU braucht X das Y?"  
3. Wandlung: "WIE wird X zu Y?"

Stand: 8. Tammus 5785
WWAQ-konform mit korrekter Transliteration
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import re
from datetime import datetime

# WWAQ-konforme Imports
try:
    from meister_transliteration import MeisterTransliteration
except ImportError:
    print("Warnung: meister_transliteration nicht gefunden")
    MeisterTransliteration = None


class FragenTiefe(Enum):
    """Die drei Tiefen der Meister-Fragen"""
    KLÄRUNG = ("Klärung", "X + Y = ?", "Was entsteht aus der Vereinigung?")
    ESSENZ = ("Essenz", "WOZU braucht X das Y?", "Welcher höhere Zweck vereint sie?")
    WANDLUNG = ("Wandlung", "WIE wird X zu Y?", "Durch welche Transformation?")


@dataclass
class Paradox:
    """Ein erkanntes Paradox"""
    begriff1: str
    begriff2: str
    kontext: str
    typ: str  # KLASSISCH, DYNAMISCH, VERBORGEN
    quelle_satz: str


@dataclass  
class MeisterFrage:
    """Eine generierte Meister-Frage"""
    paradox: Paradox
    tiefe: FragenTiefe
    frage: str
    erläuterung: str
    qabbalistischer_hinweis: Optional[str] = None


class MeisterFrageTool:
    """Hauptklasse für Paradox-Erkennung und Fragen-Generierung"""
    
    # Klassische Paradox-Paare (erweitert)
    PARADOX_PAARE = {
        # Grundlegende Gegensätze
        ('licht', 'dunkelheit'): 'KLASSISCH',
        ('or', 'choschech'): 'KLASSISCH',
        ('אור', 'חושך'): 'KLASSISCH',
        
        ('geben', 'empfangen'): 'KLASSISCH',
        ('gebender', 'empfänger'): 'KLASSISCH',
        ('maschpia', 'meqabel'): 'KLASSISCH',
        ('משפיע', 'מקבל'): 'KLASSISCH',
        
        ('liebe', 'zwang'): 'KLASSISCH',
        ('freiheit', 'notwendigkeit'): 'KLASSISCH',
        ('wahl', 'bestimmung'): 'KLASSISCH',
        
        ('einheit', 'vielheit'): 'KLASSISCH',
        ('achdut', 'ribbui'): 'KLASSISCH',
        ('אחדות', 'ריבוי'): 'KLASSISCH',
        
        ('fülle', 'mangel'): 'KLASSISCH',
        ('schlemut', 'chissaron'): 'KLASSISCH',
        ('שלמות', 'חסרון'): 'KLASSISCH',
        
        ('unendlich', 'endlich'): 'KLASSISCH',
        ('ein sof', 'gwul'): 'KLASSISCH',
        ('אין סוף', 'גבול'): 'KLASSISCH',
        
        # Qabbalistische Paare
        ('zimzum', 'hitpaschut'): 'KLASSISCH',
        ('kontraktion', 'ausdehnung'): 'KLASSISCH',
        
        ('or', 'qli'): 'KLASSISCH',
        ('licht', 'gefäß'): 'KLASSISCH',
        
        ('pnimi', 'chizoni'): 'KLASSISCH',
        ('innerlich', 'äußerlich'): 'KLASSISCH',
        
        ('reschit', 'achrit'): 'KLASSISCH',
        ('anfang', 'ende'): 'KLASSISCH',
        
        # Emotionale Paare
        ('freude', 'schmerz'): 'KLASSISCH',
        ('hoffnung', 'verzweiflung'): 'KLASSISCH',
        ('mut', 'angst'): 'KLASSISCH',
        ('vertrauen', 'zweifel'): 'KLASSISCH',
        
        # WWAQ-spezifisch
        ('bindung', 'freiheit'): 'KLASSISCH',
        ('anbindung', 'loslösung'): 'KLASSISCH',
        ('dwekut', 'hafrada'): 'KLASSISCH',
        ('דבקות', 'הפרדה'): 'KLASSISCH',
    }
    
    # Trigger-Wörter für dynamische Paradoxe
    PARADOX_TRIGGER = {
        'gleichzeitig': ['und', 'aber', 'dennoch', 'trotzdem'],
        'zwischen': ['und', 'sowie', 'bis'],
        'sowohl': ['als auch'],
        'weder': ['noch'],
        'je mehr': ['desto'],
        'einerseits': ['andererseits'],
    }
    
    def __init__(self):
        self.erkannte_paradoxe: List[Paradox] = []
        self.generierte_fragen: List[MeisterFrage] = []
        
        # Transliteration wenn verfügbar
        if MeisterTransliteration:
            self.transliteration = MeisterTransliteration()
            # Erweitere Paradox-Paare
            self.PARADOX_PAARE.update(self.transliteration.generiere_paradox_begriffe())
        else:
            self.transliteration = None
    
    def analysiere_text(self, text: str) -> List[Paradox]:
        """Hauptmethode: Findet alle Paradoxe im Text"""
        self.erkannte_paradoxe = []
        
        # Text vorbereiten
        if self.transliteration:
            text = self.transliteration.korrigiere_deutsche_begriffe(text)
        
        # Satzweise analysieren
        sätze = self._segmentiere_sätze(text)
        
        for satz in sätze:
            # 1. Klassische Paradoxe
            self._finde_klassische_paradoxe(satz)
            
            # 2. Dynamische Paradoxe
            self._finde_dynamische_paradoxe(satz)
            
            # 3. Verborgene Paradoxe
            self._finde_verborgene_paradoxe(satz)
        
        return self.erkannte_paradoxe
    
    def _segmentiere_sätze(self, text: str) -> List[str]:
        """Intelligente Satz-Segmentierung"""
        # Einfache Segmentierung, kann erweitert werden
        sätze = re.split(r'[.!?]+', text)
        return [s.strip() for s in sätze if s.strip()]
    
    def _finde_klassische_paradoxe(self, satz: str) -> None:
        """Findet vordefinierte Paradox-Paare"""
        satz_lower = satz.lower()
        wörter = set(re.findall(r'\b\w+\b', satz_lower))
        
        # Prüfe alle bekannten Paare
        for (begriff1, begriff2), typ in self.PARADOX_PAARE.items():
            if begriff1 in wörter and begriff2 in wörter:
                # Extrahiere Kontext
                kontext = self._extrahiere_kontext(satz, begriff1, begriff2)
                
                paradox = Paradox(
                    begriff1=begriff1,
                    begriff2=begriff2,
                    kontext=kontext,
                    typ=typ,
                    quelle_satz=satz
                )
                
                # Vermeidet Duplikate
                if not self._ist_duplikat(paradox):
                    self.erkannte_paradoxe.append(paradox)
    
    def _finde_dynamische_paradoxe(self, satz: str) -> None:
        """Findet Paradoxe durch Trigger-Wörter"""
        satz_lower = satz.lower()
        
        for trigger, markers in self.PARADOX_TRIGGER.items():
            if trigger in satz_lower:
                # Suche nach Marker-Wörtern
                for marker in markers:
                    pattern = f"{trigger}.*?{marker}"
                    matches = re.finditer(pattern, satz_lower)
                    
                    for match in matches:
                        # Extrahiere die beiden Seiten
                        vorher = satz_lower[:match.start()].split()[-3:]
                        nachher = satz_lower[match.end():].split()[:3]
                        
                        if vorher and nachher:
                            begriff1 = ' '.join(vorher).strip()
                            begriff2 = ' '.join(nachher).strip()
                            
                            paradox = Paradox(
                                begriff1=begriff1,
                                begriff2=begriff2,
                                kontext=match.group(),
                                typ='DYNAMISCH',
                                quelle_satz=satz
                            )
                            
                            if not self._ist_duplikat(paradox):
                                self.erkannte_paradoxe.append(paradox)
    
    def _finde_verborgene_paradoxe(self, satz: str) -> None:
        """Findet implizite Paradoxe durch semantische Analyse"""
        # Vereinfachte Version - kann mit NLP erweitert werden
        
        # Suche nach Negationen gefolgt von Affirmationen
        negations_pattern = r'\b(nicht?|kein|ohne|niemals?)\s+(\w+).*?\b(aber|dennoch|trotzdem|doch)\s+(\w+)'
        matches = re.finditer(negations_pattern, satz.lower())
        
        for match in matches:
            negation = match.group(1)
            negiertes = match.group(2)
            verbinder = match.group(3)
            affirmiertes = match.group(4)
            
            paradox = Paradox(
                begriff1=f"{negation} {negiertes}",
                begriff2=affirmiertes,
                kontext=match.group(),
                typ='VERBORGEN',
                quelle_satz=satz
            )
            
            if not self._ist_duplikat(paradox):
                self.erkannte_paradoxe.append(paradox)
    
    def _extrahiere_kontext(self, satz: str, begriff1: str, begriff2: str) -> str:
        """Extrahiert relevanten Kontext um die Begriffe"""
        # Finde Positionen
        pos1 = satz.lower().find(begriff1.lower())
        pos2 = satz.lower().find(begriff2.lower())
        
        if pos1 == -1 or pos2 == -1:
            return satz
        
        # Bestimme Kontext-Grenzen
        start = max(0, min(pos1, pos2) - 20)
        end = min(len(satz), max(pos1 + len(begriff1), pos2 + len(begriff2)) + 20)
        
        kontext = satz[start:end]
        
        # Füge ... hinzu wenn gekürzt
        if start > 0:
            kontext = "..." + kontext
        if end < len(satz):
            kontext = kontext + "..."
        
        return kontext
    
    def _ist_duplikat(self, paradox: Paradox) -> bool:
        """Prüft ob Paradox bereits erkannt wurde"""
        for p in self.erkannte_paradoxe:
            # Prüfe beide Richtungen
            if ((p.begriff1 == paradox.begriff1 and p.begriff2 == paradox.begriff2) or
                (p.begriff1 == paradox.begriff2 and p.begriff2 == paradox.begriff1)):
                return True
        return False
    
    def generiere_meister_fragen(self, paradoxe: Optional[List[Paradox]] = None) -> List[MeisterFrage]:
        """Generiert alle 3 Fragen-Tiefen für jedes Paradox"""
        if paradoxe is None:
            paradoxe = self.erkannte_paradoxe
        
        self.generierte_fragen = []
        
        for paradox in paradoxe:
            # Generiere alle 3 Tiefen
            for tiefe in FragenTiefe:
                frage = self._generiere_frage(paradox, tiefe)
                self.generierte_fragen.append(frage)
        
        return self.generierte_fragen
    
    def _generiere_frage(self, paradox: Paradox, tiefe: FragenTiefe) -> MeisterFrage:
        """Generiert eine spezifische Frage für ein Paradox"""
        b1 = paradox.begriff1.title()
        b2 = paradox.begriff2.title()
        
        if tiefe == FragenTiefe.KLÄRUNG:
            frage = f"{b1} + {b2} = ?"
            erläuterung = f"Was entsteht, wenn {b1} und {b2} sich vereinen?"
            hinweis = self._generiere_klärung_hinweis(paradox)
            
        elif tiefe == FragenTiefe.ESSENZ:
            frage = f"WOZU braucht {b1} das {b2}?"
            erläuterung = f"Welcher höhere Zweck vereint {b1} mit {b2}?"
            hinweis = self._generiere_essenz_hinweis(paradox)
            
        else:  # WANDLUNG
            frage = f"WIE wird {b1} zu {b2}?"
            erläuterung = f"Durch welche Transformation wandelt sich {b1} in {b2}?"
            hinweis = self._generiere_wandlung_hinweis(paradox)
        
        return MeisterFrage(
            paradox=paradox,
            tiefe=tiefe,
            frage=frage,
            erläuterung=erläuterung,
            qabbalistischer_hinweis=hinweis
        )
    
    def _generiere_klärung_hinweis(self, paradox: Paradox) -> str:
        """Generiert qabbalistischen Hinweis für Klärung"""
        hinweise = {
            ('licht', 'dunkelheit'): "Im Zimzum entsteht der Raum für Schöpfung",
            ('geben', 'empfangen'): "Der mittlere Pfad - Empfangen um zu Geben",
            ('liebe', 'zwang'): "Dwekut - die freie Wahl zur Anbindung",
            ('einheit', 'vielheit'): "Die Sefirot - Vielheit in vollkommener Einheit",
            ('fülle', 'mangel'): "Das Qli wird durch Chissaron zum Empfänger des Or",
        }
        
        # Suche passenden Hinweis
        for (b1, b2), hinweis in hinweise.items():
            if (paradox.begriff1.lower() == b1 and paradox.begriff2.lower() == b2) or \
               (paradox.begriff1.lower() == b2 and paradox.begriff2.lower() == b1):
                return hinweis
        
        # Standard-Hinweis
        return "Die höhere Einheit offenbart sich im Dritten"
    
    def _generiere_essenz_hinweis(self, paradox: Paradox) -> str:
        """Generiert qabbalistischen Hinweis für Essenz"""
        # Kann erweitert werden mit spezifischen Hinweisen
        return "LeMa'an Ma? - Zur Offenbarung des verborgenen Lichts"
    
    def _generiere_wandlung_hinweis(self, paradox: Paradox) -> str:
        """Generiert qabbalistischen Hinweis für Wandlung"""
        # Kann erweitert werden mit spezifischen Hinweisen
        return "Durch Birur - die Klärung und Erhebung der Funken"
    
    def generiere_bericht(self) -> str:
        """Generiert formatierten Bericht aller Funde"""
        bericht = []
        bericht.append("=== MEISTER FRAGE TOOL BERICHT ===")
        bericht.append(f"Stand: {datetime.now().strftime('%d. Tammus 5785, MESZ %H:%M')}")
        bericht.append("")
        
        # Paradoxe
        bericht.append(f"GEFUNDENE PARADOXE: {len(self.erkannte_paradoxe)}")
        bericht.append("-" * 40)
        
        for i, paradox in enumerate(self.erkannte_paradoxe, 1):
            bericht.append(f"\n{i}. PARADOX [{paradox.typ}]")
            bericht.append(f"   '{paradox.begriff1}' ←→ '{paradox.begriff2}'")
            bericht.append(f"   Kontext: {paradox.kontext}")
        
        # Fragen
        bericht.append(f"\n\nGENERIERTE MEISTER-FRAGEN: {len(self.generierte_fragen)}")
        bericht.append("=" * 40)
        
        # Gruppiere nach Paradox
        for paradox in self.erkannte_paradoxe:
            paradox_fragen = [f for f in self.generierte_fragen if f.paradox == paradox]
            
            if paradox_fragen:
                bericht.append(f"\nPARADOX: {paradox.begriff1} ←→ {paradox.begriff2}")
                bericht.append("-" * 30)
                
                for frage in paradox_fragen:
                    bericht.append(f"\n[{frage.tiefe.value[0]}]")
                    bericht.append(f"FRAGE: {frage.frage}")
                    bericht.append(f"→ {frage.erläuterung}")
                    if frage.qabbalistischer_hinweis:
                        bericht.append(f"✡ {frage.qabbalistischer_hinweis}")
        
        bericht.append("\nQ!")
        return "\n".join(bericht)


# TEST-FUNKTIONEN
def teste_meister_tool():
    """Testet das MEISTER FRAGE Tool mit verschiedenen Beispielen"""
    print("=== TEST: MEISTER FRAGE TOOL ===")
    print("Stand: 8. Tammus 5785\n")
    
    tool = MeisterFrageTool()
    
    # Test 1: Einfache Paradoxe
    print("TEST 1: Klassische Paradoxe")
    print("-" * 40)
    
    text1 = """
    Die Qabbala lehrt uns, dass Licht und Dunkelheit zusammengehören.
    Der Zwang der Mizwot führt paradoxerweise zur wahren Freiheit.
    In der Liebe finden wir gleichzeitig Bindung und Befreiung.
    """
    
    paradoxe1 = tool.analysiere_text(text1)
    fragen1 = tool.generiere_meister_fragen(paradoxe1)
    
    print(f"Gefunden: {len(paradoxe1)} Paradoxe")
    for p in paradoxe1:
        print(f"  • {p.begriff1} ←→ {p.begriff2}")
    
    # Test 2: Die 3 Tiefen
    print("\n\nTEST 2: Die 3 Tiefen am Beispiel 'Zwang + Liebe'")
    print("-" * 40)
    
    # Manuell ein Paradox erstellen
    zwang_liebe = Paradox(
        begriff1="Zwang",
        begriff2="Liebe", 
        kontext="Der Zwang führt zur Liebe",
        typ="KLASSISCH",
        quelle_satz="Test"
    )
    
    fragen = tool.generiere_meister_fragen([zwang_liebe])
    
    for frage in fragen:
        print(f"\n[{frage.tiefe.value[0]}]")
        print(f"FRAGE: {frage.frage}")
        print(f"→ {frage.erläuterung}")
        if frage.qabbalistischer_hinweis:
            print(f"✡ {frage.qabbalistischer_hinweis}")
    
    # Test 3: Komplexer Text
    print("\n\nTEST 3: Komplexer qabbalistischer Text")
    print("-" * 40)
    
    text3 = """
    In der Lehre vom Zimzum sehen wir, wie die Kontraktion zur Ausdehnung führt.
    Das unendliche Licht muss sich verbergen, damit das endliche Gefäß es empfangen kann.
    Je mehr wir geben, desto mehr können wir empfangen - dies ist das Geheimnis
    des Empfangens um zu Geben. Die Dunkelheit ist nicht die Abwesenheit von Licht,
    sondern seine Verhüllung zum Zweck der Offenbarung.
    
    Zwischen Anfang und Ende liegt die gesamte Schöpfung, und doch sind
    Reschit und Achrit eins im Gedanken des Schöpfers. Die Vielheit der
    Sefirot offenbart die absolute Einheit, und im Mangel (Chissaron) 
    entdecken wir die wahre Fülle (Schlemut).
    """
    
    paradoxe3 = tool.analysiere_text(text3)
    print(f"\nGefundene Paradoxe: {len(paradoxe3)}")
    
    for p in paradoxe3:
        print(f"\n• {p.begriff1} ←→ {p.begriff2}")
        print(f"  Typ: {p.typ}")
        print(f"  Kontext: {p.kontext}")
    
    # Generiere Bericht
    print("\n\n" + "=" * 60)
    tool.generiere_meister_fragen()
    print(tool.generiere_bericht())


# HAUPT-AUSFÜHRUNG
if __name__ == "__main__":
    # Führe Tests aus
    teste_meister_tool()
    
    print("\n\n=== IHRE EIGENEN TESTS ===")
    print("Führen Sie nun Ihre Tests aus:\n")
    
    # Ihre spezifischen Tests
    tool = MeisterFrageTool()
    
    test_fragen = [
        "Zwang + Liebe = ?",
        "WOZU braucht die Liebe den Zwang?", 
        "WIE wird Zwang zu Liebe?"
    ]
    
    print("Analyse Ihrer Test-Fragen:")
    for frage in test_fragen:
        print(f"\nFrage: {frage}")
        # Hier können Sie spezifische Analysen hinzufügen
    
    # Beispiel mit Ihrem Text
    ihr_text = "Die Liebe braucht den Zwang, wie das Licht die Dunkelheit braucht."
    paradoxe = tool.analysiere_text(ihr_text)
    fragen = tool.generiere_meister_fragen(paradoxe)
    
    print(f"\nAus Ihrem Text generiert:")
    for f in fragen:
        print(f"  • {f.frage}")
    
    print("\nQ!")
