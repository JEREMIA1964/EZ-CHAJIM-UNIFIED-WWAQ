#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ez Chajim Manuskript-Prozessor
==============================

Verarbeitet Ez Chajim Manuskripte mit Gematria und Strukturerkennung
Stand: 14. Tammus 5785

WWAK-konform implementiert
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import unicodedata

class ManuscriptProcessor:
    """
    Prozessor für Ez Chajim Manuskripte
    
    Features:
    - WWAK-konforme Textverarbeitung
    - Gematria-Berechnung
    - Struktur-Erkennung
    - Frage-Antwort-Lade System
    """
    
    def __init__(self):
        """Initialisiert Manuskript-Prozessor"""
        
        # Gematria-Werte für hebräische Buchstaben
        self.gematria_values = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
            'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
            'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
            'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80,
            'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
            'ש': 300, 'ת': 400
        }
        
        # Struktur-Muster
        self.patterns = {
            'kapitel': re.compile(r'^#\s+(.+)$', re.MULTILINE),
            'abschnitt': re.compile(r'^##\s+(.+)$', re.MULTILINE),
            'unterabschnitt': re.compile(r'^###\s+(.+)$', re.MULTILINE),
            'frage': re.compile(r'^F:\s*(.+)$', re.MULTILINE),
            'antwort': re.compile(r'^A:\s*(.+)$', re.MULTILINE),
            'quelle': re.compile(r'^\[([^\]]+)\]$', re.MULTILINE),
            'hebräisch': re.compile(r'[\u0590-\u05FF]+'),
            'lade': re.compile(r'^LADE\s+(\d+):\s*(.+)$', re.MULTILINE),
            'vers': re.compile(r'^\d+\.\s+(.+)$', re.MULTILINE)
        }
        
        # WWAK-Transformationen
        self.wwak_transforms = {
            'Kabbala': 'Kabbala',
            'kabbala': 'kabbala',
            'Kawana': 'Kawana',
            'kawana': 'kawana',
            'Kelim': 'Qelim',
            'kelim': 'qelim',
            'zerstören': 'auflösen',
            'zerbrechen': 'bersten',
            'zerfetzen': 'reißen'
        }
        
        print("✓ Manuskript-Prozessor initialisiert")
    
    def calculate_gematria(self, text: str) -> int:
        """
        Berechnet Gematria-Wert eines Textes
        
        Args:
            text: Hebräischer Text
            
        Returns:
            Gematria-Wert
        """
        total = 0
        for char in text:
            if char in self.gematria_values:
                total += self.gematria_values[char]
        
        return total
    
    def find_gematria_connections(self, words: List[str]) -> Dict[int, List[str]]:
        """
        Findet Wörter mit gleichem Gematria-Wert
        
        Args:
            words: Liste hebräischer Wörter
            
        Returns:
            Dictionary: Gematria-Wert -> Liste von Wörtern
        """
        connections = defaultdict(list)
        
        for word in words:
            value = self.calculate_gematria(word)
            if value > 0:
                connections[value].append(word)
        
        # Nur Verbindungen mit mehreren Wörtern
        return {k: v for k, v in connections.items() if len(v) > 1}
    
    def extract_structure(self, text: str) -> Dict[str, List]:
        """
        Extrahiert Struktur aus Manuskript
        
        Args:
            text: Manuskript-Text
            
        Returns:
            Dictionary mit Strukturelementen
        """
        structure = {
            'kapitel': [],
            'abschnitte': [],
            'unterabschnitte': [],
            'fragen_antworten': [],
            'quellen': [],
            'hebräische_begriffe': [],
            'laden': [],
            'verse': []
        }
        
        # Kapitel extrahieren
        for match in self.patterns['kapitel'].finditer(text):
            structure['kapitel'].append({
                'titel': match.group(1),
                'position': match.start()
            })
        
        # Abschnitte
        for match in self.patterns['abschnitt'].finditer(text):
            structure['abschnitte'].append({
                'titel': match.group(1),
                'position': match.start()
            })
        
        # Frage-Antwort-Paare
        fragen = list(self.patterns['frage'].finditer(text))
        antworten = list(self.patterns['antwort'].finditer(text))
        
        # Paare zuordnen
        for i, frage in enumerate(fragen):
            fa_paar = {
                'frage': frage.group(1),
                'frage_pos': frage.start(),
                'antwort': None,
                'antwort_pos': None
            }
            
            # Finde nächste Antwort nach dieser Frage
            for antwort in antworten:
                if antwort.start() > frage.start():
                    fa_paar['antwort'] = antwort.group(1)
                    fa_paar['antwort_pos'] = antwort.start()
                    break
            
            structure['fragen_antworten'].append(fa_paar)
        
        # Quellen
        for match in self.patterns['quelle'].finditer(text):
            structure['quellen'].append({
                'quelle': match.group(1),
                'position': match.start()
            })
        
        # Hebräische Begriffe
        hebr_terms = self.patterns['hebräisch'].findall(text)
        structure['hebräische_begriffe'] = list(set(hebr_terms))
        
        # Laden (Drawers)
        for match in self.patterns['lade'].finditer(text):
            structure['laden'].append({
                'nummer': int(match.group(1)),
                'titel': match.group(2),
                'position': match.start()
            })
        
        # Verse
        for match in self.patterns['vers'].finditer(text):
            structure['verse'].append({
                'text': match.group(1),
                'position': match.start()
            })
        
        return structure
    
    def apply_wwak_transformation(self, text: str) -> str:
        """
        Wendet WWAK-Transformationen auf Text an
        
        Args:
            text: Zu transformierender Text
            
        Returns:
            WWAK-konformer Text
        """
        result = text
        
        for old, new in self.wwak_transforms.items():
            result = result.replace(old, new)
        
        return result
    
    def segment_text(self, text: str, max_chunk_size: int = 1500) -> List[Dict]:
        """
        Segmentiert Text in semantisch sinnvolle Chunks
        
        WICHTIG: Trennt niemals Wörter oder Sätze!
        
        Args:
            text: Zu segmentierender Text
            max_chunk_size: Maximale Chunk-Größe
            
        Returns:
            Liste von Chunk-Dictionaries
        """
        chunks = []
        
        # Erst nach Kapiteln teilen
        kapitel_matches = list(self.patterns['kapitel'].finditer(text))
        
        if kapitel_matches:
            # Teile nach Kapiteln
            for i in range(len(kapitel_matches)):
                start = kapitel_matches[i].start()
                end = kapitel_matches[i+1].start() if i+1 < len(kapitel_matches) else len(text)
                
                kapitel_text = text[start:end]
                kapitel_titel = kapitel_matches[i].group(1)
                
                if len(kapitel_text) <= max_chunk_size:
                    chunks.append({
                        'text': kapitel_text,
                        'typ': 'kapitel',
                        'titel': kapitel_titel,
                        'start': start,
                        'end': end
                    })
                else:
                    # Kapitel zu groß, weiter unterteilen
                    sub_chunks = self._segment_by_paragraphs(
                        kapitel_text, max_chunk_size, start
                    )
                    chunks.extend(sub_chunks)
        else:
            # Keine Kapitel, nach Absätzen teilen
            chunks = self._segment_by_paragraphs(text, max_chunk_size, 0)
        
        return chunks
    
    def _segment_by_paragraphs(self, text: str, max_size: int, offset: int) -> List[Dict]:
        """Hilfsfunktion: Teilt Text nach Absätzen"""
        chunks = []
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        chunk_start = offset
        
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= max_size:
                if current_chunk:
                    current_chunk += "\n\n"
                current_chunk += para
            else:
                # Speichere aktuellen Chunk
                if current_chunk:
                    chunks.append({
                        'text': current_chunk,
                        'typ': 'absatz',
                        'start': chunk_start,
                        'end': chunk_start + len(current_chunk)
                    })
                
                # Starte neuen Chunk
                current_chunk = para
                chunk_start = chunk_start + len(current_chunk) + 2
        
        # Letzter Chunk
        if current_chunk:
            chunks.append({
                'text': current_chunk,
                'typ': 'absatz',
                'start': chunk_start,
                'end': chunk_start + len(current_chunk)
            })
        
        return chunks
    
    def analyze_content(self, text: str) -> Dict:
        """
        Vollständige Analyse eines Manuskripts
        
        Args:
            text: Manuskript-Text
            
        Returns:
            Analyse-Dictionary
        """
        # WWAK-Transformation
        wwak_text = self.apply_wwak_transformation(text)
        
        # Struktur extrahieren
        structure = self.extract_structure(wwak_text)
        
        # Gematria-Analyse
        hebrew_words = structure['hebräische_begriffe']
        gematria_connections = self.find_gematria_connections(hebrew_words)
        
        # Statistiken
        stats = {
            'zeichen': len(wwak_text),
            'wörter': len(wwak_text.split()),
            'zeilen': wwak_text.count('\n') + 1,
            'kapitel': len(structure['kapitel']),
            'abschnitte': len(structure['abschnitte']),
            'fragen_antworten': len(structure['fragen_antworten']),
            'hebräische_begriffe': len(structure['hebräische_begriffe']),
            'quellen': len(structure['quellen'])
        }
        
        return {
            'text': wwak_text,
            'struktur': structure,
            'gematria': gematria_connections,
            'statistiken': stats
        }
    
    def process(self, text: str) -> Dict:
        """
        Hauptverarbeitungsmethode
        
        Args:
            text: Zu verarbeitender Text
            
        Returns:
            Verarbeitungsergebnis
        """
        # Vollständige Analyse
        analysis = self.analyze_content(text)
        
        # Segmentierung
        chunks = self.segment_text(analysis['text'])
        
        # Ergebnis zusammenstellen
        result = {
            'original_length': len(text),
            'processed_length': len(analysis['text']),
            'wwak_transformed': text != analysis['text'],
            'struktur': analysis['struktur'],
            'statistiken': analysis['statistiken'],
            'chunks': chunks,
            'chunk_count': len(chunks)
        }
        
        # Gematria nur wenn vorhanden
        if analysis['gematria']:
            result['gematria_verbindungen'] = analysis['gematria']
        
        return result
    
    def format_summary(self, result: Dict) -> str:
        """
        Formatiert Verarbeitungsergebnis als Zusammenfassung
        
        Args:
            result: Verarbeitungsergebnis
            
        Returns:
            Formatierte Zusammenfassung
        """
        summary = "=== Manuskript-Verarbeitung ===\n\n"
        
        # Statistiken
        stats = result['statistiken']
        summary += "Statistiken:\n"
        summary += f"  • {stats['zeichen']} Zeichen\n"
        summary += f"  • {stats['wörter']} Wörter\n"
        summary += f"  • {stats['kapitel']} Kapitel\n"
        summary += f"  • {stats['fragen_antworten']} Frage-Antwort-Paare\n"
        summary += f"  • {stats['hebräische_begriffe']} hebräische Begriffe\n"
        
        # Chunks
        summary += f"\nSegmentierung:\n"
        summary += f"  • {result['chunk_count']} Text-Segmente erstellt\n"
        
        # WWAK
        if result['wwak_transformed']:
            summary += f"\n✓ WWAK-Transformationen angewendet\n"
        
        # Gematria
        if 'gematria_verbindungen' in result:
            summary += f"\nGematria-Verbindungen gefunden:\n"
            for value, words in result['gematria_verbindungen'].items():
                summary += f"  • {value}: {', '.join(words)}\n"
        
        summary += "\nQ!"
        
        return summary

# Test wenn direkt ausgeführt
if __name__ == "__main__":
    print("=== Manuskript-Prozessor Test ===")
    
    # Test-Text
    test_text = """# Die Lehre der Kabbala

Die Kabbala lehrt uns über den Lebensbaum.

F: Was ist Kawana?
A: Kawana ist die gerichtete Absicht beim Gebet.

[Sohar, Teil 1]

Die עץ חיים (Ez Chajim) symbolisiert die göttliche Struktur.
Das Wort חיים hat den Gematria-Wert 68.

## Die Sefirot

Die zehn Sefirot sind:
1. Keter - die Krone
2. Chochma - die Weisheit
3. Bina - das Verstehen

Q!
"""
    
    processor = ManuscriptProcessor()
    result = processor.process(test_text)
    print(processor.format_summary(result))
