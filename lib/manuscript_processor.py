#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manuscript Processor für Ez Chajim
==================================

Verarbeitet hebräische Manuskripte mit Gematria-Analyse
und WWAQ-konformer Transformation.

Stand: 20. Tammus 5785
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import json
from pathlib import Path
from datetime import datetime

class ManuscriptProcessor:
    """Hauptklasse für Manuskript-Verarbeitung"""
    
    def __init__(self):
        self.gematria_values = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
            'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
            'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
            'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80,
            'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
            'ש': 300, 'ת': 400
        }
        
        # WWAQ-Transformationen
        self.wwaq_replacements = {
            'כבלה': 'קבלה',
            'קבלה': 'קבלה',  # Bereits korrekt
            'כוונה': 'קוונה',
            'קוונה': 'קוונה',  # Bereits korrekt
            'צמצום': 'צמצום',  # Bleibt
            'אין סוף': 'אין סוף',  # Bleibt
        }
        
        # Spezielle Ez Chajim Begriffe
        self.ez_chajim_terms = {
            'עץ חיים': 'Baum des Lebens',
            'ספירות': 'Sefirot',
            'פרצופים': 'Parzufim',
            'עולמות': 'Welten',
            'אצילות': 'Azilut',
            'בריאה': 'Briah',
            'יצירה': 'Jezirah',
            'עשיה': 'Asijah'
        }
    
    def calculate_gematria(self, text: str) -> int:
        """Berechnet Gematria-Wert eines Textes"""
        total = 0
        for char in text:
            if char in self.gematria_values:
                total += self.gematria_values[char]
        return total
    
    def calculate_gematria_methods(self, text: str) -> Dict[str, int]:
        """Berechnet verschiedene Gematria-Methoden"""
        # Standard Gematria
        standard = self.calculate_gematria(text)
        
        # Kleine Gematria (Mispar Katan)
        small = sum((self.gematria_values.get(char, 0) - 1) % 9 + 1 
                   for char in text if char in self.gematria_values)
        
        # Volle Gematria (Milui) - vereinfacht
        full_values = {
            'א': 111, 'ב': 412, 'ג': 83, 'ד': 434, 'ה': 6,
            'ו': 13, 'ז': 67, 'ח': 418, 'ט': 419, 'י': 20,
            'כ': 100, 'ל': 74, 'מ': 90, 'נ': 106, 'ס': 120,
            'ע': 130, 'פ': 81, 'צ': 104, 'ק': 186, 'ר': 510,
            'ש': 360, 'ת': 406
        }
        full = sum(full_values.get(char, 0) for char in text)
        
        return {
            'standard': standard,
            'small': small,
            'full': full,
            'ordinal': len([c for c in text if c in self.gematria_values])
        }
    
    def apply_wwaq_transformation(self, text: str) -> Tuple[str, List[str]]:
        """Wendet WWAQ-Transformationen an"""
        transformed = text
        changes = []
        
        for old, new in self.wwaq_replacements.items():
            if old in transformed and old != new:
                count = transformed.count(old)
                transformed = transformed.replace(old, new)
                changes.append(f"{old} → {new} ({count}x)")
        
        # Spezielle Regeln
        if 'כ' in transformed and 'בלה' in transformed:
            # Prüfe auf versteckte Kabbala-Schreibweisen
            pattern = r'כ\s*ב\s*ל\s*ה'
            if re.search(pattern, transformed):
                transformed = re.sub(pattern, 'קבלה', transformed)
                changes.append("כ-ב-ל-ה → קבלה (getrennt)")
        
        return transformed, changes
    
    def extract_chunks(self, text: str, chunk_size: int = 500) -> List[Dict]:
        """Teilt Text in Chunks mit Metadaten"""
        # Bereinige Text
        clean_text = re.sub(r'\s+', ' ', text.strip())
        
        # Finde natürliche Trennstellen (Satzenden)
        sentences = re.split(r'([.!?:]\s+)', clean_text)
        
        chunks = []
        current_chunk = ""
        chunk_id = 1
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            separator = sentences[i + 1] if i + 1 < len(sentences) else ""
            
            if len(current_chunk) + len(sentence) + len(separator) > chunk_size:
                if current_chunk:
                    chunks.append(self._create_chunk(current_chunk.strip(), chunk_id))
                    chunk_id += 1
                current_chunk = sentence + separator
            else:
                current_chunk += sentence + separator
        
        # Letzter Chunk
        if current_chunk:
            chunks.append(self._create_chunk(current_chunk.strip(), chunk_id))
        
        return chunks
    
    def _create_chunk(self, text: str, chunk_id: int) -> Dict:
        """Erstellt einen Chunk mit Metadaten"""
        # WWAQ-Transformation
        transformed_text, changes = self.apply_wwaq_transformation(text)
        
        # Gematria-Analyse
        gematria = self.calculate_gematria_methods(text)
        
        # Extrahiere Schlüsselbegriffe
        key_terms = []
        for term, translation in self.ez_chajim_terms.items():
            if term in text:
                count = text.count(term)
                key_terms.append({
                    'hebrew': term,
                    'translation': translation,
                    'count': count,
                    'gematria': self.calculate_gematria(term)
                })
        
        return {
            'id': f"CHUNK_{chunk_id:04d}",
            'original': text,
            'transformed': transformed_text,
            'metadata': {
                'length': len(text),
                'words': len(text.split()),
                'gematria': gematria,
                'wwaq_changes': changes,
                'key_terms': key_terms,
                'created': datetime.now().isoformat()
            }
        }
    
    def analyze_manuscript(self, file_path: Path) -> Dict:
        """Analysiert komplettes Manuskript"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Chunks erstellen
        chunks = self.extract_chunks(text)
        
        # Gesamtanalyse
        total_gematria = sum(chunk['metadata']['gematria']['standard'] for chunk in chunks)
        all_key_terms = defaultdict(int)
        
        for chunk in chunks:
            for term in chunk['metadata']['key_terms']:
                all_key_terms[term['hebrew']] += term['count']
        
        # WWAQ-Statistik
        wwaq_stats = defaultdict(int)
        for chunk in chunks:
            for change in chunk['metadata']['wwaq_changes']:
                wwaq_stats[change] += 1
        
        return {
            'file': str(file_path),
            'analysis': {
                'total_chunks': len(chunks),
                'total_words': sum(chunk['metadata']['words'] for chunk in chunks),
                'total_gematria': total_gematria,
                'average_gematria': total_gematria // len(chunks) if chunks else 0,
                'key_terms_frequency': dict(all_key_terms),
                'wwaq_transformations': dict(wwaq_stats)
            },
            'chunks': chunks
        }
    
    def create_translation_batch(self, chunks: List[Dict], batch_size: int = 10) -> List[Dict]:
        """Erstellt Batches für Claude-Übersetzung"""
        batches = []
        
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            
            batch = {
                'batch_id': f"BATCH_{i//batch_size + 1:03d}",
                'chunk_ids': [chunk['id'] for chunk in batch_chunks],
                'instruction': self._create_translation_instruction(),
                'chunks': [
                    {
                        'id': chunk['id'],
                        'text': chunk['transformed'],  # WWAQ-transformierter Text
                        'gematria_hint': chunk['metadata']['gematria']['standard'],
                        'key_terms': chunk['metadata']['key_terms']
                    }
                    for chunk in batch_chunks
                ]
            }
            
            batches.append(batch)
        
        return batches
    
    def _create_translation_instruction(self) -> str:
        """Erstellt Übersetzungsanweisung für Claude"""
        return """ÜBERSETZUNGSANWEISUNG für Ez Chajim:

1. WWAQ-KONFORMITÄT:
   - Verwende IMMER "Qabbala" (mit Q)
   - Verwende IMMER "Qawana" (mit Q)
   - NIEMALS "zerstören" → verwende "auflösen/wandeln"

2. FACHBEGRIFFE:
   - Behalte hebräische Begriffe mit deutscher Erklärung
   - Beispiel: "Die Sefirot (göttliche Emanationen)"

3. GEMATRIA:
   - Beachte Gematria-Werte für tiefere Bedeutungen
   - Weise auf bedeutsame Zahlenwerte hin

4. STIL:
   - Authentisch-treue Übersetzung (ATF)
   - Bewahre die Heiligkeit des Textes
   - Klare, würdevolle Sprache

Übersetze mit Ehrfurcht und Präzision. Q!"""
    
    def validate_chunk_translation(self, original: Dict, translation: str) -> Dict[str, bool]:
        """Validiert eine Chunk-Übersetzung"""
        validations = {
            'has_content': bool(translation.strip()),
            'wwaq_conform': all(term not in translation.lower() 
                              for term in ['kabbala', 'kawana', 'zerstör']),
            'maintains_key_terms': all(
                term['hebrew'] in translation or term['translation'] in translation
                for term in original['metadata']['key_terms']
            ),
            'reasonable_length': 0.5 <= len(translation) / len(original['original']) <= 2.0
        }
        
        return {
            'is_valid': all(validations.values()),
            'checks': validations
        }

# Hilfsfunktionen
def process_ez_chajim_manuscript(file_path: str) -> Dict:
    """Verarbeitet ein Ez Chajim Manuskript"""
    processor = ManuscriptProcessor()
    return processor.analyze_manuscript(Path(file_path))

def create_translation_batches(manuscript_analysis: Dict, batch_size: int = 10) -> List[Dict]:
    """Erstellt Übersetzungs-Batches aus Manuskript-Analyse"""
    processor = ManuscriptProcessor()
    return processor.create_translation_batch(manuscript_analysis['chunks'], batch_size)

# Test und Beispiel
if __name__ == "__main__":
    print("Manuscript Processor Test")
    print("=" * 50)
    
    # Test-Text
    test_text = """עץ חיים היא למחזיקים בה. 
    הספירות הן עשר ולא תשע, עשר ולא אחת עשרה.
    הכוונה בלימוד הקבלה היא דבקות בשם."""
    
    processor = ManuscriptProcessor()
    
    # WWAQ-Transformation
    transformed, changes = processor.apply_wwaq_transformation(test_text)
    print("WWAQ-Transformation:")
    print(f"Original: {test_text}")
    print(f"Transformiert: {transformed}")
    print(f"Änderungen: {changes}")
    
    # Gematria
    gematria = processor.calculate_gematria_methods(test_text)
    print(f"\nGematria-Werte: {gematria}")
    
    print("\nQ!")
