#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def init_project():
    print("🚀 Inicializando DGM-MCP...\n")

    # Criar .env se não existir
    if not Path(".env").exists() and Path(".env.example").exists():
        Path(".env").write_text(Path(".env.example").read_text())
        print("✅ .env criado a partir do exemplo")
        print("   → Edita o ficheiro .env com as tuas API keys!")

    # Instalar em modo editável
    os.system("pip install -e .")
    print("✅ Pacote instalado em modo desenvolvimento")

    print("\n✅ DGM-MCP está pronto!")
    print("\nComandos úteis:")
    print("   dgm-mcp dashboard     → Ver estado")
    print("   dgm-mcp tools         → Ver ferramentas")
    print("   dgm-mcp test          → Teste rápido")
    print("   dgm-mcp start         → Iniciar servidor")

if __name__ == "__main__":
    init_project()
