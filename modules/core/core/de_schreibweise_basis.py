#!/usr/bin/env python3
"""B"H - Deutsche Schreibweise Modul für Ez Chajim
18. Tammus 5785, MESZ 04:50, Oostende
Vollständiges sprachwissenschaftliches Werkzeug-System
WWAK-konform nach K-Beschluss!
"""

import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from abc import ABC, abstractmethod
import unicodedata
from collections import defaultdict

# ============= 1. TRANSLITERATION (UMSCHRIFT) =============

class HebraischDeutschTransliterator:
    """DIN 31636 konforme Umschrift Hebräisch→Deutsch"""
    
    def __init__(self):
        # Konsonanten-Mapping nach DIN 31636
        self.konsonanten = {
            'א': '',      # Alef (stumm)
            'ב': 'b/w',   # Bet/Wet
            'ג': 'g',     # Gimel
            'ד': 'd',     # Dalet
            'ה': 'h',     # He (am Wortende meist stumm!)
            'ו': 'w',     # Waw
            'ז': 's',     # Sajin
            'ח': 'ch',    # Chet
            'ט': 't',     # Tet
            'י': 'j',     # Jod
            'כ': 'k/ch',  # Kaf/Chaf
            'ך': 'ch',    # Chaf sofit
            'ל': 'l',     # Lamed
            'מ': 'm',     # Mem
            'ם': 'm',     # Mem sofit
            'נ': 'n',     # Nun
            'ן': 'n',     # Nun sofit
            'ס': 'ss',    # Samech
            'ע': '',      # Ajin (stumm)
            'פ': 'p/f',   # Pe/Fe
            'ף': 'f',     # Fe sofit
            'צ': 'z',     # Zade
            'ץ': 'z',     # Zade sofit
            'ק': 'q',     # Qof (IMMER q!)
            'ר': 'r',     # Resch
            'ש': 'sch/s', # Schin/Sin
            'ת': 't'      # Taw
        }
        
        # WWAK-spezifische Transformationen
        self.wwak_regeln = {
            # v→w Transformationen
            'Gevura': 'Gewura',
            'gevura': 'gewura',
            'Gevurah': 'Gewura',
            'gevurah': 'gewura',
            
            # Doppel-SS Regel
            'Chesed': 'Chessed',
            'chesed': 'chessed',
            'Yesod': 'Jessod',
            'yesod': 'jessod',
            'Jesod': 'Jessod',
            'jesod': 'jessod',
            
            # K→Q bei hebräischen Begriffen
            'Kabbala': 'Kabbala',
            'kabbala': 'kabbala',
            'Kabbalah': 'Kabbala',
            'kabbalah': 'kabbala',
            'Kawana': 'Kawana',
            'kawana': 'kawana',
            'Kli': 'Kli',
            'kli': 'kli',
            'Klipa': 'Klipa',
            'klipa': 'klipa',
            'Klipot': 'Klipot',
            'klipot': 'klipot',
            
            # h-Elimination am Wortende
            'Torah': 'Tora',
            'torah': 'tora',
            'Binah': 'Bina',
            'binah': 'bina',
            'Chochmah': 'Chochma',
            'chochmah': 'chochma',
            'Shekinah': 'Schechina',
            'shekinah': 'schechina',
            'Halakhah': 'Halacha',
            'halakhah': 'halacha',
            
            # z→s bei Ze'ir → Se'ir
            "Ze'ir Anpin": "Se'ir Anpin",
            "ze'ir anpin": "se'ir anpin",
            "Zeir Anpin": "Se'ir Anpin",
            "zeir anpin": "se'ir anpin",
            
            # tz→z Transformation
            'Tzimtzum': 'Zimzum',
            'tzimtzum': 'zimzum',
            'Atzilut': 'Azilut',
            'atzilut': 'azilut',
            
            # Abkürzungen ohne Anführungszeichen
            'S"A': 'SA',
            'Z"A': 'SA',
            'A"A': 'AA',
            'A"K': 'AQ'
        }
    
    def transliteriere(self, text: str) -> str:
        """Hauptfunktion für Transliteration"""
        # Erst WWAK-Regeln anwenden
        for alt, neu in self.wwak_regeln.items():
            text = text.replace(alt, neu)
        
        return text


# ============= 2. ORTHOGRAFIE UND GRAMMATIK =============

class DeutscheOrthografie:
    """Deutsche Rechtschreibung und Grammatik-Prüfung"""
    
    def __init__(self):
        # Artikel-Regeln
        self.artikel = {
            'Kli': 'das',      # Neutrum!
            'Klim': 'die',     # Plural
            'Sefira': 'die',
            'Sefirot': 'die',  # Plural
            'Parzuf': 'der',
            'Parzufim': 'die', # Plural
            'Or': 'das',       # Licht
            'Orot': 'die',     # Lichter
            'Kawana': 'die',
            'Zimzum': 'der',
            'Tiqqun': 'der',
            'Dwekut': 'die'
        }
        
        # Genus-Regeln
        self.genus_endungen = {
            '-ung': 'feminin',  # die Offenbarung
            '-heit': 'feminin', # die Weisheit
            '-keit': 'feminin', # die Heiligkeit
            '-schaft': 'feminin', # die Eigenschaft
            '-ismus': 'maskulin', # der Chassidismus
            '-er': 'maskulin'    # der Lehrer
        }
    
    def pruefe_artikel(self, wort: str, artikel: str) -> Tuple[bool, str]:
        """Prüft ob der Artikel korrekt ist"""
        if wort in self.artikel:
            korrekt = self.artikel[wort]
            if artikel.lower() != korrekt:
                return False, f"'{artikel} {wort}' → '{korrekt} {wort}'"
        return True, ""
    
    def bestimme_genus(self, wort: str) -> Optional[str]:
        """Bestimmt das Genus eines Wortes"""
        for endung, genus in self.genus_endungen.items():
            if wort.endswith(endung):
                return genus
        return None


# ============= 3. SEMANTIK =============

class SemantikPruefer:
    """Prüft semantische Korrektheit und Bedeutung"""
    
    def __init__(self):
        # Bedeutungs-Mapping
        self.bedeutungen = {
            'Kabbala': 'Empfangen, Überlieferung',
            'Kawana': 'Absicht, geistige Ausrichtung',
            'Zimzum': 'Kontraktion, Selbstbeschränkung',
            'Tiqqun': 'Korrektur, Wiederherstellung',
            'Dwekut': 'Anhaftung an das Göttliche',
            'Sefirot': '10 göttliche Emanationen',
            'Parzuf': 'Spirituelle Konfiguration',
            'Klipa': 'Schale, verhüllende Kraft',
            'Or': 'Göttliches Licht',
            'Kli': 'Gefäß für göttliches Licht'
        }
        
        # Semantische Felder
        self.wortfelder = {
            'Licht': ['Or', 'Orot', 'leuchten', 'strahlen', 'erhellen'],
            'Gefäß': ['Kli', 'Klim', 'empfangen', 'aufnehmen', 'fassen'],
            'Korrektur': ['Tiqqun', 'korrigieren', 'heilen', 'wiederherstellen'],
            'Verhüllung': ['Klipa', 'verbergen', 'verhüllen', 'bedecken']
        }
    
    def erklaere_begriff(self, begriff: str) -> Optional[str]:
        """Gibt Erklärung eines Begriffs zurück"""
        return self.bedeutungen.get(begriff)
    
    def finde_verwandte_begriffe(self, wort: str) -> List[str]:
        """Findet semantisch verwandte Begriffe"""
        verwandte = []
        for feld, begriffe in self.wortfelder.items():
            if wort in begriffe:
                verwandte.extend([b for b in begriffe if b != wort])
        return verwandte


# ============= 4. AUSDRUCK UND STIL =============

class AusdruckStilPruefer:
    """Prüft Ausdruck und Schreibstil"""
    
    def __init__(self):
        # Stil-Ebenen
        self.stil_ebenen = {
            'akademisch': {
                'merkmale': ['Fachbegriffe', 'komplexe Sätze', 'Zitate'],
                'vermeiden': ['umgangssprachlich', 'Füllwörter']
            },
            'spirituell': {
                'merkmale': ['heilige Begriffe', 'ehrfürchtig', 'präzise'],
                'vermeiden': ['anthropomorph', 'profan']
            },
            'lehrend': {
                'merkmale': ['klar', 'strukturiert', 'beispielhaft'],
                'vermeiden': ['verwirrend', 'widersprüchlich']
            }
        }
        
        # Anti-anthropomorphe Ausdrücke
        self.anthropomorph_vermeiden = [
            "Gott will", "Gott denkt", "Gott fühlt",
            "der Herr sagt", "Er wünscht", "Seine Hand"
        ]
        
        # Bessere Alternativen
        self.spirituelle_alternativen = {
            "Gott will": "es ist der göttliche Wille",
            "Gott sagt": "es steht geschrieben",
            "Er": "die Höhere Kraft",
            "Seine": "die göttliche"
        }
    
    def pruefe_stil(self, text: str, stil: str = 'spirituell') -> List[str]:
        """Prüft Text auf Stil-Konformität"""
        probleme = []
        
        # Prüfe auf anthropomorphe Ausdrücke
        for ausdruck in self.anthropomorph_vermeiden:
            if ausdruck.lower() in text.lower():
                alt = self.spirituelle_alternativen.get(ausdruck, "")
                probleme.append(f"Vermeide: '{ausdruck}' → '{alt}'")
        
        return probleme


# ============= 5. ZER-ELIMINATION =============

class ZerEliminator:
    """Eliminiert 'zer'-Präfixe nach WWAK"""
    
    def __init__(self):
        self.zer_transformationen = {
            'zerbrechen': 'bersten',
            'zerbrochen': 'geborsten',
            'zerbricht': 'berstet',
            'zerstören': 'wandeln',
            'zerstört': 'gewandelt',
            'Zerstörung': 'Wandlung',
            'zerreißen': 'trennen',
            'zerrissen': 'getrennt',
            'zerschlagen': 'transformieren',
            'zerfallen': 'sich auflösen',
            'zersetzen': 'umwandeln',
            'zersplittern': 'sich teilen'
        }
    
    def eliminiere_zer(self, text: str) -> Tuple[str, List[str]]:
        """Ersetzt alle zer-Wörter"""
        aenderungen = []
        
        for alt, neu in self.zer_transformationen.items():
            if alt in text:
                text = text.replace(alt, neu)
                aenderungen.append(f"{alt} → {neu}")
            # Auch Großschreibung
            if alt.capitalize() in text:
                text = text.replace(alt.capitalize(), neu.capitalize())
                aenderungen.append(f"{alt.capitalize()} → {neu.capitalize()}")
        
        return text, aenderungen


# ============= 6. SPRACHWISSENSCHAFTLICHE WERKZEUGE =============

class SprachWerkzeuge:
    """Sammlung sprachwissenschaftlicher Werkzeuge"""
    
    def __init__(self):
        self.werkzeuge = {
            'Phonetik': self.phonetische_analyse,
            'Morphologie': self.morphologische_analyse,
            'Etymologie': self.etymologische_herkunft,
            'Gematria': self.gematria_berechnung
        }
    
    def phonetische_analyse(self, wort: str) -> Dict:
        """Analysiert Lautstruktur"""
        return {
            'silben': self._silben_trennung(wort),
            'betonung': self._finde_betonung(wort),
            'lautgruppen': self._klassifiziere_laute(wort)
        }
    
    def morphologische_analyse(self, wort: str) -> Dict:
        """Analysiert Wortstruktur"""
        return {
            'wortstamm': self._extrahiere_stamm(wort),
            'präfixe': self._finde_praefixe(wort),
            'suffixe': self._finde_suffixe(wort),
            'wortart': self._bestimme_wortart(wort)
        }
    
    def etymologische_herkunft(self, begriff: str) -> Dict:
        """Bestimmt Wortherkunft"""
        herkunft_db = {
            'Kabbala': {'sprache': 'Hebräisch', 'wurzel': 'קבל (QBL)', 'bedeutung': 'empfangen'},
            'Zimzum': {'sprache': 'Hebräisch', 'wurzel': 'צמצם', 'bedeutung': 'zusammenziehen'},
            'Schechina': {'sprache': 'Hebräisch', 'wurzel': 'שכן', 'bedeutung': 'wohnen'}
        }
        return herkunft_db.get(begriff, {'sprache': 'unbekannt'})
    
    def gematria_berechnung(self, wort: str) -> int:
        """Berechnet Gematria-Wert"""
        gematria_werte = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
            'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
            'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
            'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200,
            'ש': 300, 'ת': 400
        }
        return sum(gematria_werte.get(buchstabe, 0) for buchstabe in wort)
    
    def _silben_trennung(self, wort: str) -> List[str]:
        """Trennt Wort in Silben"""
        # Vereinfachte Silbentrennung
        silben = []
        aktuelle_silbe = ""
        
        for i, char in enumerate(wort):
            aktuelle_silbe += char
            # Einfache Regel: Nach Vokal+Konsonant trennen
            if (i < len(wort) - 1 and 
                char.lower() in 'aeiouäöü' and 
                wort[i+1].lower() not in 'aeiouäöü'):
                if i < len(wort) - 2 and wort[i+2].lower() not in 'aeiouäöü':
                    silben.append(aktuelle_silbe)
                    aktuelle_silbe = ""
        
        if aktuelle_silbe:
            silben.append(aktuelle_silbe)
        
        return silben if silben else [wort]
    
    def _finde_betonung(self, wort: str) -> str:
        """Findet betonte Silbe"""
        # Hebräische Wörter: meist Endbetonung
        if any(h in wort for h in ['Kabbala', 'Zimzum', 'Tiqqun']):
            return 'Endbetonung'
        return 'Standardbetonung'
    
    def _klassifiziere_laute(self, wort: str) -> Dict:
        """Klassifiziert Laute im Wort"""
        vokale = sum(1 for c in wort.lower() if c in 'aeiouäöüy')
        konsonanten = sum(1 for c in wort.lower() if c.isalpha() and c not in 'aeiouäöüy')
        
        return {
            'vokale': vokale,
            'konsonanten': konsonanten,
            'verhältnis': f"{konsonanten}:{vokale}"
        }
    
    def _extrahiere_stamm(self, wort: str) -> str:
        """Extrahiert Wortstamm"""
        # Entferne häufige Suffixe
        suffixe = ['ung', 'heit', 'keit', 'schaft', 'ismus', 'ist']
        for suffix in suffixe:
            if wort.endswith(suffix):
                return wort[:-len(suffix)]
        return wort
    
    def _finde_praefixe(self, wort: str) -> List[str]:
        """Findet Präfixe"""
        praefixe = []
        moegliche = ['un', 'ver', 'be', 'ent', 'er', 'ge']
        for praefix in moegliche:
            if wort.startswith(praefix):
                praefixe.append(praefix)
        return praefixe
    
    def _finde_suffixe(self, wort: str) -> List[str]:
        """Findet Suffixe"""
        suffixe = []
        moegliche = ['ung', 'heit', 'keit', 'schaft', 'lich', 'isch', 'ig']
        for suffix in moegliche:
            if wort.endswith(suffix):
                suffixe.append(suffix)
        return suffixe
    
    def _bestimme_wortart(self, wort: str) -> str:
        """Bestimmt Wortart"""
        # Vereinfachte Regeln
        if wort[0].isupper():
            return 'Substantiv'
        elif wort.endswith(('en', 'ern', 'eln')):
            return 'Verb'
        elif wort.endswith(('ig', 'lich', 'isch')):
            return 'Adjektiv'
        return 'unbestimmt'


# ============= HAUPTKLASSE =============

class DeutscheSchreibweise:
    """Hauptklasse für deutsche Schreibweise im Ez Chajim System"""
    
    def __init__(self):
        self.transliterator = HebraischDeutschTransliterator()
        self.orthografie = DeutscheOrthografie()
        self.semantik = SemantikPruefer()
        self.stil = AusdruckStilPruefer()
        self.zer_eliminator = ZerEliminator()
        self.werkzeuge = SprachWerkzeuge()
    
    def vollstaendige_pruefung(self, text: str) -> Dict:
        """Führt vollständige Prüfung durch"""
        ergebnis = {
            'original': text,
            'korrekturen': [],
            'warnungen': [],
            'empfehlungen': []
        }
        
        # 1. Transliteration
        korrigiert = self.transliterator.transliteriere(text)
        if korrigiert != text:
            ergebnis['korrekturen'].append(f"Transliteration: {len(korrigiert)} Zeichen geändert")
            text = korrigiert
        
        # 2. Zer-Elimination
        text, zer_aenderungen = self.zer_eliminator.eliminiere_zer(text)
        if zer_aenderungen:
            ergebnis['korrekturen'].extend(zer_aenderungen)
        
        # 3. Stil-Prüfung
        stil_probleme = self.stil.pruefe_stil(text)
        if stil_probleme:
            ergebnis['warnungen'].extend(stil_probleme)
        
        # 4. Finale Version
        ergebnis['korrigiert'] = text
        
        # 5. Q! am Ende sicherstellen
        if not text.strip().endswith('Q!'):
            ergebnis['korrigiert'] = text.rstrip() + '\n\nQ!'
            ergebnis['empfehlungen'].append("Q! am Ende hinzugefügt")
        
        return ergebnis
    
    def zeige_regeln(self) -> str:
        """Zeigt alle Schreibregeln"""
        regeln = """
B"H - DEUTSCHE SCHREIBWEISE REGELN
=====================================
Stand: 18. Tammus 5785, MESZ 05:07
Beschluss: JBR.-Wolff!Q!

1. SEFIROT (Korrekte Schreibweise):
   1. Keter
   2. Chochma
   3. Bina
   4. CHESSED (Doppel-SS!)
   5. GEWURA (mit W!)
   6. Tiferet
   7. Nezach
   8. Hod
   9. JESSOD (Doppel-SS!)
   10. Malchut

2. WWAK-TRANSFORMATIONEN:
   - K bleibt K! (Kabbala, Kawana, Kli)
   - Q→K bei falschen Schreibweisen
   - V→W (Gewura statt Gevura)
   - Keine h-Endungen (Tora statt Torah)
   - Zer-Elimination (bersten statt zerbrechen)

3. ABKÜRZUNGEN:
   - SA (nicht S"A) = Se'ir Anpin
   - AA (nicht A"A) = Arich Anpin
   - AK (nicht A"K) = Adam Kadmon

4. GRAMMATIK:
   - das Kli (Neutrum), die Klim (Plural)
   - der Zimzum, die Zimzumim
   - die Sefira, die Sefirot

5. ZEICHEN:
   - Q! bleibt als Zeichen (wegen QBL-Wurzel)
   - Aber KEINE Q-Schreibweise in Wörtern!

6. STIL:
   - Anti-anthropomorph
   - Keine englischen Schreibweisen
   - Q! am Ende jedes Haupttextes

PHONETISCHE BEGRÜNDUNG:
- Q im Deutschen = "Kw" Aussprache
- Würde zu falscher Aussprache führen
- Im Hebräischen kein k+w Laut
- Daher: K-Schreibweise für Klarheit!

Motto: Prüfe! Meide! Wandle!
Ki Ilu Azilut! Q!
"""
        return regeln


# ============= BEISPIEL-VERWENDUNG =============

if __name__ == "__main__":
    # Erstelle Prüfer
    pruefer = DeutscheSchreibweise()
    
    # Beispieltext mit vielen Fehlern
    test_text = """
    Die Torah lehrt uns über die Sephirot, besonders über Chesed und Gevurah.
    Durch Tzimtzum kann das göttliche Licht in die Klipot eindringen.
    Gott will dass wir Seine Gebote befolgen.
    Die Kabbala zerreißt die Schleier der Illusion.
    S"A und A"A sind wichtige Parzufim.
    """
    
    print("B\"H - Deutsche Schreibweise Prüfung")
    print("="*60)
    print("\nORIGINAL:")
    print(test_text)
    
    # Führe Prüfung durch
    ergebnis = pruefer.vollstaendige_pruefung(test_text)
    
    print("\nKORRIGIERT:")
    print(ergebnis['korrigiert'])
    
    print("\nÄNDERUNGEN:")
    for korrektur in ergebnis['korrekturen']:
        print(f"  • {korrektur}")
    
    print("\nWARNUNGEN:")
    for warnung in ergebnis['warnungen']:
        print(f"  ⚠ {warnung}")
    
    # Zeige Regeln
    print("\n" + pruefer.zeige_regeln())
