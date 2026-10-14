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
    sup = Superestrutura(op, geo, geom)       # Cria o objeto de processamento estrutural contendo os parâmetros de entrada.

    kv = sup.coeficiente_dinamico_kv()        # Executa o cálculo e armazena o coeficiente dinâmico kv.
    h_calc = sup.espessura_minima_lastro_h()  # Executa o cálculo e armazena a espessura mínima h da camada de lastro em metros. 

    # 3 - Modelagem geométrica
    sec = SecaoTransversal(geom, op, altura_lastro=h_calc)     # Cria o objeto de modelagem geométrica utilizando a espessura h do lastro recém-calculada.


    resultados_finais = {                               # Constrói o dicionário de consolidação contendo as chaves e os valores dos resultados finais do dimensionamento.
        'P': sup.carga_estatica_roda_P(),               # Mapeia a carga estática atuante em uma roda.
        'Pg': sup.carga_distribuida_dormentes_Pg(),     # Mapeia a carga estática equivalente distribuída nos dormentes.
        'kv': kv,                                       # Mapeia o coeficiente dinâmico kv.
        'Pv': sup.carga_de_calculo_Pv(),                # Mapeia a carga dinâmica de projeto atuante no dormente.
        's': geom.comp_soca,                            # Mapeia o comprimento total da faixa de soca sob o trilho.
        'Pm': sup.pressao_face_inferior_dormente_Pm(),  # Mapeia a pressão solicitante na base do dormente.
        'Pr': sup.pressao_ruptura_solo_Pr(),            # Mapeia a tensão limite de ruptura do solo.
        'Pap': sup.pressao_admissivel_plataforma_Pap(), # Mapeia a tensão admissível calculada para a plataforma.
        'h': h_calc,                                    # Mapeia a altura mínima h calculada para o lastro.
        'area_secao': sec.area_secao_tipo(),            # Mapeia a área da seção transversal tipo.
        'vol_secao': sec.volume_secao_tipo(),           # Mapeia o volume bruto total da seção do trecho.
        'Vd': sec.volume_dormente_vd(),                 # Mapeia o volume unitário ocupado por um dormente.
        'qtd_dorm_km': sec.qtd_dormentes_por_km(),      # Mapeia a quantidade de dormentes por quilômetro.
        'Vds': sec.volume_total_dormentes_vds(),        # Mapeia o volume total ocupado pelo conjunto de dormentes.
        'VL': sec.volume_total_lastro_vl(),             # Mapeia o volume líquido de pedra britada para o lastro.
        'VL_maj': sec.volume_lastro_majorado()          # Mapeia o volume final de lastro com a margem de majoração aplicada.
    }                                                   # Finaliza a montagem do dicionário resultados_finais.

    # 4 - Interface
    gerar_relatorio_terminal(resultados_finais)


if __name__ == "__main__":
    main()
