#!/bin/bash
# Backup aller README Dateien von EXISTIERENDEN Repos

echo "Sichere READMEs von archivierten Repositories..."

# Liste der ECHTEN Repositories (aus gh repo list)
REPOS=(
    "ez-chajim"
    "ez-chajim-auto-update"
    "ez-chajim-wwaq"
    "ez-chajim-meta"
    "ez-chajim-quell-nachvollziehen"
    "ez-chajim-azilut-connections"
    "ez-chajim-hns10-core"
    "ez-chajim-intelli-chunk"
    "ez-chajim-quantum-sync"
    "ez-chajim-lkv-visualizer"
    "ez-chajim-wwaq-validator"
    "ez-chajim-yaml-formatter"
    "ez-chajim-manuscript-processor"
    "ez-chajim-devops"
    "wwaq-glossar-parser"
)

for repo in "${REPOS[@]}"; do
    echo "Versuche $repo..."
    
    # Direkt README herunterladen
    if curl -s "https://raw.githubusercontent.com/JEREMIA1964/$repo/main/README.md" > "${repo}_README.md" 2>/dev/null; then
        if [ -s "${repo}_README.md" ]; then
            echo "✓ $repo README gesichert"
        else
            rm "${repo}_README.md"
            echo "✗ $repo hat keine README"
        fi
    else
        echo "✗ $repo nicht gefunden"
    fi
done

echo "Fertig!"
