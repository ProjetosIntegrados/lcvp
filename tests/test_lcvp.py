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

