"""
PARTE 1 - INSERÇÃO DE DADOS
Estruturas de dados e coleta das informações fornecidas pelo usuário.
"""
from dataclasses import dataclass


@dataclass                                                          # cria uma classe p/ armazenar dados
class ParametrosOperacionais:                                       # Guarda as variáveis ligadas ao veículo e ao tráfego ferroviário
    """Ficha 1: Parametros Operacionais –> O TREM e como opera."""   
                                                                      # Define o atributo para: 
    peso_total: float                                               # o peso total do vagão em kgf (tipo de dado esperado = decimal/real)
    num_rodas: int                                                  # o nº total de rodas do vagão -geralmente 8 em vagões de $ eixos- (tipo inteiro) 
    velocidade: float                                               # a velocidade operacional em km/h (tipo decimal)
    dist_eixos: float                                               # a distância entre eixos consecutivos em metros (tipo decimal)
    espacamento_dormentes: float                                    # o espaçamento entre dormentes em metros (tipo decimal)


@dataclass
class ParametrosGeotecnicos:                                        # Agrupa as características do terreno (plataforma/sublastro)
    
    """Ficha 2: Parametros Geotecnicos – O SOLO de fundação.""" 
                                                                      # Define o atributo para: 
    cbr: float                                                      # a capacidade de suporte CBR do solo em % (tipo decimal)
    fator_seguranca: float                                          # o fator de segurança Ns adotado (tipo decimal)


@dataclass
class ParametrosGeometricos:                                        # Geometria e Dimensões físicas da via permanente para o cálculo de tensões e volume de material
    
    """Ficha 3: Parametros Geometricos – MEDIDAS da linha (talude, trecho).""" 
                                                                      # Define o atributo para:
    comp_dormente: float                                            # o comprimento total do dormente em metros (tipo decimal)
    larg_dormente: float                                            # a largura da face superior/inferior do dormente em metros (tipo decimal)
    alt_dormente: float                                             # a altura/espessura do dormente em metros (tipo decimal)
    
    comp_soca: float                                                # a extensão total da área compactada sob o dormente em metros (tipo decimal).
    larg_ombro: float                                               # a largura da ombreira do lastro em metros (tipo decimal).
    inclinacao_talude: float                                        # a inclinação = proporção horizontal do talude X do lastro 1:X (tipo decimal).
    
    extensao_trecho_m: float                                        # a extensão total da via em metros (tipo decimal).
    extensao_trecho_km: float                                       # a extensão total da via em quilômetros (tipo decimal).
    fator_majoracao_perc: float                                     # o percentual de perdas/majoração do volume de lastro em % (tipo decimal).
    qtd_dormentes_km: float                                         # a quantidade de dormentes alocados por quilômetro (tipo decimal).


def validar_entrada(mensagem: str, tipo: type = float):
    """Lê um valor do teclado, aceitando vírgula decimal e exigindo valor > 0."""
    while True:                                                     # Cria um laço infinito para solicitar o valor repetidamente até que seja fornecida uma entrada válida
        try:                                                        # Inicia o bloco de tratamento de exceções para capturar falhas de conversão de dados
            entrada = input(mensagem).replace(',', '.')             # Lê o texto digitado pelo usuário e substitui eventuais vírgulas por pontos decimais
            valor = tipo(entrada)                                   # Converte a string limpa para o tipo especificado (float ou int)
            if valor <= 0:                                          # Verifica se o valor informado é menor ou igual a zero
                print("Erro: O valor deve ser maior que zero.")     # Exibe uma mensagem de erro indicando que a entrada deve ser estritamente positiva
                continue                                            # Reinicia o laço while solicitando a entrada do usuário novamente
            return valor                                            # Retorna o valor numérico validado e encerra o laço
        except ValueError:                                          # Captura falhas de conversão caso o usuário forneça textos inválidos ou símbolos não numéricos
            print("Erro: Entrada inválida. Insira apenas números.") # Imprime mensagem alertando que a entrada não é numérica


def coletar_dados():
    """Solicita os dados ao usuário e devolve (op, geo, geom)."""
    print("=== CÁLCULO DE LASTRO - INSERÇÃO DE DADOS ===")                                 # Exibe o título principal de entrada de dados no console.
    
                                                                                                # Solicita e valida: 
    extensao_km = InterfaceIO.validar_entrada("Extensão do trecho (km) [ex: 350]: ")       # o comprimento do trecho ferroviário em quilômetros.
    carga_vagao = InterfaceIO.validar_entrada("Carga total por vagão (kg) [ex: 90000]: ")  # a o peso bruto total do vagão em kg.
    velocidade = InterfaceIO.validar_entrada("Velocidade operacional (km/h) [ex: 70]: ")   #  velocidade máxima de operação do trem em km/h.
    num_eixos = InterfaceIO.validar_entrada("Número de eixos por veículo [ex: 4]: ", int)  # o número de eixos do vagão como um número inteiro.
    dist_eixos = InterfaceIO.validar_entrada("Distância entre eixos (m) [ex: 1.574]: ")    # a distância longitudinal entre eixos contíguos em metros.
    cbr = InterfaceIO.validar_entrada("CBR do sublastro (%) [ex: 30]: ")                   # o valor porcentual do Índice de Suporte Califórnia (CBR).


    while True:                                                                                           # Inicia o laço de repetição específico para validação do Fator de Segurança dentro da faixa normativa.
        fator_seguranca = InterfaceIO.validar_entrada("Coeficiente de segurança Ns (5 a 6) [ex: 5.5]: ")  # Solicita e lê o valor numérico do coeficiente de segurança.
        if 5.0 <= fator_seguranca <= 6.0:                                                                 # Checa se o valor digitado pertence ao intervalo fechado [5.0, 6.0].
            break                                                                                         # Encerra o laço de validação do fator de segurança se a entrada estiver correta.
        print("Erro: O coeficiente de segurança Ns deve estar entre 5 e 6.")                              # Exibe aviso informando o intervalo permitido para o fator de segurança.

    soca_lado = InterfaceIO.validar_entrada("Soca para cada lado do eixo dos trilhos (cm) [ex: 30]: ")  # Solicita e valida o comprimento da faixa socada para cada lado do trilho em centímetros.
    ombreira_cm = InterfaceIO.validar_entrada("Ombreiras para cada lado (cm) [ex: 35]: ")               # Solicita e valida a largura da ombreira do lastro em centímetros.
    espacamento_cm = InterfaceIO.validar_entrada("Espaçamento entre dormentes (cm) [ex: 55]: ")         # Solicita e valida o espaçamento centro-a-centro entre dormentes adjacentes em centímetros.
    qtd_dormentes_km = InterfaceIO.validar_entrada("Qtd. Dormentes por km [ex: 1820]: ")                # Solicita e valida a taxa de dormentes aplicados por quilômetro de via.

    print("\n-- Dimensões do Dormente --")                                    # Exibe o subcabeçalho para o bloco de parâmetros do dormente.
    comp_dormente = InterfaceIO.validar_entrada("Comprimento (m) [ex: 2]: ")  # Solicita e valida a dimensão do comprimento do dormente em metros.
    larg_dormente = InterfaceIO.validar_entrada("Largura (m) [ex: 0.22]: ")   # Solicita e valida a dimensão da largura do dormente em metros.
    alt_dormente = InterfaceIO.validar_entrada("Altura (m) [ex: 0.16]: ")      # Solicita e valida a dimensão da altura/espessura do dormente em metros.

    inclinacao_talude = InterfaceIO.validar_entrada("\nInclinação do talude (X para 1:X) [ex: 1.5]: ")            # Solicita e valida o valor da proporção horizontal X para a inclinação do talude 1:X.
    fator_majoracao_perc = InterfaceIO.validar_entrada("Coeficiente de majoração sobre o lastro (%) [ex: 10]: ")  # Solicita e valida o percentual extra de majoração do volume do lastro em %.

                                               # Conversões de unidade
    num_rodas = num_eixos * 2                  # Multiplica a quantidade de eixos por 2 para encontrar o total de rodas do veículo.
    comp_soca_total_m = (soca_lado * 2) / 100  # Calcula a extensão total socada considerando os dois lados do trilho e converte de cm para metros.

    op = ParametrosOperacionais(                      # Instancia o objeto para a Ficha 1 de parâmetros operacionais.
        peso_total=carga_vagao,                       # Atribui o peso total do vagão em kgf.
        num_rodas=num_rodas,                          # Atribui a quantidade calculada de rodas do veículo.
        velocidade=velocidade,                        # Atribui a velocidade do trem em km/h.
        dist_eixos=dist_eixos,                        # Atribui a distância entre eixos contíguos em metros.
        espacamento_dormentes=espacamento_cm / 100    # Atribui o espaçamento de dormentes convertido de cm para metros.
    )                                                 # Conclui a instanciação de ParametrosOperacionais.

    geo = ParametrosGeotecnicos(         # Instancia o objeto para a Ficha 2 de parâmetros geotécnicos.
        cbr=cbr,                         # Atribui o valor porcentual do CBR do solo.
        fator_seguranca=fator_seguranca  # Atribui o fator de segurança Ns definido.
    )

    geom = ParametrosGeometricos(                   # Instancia o objeto para a Ficha 3 de parâmetros geométricos.
        comp_dormente=comp_dormente,                # Atribui o comprimento do dormente em metros.
        larg_dormente=larg_dormente,                # Atribui a largura do dormente em metros.
        alt_dormente=alt_dormente,                  # Atribui a altura do dormente em metros.
        comp_soca=comp_soca_total_m,                # Atribui a extensão da área socada calculada em metros.
        larg_ombro=ombreira_cm / 100,               # Atribui a largura das ombreiras convertida de cm para metros.
        inclinacao_talude=inclinacao_talude,        # Atribui a razão de inclinação horizontal do talude X.
        extensao_trecho_m=extensao_km * 1000,       # Atribui a extensão total da ferrovia convertida de km para metros.
        extensao_trecho_km=extensao_km,             # Atribui a extensão total da ferrovia mantida em quilômetros.
        fator_majoracao_perc=fator_majoracao_perc,  # Atribui o fator de majoração em porcentagem.
        qtd_dormentes_km=qtd_dormentes_km           # Atribui a quantidade de dormentes alocados por quilômetro.
    ) 

    return op, geo, geom
