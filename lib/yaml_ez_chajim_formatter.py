#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML Ez Chajim Formatter
========================

Formatiert Ez Chajim Inhalte in strukturiertes YAML
mit Omer-Studienpfaden und WWAQ-Validierung.

Stand: 20. Tammus 5785
"""

import yaml
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json
from pathlib import Path
import re

# Eigene YAML-Representer für bessere Formatierung
def hebrew_str_representer(dumper, data):
    """Spezielle Behandlung für hebräische Strings"""
    if any('\u0590' <= char <= '\u05FF' for char in data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, hebrew_str_representer)

class YAMLEzChajimFormatter:
    """Hauptklasse für YAML-Formatierung"""
    
    def __init__(self):
        # Ez Chajim Struktur-Schema
        self.schema_version = "1.0"
        self.current_date = datetime.now()
        
        # Omer-Sefirot Mapping
        self.sefirot = {
            1: 'חסד',    # Chesed
            2: 'גבורה',  # Gevurah
            3: 'תפארת',  # Tiferet
            4: 'נצח',    # Netzach
            5: 'הוד',    # Hod
            6: 'יסוד',   # Yesod
            7: 'מלכות'   # Malchut
        }
        
        # Struktur-Templates
        self.templates = {
            'chunk': self._get_chunk_template(),
            'omer_study': self._get_omer_template(),
            'metadata': self._get_metadata_template()
        }
    
    def _get_chunk_template(self) -> Dict:
        """Template für Chunk-Struktur"""
        return {
            'chunk_info': {
                'id': None,
                'source': 'Ez Chajim',
                'author': 'Chajim Vital',
                'tradition': 'Lurianische Qabbala'
            },
            'content': {
                'hebrew': None,
                'german': None,
                'commentary': []
            },
            'analysis': {
                'gematria': {},
                'key_concepts': [],
                'cross_references': []
            },
            'metadata': {
                'created': None,
                'modified': None,
                'wwaq_validated': False
            }
        }
    
    def _get_omer_template(self) -> Dict:
        """Template für Omer-Studienpfad"""
        return {
            'omer_day': None,
            'date': None,
            'sefirot_combination': {
                'week': None,
                'day': None,
                'full': None
            },
            'study_focus': {
                'theme': None,
                'meditation': None,
                'practical_work': None
            },
            'assigned_chunks': [],
            'reflections': []
        }
    
    def _get_metadata_template(self) -> Dict:
        """Template für Gesamt-Metadaten"""
        return {
            'ez_chajim_metadata': {
                'version': self.schema_version,
                'type': 'translation_project',
                'status': 'in_progress',
                'stats': {
                    'total_chunks': 1342,
                    'translated': 0,
                    'reviewed': 0,
                    'final': 0
                }
            },
            'project_info': {
                'name': 'Ez Chajim Deutsche Übersetzung',
                'method': 'ATF - Ausgabetreue Übersetzung',
                'principle': 'WWAQ - Wissenschaft der Weisheit der Authentischen Qabbala',
                'dedication': 'Für die Wiederherstellung des Dritten Tempels'
            }
        }
    
    def format_chunk(self, chunk_data: Dict) -> str:
        """Formatiert einen Chunk als YAML"""
        template = self.templates['chunk'].copy()
        
        # Fülle Template
        template['chunk_info']['id'] = chunk_data.get('id')
        template['content']['hebrew'] = chunk_data.get('original', '')
        template['content']['german'] = chunk_data.get('translation', '')
        
        # Analyse-Daten
        if 'metadata' in chunk_data:
            meta = chunk_data['metadata']
            template['analysis']['gematria'] = meta.get('gematria', {})
            template['analysis']['key_concepts'] = [
                f"{term['hebrew']} ({term['translation']})"
                for term in meta.get('key_terms', [])
            ]
        
        # Metadaten
        template['metadata']['created'] = self.current_date.isoformat()
        template['metadata']['wwaq_validated'] = self._validate_wwaq(chunk_data)
        
        # YAML generieren mit speziellen Optionen
        return yaml.dump(
            template,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=80,
            indent=2
        )
    
    def format_omer_study_path(self, day: int, assigned_chunks: List[str]) -> str:
        """Erstellt Omer-Studienpfad für einen Tag"""
        if not 1 <= day <= 49:
            raise ValueError("Omer-Tag muss zwischen 1 und 49 liegen")
        
        template = self.templates['omer_study'].copy()
        
        # Berechne Sefirot-Kombination
        week = (day - 1) // 7 + 1
        weekday = (day - 1) % 7 + 1
        
        template['omer_day'] = day
        template['date'] = f"Tag {day} des Omer"
        template['sefirot_combination'] = {
            'week': self.sefirot[week],
            'day': self.sefirot[weekday],
            'full': f"{self.sefirot[weekday]} שב{self.sefirot[week]}"
        }
        
        # Studienthema basierend auf Sefirot-Kombination
        template['study_focus'] = self._generate_study_focus(week, weekday)
        template['assigned_chunks'] = assigned_chunks
        
        return yaml.dump(
            template,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2
        )
    
    def _generate_study_focus(self, week: int, day: int) -> Dict:
        """Generiert Studienfokus basierend auf Sefirot"""
        themes = {
            (1, 1): "Reine Güte - Die Essenz des Gebens",
            (1, 2): "Stärke in der Güte - Grenzen der Liebe",
            (1, 3): "Harmonie in der Güte - Ausgewogenes Geben",
            (1, 4): "Beständigkeit in der Güte - Ewige Liebe",
            (1, 5): "Demut in der Güte - Empfangen um zu Geben",
            (1, 6): "Verbindung durch Güte - Einheit schaffen",
            (1, 7): "Manifestation der Güte - Liebe in der Welt",
            # ... weitere Kombinationen
        }
        
        theme = themes.get((week, day), f"{self.sefirot[day]} in {self.sefirot[week]}")
        
        return {
            'theme': theme,
            'meditation': f"Meditation über {self.sefirot[day]} als Ausdruck von {self.sefirot[week]}",
            'practical_work': f"Praktiziere {self.sefirot[day]} im Kontext von {self.sefirot[week]}"
        }
    
    def create_project_structure(self, output_dir: Path) -> Dict:
        """Erstellt vollständige Projektstruktur"""
        structure = {
            'metadata.yaml': self.templates['metadata'],
            'chunks/': {},
            'omer_paths/': {},
            'translations/': {},
            'commentary/': {}
        }
        
        # Erstelle Verzeichnisse
        for dir_name in ['chunks', 'omer_paths', 'translations', 'commentary']:
            (output_dir / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Speichere Metadaten
        with open(output_dir / 'metadata.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(
                structure['metadata.yaml'],
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False
            )
        
        return structure
    
    def _validate_wwaq(self, data: Dict) -> bool:
        """Validiert WWAQ-Konformität"""
        text = str(data)
        
        # Prüfe auf verbotene Begriffe
        forbidden = ['kabbala', 'kawana', 'zerstör', 'zerbrech']
        for term in forbidden:
            if term.lower() in text.lower():
                return False
        
        # Prüfe auf korrekte Begriffe
        required = ['qabbala', 'qawana']
        for term in required:
            if term.lower() in text.lower():
                return True
        
        return True
    
    def generate_batch_yaml(self, batch: Dict) -> str:
        """Generiert YAML für Übersetzungs-Batch"""
        batch_structure = {
            'batch_metadata': {
                'id': batch['batch_id'],
                'created': self.current_date.isoformat(),
                'chunk_count': len(batch['chunks']),
                'instruction': batch['instruction']
            },
            'chunks_to_translate': []
        }
        
        for chunk in batch['chunks']:
            chunk_entry = {
                'chunk_id': chunk['id'],
                'hebrew_text': chunk['text'],
                'context': {
                    'gematria_value': chunk['gematria_hint'],
                    'key_terms': [
                        {
                            'hebrew': term['hebrew'],
                            'meaning': term['translation']
                        }
                        for term in chunk['key_terms']
                    ]
                },
                'translation_placeholder': "[DEUTSCHE ÜBERSETZUNG HIER]"
            }
            batch_structure['chunks_to_translate'].append(chunk_entry)
        
        return yaml.dump(
            batch_structure,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=100,
            indent=2
        )
    
    def merge_translations(self, original_chunks: List[Dict], 
                         translations: Dict[str, str]) -> List[Dict]:
        """Fügt Übersetzungen zu Original-Chunks hinzu"""
        merged = []
        
        for chunk in original_chunks:
            chunk_id = chunk['id']
            if chunk_id in translations:
                chunk['translation'] = translations[chunk_id]
                chunk['translation_metadata'] = {
                    'translated': True,
                    'date': self.current_date.isoformat(),
                    'validated': self._validate_wwaq({'text': translations[chunk_id]})
                }
            merged.append(chunk)
        
        return merged
    
    def create_study_schedule(self, total_chunks: int = 1342) -> Dict[int, List[str]]:
        """Erstellt 49-Tage Omer-Studienplan für alle Chunks"""
        chunks_per_day = total_chunks // 49
        remainder = total_chunks % 49
        
        schedule = {}
        chunk_index = 1
        
        for day in range(1, 50):
            day_chunks = chunks_per_day
            if day <= remainder:
                day_chunks += 1
            
            schedule[day] = [
                f"CHUNK_{chunk_index + i:04d}"
                for i in range(day_chunks)
            ]
            chunk_index += day_chunks
        
        return schedule

# Hilfsfunktionen
def create_formatter() -> YAMLEzChajimFormatter:
    """Factory-Funktion für Formatter"""
    return YAMLEzChajimFormatter()

def format_for_claude_batch(chunks: List[Dict], batch_size: int = 10) -> List[str]:
    """Formatiert Chunks für Claude-Batch-Verarbeitung"""
    formatter = create_formatter()
    batches = []
    
    for i in range(0, len(chunks), batch_size):
        batch = {
            'batch_id': f"BATCH_{i//batch_size + 1:03d}",
            'chunks': chunks[i:i + batch_size],
            'instruction': "Übersetze mit WWAQ-Konformität"
        }
        batches.append(formatter.generate_batch_yaml(batch))
    
    return batches

# Test und Beispiel
if __name__ == "__main__":
    print("YAML Ez Chajim Formatter Test")
    print("=" * 50)
    
    formatter = create_formatter()
    
    # Test-Chunk
    test_chunk = {
        'id': 'CHUNK_0001',
        'original': 'עץ חיים היא למחזיקים בה',
        'translation': 'Ein Baum des Lebens ist sie für die, die sie ergreifen',
        'metadata': {
            'gematria': {'standard': 1625},
            'key_terms': [
                {'hebrew': 'עץ חיים', 'translation': 'Baum des Lebens'}
            ]
        }
    }
    
    # Formatiere Chunk
    formatted = formatter.format_chunk(test_chunk)
    print("Formatierter Chunk:")
    print(formatted)
    
    # Omer-Pfad für Tag 1
    omer_path = formatter.format_omer_study_path(1, ['CHUNK_0001', 'CHUNK_0002'])
    print("\nOmer-Studienpfad Tag 1:")
    print(omer_path)
    
    print("\nQ!")
