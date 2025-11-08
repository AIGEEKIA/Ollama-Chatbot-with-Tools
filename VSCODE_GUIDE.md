# 🚀 Guide de démarrage rapide VS Code

## Démarrage en un clic depuis VS Code

### 1. **Première installation**
1. Ouvrir VS Code dans ce dossier
2. Accepter les extensions recommandées quand elles s'affichent
3. Ouvrir le terminal VS Code (`Ctrl+ù`)
4. Exécuter la tâche de setup complet :
   - `Ctrl+Shift+P` → "Tasks: Run Task" → "🚀 Setup complet (Docker + Python)"

### 2. **Démarrage rapide**
Une fois le setup terminé :

#### **Option A : Avec le debugger (Recommandé)**
1. Aller dans l'onglet "Run and Debug" (Ctrl+Shift+D)
2. Sélectionner "🚀 Démarrer Chatbot Ollama"
3. Cliquer sur le bouton play ▶️

#### **Option B : Avec les tâches**
1. `Ctrl+Shift+P` → "Tasks: Run Task"
2. Choisir les tâches dans l'ordre :
   - "🐳 Démarrer Ollama avec Docker"
   - "📦 Télécharger modèle llama3.2" (première fois seulement)
   - Puis démarrer l'app avec le debugger

### 3. **Accès rapide**
- **Interface web** : `Ctrl+Shift+P` → "Tasks: Run Task" → "🌐 Ouvrir interface web"
- **Ou directement** : http://localhost:8000

### 4. **Tâches disponibles** (Ctrl+Shift+P → "Tasks: Run Task")

| Tâche | Description |
|-------|-------------|
| 🚀 Setup complet | Installation complète (Docker + Python) |
| 🐳 Démarrer Ollama avec Docker | Lance uniquement Ollama |
| 📦 Télécharger modèle llama3.2 | Télécharge le modèle LLM |
| 🔄 Installer dépendances Python | Install pip requirements |
| 🌐 Ouvrir interface web | Ouvre http://localhost:8000 |
| 🛑 Arrêter tous les services | Stoppe Docker |

### 5. **Configurations de débogage**

| Configuration | Description |
|---------------|-------------|
| 🚀 Démarrer Chatbot Ollama | Lance l'app avec hot-reload |
| 🧪 Test Tools | Test tous les outils |

### 6. **Structure des fichiers VS Code**

```
.vscode/
├── launch.json      # Configurations de débogage
├── tasks.json       # Tâches automatisées
├── settings.json    # Paramètres du workspace
├── extensions.json  # Extensions recommandées
└── mcp.json        # Configuration MCP
```

### 7. **Raccourcis utiles**

- **F5** : Démarrer le débogage
- **Ctrl+F5** : Démarrer sans débogage
- **Shift+F5** : Arrêter le débogage
- **Ctrl+Shift+F5** : Redémarrer le débogage
- **Ctrl+Shift+P** : Palette de commandes
- **Ctrl+ù** : Terminal intégré

### 8. **Dépannage**

**Si Ollama ne répond pas :**
1. Vérifier que Docker est démarré
2. Exécuter "🐳 Démarrer Ollama avec Docker"
3. Attendre 30 secondes
4. Vérifier avec `curl http://localhost:11434/api/tags`

**Si le modèle n'est pas trouvé :**
1. Exécuter "📦 Télécharger modèle llama3.2"
2. Attendre le téléchargement complet

**Si l'app ne démarre pas :**
1. Vérifier les dépendances : "🔄 Installer dépendances Python"
2. Vérifier le terminal pour les erreurs
3. Redémarrer VS Code si nécessaire

### 9. **Logs et monitoring**

- **Logs Docker** : `docker-compose logs -f`
- **Logs app** : Visible dans le terminal de débogage VS Code
- **Health check** : http://localhost:8000/health
- **API docs** : http://localhost:8000/docs

Avec cette configuration, vous pouvez tout faire directement depuis VS Code sans avoir besoin de lignes de commande ! 🎉