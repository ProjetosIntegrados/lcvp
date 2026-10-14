# CÓDIGO FONTE
import math                           # Importa o módulo matemático do Python
from dataclasses import dataclass     # Importa dataclass p/ facilitar a criação de estruturas de dados, forma rápida e organizada de criar classes q/ servem principalmente p/ armazenar dados (como se fossem "fichas de cadastro")
from typing import Dict, Any          # Importa os tipos genéricos Dict e Any para anotações de tipo de variáveis e funções

# "try/except" significa: "tente usar; se não estiver instalada, siga sem ela"
try:                                  # (Tente): programa tenta importar o tabulate. Se o pc tiver essa biblioteca instalada, ela será carregada normalmente
    from tabulate import tabulate     # Importa a função Tabulate: é uma biblioteca externa (ñ vem instalada por padrão no Python) usada para desenhar tabelas bonitas no terminal/console
except ImportError:                   # (Caso dê erro de importação): Se o pc ñ tiver o tabulate instalado, em vez de o programa quebrar e fechar com uma mensagem de erro
    tabulate = None                   # Define tabulate como None se a biblioteca não estiver instalada

# ==================================================================================================================================================================================================================
# 1. ARQUITETURA DOS DADOS DO PROGRAMA: criação de fichas de cadastro p/ agrupar os dados de entrada (q/ usuário digita) em 3 categorias (Trem, Solo e Medidas da Linha), em vez de trabalhar com 15 variáveis
# ==================================================================================================================================================================================================================

@dataclass                                # cria uma classe p/ armazenar dados
class ParametrosOperacionais:        
    """Ficha 1: ParametrosOperacionais – O TREM e como ele opera."""   #Guarda as variáveis ligadas ao veículo e ao tráfego ferroviário.
                                # Define o atributo para: 
    peso_total: float                # o peso total do vagão em kgf (tipo decimal).
    num_rodas: int                   # o número total de rodas do vagão (tipo inteiro).
    velocidade: float                # a velocidade operacional em km/h (tipo decimal).
    dist_eixos: float                # a distância entre eixos consecutivos em metros (tipo decimal).
    espacamento_dormentes: float     # o espaçamento entre dormentes em metros (tipo decimal).


@dataclass
class ParametrosGeotecnicos:
    """Ficha 2 – O SOLO sobre o qual tudo se apoia."""
    cbr: float                    # Define o atributo para a capacidade de suporte CBR do solo em % (tipo decimal).
    fator_seguranca: float        # Define o atributo para o fator de segurança Ns adotado (tipo decimal).


@dataclass
class ParametrosGeometricos:
    """Ficha 3 – MEDIDAS da linha (dormente, ombreira, talude, trecho)."""
    comp_dormente: float          # Define o atributo para o comprimento total do dormente em metros (tipo decimal).
    larg_dormente: float          # Define o atributo para a largura da face superior/inferior do dormente em metros (tipo decimal).
    alt_dormente: float           # Define o atributo para a altura/espessura do dormente em metros (tipo decimal).
    comp_soca: float              # Define o atributo para a extensão total da área socada sob o dormente em metros (tipo decimal).
    larg_ombro: float             # Define o atributo para a largura da ombreira do lastro em metros (tipo decimal).
    inclinacao_talude: float      # Define o atributo para a proporção horizontal do talude X do lastro 1:X (tipo decimal).
    extensao_trecho_m: float      # Define o atributo para a extensão total da via em metros (tipo decimal).
    extensao_trecho_km: float     # Define o atributo para a extensão total da via em quilômetros (tipo decimal).
    fator_majoracao_perc: float   # Define o atributo para o percentual de perdas/majoração do volume de lastro em % (tipo decimal).
    qtd_dormentes_km: float       # Define o atributo para a quantidade de dormentes alocados por quilômetro (tipo decimal).
