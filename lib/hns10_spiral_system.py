#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HNS10 Spiral System - Kernbibliothek
===================================

Implementiert das Hebräische Numeral-System mit Null-Tabu
und Drei-Kalender-Integration für Ez Chajim.

Stand: 20. Tammus 5785
WWAQ-konform
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, List, Optional, Union
import pyluach
from hijri_converter import convert
import math
import json
from dataclasses import dataclass

# HNS10 Konstanten
HEBREW_NUMERALS = {
    1: 'א', 2: 'ב', 3: 'ג', 4: 'ד', 5: 'ה',
    6: 'ו', 7: 'ז', 8: 'ח', 9: 'ט', 10: 'י',
    20: 'כ', 30: 'ל', 40: 'מ', 50: 'נ', 60: 'ס',
    70: 'ע', 80: 'פ', 90: 'צ', 100: 'ק', 200: 'ר',
    300: 'ש', 400: 'ת'
}

# Null-Tabu: Grad 0 ist verboten
NULL_TABU_MESSAGE = "⚠️ NULL-TABU: Grad 0 ist im HNS10 verboten!"

# Spiralzeit-Konstanten
SPIRAL_SEGMENTS = {
    'תשרי': 1, 'חשון': 2, 'כסלו': 3, 'טבת': 4,
    'שבט': 5, 'אדר': 6, 'ניסן': 7, 'אייר': 8,
    'סיון': 9, 'תמוז': 10, 'אב': 11, 'אלול': 12
}

@dataclass
class SpiralCoordinate:
    """Repräsentiert eine Koordinate im Spiralsystem"""
    windung: int  # Jahr
    segment: int  # Monat
    punkt: float  # Tag.Stunde
    grad: int     # HNS10 Grad (nie 0!)
    
    def __post_init__(self):
        if self.grad == 0:
            raise ValueError(NULL_TABU_MESSAGE)
    
    def to_string(self) -> str:
        """Formatiert als Spiralzeit-String"""
        return f"{self.windung}.{self.segment}.{self.punkt:.2f}"

class HNS10SpiralSystem:
    """Hauptklasse für das HNS10 Spiralsystem"""
    
    def __init__(self):
        self.current_hebrew_date = pyluach.today()
        self.omer_count = self._calculate_omer()
    
    def _calculate_omer(self) -> Optional[int]:
        """Berechnet aktuellen Omer-Tag (1-49)"""
        today = pyluach.today()
        pesach_16 = pyluach.HebrewDate(today.year, 1, 16)
        shavuot = pyluach.HebrewDate(today.year, 3, 6)
        
        if pesach_16 <= today <= shavuot:
            return (today - pesach_16).days + 1
        return None
    
    def hebrew_to_hns10(self, value: int) -> str:
        """Konvertiert Zahl zu hebräischen Buchstaben (HNS10)"""
        if value == 0:
            raise ValueError(NULL_TABU_MESSAGE)
        
        if value < 0:
            return f"-{self.hebrew_to_hns10(abs(value))}"
        
        result = []
        
        # Tausender
        thousands = value // 1000
        if thousands > 0:
            result.append(self.hebrew_to_hns10(thousands))
            result.append("'")
            value %= 1000
        
        # Hunderter
        hundreds = value // 100
        if hundreds > 0:
            result.append(HEBREW_NUMERALS[hundreds * 100])
            value %= 100
        
        # Zehner und Einer
        if value >= 10:
            if value == 15:
                result.extend(['ט', 'ו'])
            elif value == 16:
                result.extend(['ט', 'ז'])
            else:
                tens = (value // 10) * 10
                ones = value % 10
                result.append(HEBREW_NUMERALS[tens])
                if ones > 0:
                    result.append(HEBREW_NUMERALS[ones])
        elif value > 0:
            result.append(HEBREW_NUMERALS[value])
        
        return ''.join(result)
    
    def calculate_spiral_position(self, date: datetime) -> SpiralCoordinate:
        """Berechnet Spiralposition für gegebenes Datum"""
        hebrew_date = pyluach.from_pydate(date)
        
        # Windung = Jahr
        windung = hebrew_date.year
        
        # Segment = Monat
        segment = hebrew_date.month
        
        # Punkt = Tag + Stunde als Dezimal
        punkt = hebrew_date.day + (date.hour / 24.0)
        
        # Grad berechnen (Spiralwinkel, nie 0)
        total_days = hebrew_date.day_of_year
        year_days = 354 if not hebrew_date.is_leap_year else 384
        grad = int((total_days / year_days) * 360)
        
        # Null-Tabu beachten
        if grad == 0:
            grad = 1
        
        return SpiralCoordinate(windung, segment, punkt, grad)
    
    def get_three_calendars(self, date: datetime) -> Dict[str, str]:
        """Gibt Datum in drei Kalendersystemen zurück"""
        # Hebräisch
        hebrew = pyluach.from_pydate(date)
        hebrew_str = f"{hebrew.day}. {hebrew.month_name()} {hebrew.year}"
        
        # Islamisch
        islamic = convert.Gregorian(date.year, date.month, date.day).to_hijri()
        islamic_str = f"{islamic.day}. {islamic.month_name()} {islamic.year}"
        
        # Solar (Gregorianisch)
        solar_str = date.strftime("%d. %B %Y")
        
        return {
            'hebrew': hebrew_str,
            'islamic': islamic_str,
            'solar': solar_str,
            'spiral': self.calculate_spiral_position(date).to_string()
        }
    
    def create_frage_antwort_lade(self, question: str, answer: str) -> Dict:
        """Erstellt eine Frage-Antwort-Lade mit Metadaten"""
        now = datetime.now()
        spiral_pos = self.calculate_spiral_position(now)
        
        return {
            'id': f"FAL_{spiral_pos.windung}_{spiral_pos.segment}_{int(spiral_pos.punkt)}",
            'frage': question,
            'antwort': answer,
            'metadata': {
                'erstellt': now.isoformat(),
                'spiralzeit': spiral_pos.to_string(),
                'kalender': self.get_three_calendars(now),
                'omer': self.omer_count,
                'grad_hns10': self.hebrew_to_hns10(spiral_pos.grad)
            }
        }
    
    def calculate_gematria(self, text: str) -> int:
        """Berechnet Gematria-Wert eines hebräischen Textes"""
        gematria_values = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
            'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
            'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
            'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80,
            'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
            'ש': 300, 'ת': 400
        }
        
        total = 0
        for char in text:
            if char in gematria_values:
                total += gematria_values[char]
        
        return total
    
    def generate_omer_path(self, day: int) -> Dict:
        """Generiert Studienpfad für Omer-Tag"""
        if not 1 <= day <= 49:
            raise ValueError("Omer-Tag muss zwischen 1 und 49 liegen")
        
        # Woche und Tag berechnen
        week = (day - 1) // 7 + 1
        weekday = (day - 1) % 7 + 1
        
        # Sefirot-Kombinationen
        sefirot = ['חסד', 'גבורה', 'תפארת', 'נצח', 'הוד', 'יסוד', 'מלכות']
        
        return {
            'tag': day,
            'woche': week,
            'tag_in_woche': weekday,
            'sefira_woche': sefirot[week - 1],
            'sefira_tag': sefirot[weekday - 1],
            'kombination': f"{sefirot[weekday - 1]} שב{sefirot[week - 1]}",
            'grad_hns10': self.hebrew_to_hns10(day)
        }
    
    def validate_null_tabu(self, value: Union[int, float, str]) -> bool:
        """Validiert dass Null-Tabu eingehalten wird"""
        if isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            try:
                num_value = float(value)
                return num_value != 0
            except ValueError:
                return True  # Nicht-numerische Strings sind OK
        return True
    
    def format_for_yaml(self, data: Dict) -> Dict:
        """Formatiert Daten YAML-Ez-Chajim-konform"""
        formatted = {
            'ez_chajim_header': {
                'version': 'WWAQ-1.0',
                'spiralzeit': self.calculate_spiral_position(datetime.now()).to_string(),
                'null_tabu_validated': True
            },
            'content': data
        }
        
        # Rekursive Null-Tabu-Validierung
        def validate_recursive(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if not self.validate_null_tabu(value):
                        raise ValueError(f"{NULL_TABU_MESSAGE} in {key}")
                    validate_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    validate_recursive(item)
        
        validate_recursive(formatted)
        return formatted

# Hilfsfunktionen für direkten Import
def create_system() -> HNS10SpiralSystem:
    """Factory-Funktion für HNS10-System"""
    return HNS10SpiralSystem()

def get_current_spiral_time() -> str:
    """Gibt aktuelle Spiralzeit zurück"""
    system = create_system()
    return system.calculate_spiral_position(datetime.now()).to_string()

def validate_wwaq_text(text: str) -> Dict[str, bool]:
    """Validiert Text auf WWAQ-Konformität"""
    violations = {
        'kabbala_statt_qabbala': 'kabbala' in text.lower() and 'qabbala' not in text.lower(),
        'kawana_statt_qawana': 'kawana' in text.lower() and 'qawana' not in text.lower(),
        'null_verwendet': '0' in text or 'null' in text.lower() or 'zero' in text.lower()
    }
    
    return {
        'is_valid': not any(violations.values()),
        'violations': violations
    }

# Beispiel-Verwendung und Tests
if __name__ == "__main__":
    print("HNS10 Spiral System - Test")
    print("=" * 50)
    
    system = create_system()
    
    # Aktuelle Spiralzeit
    current_spiral = system.calculate_spiral_position(datetime.now())
    print(f"Aktuelle Spiralzeit: {current_spiral.to_string()}")
    print(f"Grad (HNS10): {system.hebrew_to_hns10(current_spiral.grad)}")
    
    # Drei Kalender
    calendars = system.get_three_calendars(datetime.now())
    print("\nDrei Kalender:")
    for cal_type, date_str in calendars.items():
        print(f"  {cal_type}: {date_str}")
    
    # Omer-Beispiel
    if system.omer_count:
        omer_path = system.generate_omer_path(system.omer_count)
        print(f"\nOmer Tag {system.omer_count}: {omer_path['kombination']}")
    
    print("\nQ!")
