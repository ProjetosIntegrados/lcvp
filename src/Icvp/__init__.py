# CÓDIGO FONTE
import math                          # Importa o módulo matemático do Python.
from dataclasses import dataclass    # Importa dataclass p/ facilitar a criação de estruturas de dados, forma rápida e organizada de criar classes q/ servem principalmente p/ armazenar dados (como se fossem "fichas de cadastro")
from typing import Dict, Any         # Importa os tipos genéricos Dict e Any para anotações de tipo de variáveis e funções.

try:                                 # (Tente): programa tenta importar o tabulate. Se o pc tiver essa biblioteca instalada, ela será carregada normalmente.
    from tabulate import tabulate    # Importa a função Tabulate: é uma biblioteca externa (ñ vem instalada por padrão no Python) usada para desenhar tabelas bonitas no terminal/console.
except ImportError:                  # (Caso dê erro de importação): Se o pc ñ tiver o tabulate instalado, em vez de o programa quebrar e fechar com uma mensagem de erro
    tabulate = None                  # Define tabulate como None se a biblioteca não estiver instalada.

#
