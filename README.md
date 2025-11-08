# 🤖 Chatbot Ollama avec Outils LLM - Test & Déploiement Autonome

Ce projet implémente un **chatbot intelligent** utilisant **Ollama en local** avec des **outils intégrés** et un **workflow en deux phases** : test local puis déploiement autonome avec Docker.

## 🎯 Workflow en 2 Phases

### Phase 1 : Test & Développement 🔬

- Utilise votre **Ollama local** pour tester différents modèles
- Interface web pour développement et tests
- Changement rapide de modèles via `.env`
- VS Code intégré avec tâches automatisées

### Phase 2 : Production Autonome 📦

- Tout packagé dans **Docker** pour déploiement portable
- Modèle choisi "figé" dans l'image
- App complètement autonome et isolée

## 🚀 Fonctionnalités

- **🧠 Chatbot local** : Utilise Ollama pour faire tourner des LLM localement (pas de cloud)
- **🛠️ Outils intégrés** : Calculator, Weather, File explorer, Web search
- **🌐 Interface web moderne** : Sélection de modèle, historique des conversations
- **🐳 Docker Ready** : Configuration complète pour déploiement autonome
- **🔧 VS Code intégré** : Tâches automatisées, débogage, tests
- **📱 API REST** : Endpoints pour intégration dans d'autres apps

## 🛠️ Outils Disponibles

| Outil | Commande | Description |
|-------|----------|-------------|
| **Calculator** | `calc: 2+3*4` | Calculs mathématiques avancés |
| **Weather** | `weather: Paris` | Infos météo (API simulée) |
| **File** | `file: list .` | Exploration de fichiers |
| **Search** | `search: python tutorial` | Recherche web simulée |

## 📋 Prérequis

- **Docker & Docker Compose** (obligatoire)
- **Python 3.11+** (optionnel, pour développement local)
- **8GB+ RAM** (pour les modèles LLM)
- **Ollama** (installé localement pour la phase de test)

## 🚀 Installation & Démarrage

### Phase 1 : Mode Test/Développement 🔬

1. **Installer Ollama localement**

   ```bash
   # Windows : Télécharger depuis https://ollama.ai/download
   # Linux/Mac : curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Démarrer Ollama**

   ```bash
   ollama serve
   ```

3. **Télécharger des modèles pour tester**

   ```bash
   ollama pull granite4:latest    # Modèle recommandé
   ollama pull llama3.2:latest    # Alternative
   ollama pull mistral:latest     # Autre option
   ```

4. **Cloner et installer**

   ```bash
   git clone <votre-repo>
   cd test-ollama-tools-toolkit
   pip install -r requirements.txt
   ```

5. **Démarrer l'app de test**

   ```bash
   # Avec VS Code (recommandé)
   # Ctrl+Shift+P → Tasks: Run Task → "🚀 Setup complet (sans modèle)"

   # Ou manuellement
   python quick_start.py start
   ```

6. **Accéder à l'interface**

   - [http://localhost:8000](http://localhost:8000)
   - Testez différents modèles en modifiant `.env`

### Phase 2 : Mode Production Autonome 📦

Quand vous avez trouvé le modèle idéal :

#### Option A : Déploiement Rapide (Recommandé)

```bash
# Modèle téléchargé automatiquement au premier démarrage
docker-compose up -d
# ⏳ Première fois : téléchargement du modèle (~2-3 min)
# ✅ Démarrages suivants : instantané
```

#### Option B : Image avec Modèle Pré-chargé

```bash
# Image plus lourde mais démarrage instantané
docker-compose -f docker-compose-with-model.yml up --build -d
# ⏳ Build initial : téléchargement du modèle dans l'image
# ✅ Tous les démarrages suivants : instantané
```

**Les deux options donnent le même résultat :**

- Ollama + modèle granite4 dans un container
- Interface web sur [http://localhost:8000](http://localhost:8000)
- Tout isolé et portable !

## 💬 Utilisation

### Interface Web

- **Sélection de modèle** : Liste déroulante avec tous vos modèles locaux
- **Chat en temps réel** : Tapez vos messages normalement
- **Outils automatiques** : Le LLM utilise les outils quand nécessaire

### Exemples Pratiques

```
👤 Vous: "Calcule 15 * 23 + sqrt(144)"
🤖 Bot: 345 + 12 = 357

👤 Vous: "Quel temps fait-il à Paris ?"
🤖 Bot: [Outil Météo] Paris: 15°C, partiellement nuageux

👤 Vous: "Liste les fichiers Python dans src/"
🤖 Bot: [Outil Fichier] main.py, __init__.py

👤 Vous: "Recherche un tutoriel Python"
🤖 Bot: [Outil Recherche] Voici les meilleurs tutoriels...
```

### API REST

```bash
# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}],"model":"granite4:latest"}'

# Liste des modèles
curl http://localhost:8000/models

# Santé du service
curl http://localhost:8000/health
```

## 🔧 Configuration

### Variables d'environnement (.env)

```env
# Ollama (phase test)
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=granite4:latest

# Outils activés
ENABLE_CALCULATOR=true
ENABLE_WEATHER=true
ENABLE_FILE_TOOLS=true
ENABLE_SEARCH=true

# Sécurité fichiers
ALLOWED_FILE_EXTENSIONS=.txt,.md,.json,.py,.js
```

### Changer de modèle

1. **Phase test** : Modifiez `MODEL_NAME` dans `.env`
2. **Phase production** : Modifiez dans `docker-compose.yml` puis rebuild

## 🏗️ Architecture

```
├── src/main.py              # 🏠 App FastAPI + interface web
├── tools/                   # 🛠️ Outils du chatbot
│   ├── base_tool.py         # Classe de base
│   ├── calculator_tool.py   # Calculs
│   ├── weather_tool.py      # Météo
│   ├── file_tool.py         # Fichiers
│   └── search_tool.py       # Recherche
├── .vscode/                 # ⚙️ Config VS Code
├── docker-compose.yml       # 🐳 Orchestration Docker
├── Dockerfile              # 📦 Image de l'app
├── quick_start.py          # 🚀 Script de démarrage rapide
└── requirements.txt        # 📋 Dépendances Python
```

## 🐛 Dépannage

### Problèmes Courants

**❌ "Modèle non trouvé"**

```bash
# Lister vos modèles
ollama list

# Télécharger un modèle
ollama pull granite4:latest
```

**❌ "Port déjà utilisé"**

```bash
# Changer le port dans docker-compose.yml
ports:
  - "8001:8000"  # Au lieu de 8000
```

**❌ "Mémoire insuffisante"**

- Utilisez un modèle plus petit : `MODEL_NAME=llama3.2:1b`
- Augmentez la RAM allouée à Docker

**❌ Docker ne démarre pas**

```bash
# Logs détaillés
docker-compose logs -f

# Redémarrer proprement
docker-compose down && docker-compose up -d
```

### Debug Mode

```bash
# Avec rechargement automatique
python -m uvicorn src.main:app --reload --log-level debug

# Tests des outils
python test_tools.py
```

## 🔄 Workflow Recommandé

1. **📥 Installation** : Ollama local + projet
2. **🧪 Phase Test** : Tester différents modèles avec l'interface web
3. **✅ Validation** : Trouver le modèle qui convient le mieux
4. **📦 Production** : Builder l'app Docker autonome
5. **🚀 Déploiement** : Distribuer l'archive `ollama-chatbot-clean.tar.gz`

## 📚 Ressources

- [📖 Ollama Docs](https://ollama.ai/docs)
- [🚀 FastAPI](https://fastapi.tiangolo.com/)
- [🐳 Docker Compose](https://docs.docker.com/compose/)
- [🧠 Granite Model](https://ollama.ai/library/granite4)

## 🎯 Points Forts

- ✅ **Local First** : Tout reste sur votre machine
- ✅ **Modulaire** : Ajoutez facilement de nouveaux outils
- ✅ **Portable** : Déploiement Docker partout
- ✅ **Testable** : Interface pour valider les modèles
- ✅ **VS Code Ready** : Développement intégré

---

**🎉 Prêt à créer votre chatbot LLM personnalisé ?**
