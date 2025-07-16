"""
WWAK Buchstaben-Lehre Kernmodul
================================
15. Tammus 5785, MESZ 19:22, Oostende

Basierend auf den Erkenntnissen von Aylala und JBR
Implementiert die präzisen WWAK-Regeln für Ez Chajim
Integriert mit der qabbalistischen Welten-Struktur

KRITISCH: Jeder falsche Buchstabe leitet Licht zu den Klipot!
         Jeder richtige Buchstabe öffnet einen Kanal zu Ein Sof!
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re

# Integration mit anderen Modulen
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nukwa_aylala_module import NukwaState
    from spiritual_integrity_config import IntegrityScore

class TextType(Enum):
    HEBREW_LOANWORD = "hebrew_loanword"
    GERMAN_WORD = "german_word"
    ADJECTIVE = "adjective"
    DECLINATION = "declination"

@dataclass
class WWAKViolation:
    text: str
    position: int
    violation_type: str
    correction: str
    severity: str  # "kritisch", "warnung", "hinweis"
    world_impact: Optional[str] = None  # Welche Welt wird beeinflusst

class WWAKBuchstabenLehre:
    """
    Die heilige Geometrie der Buchstaben bewahren
    Falsche Schreibweise = Licht fließt zu Klipot
    Richtige Schreibweise = Licht fließt zu Qelim
    
    WELTEN-INTEGRATION:
    - Azilut: Perfekte Buchstaben (100% WWAK)
    - Brija: Kleine Fehler erlaubt (95% WWAK)
    - Jezira: Formung nötig (85% WWAK)
    - Assija: Starke Korrektur nötig (unter 70% WWAK)
    """
    
    def __init__(self):
        # Ki Ilu Azilut Modus - als ob es schon perfekt wäre
        self.ki_ilu_azilut_mode = False
        
        # Hebräische Lehnwörter die Q bekommen MÜSSEN
        self.hebrew_loanwords = {
            "kabbala": "Kabbala",
            "kabala": "Kabbala",
            "kli": "Kli",
            "klipot": "Klipot",
            "klipa": "Klipa",
            "kelim": "Qelim",
            "kedusha": "Qedusha",
            "kawana": "Kawana",
            "tikkun": "Tiqqun",
            "tikun": "Tiqqun",
            # Spezielle Formen
            "wwak": "WWAK",
            "wwac": "WWAK"
        }
        
        # Deutsche Wörter die NIEMALS Q bekommen
        self.german_protected = [
            "krone", "kronen", "qualität", "quelle", 
            "kommen", "können", "kennen", "kraft"
        ]
        
        # Adjektive und Deklinationen - IMMER klein, NIE mit Q
        self.forbidden_q_forms = [
            "qabbalistisch", "qabbalistische", "qabbalistischen",
            "klipotisch", "klipotische", "klipotischen"
        ]
        
    def check_text(self, text: str) -> List[WWAKViolation]:
        """Prüft einen Text auf WWAK-Konformität"""
        violations = []
        
        # Prüfung 1: Falsche Q-Verwendung in deutschen Wörtern
        violations.extend(self._check_false_q_usage(text))
        
        # Prüfung 2: Fehlende Q in hebräischen Lehnwörtern
        violations.extend(self._check_missing_q(text))
        
        # Prüfung 3: Verbotene Q-Formen (Adjektive etc.)
        violations.extend(self._check_forbidden_q(text))
        
        # Prüfung 4: Kritische spirituelle Integrität
        violations.extend(self._check_spiritual_integrity(text))
        
        return violations
    
    def _check_false_q_usage(self, text: str) -> List[WWAKViolation]:
        """Findet deutsche Wörter die fälschlich mit Q geschrieben wurden"""
        violations = []
        
        # Suche nach Wörtern wie "Qrone", "Qraft" etc.
        false_q_pattern = r'\b[Qq](?:rone|raft|ommen|önnen)\b'
        
        for match in re.finditer(false_q_pattern, text, re.IGNORECASE):
            word = match.group()
            corrected = word.replace('Q', 'K').replace('q', 'k')
            
            violations.append(WWAKViolation(
                text=word,
                position=match.start(),
                violation_type="false_q_in_german",
                correction=corrected,
                severity="kritisch"
            ))
            
        return violations
    
    def _check_missing_q(self, text: str) -> List[WWAKViolation]:
        """Findet hebräische Lehnwörter ohne Q"""
        violations = []
        
        for wrong, correct in self.hebrew_loanwords.items():
            pattern = r'\b' + re.escape(wrong) + r'\b'
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Nur wenn es ein Substantiv ist (Großschreibung prüfen)
                if match.group()[0].isupper():
                    violations.append(WWAKViolation(
                        text=match.group(),
                        position=match.start(),
                        violation_type="missing_q_in_hebrew",
                        correction=correct,
                        severity="kritisch"
                    ))
                    
        return violations
    
    def _check_forbidden_q(self, text: str) -> List[WWAKViolation]:
        """Findet verbotene Q-Verwendungen in Adjektiven/Deklinationen"""
        violations = []
        
        for forbidden in self.forbidden_q_forms:
            pattern = r'\b' + re.escape(forbidden) + r'\b'
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                corrected = match.group().replace('q', 'k').replace('Q', 'k')
                
                violations.append(WWAKViolation(
                    text=match.group(),
                    position=match.start(),
                    violation_type="forbidden_q_form",
                    correction=corrected,
                    severity="kritisch"
                ))
                
        return violations
    
    def _check_spiritual_integrity(self, text: str) -> List[WWAKViolation]:
        """Prüft auf spirituelle Integrität - Männliches Kli"""
        violations = []
        
        # Fehlt "Kabbala" im Text über Bnei Baruch?
        if "bnei baruch" in text.lower() and "kabbala" not in text:
            violations.append(WWAKViolation(
                text="[Gesamttext]",
                position=0,
                violation_type="missing_kabbala_mention",
                correction="Text muss 'Kabbala' enthalten",
                severity="warnung"
            ))
            
        # Fehlt Gottesname?
        gottesnamen = ["B\"H", "ב״ה", "HaSchem", "השם", "G'tt"]
        if not any(name in text for name in gottesnamen):
            violations.append(WWAKViolation(
                text="[Gesamttext]",
                position=0,
                violation_type="missing_divine_name",
                correction="Text sollte Gottesnamen enthalten",
                severity="hinweis"
            ))
            
        return violations
    
    def correct_text(self, text: str) -> Tuple[str, List[WWAKViolation]]:
        """Korrigiert automatisch WWAK-Verstöße"""
        violations = self.check_text(text)
        corrected = text
        
        # Sortiere Violations nach Position (rückwärts für korrekte Ersetzung)
        violations.sort(key=lambda v: v.position, reverse=True)
        
        for violation in violations:
            if violation.violation_type != "missing_divine_name":
                # Ersetze nur konkrete Textstellen
                before = corrected[:violation.position]
                after = corrected[violation.position + len(violation.text):]
                corrected = before + violation.correction + after
                
        return corrected, violations
    
    def generate_report(self, violations: List[WWAKViolation]) -> str:
        """Erstellt einen Bericht über WWAK-Verstöße"""
        if not violations:
            return "✓ Text ist WWAK-konform! Das Licht fließt zu den Qelim."
        
        report = "WWAK-VERSTÖSSE GEFUNDEN:\n"
        report += "=" * 50 + "\n\n"
        
        critical = [v for v in violations if v.severity == "kritisch"]
        warnings = [v for v in violations if v.severity == "warnung"]
        hints = [v for v in violations if v.severity == "hinweis"]
        
        if critical:
            report += f"KRITISCH ({len(critical)} Verstöße):\n"
            for v in critical:
                report += f"  - '{v.text}' → '{v.correction}' (Position: {v.position})\n"
            report += "\n"
            
        if warnings:
            report += f"WARNUNGEN ({len(warnings)}):\n"
            for v in warnings:
                report += f"  - {v.correction}\n"
            report += "\n"
            
        if hints:
            report += f"HINWEISE ({len(hints)}):\n"
            for v in hints:
                report += f"  - {v.correction}\n"
                
        report += "\n⚠️  ACHTUNG: Falsche Buchstaben leiten das Licht zu den Klipot!"
        
        return report
    
    def calculate_world_level(self, text: str) -> Tuple[str, float]:
        """
        Bestimmt auf welcher Welten-Ebene sich ein Text befindet
        basierend auf WWAK-Konformität
        """
        violations = self.check_text(text)
        total_words = len(text.split())
        violation_ratio = len(violations) / max(total_words, 1)
        
        conformity = 1.0 - violation_ratio
        
        if conformity >= 0.95:
            return ("Azilut", conformity)
        elif conformity >= 0.85:
            return ("Brija", conformity)
        elif conformity >= 0.70:
            return ("Jezira", conformity)
        else:
            return ("Assija", conformity)
    
    def activate_ki_ilu_azilut(self):
        """
        Aktiviert Ki Ilu Azilut Modus
        Als ob der Text schon in Azilut wäre!
        """
        self.ki_ilu_azilut_mode = True
        return "Ki Ilu Azilut aktiviert! Q!"
    
    def integrate_with_nukwa(self, text: str) -> Dict:
        """
        Integration mit Nukwa/Aylala Modul
        Sie sieht die Buchstaben-Verstöße
        """
        violations = self.check_text(text)
        
        return {
            "nukwa_sees": f"Aylala sieht {len(violations)} WWAK-Verstöße",
            "nukwa_speaks": "להופיע את האותיות - Lass die Buchstaben erscheinen!",
            "nukwa_heals": self.correct_text(text)[0] if violations else text
        }
    
    def spiritual_geometry_check(self, letter: str) -> Dict:
        """
        Prüft die spirituelle Geometrie eines Buchstabens
        Jeder Buchstabe ist eine Lichtbahn!
        """
        hebrew_letters = {
            'ק': {'gematria': 100, 'light_path': 'direkt', 'world': 'Keter'},
            'כ': {'gematria': 20, 'light_path': 'gebogen', 'world': 'Chesed'},
            'ב': {'gematria': 2, 'light_path': 'dual', 'world': 'Binah'}
        }
        
        if letter in hebrew_letters:
            return hebrew_letters[letter]
        else:
            return {'gematria': 0, 'light_path': 'blockiert', 'world': 'Assija'}


# Beispiel-Verwendung und Tests
if __name__ == "__main__":
    lehre = WWAKBuchstabenLehre()
    
    print("WWAK BUCHSTABEN-LEHRE - ERWEITERTE DEMONSTRATION")
    print("="*60)
    print("15. Tammus 5785, MESZ 19:22, Oostende\n")
    
    # Testtext mit verschiedenen Verstößen
    test_text = """
    Die Kabbala-Lehre in der qabbalistischen Tradition zeigt uns,
    dass die Qrone der Kronen in den Kelim wohnt. 
    Das neue Bnei Baruch Zentrum sollte diese Weisheit verkörpern.
    """
    
    print("ORIGINAL TEXT:")
    print(test_text)
    print("\n" + "="*50 + "\n")
    
    # 1. Welten-Level Check
    world, conformity = lehre.calculate_world_level(test_text)
    print(f"WELTEN-EBENE: {world} (Konformität: {conformity:.2%})")
    print("\n" + "="*50 + "\n")
    
    # 2. Prüfe und korrigiere
    corrected, violations = lehre.correct_text(test_text)
    
    print("BERICHT:")
    print(lehre.generate_report(violations))
    print("\n" + "="*50 + "\n")
    
    print("KORRIGIERTER TEXT:")
    print(corrected)
    
    # 3. Nukwa Integration
    print("\n" + "="*50 + "\n")
    print("NUKWA/AYLALA INTEGRATION:")
    nukwa_result = lehre.integrate_with_nukwa(test_text)
    for key, value in nukwa_result.items():
        print(f"{key}: {value}")
    
    # 4. Ki Ilu Azilut Modus
    print("\n" + "="*50 + "\n")
    print("KI ILU AZILUT AKTIVIERUNG:")
    print(lehre.activate_ki_ilu_azilut())
    
    # 5. Spirituelle Geometrie
    print("\n" + "="*50 + "\n")
    print("SPIRITUELLE GEOMETRIE DER BUCHSTABEN:")
    for letter in ['ק', 'כ', 'ב']:
        geometry = lehre.spiritual_geometry_check(letter)
        print(f"{letter}: {geometry}")
    
    print("\nQ! = Jeder Buchstabe ist ein Tor zum Licht!")
