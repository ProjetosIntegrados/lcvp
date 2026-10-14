"""
Programa principal: integra as 4 partes.
Execute com:  python main.py
"""
from entrada_dados import coletar_dados
from calculos import Superestrutura
from modelagem_geometrica import SecaoTransversal
from interface import gerar_relatorio_terminal


def main():
    # 1 - Inserção de dados
    op, geo, geom = coletar_dados()

    # 2 - Cálculos
    sup = Superestrutura(op, geo, geom)
    kv = sup.coeficiente_dinamico_kv()
    h_calc = sup.espessura_minima_lastro_h()

    # 3 - Modelagem geométrica
    sec = SecaoTransversal(geom, op, altura_lastro=h_calc)

    resultados_finais = {
        'P': sup.carga_estatica_roda_P(),
        'Pg': sup.carga_distribuida_dormentes_Pg(),
        'kv': kv,
        'Pv': sup.carga_de_calculo_Pv(),
        's': geom.comp_soca,
        'Pm': sup.pressao_face_inferior_dormente_Pm(),
        'Pr': sup.pressao_ruptura_solo_Pr(),
        'Pap': sup.pressao_admissivel_plataforma_Pap(),
        'h': h_calc,
        'area_secao': sec.area_secao_tipo(),
        'vol_secao': sec.volume_secao_tipo(),
        'Vd': sec.volume_dormente_vd(),
        'qtd_dorm_km': sec.qtd_dormentes_por_km(),
        'Vds': sec.volume_total_dormentes_vds(),
        'VL': sec.volume_total_lastro_vl(),
        'VL_maj': sec.volume_lastro_majorado(),
    }

    # 4 - Interface
    gerar_relatorio_terminal(resultados_finais)


if __name__ == "__main__":
    main()