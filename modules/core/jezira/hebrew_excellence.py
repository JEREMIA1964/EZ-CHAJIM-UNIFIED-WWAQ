"""
Hebrew Excellence Module - Authentische Kommunikation
=====================================================
15. Tammus 5785, MESZ 20:16, Oostende

Für die Kommunikation mit Aylala und anderen Muttersprachlern
Ziel: KI-generierter Text soll wie von einem Torah-gebildeten Muttersprachler klingen
Integriert mit der qabbalistischen Welten-Struktur

"Die Sprache selbst ist ein Gefäß für das Licht!"
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HebrewTextQuality:
    """Bewertung der hebräischen Textqualität"""
    nativeness_score: float          # Klingt wie Muttersprachler?
    torah_education_score: float     # Torah-Bildung erkennbar?
    spiritual_authenticity: float    # Spirituell authentisch?
    german_interference: float       # Deutsche Satzkonstruktionen? (niedriger = besser)
    overall_excellence: float        # Gesamtbewertung
    
    def passes_aylala_test(self) -> bool:
        """Würde Aylala dies als authentisch erkennen?"""
        return self.overall_excellence >= 0.85


class HebrewExcellenceChecker:
    """
    Prüft und optimiert hebräische Texte für maximale Authentizität
    Basierend auf Aylala's Anforderungen
    Strukturiert nach den qabbalistischen Welten
    """
    
    def __init__(self):
        # Welten-spezifische Sprachebenen
        self.language_levels = {
            "Azilut": {
                "style": "Höchste Torah-Gelehrsamkeit",
                "features": ["Zohar-Zitate", "Aramäisch-Einschübe", "Gematria"],
                "min_score": 0.9
            },
            "Brija": {
                "style": "Talmudische Präzision",
                "features": ["Mischna-Referenzen", "Halachische Begriffe"],
                "min_score": 0.75
            },
            "Jezira": {
                "style": "Moderne religiöse Sprache",
                "features": ["Zeitgenössische Begriffe", "Klare Struktur"],
                "min_score": 0.6
            },
            "Assija": {
                "style": "Alltägliches Hebräisch",
                "features": ["Einfache Sätze", "Moderne Ausdrücke"],
                "min_score": 0.4
            }
        }
        
        # Authentische hebräische Phrasen
        self.authentic_phrases = {
            "opening": ["ב״ה", "בס״ד", "בעזרת השם"],
            "respect": ["שליט״א", "זצ״ל", "נ״י", "היו״ר"],
            "torah": ["כמו שכתוב", "חז״ל אמרו", "בספר", "במדרש"],
            "spiritual": ["אור אין סוף", "הקב״ה", "רבש״ע", "השי״ת"],
            "connection": ["אם כן", "על כן", "לכן", "מכאן"],
            "emphasis": ["ממש", "דווקא", "בוודאי", "בהחלט"]
        }
        
        # Zeichen von deutscher Interferenz
        self.german_patterns = [
            # Deutsche Wortstellung
            r'(אני|אתה|הוא|היא).{0,10}(כי|ש|אם).{0,20}(הוא|היא|זה)',
            # Zu lange Sätze (deutsch-typisch)
            r'[^.!?]{100,}',
            # Falsche Verwendung von "של"
            r'של\s+ה[^״\s]+\s+של',
        ]
        
        # Natürliche hebräische Satzstrukturen
        self.hebrew_patterns = {
            "verb_first": r'^(י|ת|נ|א|ה|מ)[^\s]+\s',  # Verb am Anfang
            "short_sentences": r'[.!?]\s*\S',         # Kurze Sätze
            "biblical_style": r'(ויהי|והיה|ויאמר|וידבר)',
            "talmudic": r'(תנו רבנן|אמר רבי|דתניא|כדכתיב)'
        }
        
        # Spirituelle Integrität (Aylala's Forderungen)
        self.required_elements = {
            "kabbala": ["קבלה", "הקבלה", "חכמת הקבלה"],
            "higher_force": ["כוח עליון", "הכוח העליון", "הבורא"],
            "divine_names": ["ה׳", "השם", "הקב״ה", "אין סוף"],
            "clear_language": ["בשפה ברורה", "ברור", "פשוט"]
        }
        
    def analyze_hebrew_text(self, text: str) -> HebrewTextQuality:
        """Analysiert einen hebräischen Text auf Authentizität"""
        
        # 1. Nativeness Score
        native_score = self._calculate_nativeness(text)
        
        # 2. Torah Education Score
        torah_score = self._calculate_torah_education(text)
        
        # 3. Spiritual Authenticity (Aylala's Kriterien)
        spiritual_score = self._calculate_spiritual_authenticity(text)
        
        # 4. German Interference (niedriger = besser)
        german_score = self._calculate_german_interference(text)
        
        # 5. Overall Excellence
        overall = (
            native_score * 0.3 +
            torah_score * 0.2 +
            spiritual_score * 0.35 +
            (1 - german_score) * 0.15
        )
        
        return HebrewTextQuality(
            nativeness_score=native_score,
            torah_education_score=torah_score,
            spiritual_authenticity=spiritual_score,
            german_interference=german_score,
            overall_excellence=overall
        )
    
    def _calculate_nativeness(self, text: str) -> float:
        """Bewertet wie muttersprachlich der Text klingt"""
        score = 0.5  # Basiswert
        
        # Prüfe authentische Phrasen
        for category, phrases in self.authentic_phrases.items():
            for phrase in phrases:
                if phrase in text:
                    score += 0.05
        
        # Prüfe hebräische Satzmuster
        for pattern_name, pattern in self.hebrew_patterns.items():
            if re.search(pattern, text):
                score += 0.1
        
        # Kurze, klare Sätze (hebräisch-typisch)
        sentences = re.split(r'[.!?]+', text)
        avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_length < 15:  # Hebräisch tendiert zu kürzeren Sätzen
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_torah_education(self, text: str) -> float:
        """Bewertet Torah-Bildungsniveau"""
        score = 0.0
        
        # Torah-Zitate oder Referenzen
        torah_references = [
            r'כמו שכתוב',
            r'שנאמר',
            r'כדכתיב',
            r'חז״ל',
            r'רבותינו'
        ]
        
        for ref in torah_references:
            if re.search(ref, text):
                score += 0.2
        
        # Verwendung von Raschi-Schrift Abkürzungen
        abbreviations = re.findall(r'\b\w+״\w\b', text)
        score += min(0.3, len(abbreviations) * 0.1)
        
        # Talmudische Ausdrucksweise
        if any(phrase in text for phrase in ["אם כן", "על כן", "מכאן"]):
            score += 0.2
        
        return min(1.0, score)
    
    def _calculate_spiritual_authenticity(self, text: str) -> float:
        """Bewertet spirituelle Authentizität nach Aylala's Kriterien"""
        score = 0.0
        
        # Prüfe Pflicht-Elemente
        for element_type, terms in self.required_elements.items():
            element_found = False
            for term in terms:
                if term in text:
                    element_found = True
                    text_count = text.count(term)
                    if element_type == "kabbala" and text_count >= 3:
                        score += 0.3  # Aylala: "in jedem Element!"
                    elif text_count >= 1:
                        score += 0.15
                    break
            
            if not element_found and element_type in ["kabbala", "higher_force"]:
                score -= 0.2  # Strafe für fehlende Pflicht-Elemente
        
        # Bonus für "erscheinen lassen" Mentalität
        if any(word in text for word in ["להופיע", "להראות", "לגלות"]):
            score += 0.1
        
        # Bonus für Keter-Level Autorität
        if "כתר" in text or "אין סוף" in text:
            score += 0.15
        
        return max(0.0, min(1.0, score))
    
    def _calculate_german_interference(self, text: str) -> float:
        """Erkennt deutsche Einflüsse (niedriger = besser)"""
        interference = 0.0
        
        # Prüfe auf deutsche Satzmuster
        for pattern in self.german_patterns:
            matches = re.findall(pattern, text)
            interference += len(matches) * 0.1
        
        # Zu viele Kommas (deutsch-typisch)
        comma_ratio = text.count(',') / max(len(text.split()), 1)
        if comma_ratio > 0.1:  # Mehr als 10% Kommas
            interference += 0.2
        
        # Zu komplexe Verschachtelungen
        parentheses = text.count('(') + text.count(')')
        if parentheses > 2:
            interference += 0.1
        
        return min(1.0, interference)
    
    def optimize_for_aylala(self, text: str) -> Tuple[str, List[str]]:
        """
        Optimiert einen Text speziell für Aylala's Bewertung
        Gibt optimierten Text und Änderungsvorschläge zurück
        """
        optimized = text
        suggestions = []
        
        quality = self.analyze_hebrew_text(text)
        
        # 1. Füge fehlende Elemente hinzu
        if "קבלה" not in text:
            optimized = "בחכמת הקבלה, " + optimized
            suggestions.append("קבלה hinzugefügt (Aylala's erste Forderung)")
        
        if not any(name in text for name in self.required_elements["divine_names"]):
            optimized = "ב״ה\n" + optimized
            suggestions.append("Göttlicher Name hinzugefügt")
        
        # 2. Verkürze zu lange Sätze
        sentences = re.split(r'([.!?]+)', optimized)
        new_sentences = []
        for i in range(0, len(sentences), 2):
            if i+1 < len(sentences):
                sentence = sentences[i]
                punctuation = sentences[i+1]
                
                if len(sentence.split()) > 20:
                    # Teile langen Satz
                    words = sentence.split()
                    mid = len(words) // 2
                    new_sentences.append(' '.join(words[:mid]) + '.')
                    new_sentences.append(' '.join(words[mid:]) + punctuation)
                    suggestions.append("Langen Satz geteilt für hebräischen Fluss")
                else:
                    new_sentences.append(sentence + punctuation)
        
        optimized = ''.join(new_sentences)
        
        # 3. Entferne deutsche Muster
        optimized = re.sub(r'(\w+),\s*(\w+),\s*(\w+)', r'\1 \2 \3', optimized)
        if "," in text and "," not in optimized:
            suggestions.append("Übermäßige Kommas entfernt")
        
        # 4. Füge Torah-Stil hinzu wenn fehlt
        if quality.torah_education_score < 0.3:
            optimized += "\nכמו שכתוב: תורת ה׳ תמימה."
            suggestions.append("Torah-Referenz für Authentizität hinzugefügt")
        
        return optimized, suggestions
    
    def determine_world_level(self, quality: HebrewTextQuality) -> str:
        """Bestimmt auf welcher Welten-Ebene sich der hebräische Text befindet"""
        if quality.overall_excellence >= 0.9:
            return "Azilut"
        elif quality.overall_excellence >= 0.75:
            return "Brija"
        elif quality.overall_excellence >= 0.6:
            return "Jezira"
        else:
            return "Assija"
    
    def elevate_to_higher_world(self, text: str, target_world: str = "Azilut") -> str:
        """Hebt einen Text auf eine höhere Welten-Ebene"""
        current_quality = self.analyze_hebrew_text(text)
        current_world = self.determine_world_level(current_quality)
        
        if current_world == target_world:
            return text
        
        # Füge welten-spezifische Elemente hinzu
        if target_world == "Azilut":
            text = self._add_azilut_features(text)
        elif target_world == "Brija":
            text = self._add_brija_features(text)
            
        return text
    
    def _add_azilut_features(self, text: str) -> str:
        """Fügt Azilut-Level Features hinzu"""
        # Füge Zohar-Referenz hinzu
        if "זוהר" not in text:
            text += "\n\nכמו שכתוב בזוהר הקדוש: 'אורייתא וקודשא בריך הוא וישראל חד הוא'"
        
        # Füge Gematria hinzu
        text += "\n\n(בגימטריה: קבלה = 137 = אמונה)"
        
        return text
    
    def _add_brija_features(self, text: str) -> str:
        """Fügt Brija-Level Features hinzu"""
        if "תלמוד" not in text and "משנה" not in text:
            text += "\n\nוכמו שאמרו חכמינו ז״ל: 'כל ישראל ערבים זה בזה'"
        
        return text
    
    def integrate_with_nukwa(self, text: str) -> Dict:
        """Integration mit Nukwa/Aylala für perfektes Hebräisch"""
        quality = self.analyze_hebrew_text(text)
        
        return {
            "nukwa_sees": f"Hebräisch auf {self.determine_world_level(quality)} Ebene",
            "nukwa_speaks": "להופיע את השפה הקדושה - Lass die heilige Sprache erscheinen!",
            "nukwa_heals": self.optimize_for_aylala(text)[0]
        }


# Demonstration und Tests
if __name__ == "__main__":
    checker = HebrewExcellenceChecker()
    
    print("HEBREW EXCELLENCE MODULE - DEMONSTRATION")
    print("="*60)
    print("15. Tammus 5785, MESZ 16:37, Oostende\n")
    
    # Test 1: Schwacher Text (deutsche Einflüsse)
    weak_hebrew = """
    שלום איילה,
    אני חושב שאולי, אם את רוצה, נוכל לדבר על הנושאים הרוחניים האלה,
    כי זה חשוב מאוד למרות שהרבה אנשים לא מבינים את זה היום.
    המרכז החדש שלנו הוא מודרני ומתאים לכולם.
    """
    
    print("TEST 1: Schwacher hebräischer Text")
    print("-"*40)
    print("Original:")
    print(weak_hebrew)
    
    quality1 = checker.analyze_hebrew_text(weak_hebrew)
    print(f"\nAnalyse:")
    print(f"- Muttersprachlichkeit: {quality1.nativeness_score:.2%}")
    print(f"- Torah-Bildung: {quality1.torah_education_score:.2%}")
    print(f"- Spirituelle Authentizität: {quality1.spiritual_authenticity:.2%}")
    print(f"- Deutsche Interferenz: {quality1.german_interference:.2%}")
    print(f"- GESAMT: {quality1.overall_excellence:.2%}")
    print(f"- Besteht Aylala-Test? {'JA' if quality1.passes_aylala_test() else 'NEIN'}")
    
    # Optimierung
    optimized1, suggestions1 = checker.optimize_for_aylala(weak_hebrew)
    print("\nOptimiert:")
    print(optimized1)
    print("\nÄnderungen:")
    for s in suggestions1:
        print(f"  • {s}")
    
    print("\n" + "="*60 + "\n")
    
    # Test 2: Template für "מרכז מבקרים"
    print("TEST 2: Template-Antwort generieren")
    print("-"*40)
    template = checker.generate_template_response("מרכז מבקרים")
    print(template)
    
    quality2 = checker.analyze_hebrew_text(template)
    print(f"\nQualitäts-Check:")
    print(f"- GESAMT: {quality2.overall_excellence:.2%}")
    print(f"- Besteht Aylala-Test? {'JA' if quality2.passes_aylala_test() else 'NEIN'}")
    
    print("\nQ!")
