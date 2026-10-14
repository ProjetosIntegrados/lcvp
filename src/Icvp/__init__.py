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

@dataclass                                                          # cria uma classe p/ armazenar dados
class ParametrosOperacionais:                                       # Guarda as variáveis ligadas ao veículo e ao tráfego ferroviário
    """Ficha 1: Parametros Operacionais –> O TREM e como opera."""   
                                                                      # Define o atributo para: 
    peso_total: float                                               # o peso total do vagão em kgf (tipo de dado esperado = decimal/real)
    num_rodas: int                                                  # o nº total de rodas do vagão -geralmente 8 em vagões de $ eixos- (tipo inteiro) 
    velocidade: float                                               # a velocidade operacional em km/h (tipo decimal)
    dist_eixos: float                                               # a distância entre eixos consecutivos em metros (tipo decimal)
    espacamento_dormentes: float                                    # o espaçamento entre dormentes em metros (tipo decimal)


@dataclass
class ParametrosGeotecnicos:                                        # Agrupa as características do terreno (plataforma/sublastro)
    
    """Ficha 2: Parametros Geotecnicos – O SOLO de fundação.""" 
                                                                      # Define o atributo para: 
    cbr: float                                                      # a capacidade de suporte CBR do solo em % (tipo decimal)
    fator_seguranca: float                                          # o fator de segurança Ns adotado (tipo decimal)


@dataclass
class ParametrosGeometricos:                                        # Geometria e Dimensões físicas da via permanente para o cálculo de tensões e volume de material
    
    """Ficha 3: Parametros Geometricos – MEDIDAS da linha (talude, trecho).""" 
                                                                      # Define o atributo para:
    comp_dormente: float                                            # o comprimento total do dormente em metros (tipo decimal)
    larg_dormente: float                                            # a largura da face superior/inferior do dormente em metros (tipo decimal)
    alt_dormente: float                                             # a altura/espessura do dormente em metros (tipo decimal)
    
    comp_soca: float                                                # a extensão total da área compactada sob o dormente em metros (tipo decimal).
    larg_ombro: float                                               # a largura da ombreira do lastro em metros (tipo decimal).
    inclinacao_talude: float                                        # a inclinação = proporção horizontal do talude X do lastro 1:X (tipo decimal).
    
    extensao_trecho_m: float                                        # a extensão total da via em metros (tipo decimal).
    extensao_trecho_km: float                                       # a extensão total da via em quilômetros (tipo decimal).
    fator_majoracao_perc: float                                     # o percentual de perdas/majoração do volume de lastro em % (tipo decimal).
    qtd_dormentes_km: float                                         # a quantidade de dormentes alocados por quilômetro (tipo decimal).
