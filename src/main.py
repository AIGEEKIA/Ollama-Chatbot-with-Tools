from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import os
import json
from typing import List, Optional, Dict, Any
import asyncio
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(title="Ollama Chatbot", version="1.0.0")

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "granite4:latest")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]  # Changer pour accepter des dicts directement
    model: Optional[str] = MODEL_NAME
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    model: str

@app.on_event("startup")
async def startup_event():
    """Vérification de la connexion à Ollama au démarrage"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Vérifier si Ollama est accessible
            health_response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if health_response.status_code == 200:
                models_data = health_response.json()
                available_models = [model["name"] for model in models_data.get("models", [])]
                print(f"[OK] Ollama connecte - {len(available_models)} modeles disponibles")
                if MODEL_NAME in available_models:
                    print(f"[OK] Modele par defaut '{MODEL_NAME}' disponible")
                else:
                    print(f"[WARN] Modele par defaut '{MODEL_NAME}' non trouve")
            else:
                print("[WARN] Ollama non accessible au demarrage")
    except Exception as e:
        print(f"[ERROR] Erreur de connexion a Ollama: {e}")
        print("[INFO] L'application continuera sans verification du modele")

    print("[START] Application demarree - pret a utiliser les modeles locaux")

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Interface web simple pour le chatbot"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ollama Chatbot</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .chat-container { height: 400px; border: 1px solid #ddd; padding: 10px; overflow-y: auto; background-color: #fafafa; margin-bottom: 10px; border-radius: 5px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user-message { background-color: #007bff; color: white; text-align: right; }
            .bot-message { background-color: #e9ecef; color: #333; }
            .input-container { display: flex; gap: 10px; }
            input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .model-selector { margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; border: 1px solid #dee2e6; }
            .model-selector label { font-weight: bold; margin-right: 10px; }
            .model-selector select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; min-width: 300px; }
            .model-selector #currentModel { margin-left: 15px; font-size: 0.9em; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Ollama Chatbot</h1>

            <!-- Section de sélection de modèle -->
            <div class="model-selector">
                <label for="modelSelect">Modèle Ollama :</label>
                <select id="modelSelect" onchange="selectModel(this.value)">
                    <option value="">Chargement...</option>
                </select>
                <span id="currentModel">Modèle actuel: granite4:latest</span>
            </div>

            <div class="chat-container" id="chatContainer"></div>
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Tapez votre message..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Envoyer</button>
            </div>
        </div>

        <script>
            let chatHistory = [];

            function addMessage(role, content) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}-message`;
                messageDiv.innerHTML = content.replace(/\\n/g, '<br>');
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;

                addMessage('user', message);
                chatHistory.push({role: 'user', content: message});
                input.value = '';

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            messages: chatHistory
                        })
                    });

                    const data = await response.json();
                    addMessage('bot', data.response);
                    chatHistory.push({role: 'assistant', content: data.response});
                } catch (error) {
                    addMessage('bot', 'Erreur: ' + error.message);
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            // Charger les modèles disponibles
            async function loadModels() {
                try {
                    const response = await fetch('/models');
                    const data = await response.json();
                    
                    const select = document.getElementById('modelSelect');
                    select.innerHTML = '';
                    
                    data.models.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.name;
                        option.textContent = `${model.name} (${model.size_human}, ${model.family})`;
                        if (model.name === data.default_model) {
                            option.selected = true;
                        }
                        select.appendChild(option);
                    });
                    
                    updateCurrentModel(data.default_model);
                } catch (error) {
                    console.error('Erreur chargement modèles:', error);
                    const select = document.getElementById('modelSelect');
                    select.innerHTML = '<option value="">Erreur chargement modèles</option>';
                }
            }

            // Sélectionner un modèle
            async function selectModel(modelName) {
                if (!modelName) return;
                
                try {
                    const response = await fetch('/models/select', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(modelName)
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        updateCurrentModel(modelName);
                        addMessage('bot', `✅ Modèle changé pour: ${modelName}`);
                    } else {
                        addMessage('bot', `❌ Erreur changement modèle: ${data.message}`);
                    }
                } catch (error) {
                    addMessage('bot', `❌ Erreur: ${error.message}`);
                }
            }

            // Mettre à jour l'affichage du modèle actuel
            function updateCurrentModel(modelName) {
                const currentModelSpan = document.getElementById('currentModel');
                currentModelSpan.textContent = `Modèle actuel: ${modelName}`;
            }

            // Charger les modèles au démarrage
            loadModels();

            // Message de bienvenue
            addMessage('bot', 'Bonjour! Je suis un chatbot alimenté par Ollama. Sélectionnez un modèle ci-dessus et posez-moi vos questions!');
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal pour le chat"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Appel à Ollama
            ollama_response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": request.model,
                    "messages": request.messages,
                    "stream": False
                }
            )

            if ollama_response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Erreur Ollama: {ollama_response.text}")

            response_data = ollama_response.json()
            bot_response = response_data["message"]["content"]

            return ChatResponse(
                response=bot_response,
                model=request.model
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def get_models():
    """Récupère la liste des modèles disponibles"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                models = []
                for model in models_data.get("models", []):
                    models.append({
                        "name": model["name"],
                        "size": model.get("size", 0),
                        "size_human": f"{model.get('size', 0) / (1024**3):.1f}GB" if model.get("size") else "N/A",
                        "family": model.get("details", {}).get("family", "unknown"),
                        "parameter_size": model.get("details", {}).get("parameter_size", "unknown"),
                        "quantization": model.get("details", {}).get("quantization_level", "unknown"),
                        "modified_at": model.get("modified_at", "unknown")
                    })
                return {"models": models, "default_model": MODEL_NAME}
            else:
                raise HTTPException(status_code=503, detail="Ollama service not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération modèles: {str(e)}")

@app.post("/models/select")
async def select_model(model_name: str):
    """Sélectionne un modèle pour les futures conversations"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Vérifier que le modèle existe
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                available_models = [model["name"] for model in models_data.get("models", [])]
                
                if model_name in available_models:
                    # Mettre à jour la variable globale (dans un vrai projet, utiliser une config persistante)
                    global MODEL_NAME
                    MODEL_NAME = model_name
                    return {"success": True, "selected_model": model_name, "message": f"Modèle {model_name} sélectionné"}
                else:
                    raise HTTPException(status_code=404, detail=f"Modèle {model_name} non trouvé")
            else:
                raise HTTPException(status_code=503, detail="Ollama service not available")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur sélection modèle: {str(e)}")

@app.get("/health")
async def health_check():
    """Vérification de santé du service"""
    try:
        async with httpx.AsyncClient() as client:
            ollama_response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return {
                "status": "healthy",
                "ollama_status": "connected" if ollama_response.status_code == 200 else "disconnected"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)