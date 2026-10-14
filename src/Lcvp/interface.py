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
    print("\n" + "=" * 80)                                            # Imprime uma linha divisória superior composta por 80 caracteres '=' no terminal.
    print(" RELATÓRIO EXECUTIVO - VIA PERMANENTE ".center(80, "="))   # Centraliza o título do relatório em uma faixa de 80 caracteres preenchida com '='.
    print("=" * 80)                                                   # Imprime a linha divisória inferior da caixa do cabeçalho.

    dados_operacionais = [                                                          # Monta a estrutura da lista contendo a descrição e os valores calculados dos parâmetros operacionais.
        ["Carga em uma roda (P)", f"{resultados['P']:.3f} kgf"],                    # Armazena a linha formatada para a carga da roda estática.
        ["Carga em grupo de dormentes (Pg)", f"{resultados['Pg']:.3f} kgf"],        # Armazena a linha formatada para a carga distribuída nos dormentes.
        ["Coeficiente dinâmico (kv)", f"{resultados['kv']:.3f}"],                   # Armazena a linha formatada para o coeficiente dinâmico adotado.
        ["Carga de cálculo (Pv)", f"{resultados['Pv']:.3f} kgf"],                   # Armazena a linha formatada para a carga total de projeto.
        ["Largura efetiva da soca sob um trilho (s)", f"{resultados['s']:.2f} m"],  # Armazena a linha formatada para a extensão da área socada.
    ]

    dados_estruturais = [                                                                      # Monta a estrutura da lista para armazenar os resultados do dimensionamento geotécnico e estrutural
        ["Pressão na face inferior do dormente (Pm)", f"{resultados['Pm']:.3f} kgf/cm²"],      # Armazena a linha formatada referente à pressão gerada na base do dormente.
        ["Pressão de ruptura do solo (Pr)", f"{resultados['Pr']:.3f} kgf/cm²"],                # Armazena a linha formatada referente à tensão de ruptura estimada para a plataforma.
        ["Pressão admissível na Plataforma (Pap)", f"{resultados['Pap']:.3f} kgf/cm²"],        # Armazena a linha formatada referente à tensão admissível no solo com fator de segurança.
        ["Altura da camada de lastro (h) exata", f"> {resultados['h'] * 100:.3f} cm"],         # Armazena a linha formatada para a espessura exata calculada do lastro em centímetros.
    ]

    dados_cubagem = [                                                                     # Monta a estrutura da lista com os valores de área, volumes e quantitativos de materiais.
        ["Área da Seção Tipo", f"{resultados['area_secao']:.2f} m²"],                     # Armazena a linha formatada contendo a área transversal da seção tipo.
        ["Volume da Seção Tipo", f"{resultados['vol_secao']:.2f} m³"],                    # Armazena a linha formatada contendo o volume bruto total da seção transversal
        ["Volume do dormente (Vd)", f"{resultados['Vd']:.2f} m³"],                        # Armazena a linha formatada contendo o volume unitário do dormente.
        ["Qtd. Dormentes por km (inserida)", f"{resultados['qtd_dorm_km']:.0f} und/km"],  # Armazena a linha formatada indicando a taxa de dormentes por quilômetro.
        ["Volume total de dormentes (Vds)", f"{resultados['Vds']:.2f} m³"],               # Armazena a linha formatada do volume acumulado ocupado pelos dormentes.
        ["Volume total do lastro (VL)", f"{resultados['VL']:.2f} m³"],                    # Armazena a linha formatada contendo o volume líquido estrito de pedra necessário.
        ["Volume total do lastro Majorado", f"{resultados['VL_maj']:.2f} m³"],            # Armazena a linha formatada contendo o volume final de compra acrescido da majoração.
    ]                                                                                     # Encerra a definição da lista de cubagem de materiais.

    if tabulate:                                                                                   # Checa se o pacote tabulate está disponível no ambiente para desenhar tabelas formatadas.
        print("\n[PARÂMETROS DE CARGA]")                                                           # Imprime o cabeçalho do bloco de parâmetros operacionais.
        print(tabulate(dados_operacionais, headers=["Parâmetro", "Valor"], tablefmt="grid"))       # Gera e exibe no terminal a tabela com a grade formatada para os dados de carga.
        print("\n[DIMENSIONAMENTO ESTRUTURAL]")                                                    # Imprime o cabeçalho do bloco de dimensionamento estrutural.
        print(tabulate(dados_estruturais, headers=["Parâmetro", "Valor"], tablefmt="grid"))        # Gera e exibe no terminal a tabela formatada para as pressões e espessura do lastro.
        print("\n[QUANTITATIVOS E CUBAGEM]")                                                       # Imprime o cabeçalho do bloco de quantitativos e cubagem.
        print(tabulate(dados_cubagem, headers=["Parâmetro", "Valor"], tablefmt="grid"))            # Gera e exibe no terminal a tabela formatada contendo os volumes calculados.
    else:                                                                                          # Caso a biblioteca tabulate não esteja instalada no ambiente de execução.
        for k, v in dados_operacionais + dados_estruturais + dados_cubagem:                        # Itera sequencialmente sobre todos os pares parâmetro-valor combinados nas listas.
                print(f"{k}: {v}")                                                                 # Imprime as informações no formato simplificado "Parâmetro: Valor".
            print(f"{k}: {v}")
