import httpx
import json
from typing import Dict, Any, List
from .base_tool import BaseTool

class WeatherTool(BaseTool):
    """Outil de consultation météo (simulation)"""
    
    @property
    def description(self) -> str:
        return "Obtient les informations météorologiques pour une ville donnée"
    
    async def execute(self, params: Dict[str, Any]) -> str:
        """Simule la récupération d'informations météo"""
        try:
            city = params.get("city", "")
            if not city:
                return "Erreur: nom de ville manquant"
            
            # Simulation de données météo (remplacez par une vraie API comme OpenWeatherMap)
            weather_data = {
                "paris": {"temp": 15, "condition": "nuageux", "humidity": 65},
                "london": {"temp": 12, "condition": "pluvieux", "humidity": 80},
                "new york": {"temp": 18, "condition": "ensoleillé", "humidity": 45},
                "tokyo": {"temp": 22, "condition": "partiellement nuageux", "humidity": 55},
                "default": {"temp": 20, "condition": "inconnu", "humidity": 50}
            }
            
            city_lower = city.lower()
            data = weather_data.get(city_lower, weather_data["default"])
            
            return f"Météo à {city}: {data['temp']}°C, {data['condition']}, humidité: {data['humidity']}%"
            
        except Exception as e:
            return f"Erreur lors de la récupération météo: {str(e)}"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "city": {
                "type": "string",
                "description": "Nom de la ville",
                "required": True,
                "examples": ["Paris", "London", "New York"]
            }
        }
    
    def get_examples(self) -> List[str]:
        return [
            '[TOOL:weather:{"city": "Paris"}]',
            '[TOOL:weather:{"city": "London"}]',
            '[TOOL:weather:{"city": "Tokyo"}]'
        ]