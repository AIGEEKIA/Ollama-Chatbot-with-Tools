import httpx
import json
from typing import Dict, Any, List
from .base_tool import BaseTool

class SearchTool(BaseTool):
    """Outil de recherche web simulé"""
    
    @property
    def description(self) -> str:
        return "Effectue une recherche web simulée et retourne des résultats pertinents"
    
    async def execute(self, params: Dict[str, Any]) -> str:
        """Simule une recherche web"""
        try:
            query = params.get("query", "")
            if not query:
                return "Erreur: requête de recherche manquante"
            
            # Simulation de résultats de recherche
            # Dans un vrai projet, vous pourriez utiliser une API comme Google Custom Search
            simulated_results = {
                "python": [
                    "Python.org - Site officiel du langage Python",
                    "Python Tutorial - Apprenez Python facilement",
                    "Python Documentation - Guide complet"
                ],
                "docker": [
                    "Docker.com - Plateforme de conteneurisation",
                    "Docker Hub - Registre d'images Docker",
                    "Docker Documentation - Guide d'utilisation"
                ],
                "ollama": [
                    "Ollama.ai - Exécutez des LLM localement",
                    "GitHub - ollama/ollama",
                    "Guide d'installation Ollama"
                ],
                "default": [
                    f"Résultat de recherche pour '{query}'",
                    f"Information pertinente sur {query}",
                    f"Documentation de {query}"
                ]
            }
            
            # Recherche de mots-clés dans la requête
            results = simulated_results["default"]
            for keyword, keyword_results in simulated_results.items():
                if keyword in query.lower():
                    results = keyword_results
                    break
            
            result_text = f"Résultats de recherche pour '{query}':\n"
            for i, result in enumerate(results, 1):
                result_text += f"{i}. {result}\n"
            
            return result_text
            
        except Exception as e:
            return f"Erreur lors de la recherche: {str(e)}"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "Terme de recherche",
                "required": True,
                "examples": ["Python tutorial", "Docker installation", "Ollama documentation"]
            }
        }
    
    def get_examples(self) -> List[str]:
        return [
            '[TOOL:search:{"query": "Python tutorial"}]',
            '[TOOL:search:{"query": "Docker installation"}]',
            '[TOOL:search:{"query": "Ollama documentation"}]'
        ]