#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from meister_frage_tool import MeisterFrageTool

# Test die 3 Tiefen
tool = MeisterFrageTool()

test_fragen = [
    "Zwang + Liebe = ?",
    "WOZU braucht die Liebe den Zwang?",
    "WIE wird Zwang zu Liebe?"
]

print("=== DIE 3 TIEFEN NACH RAV LAITMAN ===\n")

for frage in test_fragen:
    print(f"Frage: {frage}")
    
    # Simuliere die 3 Tiefen Bewertung
    # 1. Kind verstehen?
    kind_score = 0.9 if len(frage) < 30 else 0.6
    print(f"  1. Kind verstehen: {'⭐' * int(kind_score * 5)}")
    
    # 2. Qabbalist 2h reden?
    qab_score = 0.8 if any(w in frage for w in ['Zwang', 'Liebe', 'WOZU']) else 0.5
    print(f"  2. Qabbalist reden: {'⭐' * int(qab_score * 5)}")
    
    # 3. Azilut-Verankerung?
    azilut_score = 0.9 if 'WOZU' in frage else 0.6
    print(f"  3. Azilut-Verankerung: {'⭐' * int(azilut_score * 5)}")
    
    gesamt = (kind_score + qab_score + azilut_score) / 3
    print(f"  Gesamt: {gesamt:.2f}")
    print()

print("\nQuelle: Rabash, Artikel 37 (1991)")
print("Ort: Bnei Brak, Israel")
print("Ereignis: Wöchentliche Gruppenversammlung")
print("\nQ!")
