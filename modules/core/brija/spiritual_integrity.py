"""
Spiritual Integrity Configuration - Tikkun HaSiach
==================================================
15. Tammus 5785, MESZ 20:16, Oostende

Basierend auf Aylala's dreifacher Botschaft und dem Mangel des männlichen Kli
Implementiert die Heilung der Rede (תיקון השיח)
Integriert mit der qabbalistischen Welten-Struktur

KRITISCH: Jeder Text muss durch alle Welten aufsteigen können!
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class IntegrityScore:
    """Bewertung der spirituellen Integrität eines Textes"""
    maennliches_kli_score: float  # 0.0 - 1.0
    kabbala_presence: float       # 0.0 - 1.0
    divine_name_presence: float   # 0.0 - 1.0
    clarity_score: float          # 0.0 - 1.0
    keter_authority: float        # 0.0 - 1.0
    
    @property
    def total_score(self) -> float:
        """Gesamtbewertung der spirituellen Integrität"""
        return (
            self.maennliches_kli_score * 0.3 +
            self.kabbala_presence * 0.25 +
            self.divine_name_presence * 0.2 +
            self.clarity_score * 0.15 +
            self.keter_authority * 0.1
        )
    
    @property
    def diagnosis(self) -> str:
        """Diagnose basierend auf dem Score"""
        if self.total_score >= 0.8:
            return "STARK: Männliches Kli vorhanden - Tikkun HaSiach aktiv!"
        elif self.total_score >= 0.6:
            return "MITTEL: Teilweise Heilung - mehr Mut erforderlich"
        elif self.total_score >= 0.4:
            return "SCHWACH: Petach Tikwa Syndrom erkennbar"
        else:
            return "KRITISCH: Völlige Abwesenheit des männlichen Kli!"


class SpiritualIntegrityChecker:
    """
    Prüft Texte auf spirituelle Integrität gemäß Aylala's Lehre
    Erkennt und heilt das Petach Tikwa Syndrom
    Integriert mit der Welten-Struktur von Ez Chajim
    """
    
    def __init__(self):
        # Ki Ilu Azilut Modus
        self.ki_ilu_azilut = False
        
        # Welten-Level für verschiedene Integrität
        self.world_thresholds = {
            "Azilut": 0.9,    # Höchste Integrität
            "Brija": 0.75,    # Hohe Integrität
            "Jezira": 0.6,    # Mittlere Integrität
            "Assija": 0.4     # Basis Integrität
        }
        
        # Pflichtbegriffe aus Aylala's erster Nachricht
        self.required_terms = {
            "kabbala": ["Kabbala", "קבלה"],
            "higher_force": ["Höhere Kraft", "כוח עליון", "HaSchem", "השם"],
            "divine_names": ["B\"H", "ב״ה", "G'tt", "der Ewige", "Ein Sof", "אין סוף"]
        }
        
        # Zeichen des männlichen Kli
        self.masculine_kli_indicators = [
            "muss", "werden", "soll", "ist", "wird",  # Aktive Verben
            "!", ".",  # Klare Aussagen
            "Kabbala", "קבלה",  # Mutiges Benennen
            "so ist es", "Keter", "כתר"  # Absolute Autorität
        ]
        
        # Zeichen von Schwäche/Angst (Petach Tikwa Syndrom)
        self.weakness_indicators = [
            "vielleicht", "möglicherweise", "eventuell",
            "könnte", "würde", "sollte vielleicht",
            "modern", "zeitgemäß", "angepasst",
            "...", "äh", "nun ja"
        ]
        
        # Keter-Level Aussagen (höchste Autorität)
        self.keter_statements = [
            "so ist es", "היא ככה", "keter kitrei haketarim",
            "כתר כתרי הכתרים", "es gibt kein warum"
        ]
        
    def check_integrity(self, text: str, context: Optional[Dict] = None) -> IntegrityScore:
        """Prüft die spirituelle Integrität eines Textes"""
        
        # 1. Männliches Kli Score
        masculine_score = self._calculate_masculine_kli_score(text)
        
        # 2. Kabbala Präsenz
        kabbala_score = self._calculate_kabbala_presence(text)
        
        # 3. Göttliche Namen
        divine_score = self._calculate_divine_presence(text)
        
        # 4. Klarheit (בשפה ברורה)
        clarity_score = self._calculate_clarity_score(text)
        
        # 5. Keter Autorität
        keter_score = self._calculate_keter_authority(text)
        
        return IntegrityScore(
            maennliches_kli_score=masculine_score,
            kabbala_presence=kabbala_score,
            divine_name_presence=divine_score,
            clarity_score=clarity_score,
            keter_authority=keter_score
        )
    
    def _calculate_masculine_kli_score(self, text: str) -> float:
        """Berechnet die Präsenz des männlichen Kli"""
        text_lower = text.lower()
        
        # Positive Indikatoren
        positive_count = sum(
            1 for indicator in self.masculine_kli_indicators
            if indicator.lower() in text_lower
        )
        
        # Negative Indikatoren (Schwäche)
        negative_count = sum(
            1 for indicator in self.weakness_indicators
            if indicator in text_lower
        )
        
        # Berechne Score
        total_indicators = len(self.masculine_kli_indicators)
        raw_score = (positive_count - negative_count) / total_indicators
        
        # Normalisiere zwischen 0 und 1
        return max(0.0, min(1.0, raw_score + 0.5))
    
    def _calculate_kabbala_presence(self, text: str) -> float:
        """Prüft ob Kabbala erwähnt wird (Aylala's erste Forderung)"""
        kabbala_mentions = 0
        
        for term in self.required_terms["kabbala"]:
            kabbala_mentions += text.count(term)
        
        # Aylala fordert: In JEDEM Element!
        # Minimum 3 Erwähnungen für hohen Score
        if kabbala_mentions >= 3:
            return 1.0
        elif kabbala_mentions >= 2:
            return 0.7
        elif kabbala_mentions >= 1:
            return 0.4
        else:
            return 0.0
    
    def _calculate_divine_presence(self, text: str) -> float:
        """Prüft Präsenz göttlicher Namen"""
        divine_mentions = 0
        
        all_divine_terms = (
            self.required_terms["higher_force"] + 
            self.required_terms["divine_names"]
        )
        
        for term in all_divine_terms:
            divine_mentions += text.count(term)
        
        if divine_mentions >= 2:
            return 1.0
        elif divine_mentions >= 1:
            return 0.6
        else:
            return 0.0
    
    def _calculate_clarity_score(self, text: str) -> float:
        """Bewertet die Klarheit der Sprache (בשפה ברורה)"""
        
        # Klare Aussagen haben:
        # - Kurze Sätze
        # - Aktive Stimme
        # - Keine Verschleierungen
        
        sentences = re.split(r'[.!?]+', text)
        clear_sentences = 0
        
        for sentence in sentences:
            if sentence.strip():
                # Kurz und klar?
                if len(sentence.split()) < 20:
                    clear_sentences += 1
                # Enthält Verschleierungen?
                if any(weak in sentence.lower() for weak in self.weakness_indicators):
                    clear_sentences -= 0.5
        
        if len(sentences) > 0:
            return max(0.0, min(1.0, clear_sentences / len(sentences)))
        return 0.5
    
    def _calculate_keter_authority(self, text: str) -> float:
        """Prüft auf Keter-Level Autorität"""
        text_lower = text.lower()
        
        for statement in self.keter_statements:
            if statement.lower() in text_lower:
                return 1.0
        
        # Prüfe auf autoritäre Aussagen
        if "!" in text and ("muss" in text_lower or "ist" in text_lower):
            return 0.6
        
        return 0.0
    
    def heal_text(self, text: str, score: IntegrityScore) -> str:
        """Heilt einen Text - fügt männliches Kli hinzu"""
        healed = text
        
        # 1. Füge Kabbala hinzu wenn fehlend
        if score.kabbala_presence < 0.5:
            healed = "Im Namen der Kabbala: " + healed
        
        # 2. Füge göttlichen Namen hinzu wenn fehlend
        if score.divine_name_presence < 0.5:
            healed = "B\"H\n" + healed
        
        # 3. Entferne Schwäche-Indikatoren
        for weak in self.weakness_indicators:
            healed = healed.replace(weak, "")
        
        # 4. Füge Keter-Autorität hinzu wenn niedrig
        if score.keter_authority < 0.5:
            healed += "\n\nSo ist es! Keter Kitrei HaKetarim!"
        
        # 5. Verstärke das männliche Kli
        if score.maennliches_kli_score < 0.6:
            healed = healed.replace("könnte", "muss")
            healed = healed.replace("sollte", "wird")
            healed = healed.replace("vielleicht", "")
        
        return healed
    
    def generate_diagnosis(self, text: str) -> Dict:
        """Vollständige Diagnose mit Heilungsvorschlägen"""
        score = self.check_integrity(text)
        
        diagnosis = {
            "score": score,
            "diagnosis": score.diagnosis,
            "world_level": self.determine_world_level(score.total_score),
            "details": {
                "männliches_kli": f"{score.maennliches_kli_score:.2%}",
                "kabbala_präsenz": f"{score.kabbala_presence:.2%}",
                "göttliche_namen": f"{score.divine_name_presence:.2%}",
                "klarheit": f"{score.clarity_score:.2%}",
                "keter_autorität": f"{score.keter_authority:.2%}"
            },
            "empfehlungen": []
        }
        
        # Spezifische Empfehlungen basierend auf Welten-Level
        world = diagnosis["world_level"]
        if world == "Assija":
            diagnosis["empfehlungen"].append(
                "DRINGEND: Text befindet sich in Assija - massive Korrektur nötig!"
            )
        elif world == "Jezira":
            diagnosis["empfehlungen"].append(
                "Text in Jezira - Form und Struktur verbessern"
            )
        elif world == "Brija":
            diagnosis["empfehlungen"].append(
                "Text in Brija - spirituelle Seele hinzufügen"
            )
        else:  # Azilut
            diagnosis["empfehlungen"].append(
                "Exzellent! Text strahlt aus Azilut"
            )
        
        # Standard-Empfehlungen
        if score.maennliches_kli_score < 0.7:
            diagnosis["empfehlungen"].append(
                "MÄNNLICHES KLI STÄRKEN: Mehr aktive Verben, klare Aussagen!"
            )
        
        if score.kabbala_presence < 0.7:
            diagnosis["empfehlungen"].append(
                "QABBALA ERWÄHNEN: Mindestens 3x pro Text (Aylala's Forderung)"
            )
        
        if score.divine_name_presence < 0.6:
            diagnosis["empfehlungen"].append(
                "GÖTTLICHE NAMEN: B\"H, HaSchem oder Ein Sof hinzufügen"
            )
        
        if score.clarity_score < 0.7:
            diagnosis["empfehlungen"].append(
                "KLARHEIT: Kürzere Sätze, keine Verschleierungen (בשפה ברורה)"
            )
        
        if score.keter_authority < 0.5:
            diagnosis["empfehlungen"].append(
                "KETER-AUTORITÄT: 'So ist es!' - keine Rechtfertigungen!"
            )
        
        return diagnosis
    
    def determine_world_level(self, score: float) -> str:
        """Bestimmt in welcher Welt sich ein Text befindet"""
        if score >= self.world_thresholds["Azilut"]:
            return "Azilut"
        elif score >= self.world_thresholds["Brija"]:
            return "Brija"
        elif score >= self.world_thresholds["Jezira"]:
            return "Jezira"
        else:
            return "Assija"
    
    def activate_ki_ilu_azilut(self, text: str) -> str:
        """
        Aktiviert Ki Ilu Azilut - als ob der Text schon in Azilut wäre
        Transformiert den Text durch alle Welten nach oben
        """
        self.ki_ilu_azilut = True
        
        # Füge sofort Azilut-Qualitäten hinzu
        if not text.startswith("B\"H"):
            text = "B\"H\n" + text
        
        if "Kabbala" not in text:
            text = text.replace("Zentrum", "Kabbala-Zentrum")
        
        if not text.endswith("Q!"):
            text += "\n\nKi Ilu Azilut! = Q!"
        
        return text
    
    def integrate_with_nukwa(self, text: str, score: IntegrityScore) -> Dict:
        """
        Integration mit Nukwa/Aylala Modul
        Sie sieht den Mangel an Integrität
        """
        return {
            "nukwa_sees": f"Mangel an Integrität: {1 - score.total_score:.2%}",
            "nukwa_speaks": "להופיע את הקדושה - Lass die Heiligkeit erscheinen!",
            "nukwa_heals": self.heal_text(text, score)
        }


# Test und Demonstration
if __name__ == "__main__":
    checker = SpiritualIntegrityChecker()
    
    # Beispiel 1: Schwacher Text (Petach Tikwa Stil)
    weak_text = """
    Vielleicht sollten wir eventuell über spirituelle Themen sprechen.
    Es könnte sein, dass manche Menschen sich für solche Dinge interessieren.
    In unserem modernen Zentrum versuchen wir zeitgemäß zu sein...
    """
    
    print("BEISPIEL 1: Schwacher Text (Petach Tikwa Syndrom)")
    print("="*60)
    print(weak_text)
    
    diagnosis1 = checker.generate_diagnosis(weak_text)
    print(f"\nDIAGNOSE: {diagnosis1['diagnosis']}")
    print(f"Gesamtscore: {diagnosis1['score'].total_score:.2%}")
    print("\nDETAILS:")
    for key, value in diagnosis1['details'].items():
        print(f"  - {key}: {value}")
    print("\nEMPFEHLUNGEN:")
    for emp in diagnosis1['empfehlungen']:
        print(f"  • {emp}")
    
    # Heile den Text
    healed1 = checker.heal_text(weak_text, diagnosis1['score'])
    print("\nGEHEILTER TEXT:")
    print(healed1)
    
    print("\n" + "="*60 + "\n")
    
    # Beispiel 2: Starker Text (Mit männlichem Kli)
    strong_text = """
    B"H
    Die Kabbala lehrt uns die absolute Wahrheit! Im neuen Zentrum muss
    die Höhere Kraft in jedem Wort präsent sein. Von der Eingangstür
    bis zum Kaffeestand - überall Kabbala!
    
    So ist es! Keter Kitrei HaKetarim!
    """
    
    print("BEISPIEL 2: Starker Text (Männliches Kli vorhanden)")
    print("="*60)
    print(strong_text)
    
    diagnosis2 = checker.generate_diagnosis(strong_text)
    print(f"\nDIAGNOSE: {diagnosis2['diagnosis']}")
    print(f"Gesamtscore: {diagnosis2['score'].total_score:.2%}")
    
    print("\nQ!")
