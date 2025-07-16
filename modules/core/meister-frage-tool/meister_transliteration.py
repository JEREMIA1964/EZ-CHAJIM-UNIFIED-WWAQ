#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEISTER Transliteration - WWAK-konforme Umschrift
===============================================

Implementiert korrekte Transliteration mit:
- Dagesh-Verdopplung (Massach, Chessed, Jessod)
- WWAK K→Q Transformation
- Zer-Elimination

Stand: 12.Tammus 5785
"""

import re
from typing import Dict, List

class MeisterTransliteration:
    """WWAK-konforme Transliteration für MEISTER FRAGE Tool"""
    
    # Korrekte Schreibweisen wichtiger Begriffe
    KORREKTE_BEGRIFFE = {
        # Sefirot (mit Dagesh wo nötig!)
        'חסד': 'Chessed',     # MIT Dagesh!
        'גבורה': 'Gewura',    
        'תפארת': 'Tiferet',   
        'נצח': 'Nezach',      # KEIN Dagesh
        'הוד': 'Hod',         # KEIN Dagesh
        'יסוד': 'Jessod',     # MIT Dagesh!
        'מלכות': 'Malchut',   
        
        # Zentrale Begriffe
        'מסך': 'Massach',     # MIT Dagesh!
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
    }
    
    # WWAK K→Q Transformationen
    WWAK_TRANSFORM = {
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
        'tikun': 'tiqqun',
        'tikunim': 'tiqqunim',
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
    
    # Dagesh-Korrekturen
    DAGESH_KORREKTUREN = {
        'masach': 'massach',
        'chesed': 'chessed',
        'jesod': 'jessod',
        'tikun': 'tiqqun',
        # Großschreibung
        'Masach': 'Massach',
        'Chesed': 'Chessed', 
        'Jesod': 'Jessod',
        'Tikun': 'Tiqqun',
    }
    
    def korrigiere_deutsche_begriffe(self, text: str) -> str:
        """Korrigiert Text nach WWAK-Standard"""
        korrigiert = text
        
        # 1. Zer-Elimination
        for alt, neu in self.ZER_ELIMINATION.items():
            pattern = re.compile(r'\b' + re.escape(alt) + r'\b', re.IGNORECASE)
            korrigiert = pattern.sub(neu, korrigiert)
        
        # 2. K→Q Transformation
        for alt, neu in self.WWAK_TRANSFORM.items():
            pattern = re.compile(r'\b' + re.escape(alt) + r'\b', re.IGNORECASE)
            korrigiert = pattern.sub(neu, korrigiert)
        
        # 3. Dagesh-Korrekturen
        for alt, neu in self.DAGESH_KORREKTUREN.items():
            korrigiert = korrigiert.replace(alt, neu)
        
        return korrigiert
    
    def generiere_paradox_begriffe(self) -> Dict[tuple, str]:
        """Generiert Paradox-Paare mit korrekter Schreibweise"""
        paare = {}
        
        # Hebräische Paradox-Paare mit Transliteration
        hebr_paare = [
            (('אור', 'חושך'), ('or', 'choschech')),
            (('משפיע', 'מקבל'), ('maschpia', 'meqabel')),
            (('עליון', 'תחתון'), ('eljon', 'tachton')),
            (('פנימי', 'חיצוני'), ('pnimi', 'chizoni')),
            (('אחדות', 'ריבוי'), ('achdut', 'ribbui')),
            (('חסרון', 'שלמות'), ('chissaron', 'schlemut')),
            (('יש', 'אין'), ('jesch', 'ajin')),
            (('ראשית', 'אחרית'), ('reschit', 'achrit')),
            (('פרט', 'כלל'), ('prat', 'klal')),
            (('צמצום', 'התפשטות'), ('zimzum', 'hitpaschut')),
        ]
        
        for (hebr1, hebr2), (trans1, trans2) in hebr_paare:
            # Hebräisch
            paare[(hebr1, hebr2)] = 'KLASSISCH'
            paare[(hebr2, hebr1)] = 'KLASSISCH'
            
            # Transliteration
            paare[(trans1, trans2)] = 'KLASSISCH'
            paare[(trans2, trans1)] = 'KLASSISCH'
            
            # Auch kleingeschrieben
            paare[(trans1.lower(), trans2.lower())] = 'KLASSISCH'
            paare[(trans2.lower(), trans1.lower())] = 'KLASSISCH'
        
        return paare
    
    def prüfe_text_korrektheit(self, text: str) -> Dict[str, List[str]]:
        """Prüft Text auf Transliterations-Fehler"""
        fehler = {
            'k_statt_q': [],
            'fehlende_dagesh': [],
            'zer_wörter': [],
        }
        
        # K-Wörter die Q sein sollten
        k_muster = re.compile(r'\b[Kk]abbal|[Kk]awana|[Kk]elim|[Kk]li[^n]', re.IGNORECASE)
        for match in k_muster.finditer(text):
            fehler['k_statt_q'].append(match.group())
        
        # Fehlende Dagesh
        dagesh_muster = [
            (r'\b[Mm]asach\b', 'Massach'),
            (r'\b[Cc]hesed\b', 'Chessed'),
            (r'\b[Jj]esod\b', 'Jessod'),
            (r'\b[Tt]ikun\b', 'Tiqqun'),
        ]
        
        for muster, korrekt in dagesh_muster:
            if re.search(muster, text):
                fehler['fehlende_dagesh'].append(f"{muster} → {korrekt}")
        
        # Zer-Wörter
        zer_muster = re.compile(r'\bzer\w+', re.IGNORECASE)
        for match in zer_muster.finditer(text):
            fehler['zer_wörter'].append(match.group())
        
        return {k: v for k, v in fehler.items() if v}


# Test wenn direkt ausgeführt
if __name__ == "__main__":
    print("=== TEST: MEISTER Transliteration ===")
    
    trans = MeisterTransliteration()
    
    # Test-Sätze
    test_sätze = [
        "In der Kabbala lernen wir über Masach und Tikun.",
        "Die Kelim müssen durch Chesed und Jesod gereinigt werden.",
        "Wir wollen die Klipot zerstören und zerbrechen."
    ]
    
    print("Korrekturen:")
    print("-" * 40)
    
    for satz in test_sätze:
        korrigiert = trans.korrigiere_deutsche_begriffe(satz)
        print(f"Alt: {satz}")
        print(f"Neu: {korrigiert}")
        print()
    
    # Fehler-Prüfung
    fehler_text = "Die Kabbala lehrt über Masach, Chesed und Tikun."
    fehler = trans.prüfe_text_korrektheit(fehler_text)
    
    print("\nFehler-Analyse:")
    print("-" * 40)
    for typ, liste in fehler.items():
        print(f"{typ}: {', '.join(liste)}")
    
    print("\nQ!")
