import os
import json
from typing import Dict, Any, List
from .base_tool import BaseTool

class FileTool(BaseTool):
    """Outil de gestion de fichiers basique"""
    
    @property
    def description(self) -> str:
        return "Lit le contenu de fichiers texte ou liste les fichiers d'un dossier"
    
    async def execute(self, params: Dict[str, Any]) -> str:
        """Exécute une opération sur fichier"""
        try:
            action = params.get("action", "")
            path = params.get("path", "")
            
            if not action or not path:
                return "Erreur: action et path requis"
            
            # Sécurité: limiter aux fichiers dans le dossier de travail
            if ".." in path or path.startswith("/"):
                return "Erreur: chemin non autorisé"
            
            if action == "read":
                return self._read_file(path)
            elif action == "list":
                return self._list_directory(path)
            else:
                return f"Action non supportée: {action}"
                
        except Exception as e:
            return f"Erreur fichier: {str(e)}"
    
    def _read_file(self, filepath: str) -> str:
        """Lit le contenu d'un fichier"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                # Limiter la taille pour éviter les réponses trop longues
                if len(content) > 1000:
                    content = content[:1000] + "... (contenu tronqué)"
                return f"Contenu de {filepath}:\n{content}"
        except FileNotFoundError:
            return f"Fichier non trouvé: {filepath}"
        except Exception as e:
            return f"Erreur lecture fichier: {str(e)}"
    
    def _list_directory(self, dirpath: str) -> str:
        """Liste les fichiers d'un dossier"""
        try:
            if not os.path.exists(dirpath):
                return f"Dossier non trouvé: {dirpath}"
            
            items = os.listdir(dirpath)
            if not items:
                return f"Dossier vide: {dirpath}"
            
            files = []
            dirs = []
            for item in items:
                item_path = os.path.join(dirpath, item)
                if os.path.isdir(item_path):
                    dirs.append(f"📁 {item}/")
                else:
                    files.append(f"📄 {item}")
            
            result = f"Contenu de {dirpath}:\n"
            result += "\n".join(dirs + files)
            return result
            
        except Exception as e:
            return f"Erreur liste dossier: {str(e)}"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "action": {
                "type": "string",
                "description": "Action à effectuer: 'read' ou 'list'",
                "required": True,
                "enum": ["read", "list"]
            },
            "path": {
                "type": "string",
                "description": "Chemin du fichier ou dossier",
                "required": True
            }
        }
    
    def get_examples(self) -> List[str]:
        return [
            '[TOOL:file:{"action": "read", "path": "config.txt"}]',
            '[TOOL:file:{"action": "list", "path": "."}]',
            '[TOOL:file:{"action": "list", "path": "src"}]'
        ]