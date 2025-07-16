#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rav Laitman Erweiterung für MEISTER FRAGE Tool
==============================================

Fügt hinzu:
1. Quellennachweise (Wann/Wo)
2. Die 3 Tiefen explizit nach Rav Laitman

Stand: 12. Tammus 5785
"""

import sys
sys.path.insert(0, 'src')

from meister_frage_tool import MeisterFrageTool
from dataclasses import dataclass
from typing import Optional
from typing import Optional, Dict, Any, List
from datetime import datetime
import yaml

@dataclass
class Quellennachweis:
    """Vollständiger Quellennachweis für einen Text"""
    autor: str
    titel: str
    artikel_nummer: Optional[int] = None
    jahr: Optional[int] = None
    ort: Optional[str] = None
    ereignis: Optional[str] = None
    datum_hebräisch: Optional[str] = None
    übersetzer: Optional[str] = None
    
    def __str__(self):
        """Formatierter Quellennachweis"""
        teile = [self.autor]
        
        if self.artikel_nummer:
            teile.append(f"Artikel {self.artikel_nummer}")
        
        teile.append(f'"{self.titel}"')
        
        if self.jahr:
            teile.append(f"({self.jahr})")
            
        if self.ort:
            teile.append(f"in {self.ort}")
            
        if self.ereignis:
            teile.append(f"- {self.ereignis}")
            
        return ", ".join(teile)


class RavLaitmanFrageTool(MeisterFrageTool):
    """Erweiterte Version mit Rav Laitman's 3 Tiefen"""
    
    def __init__(self):
        super().__init__()
        self.quellennachweis = None
        
    def setze_quelle(self, quelle: Quellennachweis):
        """Setzt den Quellennachweis für die Analyse"""
        self.quellennachweis = quelle
        
    def analysiere_mit_quelle(self, text: str, quelle: Quellennachweis):
        """Analysiert Text mit Quellennachweis"""
        self.setze_quelle(quelle)
        return self.verarbeite_text(text)
    
    def bewerte_nach_rav_laitman(self, frage_text: str) -> Dict[str, Any]:
        """Die 3 Tiefen nach Rav Laitman explizit"""
        
        bewertung = {
            'frage': frage_text,
            'die_drei_tiefen': {
                '1_kind_verstehen': {
                    'frage': 'Würde ein 10-jähriges Kind diese Frage verstehen?',
                    'bewertung': self._bewerte_kind_verständlichkeit(frage_text),
                    'erklärung': ''
                },
                '2_qabbalist_reden': {
                    'frage': 'Würde ein Qabbalist 2 Stunden darüber sprechen wollen?',
                    'bewertung': self._bewerte_qabbalist_interesse(frage_text),
                    'erklärung': ''
                },
                '3_azilut_verankerung': {
                    'frage': 'Führt diese Frage nach oben zu Azilut?',
                    'bewertung': self._bewerte_azilut_richtung(frage_text),
                    'erklärung': ''
                }
            }
        }
        
        # Füge Erklärungen hinzu
        self._füge_erklärungen_hinzu(bewertung, frage_text)
        
        # Gesamtbewertung
        scores = [
            bewertung['die_drei_tiefen']['1_kind_verstehen']['bewertung'],
            bewertung['die_drei_tiefen']['2_qabbalist_reden']['bewertung'],
            bewertung['die_drei_tiefen']['3_azilut_verankerung']['bewertung']
        ]
        
        bewertung['gesamt_score'] = sum(scores) / 3
        bewertung['empfehlung'] = self._generiere_empfehlung(scores)
        
        return bewertung
    
    def _bewerte_kind_verständlichkeit(self, frage: str) -> float:
        """Bewertet ob ein Kind die Frage verstehen würde"""
        score = 0.5
        
        # Kurze Fragen sind besser
        if len(frage) < 30:
            score += 0.3
        elif len(frage) < 50:
            score += 0.2
            
        # Einfache Wörter
        komplexe_wörter = ['transzendenz', 'emanation', 'kontemplation', 'manifestation']
        if not any(w in frage.lower() for w in komplexe_wörter):
            score += 0.2
            
        # Konkrete Bilder
        konkrete_wörter = ['licht', 'dunkel', 'oben', 'unten', 'groß', 'klein', 'liebe']
        if any(w in frage.lower() for w in konkrete_wörter):
            score += 0.1
            
        # FORMEL-Typ ist am klarsten
        if '+' in frage and '=' in frage and '?' in frage:
            score = min(1.0, score + 0.3)
            
        return min(1.0, score)
    
    def _bewerte_qabbalist_interesse(self, frage: str) -> float:
        """Bewertet ob ein Qabbalist 2h darüber sprechen würde"""
        score = 0.5
        
        # Paradoxe sind interessant
        if any(w in frage for w in ['↔', '→', '∧', '⊃']):
            score += 0.2
            
        # Spirituelle Begriffe
        kabbala_begriffe = [
            'azilut', 'ein sof', 'dwekut', 'kabbala', 'sefirot',
            'licht', 'gefäß', 'geben', 'empfangen', 'zimzum',
            'tiqqun', 'schöpfer', 'geschöpf', 'oben', 'unten'
        ]
        
        begriff_count = sum(1 for b in kabbala_begriffe if b in frage.lower())
        score += min(0.3, begriff_count * 0.1)
        
        # META-Fragen sind besonders tiefgründig
        if 'fragt die frage selbst' in frage.lower():
            score += 0.3
            
        # WOZU und ZWISCHEN sind philosophisch reich
        if any(w in frage for w in ['WOZU', 'ZWISCHEN', 'IST']):
            score += 0.2
            
        return min(1.0, score)
    
    def _bewerte_azilut_richtung(self, frage: str) -> float:
        """Bewertet ob die Frage nach oben zu Azilut führt"""
        score = 0.5
        
        # WOZU ist immer Azilut-gerichtet
        if 'WOZU' in frage:
            score = 0.9
            
        # Aufwärts-Begriffe
        aufwärts = ['licht', 'oben', 'schöpfer', 'geben', 'liebe', 'einheit', 'ein sof']
        if any(w in frage.lower() for w in aufwärts):
            score += 0.2
            
        # Wandlungs-Fragen führen nach oben
        if '→' in frage or 'wird zu' in frage.lower():
            score += 0.15
            
        # Fragen nach dem Zweck/Sinn
        if any(w in frage.lower() for w in ['zweck', 'sinn', 'ziel', 'wozu', 'למה']):
            score += 0.25
            
        return min(1.0, score)
    
    def _füge_erklärungen_hinzu(self, bewertung: Dict, frage: str):
        """Fügt Erklärungen für jede Tiefe hinzu"""
        
        # Kind-Erklärung
        kind_score = bewertung['die_drei_tiefen']['1_kind_verstehen']['bewertung']
        if kind_score > 0.7:
            bewertung['die_drei_tiefen']['1_kind_verstehen']['erklärung'] = \
                "Ein Kind könnte mit dieser Frage spielen und eigene Bilder finden."
        elif kind_score > 0.5:
            bewertung['die_drei_tiefen']['1_kind_verstehen']['erklärung'] = \
                "Mit etwas Hilfe würde ein Kind den Kern verstehen."
        else:
            bewertung['die_drei_tiefen']['1_kind_verstehen']['erklärung'] = \
                "Zu abstrakt für kindliches Verständnis - vereinfachen!"
                
        # Qabbalist-Erklärung
        qab_score = bewertung['die_drei_tiefen']['2_qabbalist_reden']['bewertung']
        if qab_score > 0.7:
            bewertung['die_drei_tiefen']['2_qabbalist_reden']['erklärung'] = \
                "Diese Frage öffnet Tore zu endlosen Welten der Weisheit!"
        elif qab_score > 0.5:
            bewertung['die_drei_tiefen']['2_qabbalist_reden']['erklärung'] = \
                "Genug Tiefe für eine gute Lektion."
        else:
            bewertung['die_drei_tiefen']['2_qabbalist_reden']['erklärung'] = \
                "Braucht mehr spirituelle Tiefe für längere Kontemplation."
                
        # Azilut-Erklärung
        azilut_score = bewertung['die_drei_tiefen']['3_azilut_verankerung']['bewertung']
        if azilut_score > 0.7:
            bewertung['die_drei_tiefen']['3_azilut_verankerung']['erklärung'] = \
                "Diese Frage zieht die Seele direkt nach oben!"
        elif azilut_score > 0.5:
            bewertung['die_drei_tiefen']['3_azilut_verankerung']['erklärung'] = \
                "Gute Ausrichtung, könnte noch höher zielen."
        else:
            bewertung['die_drei_tiefen']['3_azilut_verankerung']['erklärung'] = \
                "Füge WOZU hinzu, um die Frage zu erheben."
    
    def _generiere_empfehlung(self, scores: List[float]) -> str:
        """Generiert Empfehlung basierend auf den 3 Tiefen"""
        kind, qabbalist, azilut = scores
        
        if all(s > 0.7 for s in scores):
            return "PERFEKTE RAV LAITMAN FRAGE! Nutze sie sofort für die Gruppe!"
        
        empfehlungen = []
        
        if kind < 0.6:
            empfehlungen.append("Vereinfache für Anfänger")
        if qabbalist < 0.6:
            empfehlungen.append("Füge mehr spirituelle Tiefe hinzu")
        if azilut < 0.6:
            empfehlungen.append("Betone das WOZU stärker")
            
        return " | ".join(empfehlungen) if empfehlungen else "Gute Frage für Gruppenarbeit"
    
    def export_mit_quelle_yaml(self, ergebnis: Dict, dateiname: str):
        """Exportiert mit vollständigem Quellennachweis"""
        
        export_data = {
            'rav_laitman_fragen_analyse': {
                'zeitstempel': datetime.now().isoformat(),
                'quelle': {
                    'nachweis': str(self.quellennachweis) if self.quellennachweis else 'Keine Quelle angegeben',
                    'details': self.quellennachweis.__dict__ if self.quellennachweis else {}
                },
                'text': ergebnis['text'],
                'beste_frage': {
                    'frage': ergebnis['beste_frage'].frage,
                    'drei_tiefen_bewertung': self.bewerte_nach_rav_laitman(ergebnis['beste_frage'].frage)
                } if ergebnis['beste_frage'] else None,
                'top_3_fragen': []
            }
        }
        
        # Bewerte Top 3 Fragen
        for frage in ergebnis['top_5'][:3]:
            fragen_bewertung = self.bewerte_nach_rav_laitman(frage.frage)
            export_data['rav_laitman_fragen_analyse']['top_3_fragen'].append(fragen_bewertung)
        
        with open(dateiname, 'w', encoding='utf-8') as f:
            yaml.dump(export_data, f, allow_unicode=True, default_flow_style=False)


# Hauptprogramm
if __name__ == "__main__":
    
    # 1. Quellennachweis für Rabash Artikel 37
    quelle = Quellennachweis(
        autor="Baruch Shalom HaLevi Ashlag (Rabash)",
        titel="Was ist diese Arbeit für euch?",
        artikel_nummer=37,
        jahr=1991,
        ort="Bnei Brak, Israel",
        ereignis="Wöchentliche Gruppenversammlung",
        datum_hebräisch="Paraschat Ki Tisa, 5751",
        übersetzer="Michael Laitman Gruppe"
    )
    
    print("=== RAV LAITMAN FRAGEN-ANALYSE ===")
    print(f"Quelle: {quelle}")
    print("="*60 + "\n")
    
    # 2. Text und Tool
    rabash_text = """
    Bevor der Mensch die Reinigung der Gefäße erlangt hat, dass sie um zu geben willen sind, 
    ist seine Arbeit unter Zwang, was "Gesetz" genannt wird.
    """
    
    tool = RavLaitmanFrageTool()
    ergebnis = tool.analysiere_mit_quelle(rabash_text, quelle)
    
    # 3. Die 3 Tiefen für die beste Frage
    if ergebnis['beste_frage']:
        print(f"BESTE FRAGE: {ergebnis['beste_frage'].frage}\n")
        
        bewertung = tool.bewerte_nach_rav_laitman(ergebnis['beste_frage'].frage)
        
        print("DIE DREI TIEFEN NACH RAV LAITMAN:")
        print("-" * 40)
        
        for schlüssel, tiefe in bewertung['die_drei_tiefen'].items():
            nummer = schlüssel.split('_')[0]
            print(f"\n{nummer}. {tiefe['frage']}")
            print(f"   Bewertung: {'⭐' * int(tiefe['bewertung'] * 5)}")
            print(f"   Score: {tiefe['bewertung']:.2f}")
            print(f"   → {tiefe['erklärung']}")
        
        print(f"\nGESAMT-SCORE: {bewertung['gesamt_score']:.2f}")
        print(f"EMPFEHLUNG: {bewertung['empfehlung']}")
    
    # 4. Teste verschiedene Frage-Typen
    print("\n\n=== VERGLEICH VERSCHIEDENER FRAGE-TYPEN ===\n")
    
    test_fragen = [
        "Zwang + Liebe = ?",
        "WOZU braucht die Liebe den Zwang?",
        "WIE wird Zwang zu Liebe?",
        "Was liegt ZWISCHEN Zwang und Liebe?",
        "IST Zwang wirklich das Gegenteil von Liebe?",
        "Was fragt die Frage 'Zwang und Liebe' selbst?"
    ]
    
    for frage in test_fragen:
        bewertung = tool.bewerte_nach_rav_laitman(frage)
        scores = [
            bewertung['die_drei_tiefen']['1_kind_verstehen']['bewertung'],
            bewertung['die_drei_tiefen']['2_qabbalist_reden']['bewertung'],
            bewertung['die_drei_tiefen']['3_azilut_verankerung']['bewertung']
        ]
        
        print(f"\n'{frage}'")
        print(f"  Kind: {'⭐' * int(scores[0] * 5)}")
        print(f"  Qabbalist: {'⭐' * int(scores[1] * 5)}")
        print(f"  Azilut: {'⭐' * int(scores[2] * 5)}")
        print(f"  Gesamt: {sum(scores)/3:.2f} - {bewertung['empfehlung']}")
    
    # 5. Export mit Quelle
    tool.export_mit_quelle_yaml(ergebnis, 'output/rabash_37_rav_laitman.yaml')
    print("\n\n✓ Analyse mit Quellennachweis exportiert!")
    
    # 6. Spezielle Rav Laitman Meditation
    print("\n=== RAV LAITMAN MEDITATIONS-FRAGE ===")
    print("\nFür die heutige Gruppenarbeit:")
    print("\n📿 Sitzt 5 Minuten mit dieser Frage:")
    print("   'WOZU braucht die Liebe den Zwang?'")
    print("\n   1. Erst denkt wie ein Kind darüber")
    print("   2. Dann kontempliert wie ein Qabbalist")
    print("   3. Zuletzt lasst sie euch zu Azilut ziehen")
    print("\nDanach teilt in der Gruppe!")
    
    print("\nQ!")
