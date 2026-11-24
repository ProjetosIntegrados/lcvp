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

    # 3. Parâmetros Geométricos
    # Soca = 40 cm para cada lado do eixo do trilho -> 80 cm (0,80 m) sob um trilho
    geom = ParametrosGeometricos(
        comp_dormente=2.80,           # Comprimento do dormente (m)
        larg_dormente=0.24,           # Largura do dormente (m)
        alt_dormente=0.17,            # Altura do dormente (m)
        comp_soca=0.80,               # Largura efetiva da soca sob um trilho (m)
        larg_ombro=0.30,              # Ombreira (30 cm)
        inclinacao_talude=1.5,        # Inclinação do talude (1:1,5)
        extensao_trecho_m=200_000.0,  # Extensão em metros (200 km)
        extensao_trecho_km=200.0,     # Extensão em quilômetros
        fator_majoracao_perc=10.0,    # Fator de majoração sobre a compactação (%)
        qtd_dormentes_km=1820.0,      # Quantidade de dormentes por km
    )

    # 4. Dimensionamento Estrutural (8 passos - Talbot)
    sup = Superestrutura(op, geo, geom)
    h_exato = sup.espessura_minima_lastro_h()
    h_adotado = math.ceil(h_exato * 100) / 100

    # 5. Modelagem Geométrica e Cubagem
    sec = SecaoTransversal(geom, op, altura_lastro=h_adotado)

    resultados = {
        "P": sup.carga_estatica_roda_P(),
        "Pg": sup.carga_distribuida_dormentes_Pg(),
        "kv": sup.coeficiente_dinamico_kv(),
        "Pv": sup.carga_de_calculo_Pv(),
        "s": geom.comp_soca,
        "Pm": sup.pressao_face_inferior_dormente_Pm(),
        "Pr": sup.pressao_ruptura_solo_Pr(),
        "Pap": sup.pressao_admissivel_plataforma_Pap(),
        "h": h_exato,
        "area_secao": sec.area_secao_tipo(),
        "vol_secao": sec.volume_secao_tipo(),
        "Vd": sec.volume_dormente_vd(),
        "qtd_dorm_km": sec.qtd_dormentes_por_km(),
        "Vds": sec.volume_total_dormentes_vds(),
        "VL": sec.volume_total_lastro_vl(),
        "VL_maj": sec.volume_lastro_majorado(),
    }

    # 6. Relatório no terminal
    gerar_relatorio_terminal(resultados)

    # 7. Representação gráfica da seção tipo (caso plotar_secao_transversal esteja no interface.py)
    if plotar_secao_transversal is not None:
        plotar_secao_transversal(
            {**resultados, "h": h_adotado},
            comp_dormente=geom.comp_dormente,
            larg_ombro=geom.larg_ombro,
            alt_dormente=geom.alt_dormente,
            inclinacao_talude=geom.inclinacao_talude,
            cbr=geo.cbr,
        )

if __name__ == "__main__":
    executar_exemplo()
