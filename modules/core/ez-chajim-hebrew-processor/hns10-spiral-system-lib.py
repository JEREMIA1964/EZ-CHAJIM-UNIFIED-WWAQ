#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HNS10 Spiral System - Hebraic Numeric Spiral 10
===============================================

WWAK-konforme Implementierung des Spiralzeit-Systems
Stand: 14. Tammus 5785

Null-Linien-Tabu: Grad 0 ist verboten!
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import math
import pyluach
from hijri_converter import Hijri, Gregorian

class HNS10SpiralSystem:
    """
    HNS10 Spiralzeit-System mit Drei-Kalender-Integration
    
    Features:
    - Null-Linien-Tabu (Grad 0 verboten)
    - Hebräischer Primärkalender
    - Solar/Islamisch Sekundärkalender
    - Spiralzeit-Berechnung
    """
    
    def __init__(self, null_tabu: bool = True):
        """
        Initialisiert HNS10 System
        
        Args:
            null_tabu: Wenn True, ist Grad 0 verboten (Standard)
        """
        self.null_tabu = null_tabu
        self.min_grad = 1 if null_tabu else 0
        self.max_grad = 360
        
        # Spiralkonstanten
        self.phi = (1 + math.sqrt(5)) / 2  # Goldener Schnitt
        self.spiralwindungen = 10
        
        # Zeitbasis
        self.epoch_hebrew = pyluach.HebrewDate(5785, 7, 1)  # 1. Tischri 5785
        self.epoch_gregorian = datetime(2024, 10, 3)  # Entsprechung
        
        print(f"HNS10 Spiralsystem initialisiert (Null-Tabu: {null_tabu})")
    
    def get_current_hebrew_date(self) -> pyluach.HebrewDate:
        """Hole aktuelles hebräisches Datum"""
        return pyluach.HebrewDate.today()
    
    def get_current_islamic_date(self) -> Dict[str, int]:
        """Hole aktuelles islamisches Datum"""
        today = datetime.now()
        hijri = Hijri.fromdate(today)
        
        return {
            'jahr': hijri.year,
            'monat': hijri.month,
            'tag': hijri.day,
            'monatsname': hijri.month_name()
        }
    
    def get_three_calendar_sync(self) -> Dict[str, str]:
        """
        Synchronisiert alle drei Kalender
        
        Returns:
            Dictionary mit allen drei Kalenderdaten
        """
        # Hebräisch (Primär)
        hebrew = self.get_current_hebrew_date()
        hebrew_str = f"{hebrew.day}. {hebrew.month_name()} {hebrew.year}"
        
        # Solar (Gregorianisch)
        solar = datetime.now()
        solar_str = solar.strftime("%d. %B %Y")
        
        # Islamisch
        islamic = self.get_current_islamic_date()
        islamic_str = f"{islamic['tag']}. {islamic['monatsname']} {islamic['jahr']}"
        
        return {
            'hebrew': hebrew_str,
            'solar': solar_str,
            'islamic': islamic_str,
            'primary': 'hebrew'
        }
    
    def calculate_spiral_position(self, date: datetime) -> Tuple[float, float, int]:
        """
        Berechnet Spiralposition für ein Datum
        
        Args:
            date: Datum für Berechnung
            
        Returns:
            (radius, winkel, windung)
        """
        # Tage seit Epoche
        delta = date - self.epoch_gregorian
        tage = delta.days
        
        # Spiralberechnung
        windung = (tage // 365) % self.spiralwindungen
        tage_in_windung = tage % 365
        
        # Winkel (1-360, niemals 0!)
        winkel_roh = (tage_in_windung / 365) * 360
        winkel = max(self.min_grad, winkel_roh) if self.null_tabu else winkel_roh
        
        # Radius mit goldenem Schnitt
        radius = windung * self.phi + (tage_in_windung / 365) * self.phi
        
        return radius, winkel, windung
    
    def get_current_spiral_time(self) -> str:
        """
        Hole aktuelle Spiralzeit im Format Jahr.Monat.Tag.Stunde
        
        Returns:
            Spiralzeit-String
        """
        now = datetime.now()
        hebrew = self.get_current_hebrew_date()
        
        # Format: HebrJahr.Monat.Tag.Stunde
        spiral_time = f"{hebrew.year}.{hebrew.month}.{hebrew.day}.{now.hour}"
        
        return spiral_time
    
    def get_spiral_coordinates(self) -> Dict[str, float]:
        """
        Berechnet aktuelle Spiralkoordinaten
        
        Returns:
            Dictionary mit Koordinaten
        """
        now = datetime.now()
        radius, winkel, windung = self.calculate_spiral_position(now)
        
        # Kartesische Koordinaten
        x = radius * math.cos(math.radians(winkel))
        y = radius * math.sin(math.radians(winkel))
        
        return {
            'radius': radius,
            'winkel': winkel,
            'windung': windung,
            'x': x,
            'y': y,
            'spiralzeit': self.get_current_spiral_time()
        }
    
    def validate_spiral_degree(self, grad: float) -> bool:
        """
        Validiert einen Grad-Wert gemäß Null-Tabu
        
        Args:
            grad: Zu prüfender Grad-Wert
            
        Returns:
            True wenn valide
        """
        if self.null_tabu and grad == 0:
            raise ValueError("Null-Linien-Tabu: Grad 0 ist verboten!")
        
        return self.min_grad <= grad <= self.max_grad
    
    def calculate_omer_position(self, hebrew_date: pyluach.HebrewDate) -> Optional[int]:
        """
        Berechnet Omer-Position (1-49) wenn in Omer-Zeit
        
        Args:
            hebrew_date: Hebräisches Datum
            
        Returns:
            Omer-Tag (1-49) oder None
        """
        # Omer beginnt am 16. Nissan
        if hebrew_date.month == 1 and hebrew_date.day >= 16:
            return hebrew_date.day - 15
        elif hebrew_date.month == 2:  # Iyar
            return 15 + hebrew_date.day
        elif hebrew_date.month == 3 and hebrew_date.day <= 5:  # Sivan bis 5.
            return 44 + hebrew_date.day
        
        return None
    
    def get_weekly_portion(self) -> str:
        """
        Hole aktuelle Wochenlesung (Parascha)
        
        Returns:
            Name der aktuellen Parascha
        """
        hebrew = self.get_current_hebrew_date()
        
        # Hier würde normalerweise eine vollständige Parascha-Berechnung stehen
        # Für Demo: Vereinfachte Version
        parschiot = [
            "Bereschit", "Noach", "Lech Lecha", "Wajera", "Chaje Sara",
            "Toldot", "Wajeze", "Wajischlach", "Wajeschew", "Mikez"
        ]
        
        # Sehr vereinfachte Berechnung
        wochen_seit_tischri = (hebrew.month - 7) * 4 + (hebrew.day // 7)
        parascha_index = wochen_seit_tischri % len(parschiot)
        
        return parschiot[parascha_index]
    
    def format_hebrew_date(self, include_portion: bool = True) -> str:
        """
        Formatiert hebräisches Datum mit optionaler Wochenlesung
        
        Args:
            include_portion: Wochenlesung einschließen?
            
        Returns:
            Formatiertes Datum
        """
        hebrew = self.get_current_hebrew_date()
        date_str = f"{hebrew.day}. {hebrew.month_name()} {hebrew.year}"
        
        if include_portion:
            portion = self.get_weekly_portion()
            date_str += f" (Parascha: {portion})"
        
        # Omer-Zeit?
        omer = self.calculate_omer_position(hebrew)
        if omer:
            date_str += f" [Omer-Tag {omer}]"
        
        return date_str
    
    def __repr__(self) -> str:
        """String-Repräsentation"""
        coords = self.get_spiral_coordinates()
        return (
            f"HNS10SpiralSystem("
            f"spiralzeit={coords['spiralzeit']}, "
            f"windung={coords['windung']}, "
            f"winkel={coords['winkel']}°)"
        )

# Convenience-Funktionen
def get_spiral_time() -> str:
    """Hole aktuelle Spiralzeit"""
    hns10 = HNS10SpiralSystem()
    return hns10.get_current_spiral_time()

def get_hebrew_date() -> str:
    """Hole formatiertes hebräisches Datum"""
    hns10 = HNS10SpiralSystem()
    return hns10.format_hebrew_date()

def validate_degree(grad: float) -> bool:
    """Validiere Grad gemäß Null-Tabu"""
    hns10 = HNS10SpiralSystem()
    return hns10.validate_spiral_degree(grad)

# Test wenn direkt ausgeführt
if __name__ == "__main__":
    print("=== HNS10 Spiral System Test ===")
    
    hns10 = HNS10SpiralSystem()
    
    # Zeige alle drei Kalender
    kalender = hns10.get_three_calendar_sync()
    print("\nKalender-Synchronisation:")
    for typ, datum in kalender.items():
        if typ != 'primary':
            print(f"  {typ.capitalize()}: {datum}")
    
    # Spiralkoordinaten
    coords = hns10.get_spiral_coordinates()
    print(f"\nSpiralkoordinaten:")
    print(f"  Spiralzeit: {coords['spiralzeit']}")
    print(f"  Windung: {coords['windung']}")
    print(f"  Winkel: {coords['winkel']}°")
    print(f"  Position: ({coords['x']:.2f}, {coords['y']:.2f})")
    
    # Hebräisches Datum mit Details
    print(f"\nHebräisch: {hns10.format_hebrew_date()}")
    
    print("\nQ!")
