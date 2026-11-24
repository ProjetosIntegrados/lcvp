# TESTE - para Dimensionamento de Lastro e Cubagem

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

def test_passo1_carga_estatica_roda_P(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    # 90.000 / 8 = 11.250 kgf
    assert sup.carga_estatica_roda_P() == pytest.approx(11250.0, rel=1e-4)

def test_passo2_carga_distribuida_dormentes_Pg(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    # 11.250 * (0.55 / 1.574) = 3931.0673 kgf
    assert sup.carga_distribuida_dormentes_Pg() == pytest.approx(3931.0673, rel=1e-4)

def test_passo3_coeficiente_dinamico_kv_minimo_normativo(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    # Para v = 70 km/h, kv_calc = 1.2205 (< 1.4), portanto deve adotar 1.4
    assert sup.coeficiente_dinamico_kv() == pytest.approx(1.4, rel=1e-4)
    assert sup.aviso_kv_impresso is True

def test_passo3_coeficiente_dinamico_kv_velocidade_alta(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    op.velocidade = 100.0  # kv_calc = 1 + (4.5 * 10000 / 100000) = 1.45 (>= 1.4)
    sup = Superestrutura(op, geo, geom)
    assert sup.coeficiente_dinamico_kv() == pytest.approx(1.45, rel=1e-4)


def test_passo4_a_7_cargas_e_pressoes(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    assert sup.carga_de_calculo_Pv() == pytest.approx(5503.4943, rel=1e-4)
    assert sup.pressao_face_inferior_dormente_Pm() == pytest.approx(4.1693, rel=1e-4)
    assert sup.pressao_ruptura_solo_Pr() == pytest.approx(21.0, rel=1e-4)
    assert sup.pressao_admissivel_plataforma_Pap() == pytest.approx(3.8182, rel=1e-4)

def test_passo8_espessura_minima_lastro_h(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    # Sem arredondamento intermediário: 26,0404 cm (no caderno arredondado: 26,039 cm)
    h_metros = sup.espessura_minima_lastro_h()
    assert h_metros * 100 == pytest.approx(26.0404, abs=1e-3)

def test_espessura_lastro_com_pap_zero(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    geo.cbr = 0.0  # Força Pap = 0 para testar proteção contra divisão por zero
    sup = Superestrutura(op, geo, geom)
    assert sup.espessura_minima_lastro_h() == 0.0

# ---------------- Testes da Parte 3: Modelagem Geométrica ----------------

def test_modelagem_geometrica_e_cubagem(dados_exemplo_aula):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    h = sup.espessura_minima_lastro_h()
    sec = SecaoTransversal(geom, op, altura_lastro=h)

    assert sec.area_secao_tipo() == pytest.approx(1.24, abs=1e-2)
    assert sec.volume_secao_tipo() == pytest.approx(434_000.0, rel=1e-4)
    assert sec.volume_dormente_vd() == pytest.approx(0.07, abs=1e-2)
    assert sec.qtd_dormentes_por_km() == 1820.0
    assert sec.volume_total_dormentes_vds() == pytest.approx(44_590.0, rel=1e-4)
    assert sec.volume_total_lastro_vl() == pytest.approx(389_410.0, rel=1e-4)
    assert sec.volume_lastro_majorado() == pytest.approx(428_351.0, rel=1e-4)


# ---------------- Teste da Parte 4: Interface ----------------

def test_gerar_relatorio_terminal(dados_exemplo_aula, capsys):
    op, geo, geom = dados_exemplo_aula
    sup = Superestrutura(op, geo, geom)
    h = sup.espessura_minima_lastro_h()
    sec = SecaoTransversal(geom, op, altura_lastro=h)

    resultados = {
        'P': sup.carga_estatica_roda_P(),
        'Pg': sup.carga_distribuida_dormentes_Pg(),
        'kv': sup.coeficiente_dinamico_kv(),
        'Pv': sup.carga_de_calculo_Pv(),
        's': geom.comp_soca,
        'Pm': sup.pressao_face_inferior_dormente_Pm(),
        'Pr': sup.pressao_ruptura_solo_Pr(),
        'Pap': sup.pressao_admissivel_plataforma_Pap(),
        'h': h,
        'area_secao': sec.area_secao_tipo(),
        'vol_secao': sec.volume_secao_tipo(),
        'Vd': sec.volume_dormente_vd(),
        'qtd_dorm_km': sec.qtd_dormentes_por_km(),
        'Vds': sec.volume_total_dormentes_vds(),
        'VL': sec.volume_total_lastro_vl(),
        'VL_maj': sec.volume_lastro_majorado(),
    }

    gerar_relatorio_terminal(resultados)
    saida = capsys.readouterr().out
    assert "RELATÓRIO EXECUTIVO - VIA PERMANENTE" in saida
    assert "428351.00 m³" in saida
