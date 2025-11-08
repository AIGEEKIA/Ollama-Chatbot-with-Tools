import json
import re
import asyncio
from typing import Dict, List, Any, Tuple
from .calculator_tool import CalculatorTool
from .weather_tool import WeatherTool
from .file_tool import FileTool
from .search_tool import SearchTool

class ToolManager:
    """Gestionnaire central pour tous les outils disponibles"""
    
    def __init__(self):
        self.tools = {}
        self._load_tools()
    
    def _load_tools(self):
        """Charge tous les outils disponibles"""
        self.tools = {
            "calculator": CalculatorTool(),
            "weather": WeatherTool(),
            "file": FileTool(),
            "search": SearchTool()
        }
    
    def get_tools_description(self) -> str:
        """Retourne une description de tous les outils disponibles"""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)
    
    def get_tools_info(self) -> Dict[str, Any]:
        """Retourne les informations détaillées sur tous les outils"""
        tools_info = {}
        for name, tool in self.tools.items():
            tools_info[name] = {
                "description": tool.description,
                "parameters": tool.get_parameters(),
                "examples": tool.get_examples()
            }
        return tools_info
    
    async def process_response(self, response: str) -> Tuple[str, List[str]]:
        """
        Traite la réponse du LLM pour identifier et exécuter les outils
        Format attendu: [TOOL:nom_outil:paramètres_json]
        """
        tools_used = []
        processed_response = response
        
        # Pattern pour identifier les appels d'outils
        tool_pattern = r'\[TOOL:(\w+):({.*?})\]'
        matches = re.findall(tool_pattern, processed_response)
        
        for tool_name, params_json in matches:
            if tool_name in self.tools:
                try:
                    # Parse des paramètres JSON
                    params = json.loads(params_json)
                    
                    # Exécution de l'outil
                    result = await self.tools[tool_name].execute(params)
                    tools_used.append(tool_name)
                    
                    # Remplacement du placeholder par le résultat
                    tool_call = f"[TOOL:{tool_name}:{params_json}]"
                    processed_response = processed_response.replace(
                        tool_call, 
                        f"[Résultat de {tool_name}: {result}]"
                    )
                    
                except json.JSONDecodeError as e:
                    processed_response = processed_response.replace(
                        f"[TOOL:{tool_name}:{params_json}]",
                        f"[Erreur JSON dans l'outil {tool_name}: {str(e)}]"
                    )
                except Exception as e:
                    processed_response = processed_response.replace(
                        f"[TOOL:{tool_name}:{params_json}]",
                        f"[Erreur dans l'outil {tool_name}: {str(e)}]"
                    )
            else:
                processed_response = processed_response.replace(
                    f"[TOOL:{tool_name}:{params_json}]",
                    f"[Outil '{tool_name}' non trouvé]"
                )
        
        return processed_response, tools_used