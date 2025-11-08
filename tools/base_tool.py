from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseTool(ABC):
    """Classe de base pour tous les outils"""
    
    def __init__(self):
        self.name = self.__class__.__name__.replace("Tool", "").lower()
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description de l'outil"""
        pass
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> str:
        """Exécute l'outil avec les paramètres donnés"""
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Retourne la description des paramètres de l'outil"""
        pass
    
    def get_examples(self) -> List[str]:
        """Retourne des exemples d'utilisation de l'outil"""
        return []