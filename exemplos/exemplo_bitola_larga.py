# EXEMPLO 2 - Ferrovia de Bitola Larga, 200 km (escoamento de minério de ferro).

import builtins
import math
import sys
import typing
from pathlib import Path

# Mantém compatibilidade com interface.py em versões do Python < 3.14
builtins.Dict = typing.Dict
builtins.Any = typing.Any

# Configura o caminho para localizar o pacote em src/Lcvp/
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DIR_LCVP = RAIZ_PROJETO / "src" / "Lcvp"

if str(DIR_LCVP) not in sys.path:
    sys.path.insert(0, str(DIR_LCVP))
if str(RAIZ_PROJETO / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from Lcvp.entrada_dados import (
    ParametrosOperacionais,
    ParametrosGeotecnicos,
    ParametrosGeometricos,
)
from Lcvp.calculos import Superestrutura
from Lcvp.modelagem_geometrica import SecaoTransversal
from Lcvp.interface import gerar_relatorio_terminal

try:
    from Lcvp.interface import plotar_secao_transversal
except ImportError:
    plotar_secao_transversal = None


def executar_exemplo():
    print("=" * 80)
    print(" EXEMPLO: FERROVIA DE BITOLA LARGA (200 km - MINÉRIO DE FERRO) ".center(80, "="))
    print("=" * 80)

    # 1. Parâmetros Operacionais
    # 4 eixos por veículo = 8 rodas
    op = ParametrosOperacionais(
        peso_total=119_000.0,         # Carga total por vagão (kgf)
        num_rodas=8,                  # 4 eixos x 2 rodas/eixo
        velocidade=70.0,              # Velocidade operacional (km/h)
        dist_eixos=2.0,               # Distância entre eixos (m)
        espacamento_dormentes=0.55,   # Espaçamento entre dormentes (55 cm)
    )

    # 2. Parâmetros Geotécnicos
    geo = ParametrosGeotecnicos(
        cbr=18.5,                     # CBR da plataforma (%)
        fator_seguranca=5.5,          # Coeficiente de segurança (Ns)
    )
