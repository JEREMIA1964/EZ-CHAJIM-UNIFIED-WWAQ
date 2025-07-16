#!/bin/bash
echo "ARCHIVIERE alle alten Ez Chajim Repos..."

repos=(
"ez-chajim"
"ez-chajim-auto-update"
"ez-chajim-wwaq"
"ez-chajim-meta"
"ez-chajim-quell-nachweis"
"ez-chajim-azilut-converter"
"ez-chajim-hns10-core"
"ez-chajim-intelli-chunk"
"ez-chajim-quantum-sync"
"ez-chajim-lkv-visualizer"
"ez-chajim-wwaq-validator"
"ez-chajim-yaml-formatter"
"ez-chajim-manuscript-proc"
"ez-chajim-devops"
)

for repo in "${repos[@]}"; do
    echo "Archiviere: $repo"
    gh repo archive "JEREMIA1964/$repo" --yes || echo "Fehler bei $repo"
done

echo "✅ Alle alten Repos archiviert!"
echo "   Nur noch EZ-CHAJIM-UNIFIED-WWAQ ist aktiv!"
