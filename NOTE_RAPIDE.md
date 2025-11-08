# 🚀 NOTE RAPIDE - Chatbot Ollama (SANS OUTILS)

## 🎯 À QUOI ÇA SERT ?

**Chatbot intelligent local** qui utilise **Ollama** (pas de cloud) pour des **conversations simples** :

- 🧠 **Chatbot** : Conversation basique avec LLM local
- 🌐 **Interface web** : Sélection de modèle, historique
- 🐳 **Docker** : Déploiement autonome

## 📋 WORKFLOW SIMPLIFIÉ

### Phase 1 : Test Local 🔬

- Utilise Ollama local pour tester
- Interface web basique
- Changement rapide de modèles

### Phase 2 : Production 📦

- Tout packagé dans Docker
- Modèle figé dans l'image
- App complètement autonome

## 🚀 COMMENT ÇA MARCHE ?

### Architecture

```mermaid
Utilisateur → Interface Web → FastAPI → Ollama → LLM → Réponse
```

### Composants

- **FastAPI** : Serveur web Python
- **Ollama** : Moteur LLM local
- **Docker** : Conteneurisation

## 🛠️ COMMANDES PRINCIPALES

### Installation

```bash
# 1. Ollama (local)
ollama serve
ollama pull granite4:latest

# 2. Dépendances
pip install -r requirements.txt
```

### Démarrage

```bash
# Mode test (recommandé)
python quick_start.py start

# Mode production Docker
docker-compose up -d

# Avec modèle pré-téléchargé
docker-compose -f docker-compose-with-model.yml up -d
```

### Débogage VS Code

```text
F1 → "Debug: Select and Start Debugging"
→ "🚀 Chatbot Ollama (Start & Debug)"
```

## 🎮 UTILISATION

### Interface Web

- URL : `http://localhost:8000`
- Tape message : "Bonjour !" ou "Comment ça va ?"
- Sélectionne modèle dans dropdown

### Conversation Simple

Tapez simplement vos messages en langage naturel - pas de commandes spéciales !

## 🐛 DÉBOGAGE

### Breakpoints

- `src/main.py` : Logique chatbot
- Clic rouge à gauche des numéros de ligne

### Contrôles

- **F5** : Continue
- **F10** : Step Over
- **F11** : Step Into

## 📁 STRUCTURE PROJET

```text
├── src/main.py          # App FastAPI principale
├── quick_start.py       # Script de démarrage
├── docker-compose.yml   # Docker léger
├── docker-compose-with-model.yml  # Docker avec modèle
├── .vscode/             # Config VS Code (debug, tasks)
└── requirements.txt     # Dépendances Python
```

## ⚡ RAPPEL RAPIDE

**Pour démarrer rapidement :**

1. `ollama serve` (dans un terminal)
2. `python quick_start.py start` (dans VS Code)
3. Ouvrir <http://localhost:8000>
4. Tester : "Bonjour, comment allez-vous ?"

**Pour déboguer :**

1. Ouvrir VS Code
2. F1 → Debug → "🚀 Chatbot Ollama"
3. Placer breakpoints
4. Tester via interface web

---

**🤖 Demande à l'IA :** "explique-moi le projet Ollama Chatbot"</content>
<parameter name="filePath">e:\My-learn\test-ollama-tools-toolkit\NOTE_RAPIDE.md
