#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEISTER FRAGE Tool - Transliteration Erweiterung
===============================================

Korrekte Umschrift mit Dagesh-Regeln und WWAK-Konformität
Stand: 12. Tammus 5785
"""

import re
from typing import Dict, Tuple, List

class MeisterTransliteration:
    """Erweiterte Transliteration für das MEISTER FRAGE Tool"""
    
    # Hebräische Buchstaben → Deutsche Umschrift (DIN 31636)
    BUCHSTABEN_BASIS = {
        'א': '',      # Alef (stumm am Wortanfang)
        'ב': 'b',     # Bet
        'בּ': 'bb',   # Bet mit Dagesh
        'ג': 'g',     # Gimel
        'גּ': 'gg',   # Gimel mit Dagesh
        'ד': 'd',     # Dalet
        'דּ': 'dd',   # Dalet mit Dagesh
        'ה': 'h',     # He
        'ו': 'w',     # Waw
        'וּ': 'u',    # Waw als Vokal
        'ז': 'z',     # Zajin
        'זּ': 'zz',   # Zajin mit Dagesh
        'ח': 'ch',    # Chet
        'ט': 't',     # Tet
        'טּ': 'tt',   # Tet mit Dagesh
        'י': 'j',     # Jod
        'יּ': 'jj',   # Jod mit Dagesh
        'כ': 'ch',    # Kaf
        'כּ': 'kk',   # Kaf mit Dagesh → WWAK: qq!
        'ך': 'ch',    # Kaf sofit
        'ל': 'l',     # Lamed
        'לּ': 'll',   # Lamed mit Dagesh
        'מ': 'm',     # Mem
        'מּ': 'mm',   # Mem mit Dagesh
        'ם': 'm',     # Mem sofit
        'נ': 'n',     # Nun
        'נּ': 'nn',   # Nun mit Dagesh
        'ן': 'n',     # Nun sofit
        'ס': 's',     # Samech
        'סּ': 'ss',   # Samech mit Dagesh → WICHTIG für Massach!
        'ע': '',      # Ajin (meist stumm)
        'פ': 'f',     # Pe
        'פּ': 'pp',   # Pe mit Dagesh
        'ף': 'f',     # Pe sofit
        'צ': 'z',     # Zade
        'צּ': 'zz',   # Zade mit Dagesh
        'ץ': 'z',     # Zade sofit
        'ק': 'q',     # Qof → WWAK!
        'קּ': 'qq',   # Qof mit Dagesh
        'ר': 'r',     # Resch
        'רּ': 'rr',   # Resch mit Dagesh (selten)
        'ש': 'sch',   # Schin
        'שׁ': 'sch',  # Schin mit Punkt rechts
        'שׂ': 's',    # Sin mit Punkt links
        'שּ': 'sch',  # Schin mit Dagesh
        'ת': 't',     # Taw
        'תּ': 'tt',   # Taw mit Dagesh
    }
    
    # Vokalzeichen (Niqqud)
    VOKALE = {
        'ַ': 'a',     # Patach
        'ָ': 'a',     # Qamaz
        'ֵ': 'e',     # Zere
        'ֶ': 'e',     # Segol
        'ִ': 'i',     # Chiriq
        'ֹ': 'o',     # Cholam
        'ֻ': 'u',     # Qibbuz
        'ְ': 'e',     # Schwa (meist e)
        'ֱ': 'e',     # Chataf-Segol
        'ֲ': 'a',     # Chataf-Patach
        'ֳ': 'o',     # Chataf-Qamaz
    }
    
    # WWAK K→Q Transformationen (erweitert)
    WWAK_TRANSFORM = {
        # Basis-Transformationen
        'k': 'q',
        'kk': 'qq',  # Dagesh beachten!
        
        # Wort-spezifisch
        'kabbala': 'kabbala',
        'kabbalah': 'kabbala',
        'kawana': 'kawana',
        'kawanot': 'qawanot',
        'kelim': 'qelim',
        'keli': 'qeli',
        'kli': 'kli',
        'klipot': 'klipot',
        'klipa': 'klipa',
        'kabbalistisch': 'qabbalistisch',
        'kadesch': 'qadesch',
        'kedusha': 'qedusha',
        'keter': 'qeter',
        'tikun': 'tiqqun',  # Doppel-q wegen Dagesh!
        'tikunim': 'tiqqunim',
    }
    
    # Wichtige Begriffe mit korrekter Schreibweise
    KORREKTE_BEGRIFFE = {
        # Sefirot (mit Dagesh!)
        'חסד': 'Chessed',     # NICHT Chesed!
        'גבורה': 'Gewura',    
        'תפארת': 'Tiferet',   
        'נצח': 'Nezach',      # KEIN Dagesh
        'הוד': 'Hod',         # KEIN Dagesh
        'יסוד': 'Jessod',     # NICHT Jesod!
        'מלכות': 'Malchut',   
        
        # Zentrale Begriffe
        'מסך': 'Massach',     # NICHT Masach!
        'תיקון': 'Tiqqun',    # Doppel-q!
        'צמצום': 'Zimzum',    
        'דבקות': 'Dwekut',    
        'קבלה': 'Kabbala',    # K→Q
        'כוונה': 'Kawana',    # K→Q
        'כלים': 'Qelim',      # K→Q
        'קליפות': 'Klipot',   # K→Q
        
        # Welten
        'אצילות': 'Azilut',
        'בריאה': 'Berija',
        'יצירה': 'Jezira',
        'עשייה': 'Asija',
        
        # Paradox-relevante Begriffe
        'אור': 'Or',
        'חושך': 'Choschech',
        'משפיע': 'Maschpia',
        'מקבל': 'Meqabel',
        'עליון': 'Eljon',
        'תחתון': 'Tachton',
        'פנימי': 'Pnimi',
        'חיצוני': 'Chizoni',
        'אחדות': 'Achdut',
        'ריבוי': 'Ribbui',
        'חסרון': 'Chissaron',
        'שלמות': 'Schlemut',
        'יש': 'Jesch',
        'אין': 'Ajin',
        'ראשית': 'Reschit',
        'אחרית': 'Achrit',
        'פרט': 'Prat',
        'כלל': 'Klal',
    }
    
    # Zer-Elimination
    ZER_ELIMINATION = {
        'zerstören': 'wandeln',
        'zerstört': 'gewandelt',
        'zerstörung': 'wandlung',
        'zerstörend': 'wandelnd',
        'zerstörerisch': 'wandelnd',
        'zerbrechen': 'bersten',
        'zerbricht': 'berstet',
        'zerbrochen': 'geborsten',
        'zerfallen': 'sich wandeln',
        'zerfällt': 'wandelt sich',
        'zerstreuen': 'verteilen',
        'zerstreut': 'verteilt',
    }
    
    def transliteriere_hebräisch(self, text: str) -> str:
        """Transliteriert hebräischen Text nach DIN 31636 + WWAK"""
        result = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # Prüfe auf Dagesh (Punkt in der Mitte)
            if i + 1 < len(text) and text[i + 1] == 'ּ':
                # Buchstabe mit Dagesh
                combo = char + 'ּ'
                if combo in self.BUCHSTABEN_BASIS:
                    trans = self.BUCHSTABEN_BASIS[combo]
                    # WWAK-Spezialfall für כּ
                    if char == 'כ':
                        trans = 'qq'  # Nicht kk!
                    result.append(trans)
                    i += 2
                    continue
            
            # Normale Buchstaben
            if char in self.BUCHSTABEN_BASIS:
                result.append(self.BUCHSTABEN_BASIS[char])
            # Vokale
            elif char in self.VOKALE:
                result.append(self.VOKALE[char])
            # Sonstige Zeichen
            else:
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    def korrigiere_deutsche_begriffe(self, text: str) -> str:
        """Korrigiert deutsche Begriffe nach WWAK-Standard"""
        korrigiert = text
        
        # 1. Zer-Elimination
        for alt, neu in self.ZER_ELIMINATION.items():
            # Case-insensitive Ersetzung
            pattern = re.compile(re.escape(alt), re.IGNORECASE)
            korrigiert = pattern.sub(neu, korrigiert)
        
        # 2. K→Q Transformation
        for alt, neu in self.WWAK_TRANSFORM.items():
            pattern = re.compile(r'\b' + re.escape(alt) + r'\b', re.IGNORECASE)
            korrigiert = pattern.sub(neu, korrigiert)
        
        # 3. Dagesh-Korrekturen
        dagesh_fehler = {
            'masach': 'massach',
            'Masach': 'Massach',
            'chesed': 'chessed',
            'Chesed': 'Chessed',
            'jesod': 'jessod',
            'Jesod': 'Jessod',
            'tikun': 'tiqqun',
            'Tikun': 'Tiqqun',
        }
        
        for alt, neu in dagesh_fehler.items():
            korrigiert = korrigiert.replace(alt, neu)
        
        return korrigiert
    
    def prüfe_text_korrektheit(self, text: str) -> Dict[str, List[str]]:
        """Prüft Text auf Transliterations-Fehler"""
        fehler = {
            'k_statt_q': [],
            'fehlende_dagesh': [],
            'zer_wörter': [],
            'sonstige': []
        }
        
        # Finde K-Wörter die Q sein sollten
        k_muster = re.compile(r'\b[Kk]abbal|[Kk]awana|[Kk]elim|[Kk]li[^n]', re.IGNORECASE)
        for match in k_muster.finditer(text):
            fehler['k_statt_q'].append(match.group())
        
        # Finde fehlende Dagesh-Verdopplungen
        dagesh_muster = [
            (r'\b[Mm]asach\b', 'Massach'),
            (r'\b[Cc]hesed\b', 'Chessed'),
            (r'\b[Jj]esod\b', 'Jessod'),
            (r'\b[Tt]ikun\b', 'Tiqqun'),
        ]
        
        for muster, korrekt in dagesh_muster:
            if re.search(muster, text):
                fehler['fehlende_dagesh'].append(f"{muster} → {korrekt}")
        
        # Finde Zer-Wörter
        zer_muster = re.compile(r'\bzer\w+', re.IGNORECASE)
        for match in zer_muster.finditer(text):
            fehler['zer_wörter'].append(match.group())
        
        return {k: v for k, v in fehler.items() if v}
    
    def generiere_paradox_begriffe(self) -> Dict[str, str]:
        """Generiert korrekte Paradox-Paare für MEISTER FRAGE Tool"""
        paare = {}
        
        # Hebräische Paradox-Paare
        hebr_paare = [
            ('אור', 'חושך'),      # Licht - Dunkelheit
            ('משפיע', 'מקבל'),    # Gebender - Empfänger
            ('עליון', 'תחתון'),   # Oben - Unten
            ('פנימי', 'חיצוני'),  # Innen - Außen
            ('אחדות', 'ריבוי'),   # Einheit - Vielheit
            ('חסרון', 'שלמות'),  # Mangel - Fülle
            ('יש', 'אין'),        # Sein - Nichts
            ('ראשית', 'אחרית'),  # Anfang - Ende
            ('פרט', 'כלל'),       # Teil - Ganzes
        ]
        
        for hebr1, hebr2 in hebr_paare:
            trans1 = self.KORREKTE_BEGRIFFE.get(hebr1, self.transliteriere_hebräisch(hebr1))
            trans2 = self.KORREKTE_BEGRIFFE.get(hebr2, self.transliteriere_hebräisch(hebr2))
            
            # Speichere in beide Richtungen
            paare[(trans1.lower(), trans2.lower())] = 'KLASSISCH'
            paare[(trans2.lower(), trans1.lower())] = 'KLASSISCH'
            
            # Auch hebräisch
            paare[(hebr1, hebr2)] = 'KLASSISCH'
            paare[(hebr2, hebr1)] = 'KLASSISCH'
        
        return paare


# Integration in MEISTER FRAGE Tool
def erweitere_meister_tool():
    """Erweitert das MEISTER FRAGE Tool um korrekte Transliteration"""
    
    # Patch für meister_frage_tool.py
    patch_code = '''
# Am Anfang von meister_frage_tool.py hinzufügen:
from meister_transliteration import MeisterTransliteration

class MeisterFrageTool:
    def __init__(self):
        self.erkannte_paradoxe: List[Paradox] = []
        self.generierte_fragen: List[MeisterFrage] = []
        # NEU: Transliteration
        self.transliteration = MeisterTransliteration()
        # Erweitere Paradox-Paare
        self.PARADOX_PAARE.update(self.transliteration.generiere_paradox_begriffe())
    
    def _normalisiere_text(self, text: str) -> str:
        """Normalisiert Text für Analyse"""
        # Erst deutsche Korrekturen
        text = self.transliteration.korrigiere_deutsche_begriffe(text)
        
        # Dann Kleinschreibung
        text = text.lower()
        
        return text
    
    def _prüfe_transliteration(self, text: str) -> Dict[str, List[str]]:
        """Prüft und meldet Transliterations-Fehler"""
        return self.transliteration.prüfe_text_korrektheit(text)
'''
    
    return patch_code


# Standalone-Test
if __name__ == "__main__":
    print("=== MEISTER Transliteration Test ===")
    print("Stand: 12. Tammus 5785")
    print()
    
    trans = MeisterTransliteration()
    
    # Test 1: Hebräische Begriffe
    print("1. Hebräische Begriffe:")
    test_begriffe = ['חסד', 'מסך', 'תיקון', 'קבלה', 'כוונה']
    for hebr in test_begriffe:
        korrekt = trans.KORREKTE_BEGRIFFE.get(hebr, trans.transliteriere_hebräisch(hebr))
        print(f"   {hebr} → {korrekt}")
    
    print("\n2. Deutsche Korrekturen:")
    test_sätze = [
        "Die Kabbala lehrt über Chesed und Jesod.",
        "Der Masach muss durch Tikun gereinigt werden.",
        "Wir müssen die Klipot zerstören."
    ]
    
    for satz in test_sätze:
        korrigiert = trans.korrigiere_deutsche_begriffe(satz)
        print(f"   Vorher:  {satz}")
        print(f"   Nachher: {korrigiert}")
        print()
    
    print("3. Fehler-Prüfung:")
    fehler_text = "In der Kabbala lernen wir über Masach und Tikun, um die Kelim zu verstehen."
    fehler = trans.prüfe_text_korrektheit(fehler_text)
    
    for typ, liste in fehler.items():
        print(f"   {typ}: {', '.join(liste)}")
    
    print("\nQ!")
