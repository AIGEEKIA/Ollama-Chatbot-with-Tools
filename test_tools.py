#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les outils fonctionnent correctement
"""

import asyncio
import sys
import os

# Ajouter le dossier racine au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.tool_manager import ToolManager

async def test_tools():
    """Test de tous les outils disponibles"""
    print("🧪 Test des outils du chatbot Ollama\n")
    
    tool_manager = ToolManager()
    
    # Test Calculator
    print("🔢 Test Calculator Tool:")
    result = await tool_manager.tools["calculator"].execute({"expression": "2 + 3 * 4"})
    print(f"   2 + 3 * 4 = {result}")
    
    result = await tool_manager.tools["calculator"].execute({"expression": "sqrt(16)"})
    print(f"   sqrt(16) = {result}")
    
    # Test Weather
    print("\n🌤️ Test Weather Tool:")
    result = await tool_manager.tools["weather"].execute({"city": "Paris"})
    print(f"   Météo Paris: {result}")
    
    # Test File
    print("\n📁 Test File Tool:")
    result = await tool_manager.tools["file"].execute({"action": "list", "path": "."})
    print(f"   Fichiers racine: {result[:100]}...")
    
    # Test Search
    print("\n🔍 Test Search Tool:")
    result = await tool_manager.tools["search"].execute({"query": "Python tutorial"})
    print(f"   Recherche Python: {result[:100]}...")
    
    # Test du gestionnaire complet
    print("\n🔧 Test du gestionnaire d'outils:")
    test_response = "Calculons 15 * 23: [TOOL:calculator:{\"expression\": \"15 * 23\"}]"
    processed_response, tools_used = await tool_manager.process_response(test_response)
    print(f"   Réponse traitée: {processed_response}")
    print(f"   Outils utilisés: {tools_used}")
    
    print("\n✅ Tous les tests sont terminés!")

if __name__ == "__main__":
    asyncio.run(test_tools())