"""
EXEMPLO – Ferrovia de bitola estreita, 350 km (produtos agrícolas e carga geral).

Reproduz, sem digitar nada no terminal, a resolução à mão deste problema da aula
(ENG09030) e confere o resultado do programa com o caderno.

Execute com:
    poetry run python exemplos/exemplo__lastro_ferrovia.py
"""
import sys
import typing
from pathlib import Path

# 1. Injeta 'Dict' e 'Any' no escopo global para compatibilidade do interface.py sem alterar o arquivo
import builtins
builtins.Dict = typing.Dict
builtins.Any = typing.Any

# 2. Configura os caminhos de busca do Python (sys.path)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DIR_LCVP = RAIZ_PROJETO / "src" / "Lcvp"

if str(DIR_LCVP) not in sys.path:
    sys.path.insert(0, str(DIR_LCVP))
if str(RAIZ_PROJETO / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO / "src"))

# 3. Importações do projeto (funciona 100% com a pasta src/Lcvp intocada)
from Lcvp.calculos import Superestrutura
from Lcvp.entrada_dados import (ParametrosGeometricos, ParametrosGeotecnicos,
                                ParametrosOperacionais)
from Lcvp.interface import gerar_relatorio_terminal
from Lcvp.modelagem_geometrica import SecaoTransversal

# ---------------- Dados do enunciado ----------------
EXTENSAO_KM = 350
CARGA_VAGAO_KG = 90_000
VELOCIDADE_KMH = 70
NUM_EIXOS = 4
DIST_EIXOS_M = 1.574
CBR_PERC = 30
NS = 5.5
SOCA_LADO_CM = 30
OMBREIRA_CM = 35
ESPACAMENTO_CM = 55
DORMENTES_POR_KM = 1820
DORMENTE_M = (2.0, 0.22, 0.16)          # comprimento, largura, altura
TALUDE_X = 1.5                          # talude 1:1,5
MAJORACAO_PERC = 10


def montar_dados():
    """Converte o enunciado (cm, km) para as unidades do programa (m)."""
    op = ParametrosOperacionais(
        peso_total=CARGA_VAGAO_KG, num_rodas=NUM_EIXOS * 2,
        velocidade=VELOCIDADE_KMH, dist_eixos=DIST_EIXOS_M,
        espacamento_dormentes=ESPACAMENTO_CM / 100)
    geo = ParametrosGeotecnicos(cbr=CBR_PERC, fator_seguranca=NS)
    geom = ParametrosGeometricos(
        comp_dormente=DORMENTE_M[0], larg_dormente=DORMENTE_M[1],
        alt_dormente=DORMENTE_M[2], comp_soca=SOCA_LADO_CM * 2 / 100,
        larg_ombro=OMBREIRA_CM / 100, inclinacao_talude=TALUDE_X,
        extensao_trecho_m=EXTENSAO_KM * 1000, extensao_trecho_km=EXTENSAO_KM,
        fator_majoracao_perc=MAJORACAO_PERC, qtd_dormentes_km=DORMENTES_POR_KM)
    return op, geo, geom


def main():
    op, geo, geom = montar_dados()
    sup = Superestrutura(op, geo, geom)
    h = sup.espessura_minima_lastro_h()
    sec = SecaoTransversal(geom, op, altura_lastro=h)

    resultados = {
        'P': sup.carga_estatica_roda_P(), 'Pg': sup.carga_distribuida_dormentes_Pg(),
        'kv': sup.coeficiente_dinamico_kv(), 'Pv': sup.carga_de_calculo_Pv(),
        's': geom.comp_soca, 'Pm': sup.pressao_face_inferior_dormente_Pm(),
        'Pr': sup.pressao_ruptura_solo_Pr(), 'Pap': sup.pressao_admissivel_plataforma_Pap(),
        'h': h, 'area_secao': sec.area_secao_tipo(), 'vol_secao': sec.volume_secao_tipo(),
        'Vd': sec.volume_dormente_vd(), 'qtd_dorm_km': sec.qtd_dormentes_por_km(),
        'Vds': sec.volume_total_dormentes_vds(), 'VL': sec.volume_total_lastro_vl(),
        'VL_maj': sec.volume_lastro_majorado(),
    }
    print("=== EXEMPLO:  lastro ferrovia, 350 km ===")
    gerar_relatorio_terminal(resultados)

    print("\nConferência com a resolução à mão (caderno):")
    print(f"  h calculado ........ {h * 100:.3f} cm   (caderno: h >= 26,039 cm)")
    print(f"  Área da seção ...... {resultados['area_secao']:.2f} m²    (caderno: 1,24 m²)")
    print(f"  Lastro majorado .... {resultados['VL_maj']:.0f} m³ (caderno: 428.351 m³)")


if __name__ == "__main__":
    main()
