"""
PARTE 4 - MÓDULO DE INTERFACE
Apresentação dos resultados (relatório no terminal).
"""
# "try/except" significa: "tente usar; se não estiver instalada, siga sem ela"
try:                                  # (Tente): programa tenta importar o tabulate. Se o pc tiver essa biblioteca instalada, ela será carregada normalmente
    from tabulate import tabulate     # Importa a função Tabulate: é uma biblioteca externa (ñ vem instalada por padrão no Python) usada para desenhar tabelas bonitas no terminal/console
except ImportError:                   # (Caso dê erro de importação): Se o pc ñ tiver o tabulate instalado, em vez de o programa quebrar e fechar com uma mensagem de erro
    tabulate = None                   # Define tabulate como None se a biblioteca não estiver instalada


def gerar_relatorio_terminal(resultados: Dict[str, Any]):
    print("\n" + "=" * 80)
    print(" RELATÓRIO EXECUTIVO - VIA PERMANENTE ".center(80, "="))
    print("=" * 80)

    dados_operacionais = [
        ["Carga em uma roda (P)", f"{resultados['P']:.3f} kgf"],
        ["Carga em grupo de dormentes (Pg)", f"{resultados['Pg']:.3f} kgf"],
        ["Coeficiente dinâmico (kv)", f"{resultados['kv']:.3f}"],
        ["Carga de cálculo (Pv)", f"{resultados['Pv']:.3f} kgf"],
        ["Largura efetiva da soca sob um trilho (s)", f"{resultados['s']:.2f} m"],
    ]

    dados_estruturais = [
        ["Pressão na face inferior do dormente (Pm)", f"{resultados['Pm']:.3f} kgf/cm²"],
        ["Pressão de ruptura do solo (Pr)", f"{resultados['Pr']:.3f} kgf/cm²"],
        ["Pressão admissível na Plataforma (Pap)", f"{resultados['Pap']:.3f} kgf/cm²"],
        ["Altura da camada de lastro (h) exata", f"> {resultados['h'] * 100:.3f} cm"],
    ]

    dados_cubagem = [
        ["Área da Seção Tipo", f"{resultados['area_secao']:.2f} m²"],
        ["Volume da Seção Tipo", f"{resultados['vol_secao']:.2f} m³"],
        ["Volume do dormente (Vd)", f"{resultados['Vd']:.2f} m³"],
        ["Qtd. Dormentes por km (inserida)", f"{resultados['qtd_dorm_km']:.0f} und/km"],
        ["Volume total de dormentes (Vds)", f"{resultados['Vds']:.2f} m³"],
        ["Volume total do lastro (VL)", f"{resultados['VL']:.2f} m³"],
        ["Volume total do lastro Majorado", f"{resultados['VL_maj']:.2f} m³"],
    ]

    if tabulate:
        print("\n[PARÂMETROS DE CARGA]")
        print(tabulate(dados_operacionais, headers=["Parâmetro", "Valor"], tablefmt="grid"))
        print("\n[DIMENSIONAMENTO ESTRUTURAL]")
        print(tabulate(dados_estruturais, headers=["Parâmetro", "Valor"], tablefmt="grid"))
        print("\n[QUANTITATIVOS E CUBAGEM]")
        print(tabulate(dados_cubagem, headers=["Parâmetro", "Valor"], tablefmt="grid"))
    else:
        for k, v in dados_operacionais + dados_estruturais + dados_cubagem:
            print(f"{k}: {v}")
