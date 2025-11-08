#!/usr/bin/env python3
"""
Script de démarrage rapide pour VS Code
Usage: python quick_start.py [action]
Actions: start, stop, test, open
"""

import subprocess
import sys
import time
import webbrowser
import requests
from pathlib import Path

def run_command(command, shell=True, capture_output=False):
    """Exécute une commande système"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result.returncode == 0, result.stdout.strip()
        else:
            result = subprocess.run(command, shell=shell)
            return result.returncode == 0, ""
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de: {command}")
        print(f"   {str(e)}")
        return False, ""

def check_docker():
    """Vérifie que Docker est disponible"""
    print("🔍 Vérification de Docker...")
    success, output = run_command("docker --version", capture_output=True)
    if success:
        print(f"✅ Docker disponible: {output}")
        return True
    else:
        print("❌ Docker n'est pas installé ou n'est pas démarré")
        return False

def check_ollama():
    """Vérifie qu'Ollama répond"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_services():
    """Démarre tous les services"""
    print("🚀 Démarrage des services...")
    
    if not check_docker():
        return False
    
    # Démarrer Ollama avec Docker
    print("🐳 Démarrage d'Ollama...")
    success, _ = run_command("docker-compose up -d ollama")
    if not success:
        print("❌ Erreur lors du démarrage d'Ollama")
        return False
    
    # Attendre qu'Ollama soit prêt
    print("⏳ Attente qu'Ollama soit prêt...")
    for i in range(30):
        if check_ollama():
            print("✅ Ollama est prêt!")
            break
        time.sleep(2)
        print(f"   Tentative {i+1}/30...")
    else:
        print("❌ Ollama ne répond pas après 60 secondes")
        return False
    
    # Lister les modèles disponibles au lieu de télécharger
    print("� Vérification des modèles disponibles...")
    success, output = run_command("docker exec ollama ollama list", capture_output=True)
    if success:
        lines = output.strip().split('\n')
        if len(lines) > 1:  # Au moins l'en-tête et un modèle
            model_count = len(lines) - 1  # -1 pour l'en-tête
            print(f"✅ {model_count} modèles disponibles localement")
            print("💡 Utilisez l'interface web pour sélectionner un modèle")
        else:
            print("⚠️ Aucun modèle trouvé. Téléchargez-en un avec: ollama pull <nom_modele>")
    else:
        print("⚠️ Impossible de lister les modèles")
    
    print("🎉 Services démarrés avec succès!")
    return True

def stop_services():
    """Arrête tous les services"""
    print("🛑 Arrêt des services...")
    success, _ = run_command("docker-compose down")
    if success:
        print("✅ Services arrêtés")
    else:
        print("❌ Erreur lors de l'arrêt des services")
    return success

def test_tools():
    """Test les outils"""
    print("🧪 Test des outils...")
    success, _ = run_command("python test_tools.py")
    return success

def open_interface():
    """Ouvre l'interface web"""
    url = "http://localhost:8000"
    print(f"🌐 Ouverture de {url}...")
    
    # Vérifier que l'app répond
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            webbrowser.open(url)
            print("✅ Interface ouverte dans le navigateur")
            return True
        else:
            print("❌ L'application ne répond pas")
            return False
    except:
        print("❌ L'application n'est pas démarrée")
        print("   Démarrez-la d'abord avec: python quick_start.py start")
        return False

def show_help():
    """Affiche l'aide"""
    print("""
🚀 Script de démarrage rapide Ollama Chatbot

Usage: python quick_start.py [action]

Actions disponibles:
  start    - Démarre tous les services (Ollama + modèle)
  stop     - Arrête tous les services Docker
  test     - Test les outils du chatbot
  open     - Ouvre l'interface web
  status   - Affiche le statut des services
  help     - Affiche cette aide

Exemples:
  python quick_start.py start
  python quick_start.py open
  python quick_start.py stop

Une fois démarré, accédez à: http://localhost:8000
""")

def check_status():
    """Affiche le statut des services"""
    print("📊 Statut des services:")
    
    # Docker
    docker_ok = check_docker()
    print(f"   Docker: {'✅' if docker_ok else '❌'}")
    
    # Ollama
    ollama_ok = check_ollama()
    print(f"   Ollama: {'✅' if ollama_ok else '❌'}")
    
    # App
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        app_ok = response.status_code == 200
    except:
        app_ok = False
    print(f"   Chatbot: {'✅' if app_ok else '❌'}")
    
    if ollama_ok and app_ok:
        print("\n🎉 Tout fonctionne! Accédez à: http://localhost:8000")
    elif ollama_ok:
        print("\n⚠️ Ollama fonctionne mais le chatbot n'est pas démarré")
        print("   Démarrez-le avec F5 dans VS Code ou:")
        print("   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n❌ Services non démarrés. Utilisez: python quick_start.py start")

def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    action = sys.argv[1].lower()
    
    if action == "start":
        start_services()
    elif action == "stop":
        stop_services()
    elif action == "test":
        test_tools()
    elif action == "open":
        open_interface()
    elif action == "status":
        check_status()
    elif action == "help":
        show_help()
    else:
        print(f"❌ Action inconnue: {action}")
        show_help()

if __name__ == "__main__":
    main()