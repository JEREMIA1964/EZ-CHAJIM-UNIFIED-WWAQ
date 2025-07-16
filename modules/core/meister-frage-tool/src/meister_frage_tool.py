#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ez Chajim MEISTER FRAGE TOOL
===========================

Paradox-Erkennung und Fragen-Generation für spirituelle Texte
Stand: 12. Tammus 5785
WWAK-konform

Autor: JEREMIA1964 / JBR Wolff
"""

import re
import yaml
import json
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
from datetime import datetime
import hashlib
# Nach den anderen Imports, vor class ParadoxTyp:
try:
    from meister_transliteration import MeisterTransliteration
except ImportError:
    MeisterTransliteration = None

class ParadoxTyp(Enum):
    """Kategorien von Paradoxen"""
    KLASSISCH = "Klassische Gegensätze"          # Licht ↔ Dunkelheit
    EINSCHLUSS = "Einschluss-Paradoxe"          # Im Kleinen das Große
    WANDLUNG = "Wandlungs-Paradoxe"             # Zwang → Liebe  
    SIMULTAN = "Simultane Paradoxe"             # A und B zugleich
    HIERARCHIE = "Hierarchie-Paradoxe"          # Oben ist Unten
    IDENTITÄT = "Identitäts-Paradoxe"           # A ist B und Nicht-B
    REZIPROK = "Reziproke Paradoxe"             # Gebender wird Empfänger

class FrageTyp(Enum):
    """Die 7 Meister-Frage-Typen"""
    FORMEL = "X + Y = ?"                         # Mathematisch klar
    WOZU = "WOZU braucht X das Y?"             # Azilut-verankert
    WIE = "WIE wird X zu Y?"                    # Prozess-fokussiert
    WENN_DANN = "WENN X → DANN Y?"             # Bedingt
    IST = "IST X wirklich Y?"                  # Seins-Frage
    ZWISCHEN = "Was liegt ZWISCHEN X und Y?"    # Raum-Frage
    META = "Was fragt die Frage selbst?"       # Meta-Ebene

@dataclass
class Paradox:
    """Ein erkanntes Paradox"""
    element1: str
    element2: str
    beziehung: str  # "↔", "→", "⊃", "∧", "≡", "≠"
    typ: ParadoxTyp
    kontext: str
    stärke: float = 0.0

@dataclass
class MeisterFrage:
    """Eine generierte Meister-Frage"""
    frage: str
    typ: FrageTyp
    paradox: Paradox
    scores: Dict[str, float] = field(default_factory=dict)
    
    @property
    def gesamt_score(self) -> float:
        """Berechnet Gesamt-Score"""
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)

class MeisterFrageTool:
    """Das ultimative Paradox-Frage-Tool"""
    
    # Paradox-Indikatoren
    GEGENSATZ_MUSTER = {
        # Explizite Gegensätze
        r'(\w+)\s+und\s+(\w+)\s+zugleich': '∧',
        r'sowohl\s+(\w+)\s+als\s+auch\s+(\w+)': '∧',
        r'(\w+)\s+oder\s+(\w+)': '∨',
        r'weder\s+(\w+)\s+noch\s+(\w+)': '¬∧¬',
        r'(\w+)\s+statt\s+(\w+)': '↔',
        r'(\w+)\s+versus\s+(\w+)': '↔',
        
        # Wandlungen
        r'(\w+)\s+wird\s+zu\s+(\w+)': '→',
        r'aus\s+(\w+)\s+wird\s+(\w+)': '→',
        r'(\w+)\s+führt\s+zu\s+(\w+)': '→',
        r'durch\s+(\w+)\s+entsteht\s+(\w+)': '→',
        
        # Einschlüsse
        r'im\s+(\w+)\s+das\s+(\w+)': '⊃',
        r'(\w+)\s+enthält\s+(\w+)': '⊃',
        r'(\w+)\s+umfasst\s+(\w+)': '⊃',
        
        # Identitäten
        r'(\w+)\s+ist\s+(\w+)': '≡',
        r'(\w+)\s+bedeutet\s+(\w+)': '≡',
        r'(\w+)\s+gleich\s+(\w+)': '≡',
        
        # Verneinungen
        r'(\w+)\s+nicht\s+(\w+)': '≠',
        r'kein\s+(\w+)\s+ohne\s+(\w+)': '⇔',
        r'ohne\s+(\w+)\s+kein\s+(\w+)': '⇔',
    }
    
    # Klassische Paradox-Paare
    PARADOX_PAARE = {
        # Qabbalistisch
        ('licht', 'dunkelheit'): ParadoxTyp.KLASSISCH,
        ('or', 'choschech'): ParadoxTyp.KLASSISCH,
        ('geben', 'empfangen'): ParadoxTyp.REZIPROK,
        ('maschpia', 'meqabel'): ParadoxTyp.REZIPROK,
        ('oben', 'unten'): ParadoxTyp.HIERARCHIE,
        ('eljon', 'tachton'): ParadoxTyp.HIERARCHIE,
        ('innen', 'außen'): ParadoxTyp.KLASSISCH,
        ('pnimi', 'chizoni'): ParadoxTyp.KLASSISCH,
        
        # Spirituell
        ('zwang', 'liebe'): ParadoxTyp.WANDLUNG,
        ('freiheit', 'notwendigkeit'): ParadoxTyp.KLASSISCH,
        ('einheit', 'vielheit'): ParadoxTyp.EINSCHLUSS,
        ('achdut', 'ribbui'): ParadoxTyp.EINSCHLUSS,
        ('mangel', 'fülle'): ParadoxTyp.WANDLUNG,
        ('chissaron', 'schlemut'): ParadoxTyp.WANDLUNG,
        
        # Existenziell
        ('sein', 'nichts'): ParadoxTyp.KLASSISCH,
        ('jesch', 'ajin'): ParadoxTyp.KLASSISCH,
        ('anfang', 'ende'): ParadoxTyp.SIMULTAN,
        ('reschit', 'achrit'): ParadoxTyp.SIMULTAN,
        ('teil', 'ganzes'): ParadoxTyp.EINSCHLUSS,
        ('prat', 'klal'): ParadoxTyp.EINSCHLUSS,
        
        # Psychologisch
        ('ich', 'wir'): ParadoxTyp.IDENTITÄT,
        ('ego', 'selbstlosigkeit'): ParadoxTyp.WANDLUNG,
        ('wille', 'hingabe'): ParadoxTyp.KLASSISCH,
        ('kontrolle', 'loslassen'): ParadoxTyp.KLASSISCH,
    }
    
    def __init__(self):
        self.erkannte_paradoxe: List[Paradox] = []
        self.generierte_fragen: List[MeisterFrage] = []
        
        # Transliteration Integration
        if MeisterTransliteration:
            self.transliteration = MeisterTransliteration()
            # Erweitere Paradox-Paare mit korrekten Transliterationen
            zusatz_paare = self.transliteration.generiere_paradox_begriffe()
            self.PARADOX_PAARE.update(zusatz_paare)
        else:
            self.transliteration = None
        
    def verarbeite_text(self, text: str) -> Dict[str, Any]:
        """Hauptmethode: Text → Paradoxe → Fragen"""
        
        # 0. Prüfe Transliteration wenn verfügbar
        transliteration_fehler = None
        if self.transliteration:
            transliteration_fehler = self.transliteration.prüfe_text_korrektheit(text)
        
        # 1. Text normalisieren
        text_norm = self._normalisiere_text(text)
        
        # 2. Paradoxe erkennen
        paradoxe = self._erkenne_paradoxe(text_norm, text)
        
        # 3. Fragen generieren
        fragen = []
        for paradox in paradoxe:
            fragen.extend(self._generiere_fragen(paradox))
        
        # 4. Bewerten und sortieren
        fragen_bewertet = self._bewerte_fragen(fragen)
        fragen_sortiert = sorted(fragen_bewertet, 
                                key=lambda f: f.gesamt_score, 
                                reverse=True)
        
        # 5. Beste Frage(n) auswählen
        beste_frage = fragen_sortiert[0] if fragen_sortiert else None
        top_5 = fragen_sortiert[:5]
        
        return {
            'text': text,
            'text_normalisiert': text_norm,
            'transliteration_fehler': transliteration_fehler,
            'paradoxe': paradoxe,
            'alle_fragen': fragen_sortiert,
            'beste_frage': beste_frage,
            'top_5': top_5,
            'statistik': {
                'paradoxe_gefunden': len(paradoxe),
                'fragen_generiert': len(fragen),
                'durchschnitt_score': sum(f.gesamt_score for f in fragen) / len(fragen) if fragen else 0
            }
        }
    
    def _normalisiere_text(self, text: str) -> str:
        """Normalisiert Text für Analyse"""
        # Transliteration wenn verfügbar
        if self.transliteration:
            # Korrigiere deutsche Begriffe (K→Q, Dagesh, Zer-Elimination)
            text = self.transliteration.korrigiere_deutsche_begriffe(text)
        else:
            # Fallback: Basis WWAK-Korrekturen
            wwak_map = {
                'kabbala': 'kabbala',
                'kabbalah': 'kabbala',
                'kawana': 'kawana',
                'tikun': 'tiqqun',
                'kelim': 'qelim',
                'kli': 'kli',
                'klipot': 'klipot',
                # Dagesh-Korrekturen
                'masach': 'massach',
                'chesed': 'chessed',
                'jesod': 'jessod',
                # Zer-Elimination
                'zerstören': 'wandeln',
                'zerbrechen': 'bersten'
            }
            
            for alt, neu in wwak_map.items():
                text = text.replace(alt, neu)
        
        # Kleinschreibung
        text = text.lower()
        
        return text
    
    def _erkenne_paradoxe(self, text_norm: str, text_orig: str) -> List[Paradox]:
        """Erkennt alle Paradoxe im Text"""
        paradoxe = []
        
        # 1. Muster-basierte Erkennung
        for muster, beziehung in self.GEGENSATZ_MUSTER.items():
            matches = re.finditer(muster, text_norm, re.IGNORECASE)
            for match in matches:
                el1, el2 = match.groups()[:2]
                
                # Kontext extrahieren
                start = max(0, match.start() - 50)
                end = min(len(text_orig), match.end() + 50)
                kontext = text_orig[start:end]
                
                # Typ bestimmen
                typ = self._bestimme_paradox_typ(el1, el2, beziehung)
                
                paradox = Paradox(
                    element1=el1,
                    element2=el2,
                    beziehung=beziehung,
                    typ=typ,
                    kontext=kontext,
                    stärke=self._berechne_stärke(el1, el2, typ)
                )
                
                paradoxe.append(paradox)
        
        # 2. Bekannte Paare suchen
        for (el1, el2), typ in self.PARADOX_PAARE.items():
            if el1 in text_norm and el2 in text_norm:
                # Prüfe Nähe (max 100 Zeichen)
                pos1 = text_norm.find(el1)
                pos2 = text_norm.find(el2)
                
                if abs(pos1 - pos2) < 100:
                    start = min(pos1, pos2) - 20
                    end = max(pos1 + len(el1), pos2 + len(el2)) + 20
                    kontext = text_orig[max(0, start):min(len(text_orig), end)]
                    
                    paradox = Paradox(
                        element1=el1,
                        element2=el2,
                        beziehung='↔',
                        typ=typ,
                        kontext=kontext,
                        stärke=0.9  # Bekannte Paare = hohe Stärke
                    )
                    
                    paradoxe.append(paradox)
        
        # Duplikate entfernen
        seen = set()
        unique_paradoxe = []
        for p in paradoxe:
            key = (p.element1, p.element2, p.beziehung)
            if key not in seen:
                seen.add(key)
                unique_paradoxe.append(p)
        
        return unique_paradoxe
    
    def _bestimme_paradox_typ(self, el1: str, el2: str, 
                              beziehung: str) -> ParadoxTyp:
        """Bestimmt den Typ eines Paradoxes"""
        
        # Prüfe bekannte Paare
        paar = (el1.lower(), el2.lower())
        if paar in self.PARADOX_PAARE:
            return self.PARADOX_PAARE[paar]
        
        # Sonst nach Beziehung
        if beziehung in ['↔', '∨', '≠']:
            return ParadoxTyp.KLASSISCH
        elif beziehung in ['→']:
            return ParadoxTyp.WANDLUNG
        elif beziehung in ['⊃']:
            return ParadoxTyp.EINSCHLUSS
        elif beziehung in ['∧']:
            return ParadoxTyp.SIMULTAN
        elif beziehung in ['≡']:
            return ParadoxTyp.IDENTITÄT
        else:
            return ParadoxTyp.KLASSISCH
    
    def _berechne_stärke(self, el1: str, el2: str, 
                         typ: ParadoxTyp) -> float:
        """Berechnet die Stärke eines Paradoxes"""
        stärke = 0.5  # Basis
        
        # Bekannte Paare
        if (el1.lower(), el2.lower()) in self.PARADOX_PAARE:
            stärke += 0.4
        
        # Typ-spezifisch
        if typ in [ParadoxTyp.WANDLUNG, ParadoxTyp.IDENTITÄT]:
            stärke += 0.2
        elif typ == ParadoxTyp.EINSCHLUSS:
            stärke += 0.15
        
        # Länge (kurz = stark)
        if len(el1) + len(el2) < 10:
            stärke += 0.1
        
        return min(1.0, stärke)
    
    def _generiere_fragen(self, paradox: Paradox) -> List[MeisterFrage]:
        """Generiert alle Frage-Typen für ein Paradox"""
        fragen = []
        
        el1, el2 = paradox.element1.title(), paradox.element2.title()
        
        # 1. FORMEL
        if paradox.beziehung in ['↔', '→', '∧']:
            frage = MeisterFrage(
                frage=f"{el1} + {el2} = ?",
                typ=FrageTyp.FORMEL,
                paradox=paradox
            )
            fragen.append(frage)
        
        # 2. WOZU (immer!)
        if paradox.beziehung == '→':
            frage = MeisterFrage(
                frage=f"WOZU führt {el1} zu {el2}?",
                typ=FrageTyp.WOZU,
                paradox=paradox
            )
        else:
            frage = MeisterFrage(
                frage=f"WOZU braucht {el1} das {el2}?",
                typ=FrageTyp.WOZU,
                paradox=paradox
            )
        fragen.append(frage)
        
        # 3. WIE
        if paradox.typ in [ParadoxTyp.WANDLUNG, ParadoxTyp.IDENTITÄT]:
            frage = MeisterFrage(
                frage=f"WIE wird {el1} zu {el2}?",
                typ=FrageTyp.WIE,
                paradox=paradox
            )
            fragen.append(frage)
        
        # 4. WENN-DANN
        if paradox.beziehung in ['→', '⇔']:
            frage = MeisterFrage(
                frage=f"WENN {el1} → DANN {el2}?",
                typ=FrageTyp.WENN_DANN,
                paradox=paradox
            )
            fragen.append(frage)
        
        # 5. IST
        if paradox.typ == ParadoxTyp.IDENTITÄT or paradox.beziehung == '≡':
            frage = MeisterFrage(
                frage=f"IST {el1} wirklich {el2}?",
                typ=FrageTyp.IST,
                paradox=paradox
            )
            fragen.append(frage)
        
        # 6. ZWISCHEN
        if paradox.typ in [ParadoxTyp.KLASSISCH, ParadoxTyp.HIERARCHIE]:
            frage = MeisterFrage(
                frage=f"Was liegt ZWISCHEN {el1} und {el2}?",
                typ=FrageTyp.ZWISCHEN,
                paradox=paradox
            )
            fragen.append(frage)
        
        # 7. META (für starke Paradoxe)
        if paradox.stärke > 0.7:
            frage = MeisterFrage(
                frage=f"Was fragt die Frage '{el1} & {el2}' selbst?",
                typ=FrageTyp.META,
                paradox=paradox
            )
            fragen.append(frage)
        
        return fragen
    
    def _bewerte_fragen(self, fragen: List[MeisterFrage]) -> List[MeisterFrage]:
        """Bewertet alle Fragen nach 3D-System"""
        
        for frage in fragen:
            # KRAFT: Würde ein Kind es verstehen?
            kraft = self._bewerte_kraft(frage)
            
            # TIEFE: Kann ein Qabbalist 2h darüber sprechen?
            tiefe = self._bewerte_tiefe(frage)
            
            # WOZU: Ist es Azilut-verankert?
            wozu = self._bewerte_wozu(frage)
            
            frage.scores = {
                'kraft': kraft,
                'tiefe': tiefe,
                'wozu': wozu
            }
        
        return fragen
    
    def _bewerte_kraft(self, frage: MeisterFrage) -> float:
        """Bewertet Einfachheit/Klarheit"""
        score = 0.5
        
        # Kurze Fragen = kraftvoll
        if len(frage.frage) < 20:
            score += 0.3
        elif len(frage.frage) < 30:
            score += 0.2
        
        # FORMEL-Typ = maximal klar
        if frage.typ == FrageTyp.FORMEL:
            score += 0.3
        
        # Einfache Wörter
        if all(len(w) < 10 for w in frage.frage.split()):
            score += 0.2
        
        return min(1.0, score)
    
    def _bewerte_tiefe(self, frage: MeisterFrage) -> float:
        """Bewertet philosophische Tiefe"""
        score = 0.5
        
        # Paradox-Stärke
        score += frage.paradox.stärke * 0.3
        
        # Typ-spezifisch
        if frage.typ in [FrageTyp.META, FrageTyp.IST]:
            score += 0.3
        elif frage.typ == FrageTyp.ZWISCHEN:
            score += 0.2
        
        # Qabbalistische Begriffe
        kabbala_begriffe = ['licht', 'dwekut', 'azilut', 'kabbala', 
                           'sefirot', 'ein sof', 'tiqqun']
        if any(b in frage.frage.lower() for b in kabbala_begriffe):
            score += 0.2
        
        return min(1.0, score)
    
    def _bewerte_wozu(self, frage: MeisterFrage) -> float:
        """Bewertet spirituelle Ausrichtung"""
        score = 0.5
        
        # WOZU-Typ = maximal
        if frage.typ == FrageTyp.WOZU:
            score = 0.9
        
        # Wandlungs-Paradoxe
        if frage.paradox.typ == ParadoxTyp.WANDLUNG:
            score += 0.2
        
        # Aufwärts-gerichtet
        aufwärts_begriffe = ['licht', 'liebe', 'einheit', 'geben']
        if any(b in frage.frage.lower() for b in aufwärts_begriffe):
            score += 0.2
        
        return min(1.0, score)
    
    # Export-Methoden
    def export_yaml(self, ergebnis: Dict[str, Any], 
                    dateiname: Optional[str] = None) -> str:
        """Exportiert als YAML"""
        
        export_data = {
            'meister_frage_analyse': {
                'zeitstempel': datetime.now().isoformat(),
                'text': ergebnis['text'],
                'paradoxe': [
                    {
                        'elemente': f"{p.element1} {p.beziehung} {p.element2}",
                        'typ': p.typ.value,
                        'stärke': p.stärke,
                        'kontext': p.kontext
                    }
                    for p in ergebnis['paradoxe']
                ],
                'beste_frage': {
                    'frage': ergebnis['beste_frage'].frage,
                    'typ': ergebnis['beste_frage'].typ.value,
                    'scores': ergebnis['beste_frage'].scores
                } if ergebnis['beste_frage'] else None,
                'top_5_fragen': [
                    {
                        'frage': f.frage,
                        'typ': f.typ.value,
                        'gesamt_score': f.gesamt_score
                    }
                    for f in ergebnis['top_5']
                ],
                'statistik': ergebnis['statistik']
            }
        }
        
        yaml_str = yaml.dump(export_data, allow_unicode=True, 
                            default_flow_style=False, sort_keys=False)
        
        if dateiname:
            with open(dateiname, 'w', encoding='utf-8') as f:
                f.write(yaml_str)
        
        return yaml_str
    
    def export_markdown(self, ergebnis: Dict[str, Any], 
                       dateiname: Optional[str] = None) -> str:
        """Exportiert als Markdown"""
        
        md_lines = [
            "# MEISTER FRAGE Analyse",
            f"Stand: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            "",
            "## Original-Text",
            f"> {ergebnis['text']}",
            "",
            "## Gefundene Paradoxe",
            ""
        ]
        
        for i, p in enumerate(ergebnis['paradoxe'], 1):
            md_lines.extend([
                f"### {i}. {p.element1} {p.beziehung} {p.element2}",
                f"- **Typ**: {p.typ.value}",
                f"- **Stärke**: {p.stärke:.2f}",
                f"- **Kontext**: ...{p.kontext}...",
                ""
            ])
        
        if ergebnis['beste_frage']:
            md_lines.extend([
                "## 🏆 BESTE FRAGE",
                f"### {ergebnis['beste_frage'].frage}",
                f"- **Typ**: {ergebnis['beste_frage'].typ.value}",
                f"- **Kraft**: {ergebnis['beste_frage'].scores['kraft']:.2f}",
                f"- **Tiefe**: {ergebnis['beste_frage'].scores['tiefe']:.2f}",
                f"- **WOZU**: {ergebnis['beste_frage'].scores['wozu']:.2f}",
                ""
            ])
        
        md_lines.extend([
            "## Top 5 Fragen",
            ""
        ])
        
        for i, f in enumerate(ergebnis['top_5'], 1):
            md_lines.append(f"{i}. **{f.frage}** (Score: {f.gesamt_score:.2f})")
        
        md_lines.extend([
            "",
            "---",
            "Q! = Die Frage öffnet, was keine Antwort öffnen kann!"
        ])
        
        md_str = "\n".join(md_lines)
        
        if dateiname:
            with open(dateiname, 'w', encoding='utf-8') as f:
                f.write(md_str)
        
        return md_str
    
    def export_json(self, ergebnis: Dict[str, Any], 
                   dateiname: Optional[str] = None) -> str:
        """Exportiert als JSON"""
        
        # Konvertiere Enums zu Strings
        export_data = {
            'zeitstempel': datetime.now().isoformat(),
            'text': ergebnis['text'],
            'paradoxe': [
                {
                    'element1': p.element1,
                    'element2': p.element2,
                    'beziehung': p.beziehung,
                    'typ': p.typ.value,
                    'kontext': p.kontext,
                    'stärke': p.stärke
                }
                for p in ergebnis['paradoxe']
            ],
            'beste_frage': {
                'frage': ergebnis['beste_frage'].frage,
                'typ': ergebnis['beste_frage'].typ.value,
                'scores': ergebnis['beste_frage'].scores,
                'gesamt_score': ergebnis['beste_frage'].gesamt_score
            } if ergebnis['beste_frage'] else None,
            'alle_fragen': [
                {
                    'frage': f.frage,
                    'typ': f.typ.value,
                    'scores': f.scores,
                    'gesamt_score': f.gesamt_score
                }
                for f in ergebnis['alle_fragen']
            ],
            'statistik': ergebnis['statistik']
        }
        
        json_str = json.dumps(export_data, ensure_ascii=False, 
                             indent=2)
        
        if dateiname:
            with open(dateiname, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str


# CLI wenn direkt ausgeführt
if __name__ == "__main__":
    import sys
    
    print("=== MEISTER FRAGE TOOL ===")
    print("Stand: 12. Tammus 5785")
    print("WWAK-konform mit Transliteration")
    print()
    
    if len(sys.argv) > 1:
        # Text aus Kommandozeile
        text = " ".join(sys.argv[1:])
    else:
        # Interaktiv
        print("Geben Sie einen Text ein (Enter + Ctrl-D zum Beenden):")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        text = "\n".join(lines)
    
    if not text.strip():
        print("Kein Text eingegeben!")
        sys.exit(1)
    
    # Verarbeiten
    tool = MeisterFrageTool()
    ergebnis = tool.verarbeite_text(text)
    
    # Transliterationsfehler anzeigen
    if ergebnis.get('transliteration_fehler'):
        print("\n⚠️  TRANSLITERATIONSFEHLER GEFUNDEN:")
        for typ, fehler in ergebnis['transliteration_fehler'].items():
            print(f"   {typ}: {', '.join(fehler)}")
        print()
    
    # Ausgabe
    print("\n" + "="*50)
    print(f"Original: {ergebnis['text']}")
    if ergebnis.get('text_normalisiert') and ergebnis['text_normalisiert'] != ergebnis['text'].lower():
        print(f"Korrigiert: {ergebnis['text_normalisiert']}")
    print(f"Paradoxe gefunden: {len(ergebnis['paradoxe'])}")
    print(f"Fragen generiert: {len(ergebnis['alle_fragen'])}")
    
    if ergebnis['beste_frage']:
        print("\n🏆 BESTE FRAGE:")
        print(f"   {ergebnis['beste_frage'].frage}")
        print(f"   Typ: {ergebnis['beste_frage'].typ.value}")
        print(f"   Score: {ergebnis['beste_frage'].gesamt_score:.2f}")
    
    print("\n📄 Exportiere als:")
    print("   - meister_analyse.yaml")
    print("   - meister_analyse.md")
    print("   - meister_analyse.json")
    
    tool.export_yaml(ergebnis, "meister_analyse.yaml")
    tool.export_markdown(ergebnis, "meister_analyse.md")
    tool.export_json(ergebnis, "meister_analyse.json")
    
    print("\nQ!")
