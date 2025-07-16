#!/bin/bash
# CLAUDE VERARBEITUNGS-SKRIPT
# Dieses Skript zeigt, wie die Batches an Claude gesendet werden

echo "🤖 CLAUDE EZ CHAJIM ÜBERSETZUNG"
echo "================================"
echo ""
echo "ANLEITUNG:"
echo "1. Öffne einen Batch (z.B. batch_001.txt)"
echo "2. Kopiere den GESAMTEN Inhalt"
echo "3. Füge ihn in Claude ein"
echo "4. Claude übersetzt alle Chunks im Batch"
echo "5. Speichere die Übersetzungen"
echo ""
echo "BATCHES:"
ls -la claude_batches/batch_*.txt
echo ""
echo "CHUNK-NUMMERIERUNG:"
echo "Die Chunks sind nummeriert nach ihrem Original-Dateinamen"
echo "z.B. CHUNK 001 = aus Datei 001_hebr.txt"
echo ""
echo "TIPP: Beginne mit batch_001.txt"
echo ""
echo "Q!"
