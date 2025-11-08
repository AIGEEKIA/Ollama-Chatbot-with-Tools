#!/bin/bash

# Script d'initialisation pour Ollama avec modèle granite4
echo "🤖 Initialisation d'Ollama avec granite4:latest..."

# Attendre qu'Ollama soit prêt
echo "⏳ Attente du démarrage d'Ollama..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "   Ollama pas encore prêt, attente..."
    sleep 2
done

echo "✅ Ollama est prêt !"

# Vérifier si le modèle granite4 est déjà présent
echo "🔍 Vérification du modèle granite4:latest..."
if ! curl -s http://localhost:11434/api/tags | grep -q "granite4:latest"; then
    echo "📥 Téléchargement du modèle granite4:latest..."
    echo "   Cette opération peut prendre plusieurs minutes..."

    # Télécharger le modèle
    if curl -s http://localhost:11434/api/pull -d '{"name":"granite4:latest"}' > /dev/null; then
        echo "✅ Modèle granite4:latest téléchargé avec succès !"
    else
        echo "❌ Erreur lors du téléchargement du modèle"
        exit 1
    fi
else
    echo "✅ Modèle granite4:latest déjà présent"
fi

echo "🚀 Initialisation terminée ! Ollama avec granite4:latest est prêt."
echo "🌐 Votre chatbot est accessible sur http://localhost:8000"