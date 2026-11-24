"""
Testes automatizados para o pacote Lcvp (Dimensionamento de Lastro e Cubagem).
Execute com:
    poetry run pytest
"""
import builtins
import sys
import typing
from pathlib import Path
import pytest

# Mantém compatibilidade caso o teste rode em Python < 3.14
builtins.Dict = typing.Dict
builtins.Any = typing.Any

# Garante que os módulos dentro de src/Lcvp sejam encontrados sem alterar a pasta src/
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

@pytest.fixture
def dados_exemplo_aula():
    """Retorna os parâmetros do problema de 350 km da disciplina ENG09030."""
    op = ParametrosOperacionais(
        peso_total=90_000.0,
        num_rodas=8,
        velocidade=70.0,
        dist_eixos=1.574,
        espacamento_dormentes=0.55,
    )
    geo = ParametrosGeotecnicos(
        cbr=30.0,
        fator_seguranca=5.5,
    )
    geom = ParametrosGeometricos(
        comp_dormente=2.0,
        larg_dormente=0.22,
        alt_dormente=0.16,
        comp_soca=0.60,
        larg_ombro=0.35,
        inclinacao_talude=1.5,
        extensao_trecho_m=350_000.0,
        extensao_trecho_km=350.0,
        fator_majoracao_perc=10.0,
        qtd_dormentes_km=1820.0,
    )
    return op, geo, geom


# ---------------- Testes da Parte 2: Cálculos (Superestrutura) ----------------

