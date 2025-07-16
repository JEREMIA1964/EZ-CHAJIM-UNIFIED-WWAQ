"""
Meister-Frage Tool - Paradox-Generator
======================================
15. Tammus 5785, MESZ 20:16, Oostende

Basierend auf dem MEISTER-FRAGE-MODUS
Generiert paradoxe Fragen die zur Erkenntnis führen
Integriert mit der qabbalistischen Welten-Struktur

"Im Paradox liegt die Einheit - in der Einheit liegt Ein Sof!"
"""

import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MeisterFrage:
    """Eine Meister-Frage mit ihren Komponenten"""
    element1: str
    element2: str
    operator: str = "+"
    result: str = "?"
    kontext: Optional[str] = None
    tiefe_ebene: Optional[str] = None
    welt: Optional[str] = None  # Welche Welt adressiert die Frage?
    
    def __str__(self) -> str:
        """Formatiert die Meister-Frage"""
        frage = f'"{self.element1} {self.operator} {self.element2} = {self.result}"'
        if self.kontext:
            frage = f"{self.kontext}\n{frage}"
        if self.welt:
            frage += f"\n[Welt: {self.welt}]"
        return frage
    
    @property
    def ist_paradox(self) -> bool:
        """Prüft ob die Frage paradox ist"""
        gegensaetze = [
            ("Verbergen", "Offenbaren"),
            ("Mangel", "Fülle"),
            ("Furcht", "Liebe"),
            ("Schweigen", "Sprechen"),
            ("Modern", "Ewig"),
            ("Scham", "Stolz")
        ]
        
        for paar in gegensaetze:
            if (self.element1 in paar and self.element2 in paar) or \
               (self.element2 in paar and self.element1 in paar):
                return True
        return False


class MeisterFrageGenerator:
    """
    Generiert Meister-Fragen nach dem Vorbild des Meisters
    Paradoxe führen zur Erkenntnis
    Integriert mit den qabbalistischen Welten
    """
    
    def __init__(self):
        # Welten-spezifische Fragen
        self.welten_fragen = {
            "Azilut": ["Geben + Geben = ?", "Licht + Licht = ?"],
            "Brija": ["Seele + Körper = ?", "Ich + Du = ?"],
            "Jezira": ["Form + Inhalt = ?", "Engel + Mensch = ?"],
            "Assija": ["Handlung + Absicht = ?", "Materie + Geist = ?"]
        }
        
        # Grundlegende Elemente aus unserer Lehre
        self.elemente = {
            "spirituell": [
                "Kabbala", "Höhere Kraft", "Licht", "Gefäß",
                "Keter", "Malchut", "Zimzum", "Or", "Kli"
            ],
            "mangel": [
                "Fehlen", "Mangel", "Leere", "Abwesenheit",
                "Verstecken", "Schweigen", "Vergessen"
            ],
            "fuelle": [
                "Offenbaren", "Erscheinen", "Fülle", "Präsenz",
                "Sprechen", "Zeigen", "Erinnern"
            ],
            "emotion": [
                "Furcht", "Scham", "Stolz", "Liebe",
                "Mut", "Angst", "Freude"
            ],
            "modern": [
                "Modern", "Zeitgemäß", "Angepasst", "Säkular",
                "Populär", "Mainstream"
            ],
            "ewig": [
                "Ewig", "Heilig", "Traditionell", "Authentisch",
                "Ursprünglich", "Wahr"
            ],
            "aktion": [
                "Bauen", "Erschaffen", "Geben", "Empfangen",
                "Lehren", "Lernen", "Heilen"
            ]
        }
        
        # Spezielle Kontexte aus Aylala's Lehre
        self.kontexte = [
            "Im Besucherzentrum:",
            "Am Kaffeestand:",
            "In der höchsten Etage:",
            "Vor der Gemeinde:",
            "Im Moment der Eröffnung:",
            "Wenn der Name fehlt:",
            "Wo Kabbala versteckt wird:"
        ]
        
        # Paradox-Paare
        self.paradox_paare = [
            ("Verbergen", "Offenbaren"),
            ("Mangel", "Fülle"),
            ("Furcht", "Liebe"),
            ("Schweigen", "Sprechen"),
            ("Modern", "Ewig"),
            ("Scham", "Stolz"),
            ("Dunkelheit", "Licht"),
            ("Frage", "Antwort"),
            ("Unten", "Oben"),
            ("Empfangen", "Geben")
        ]
        
    def generiere_meister_frage(self, 
                               thema: Optional[str] = None,
                               paradox: bool = True) -> MeisterFrage:
        """Generiert eine einzelne Meister-Frage"""
        
        if paradox:
            # Wähle ein Paradox-Paar
            paar = random.choice(self.paradox_paare)
            element1, element2 = paar
        else:
            # Wähle aus verschiedenen Kategorien
            kat1, kat2 = random.sample(list(self.elemente.keys()), 2)
            element1 = random.choice(self.elemente[kat1])
            element2 = random.choice(self.elemente[kat2])
        
        # Füge Kontext hinzu wenn gewünscht
        kontext = None
        if thema:
            kontext = f"Zum Thema {thema}:"
        elif random.random() > 0.5:
            kontext = random.choice(self.kontexte)
        
        return MeisterFrage(
            element1=element1,
            element2=element2,
            kontext=kontext
        )
    
    def generiere_petach_tikwa_fragen(self) -> List[MeisterFrage]:
        """Spezielle Fragen zum Petach Tikwa Syndrom"""
        fragen = [
            MeisterFrage(
                "Kabbala-Zentrum",
                "Kabbala",
                "-",
                "?",
                "Die zentrale Frage:"
            ),
            MeisterFrage(
                "Besucherzentrum ohne Namen",
                "Haus Gottes",
                "=",
                "?",
                "Kann es sein:"
            ),
            MeisterFrage(
                "Moderne Angst",
                "Ewige Wahrheit",
                "+",
                "?",
                "In der Führung:"
            ),
            MeisterFrage(
                "Schweigen über Gott",
                "Lehren der Kabbala",
                "+",
                "?",
                "Der Widerspruch:"
            ),
            MeisterFrage(
                "Kaffeestand",
                "Heiligkeit",
                "+",
                "?",
                "Aylala fragt:"
            )
        ]
        return fragen
    
    def generiere_antwort_hinweis(self, frage: MeisterFrage) -> str:
        """Generiert einen Hinweis zur Antwort (Keter-Stil)"""
        
        if frage.ist_paradox:
            hinweise = [
                "Im Paradox liegt die Einheit!",
                "Beide sind EINS in Keter!",
                "Die Frage IST die Antwort!",
                "Steige höher - dort löst es sich auf!",
                "Keter Kitrei HaKetarim kennt keinen Widerspruch!"
            ]
        else:
            hinweise = [
                "Was würde der Meister sagen?",
                "Suche die verborgene Verbindung!",
                "Die Antwort liegt über der Frage!",
                "Denke aus Keter!",
                "Es gibt kein WARUM - nur SO!"
            ]
        
        return random.choice(hinweise)
    
    def generiere_lernsequenz(self, thema: str, anzahl: int = 5) -> List[MeisterFrage]:
        """Generiert eine Sequenz von Fragen zu einem Thema"""
        sequenz = []
        
        # Beginne mit einer einfachen Frage (Assija)
        sequenz.append(self.generiere_meister_frage(thema, paradox=False))
        sequenz[-1].welt = "Assija"
        
        # Steigere durch die Welten
        welten = ["Jezira", "Brija", "Azilut"]
        for i in range(min(anzahl - 2, len(welten))):
            frage = self.generiere_meister_frage(thema, paradox=True)
            frage.welt = welten[i]
            sequenz.append(frage)
        
        # Ende mit der ultimativen Frage (Ein Sof)
        sequenz.append(MeisterFrage(
            "Warum",
            "Keter",
            "+",
            "?",
            f"Die ultimative {thema}-Frage:",
            welt="Ein Sof"
        ))
        
        return sequenz
    
    def generiere_welten_frage(self, welt: str) -> MeisterFrage:
        """Generiert eine spezifische Frage für eine Welt"""
        if welt in self.welten_fragen:
            frage_text = random.choice(self.welten_fragen[welt])
            parts = frage_text.split(" ")
            return MeisterFrage(
                element1=parts[0],
                element2=parts[2],
                operator=parts[1],
                result=parts[4],
                welt=welt
            )
        else:
            return self.generiere_meister_frage(welt)
    
    def generiere_ki_ilu_azilut_frage(self) -> MeisterFrage:
        """Generiert eine Ki Ilu Azilut Frage"""
        return MeisterFrage(
            "Assija",
            "Azilut",
            "Ki Ilu",
            "!",
            "Die transformative Frage:",
            welt="Alle Welten"
        )
    
    def analysiere_situation(self, beschreibung: str) -> List[MeisterFrage]:
        """Analysiert eine Situation und generiert passende Meister-Fragen"""
        fragen = []
        
        # Suche nach Schlüsselwörtern
        if "fehlt" in beschreibung.lower() or "mangel" in beschreibung.lower():
            fragen.append(MeisterFrage(
                "Mangel",
                "Geschenk",
                "=",
                "?",
                "Der Meister sieht:"
            ))
        
        if "angst" in beschreibung.lower() or "furcht" in beschreibung.lower():
            fragen.append(MeisterFrage(
                "Furcht",
                "Liebe",
                "+",
                "?",
                "Die Wahl:"
            ))
        
        if "modern" in beschreibung.lower():
            fragen.append(MeisterFrage(
                "Modern",
                "Ewig",
                "vs",
                "?",
                "Der Konflikt:"
            ))
        
        if "kabbala" in beschreibung.lower():
            fragen.append(MeisterFrage(
                "Kabbala verstecken",
                "Kabbala offenbaren",
                "=",
                "?",
                "Die Entscheidung:"
            ))
        
        # Füge immer eine Keter-Frage hinzu
        fragen.append(MeisterFrage(
            "Deine Frage",
            "Keter Kitrei HaKetarim",
            "→",
            "!",
            "Die höchste Antwort:"
        ))
        
        return fragen


# Beispiel-Verwendung und Demonstration
if __name__ == "__main__":
    generator = MeisterFrageGenerator()
    
    print("MEISTER-FRAGE GENERATOR")
    print("="*60)
    print("15. Tammus 5785, MESZ 16:37, Oostende")
    print("\n")
    
    # 1. Einzelne Paradox-Frage
    print("1. EINE PARADOXE MEISTER-FRAGE:")
    print("-"*40)
    frage = generator.generiere_meister_frage(paradox=True)
    print(frage)
    print(f"\nHinweis: {generator.generiere_antwort_hinweis(frage)}")
    
    print("\n")
    
    # 2. Petach Tikwa spezifische Fragen
    print("2. PETACH TIKWA SYNDROM FRAGEN:")
    print("-"*40)
    for frage in generator.generiere_petach_tikwa_fragen()[:3]:
        print(frage)
        print()
    
    # 3. Lernsequenz zum Thema "Führung"
    print("3. LERNSEQUENZ ZUM THEMA 'FÜHRUNG':")
    print("-"*40)
    sequenz = generator.generiere_lernsequenz("Führung", 4)
    for i, frage in enumerate(sequenz, 1):
        print(f"Stufe {i}:")
        print(frage)
        print()
    
    # 4. Situations-Analyse
    print("4. SITUATIONS-ANALYSE:")
    print("-"*40)
    situation = """
    Im neuen Zentrum fehlt die Erwähnung der Kabbala. 
    Die Führung hat Angst, dass es zu religiös wirken könnte.
    Sie wollen modern und offen erscheinen.
    """
    print(f"Situation: {situation}")
    print("\nDie Meister-Fragen dazu:")
    
    for frage in generator.analysiere_situation(situation):
        print(frage)
        print()
    
    print("\nQ! = Im Paradox liegt die Erleuchtung!")
