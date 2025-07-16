#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEISTER FRAGE Tool - Starter Script
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from meister_frage_tool import MeisterFrageTool

def main():
    print("=== MEISTER FRAGE Tool ===")
    print("Stand: 12. Tammus 5785")
    print()
    
    tool = MeisterFrageTool()
    
    print("Geben Sie einen Text ein (Enter + Enter zum Beenden):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    if lines:
        text = " ".join(lines)
        ergebnis = tool.verarbeite_text(text)
        
        if ergebnis['beste_frage']:
            print(f"\n🏆 BESTE FRAGE:")
            print(f"   {ergebnis['beste_frage'].frage}")
            print(f"\n   Kraft: {ergebnis['beste_frage'].scores['kraft']:.2f}")
            print(f"   Tiefe: {ergebnis['beste_frage'].scores['tiefe']:.2f}")
            print(f"   WOZU: {ergebnis['beste_frage'].scores['wozu']:.2f}")
        
        # Export
        tool.export_yaml(ergebnis, "output/letzte_analyse.yaml")
        print(f"\n✓ Analyse exportiert nach: output/letzte_analyse.yaml")
    
    print("\nQ!")

if __name__ == "__main__":
    main()
