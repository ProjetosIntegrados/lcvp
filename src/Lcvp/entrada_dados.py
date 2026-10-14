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
    while True:
        try:
            entrada = input(mensagem).replace(',', '.')
            valor = tipo(entrada)
            if valor <= 0:
                print("Erro: O valor deve ser maior que zero.")
                continue
            return valor
        except ValueError:
            print("Erro: Entrada inválida. Insira apenas números.")


def coletar_dados():
    """Solicita os dados ao usuário e devolve (op, geo, geom)."""
    print("=== CÁLCULO DE LASTRO - INSERÇÃO DE DADOS ===")

    extensao_km = validar_entrada("Extensão do trecho (km) [ex: 350]: ")
    carga_vagao = validar_entrada("Carga total por vagão (kg) [ex: 90000]: ")
    velocidade = validar_entrada("Velocidade operacional (km/h) [ex: 70]: ")
    num_eixos = validar_entrada("Número de eixos por veículo [ex: 4]: ", int)
    dist_eixos = validar_entrada("Distância entre eixos (m) [ex: 1.574]: ")
    cbr = validar_entrada("CBR do sublastro (%) [ex: 30]: ")

    while True:
        fator_seguranca = validar_entrada("Coeficiente de segurança Ns (5 a 6) [ex: 5.5]: ")
        if 5.0 <= fator_seguranca <= 6.0:
            break
        print("Erro: O coeficiente de segurança Ns deve estar entre 5 e 6.")

    soca_lado = validar_entrada("Soca para cada lado do eixo dos trilhos (cm) [ex: 30]: ")
    ombreira_cm = validar_entrada("Ombreiras para cada lado (cm) [ex: 35]: ")
    espacamento_cm = validar_entrada("Espaçamento entre dormentes (cm) [ex: 55]: ")
    qtd_dormentes_km = validar_entrada("Qtd. Dormentes por km [ex: 1820]: ")

    print("\n-- Dimensões do Dormente --")
    comp_dormente = validar_entrada("Comprimento (m) [ex: 2]: ")
    larg_dormente = validar_entrada("Largura (m) [ex: 0.22]: ")
    alt_dormente = validar_entrada("Altura (m) [ex: 0.16]: ")

    inclinacao_talude = validar_entrada("\nInclinação do talude (X para 1:X) [ex: 1.5]: ")
    fator_majoracao_perc = validar_entrada("Coeficiente de majoração sobre o lastro (%) [ex: 10]: ")

    # Conversões de unidade
    num_rodas = num_eixos * 2
    comp_soca_total_m = (soca_lado * 2) / 100

    op = ParametrosOperacionais(
        peso_total=carga_vagao,
        num_rodas=num_rodas,
        velocidade=velocidade,
        dist_eixos=dist_eixos,
        espacamento_dormentes=espacamento_cm / 100,
    )

    geo = ParametrosGeotecnicos(
        cbr=cbr,
        fator_seguranca=fator_seguranca,
    )

    geom = ParametrosGeometricos(
        comp_dormente=comp_dormente,
        larg_dormente=larg_dormente,
        alt_dormente=alt_dormente,
        comp_soca=comp_soca_total_m,
        larg_ombro=ombreira_cm / 100,
        inclinacao_talude=inclinacao_talude,
        extensao_trecho_m=extensao_km * 1000,
        extensao_trecho_km=extensao_km,
        fator_majoracao_perc=fator_majoracao_perc,
        qtd_dormentes_km=qtd_dormentes_km,
    )

    return op, geo, geom
