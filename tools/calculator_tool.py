import math
import operator
from typing import Dict, Any, List
from .base_tool import BaseTool

class CalculatorTool(BaseTool):
    """Outil de calcul mathématique"""
    
    @property
    def description(self) -> str:
        return "Effectue des calculs mathématiques simples (addition, soustraction, multiplication, division, puissance, racine carrée)"
    
    async def execute(self, params: Dict[str, Any]) -> str:
        """Exécute un calcul mathématique"""
        try:
            expression = params.get("expression", "")
            if not expression:
                return "Erreur: expression manquante"
            
            # Sécurisation de l'expression (autorise seulement certaines opérations)
            allowed_chars = set("0123456789+-*/().,math.sqrt math.pow math.sin math.cos math.tan math.log ")
            if not all(c in allowed_chars or c.isspace() for c in expression.replace("math.", "")):
                return "Erreur: caractères non autorisés dans l'expression"
            
            # Remplacement des fonctions mathématiques courantes
            safe_expression = expression.replace("^", "**")
            safe_expression = safe_expression.replace("sqrt", "math.sqrt")
            safe_expression = safe_expression.replace("sin", "math.sin")
            safe_expression = safe_expression.replace("cos", "math.cos")
            safe_expression = safe_expression.replace("tan", "math.tan")
            safe_expression = safe_expression.replace("log", "math.log")
            
            # Évaluation sécurisée
            allowed_names = {
                "__builtins__": {},
                "math": math,
                "abs": abs,
                "round": round,
                "min": min,
                "max": max
            }
            
            result = eval(safe_expression, allowed_names, {})
            return f"Résultat: {result}"
            
        except ZeroDivisionError:
            return "Erreur: division par zéro"
        except Exception as e:
            return f"Erreur de calcul: {str(e)}"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "expression": {
                "type": "string",
                "description": "Expression mathématique à calculer",
                "required": True,
                "examples": ["2 + 3", "sqrt(16)", "sin(3.14159/2)", "2^3"]
            }
        }
    
    def get_examples(self) -> List[str]:
        return [
            '[TOOL:calculator:{"expression": "2 + 3 * 4"}]',
            '[TOOL:calculator:{"expression": "sqrt(16)"}]',
            '[TOOL:calculator:{"expression": "2^3"}]'
        ]