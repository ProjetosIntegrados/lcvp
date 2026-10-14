"""
PARTE 2 - RESOLUÇÃO DOS CÁLCULOS
Modelagem analítica da superestrutura (cargas, pressões e espessura do lastro).
"""
from entrada_dados import ParametrosOperacionais, ParametrosGeotecnicos, ParametrosGeometricos

class Superestrutura:                """Faz os cálculos de peso, pressão e espessura do lastro."""
    
    def __init__(self, op: ParametrosOperacionais, geo: ParametrosGeotecnicos, geom: ParametrosGeometricos):
        self.op = op                       # Armazena a instância dos parâmetros operacionais no objeto.
        self.geo = geo                     # Armazena a instância dos parâmetros geotécnicos no objeto.
        self.geom = geom                   # Armazena a instância dos parâmetros geométricos no objeto.
        self.aviso_kv_impresso = False     # Inicializa a flag de controle para evitar a duplicação do aviso de kv no console.


    def carga_estatica_roda_P(self) -> float:                 """PASSO 1 – Quanto peso cada roda carrega?"""
        return self.op.peso_total / self.op.num_rodas       # Divide o peso total do veículo pelo número de rodas para obter a carga por roda (kgf).

    def carga_distribuida_dormentes_Pg(self) -> float:                                                      """PASSO 2 – Quanto do peso de UMA roda fica em UM dormente?"""
        return self.carga_estatica_roda_P() * (self.op.espacamento_dormentes / self.op.dist_eixos)           # Distribui a carga da roda nos dormentes proporcionalmente à razão (espacamento / distância_eixos) (kgf).

    def coeficiente_dinamico_kv(self) -> float:                            """PASSO 3 – Quanto o movimento "aumenta" o peso? (coeficiente dinâmico)"""
        kv_calculado = 1.0 + (4.5 * (self.op.velocidade ** 2) / 100000)    # Aplica a fórmula empírica para calcular o coeficiente dinâmico kv em função da velocidade (sem dimensão).

        if kv_calculado < 1.4:                                                                                                     # Verifica se o coeficiente calculado é inferior ao limite normativo mínimo de 1,4.
            if not self.aviso_kv_impresso:                                                                                         # Checa se o aviso de substituição do kv ainda não foi exibido na tela.
                print(f"\n[AVISO] O coeficiente dinâmico (kv) calculated foi {kv_calculado:.3f}. Adotando o valor mínimo: 1.400")  # Imprime no terminal o aviso de adoção do kv mínimo.
                self.aviso_kv_impresso = True                                                                                      # Atualiza a flag para indicar que o aviso do kv já foi exibido.
            return 1.4                                                                                                             # Retorna o valor normativo mínimo de 1,4.
        return kv_calculado                                                                                                        # Retorna o coeficiente dinâmico calculado quando este for maior ou igual a 1,4.

    def carga_de_calculo_Pv(self) -> float:
                                                                                             """PASSO 4 – Peso "de projeto" sobre um dormente (já com o efeito do movimento)."""
        return self.carga_distribuida_dormentes_Pg() * self.coeficiente_dinamico_kv()        # Majora a carga distribuída estática pelo coeficiente dinâmico kv (kgf).

    def pressao_face_inferior_dormente_Pm(self) -> float:
                                                                      """PASSO 5 – Pressão que o dormente faz na pedra logo abaixo dele."""
        area_soca = self.geom.comp_soca * self.geom.larg_dormente     # Calcula a área de contato efetiva das faixas de soca do dormente em m².
        return self.carga_de_calculo_Pv() / (area_soca * 10000)       # Divide a carga vertical Pv pela área da soca convertida para cm² (1 m² = 10.000 cm²), retornando a pressão em kgf/cm².

    def pressao_ruptura_solo_Pr(self) -> float:
                                     """PASSO 6 – Pressão que faria o solo ROMPER (ceder)."""
        return self.geo.cbr * 0.7    # Estima a tensão de ruptura do solo multiplicando a porcentagem do CBR pelo fator empírico 0,7 (kgf/cm²).

    def pressao_admissivel_plataforma_Pap(self) -> float:
                                                                            """PASSO 7 – Pressão que aceitamos aplicar no solo (com folga de segurança)."""
        return self.pressao_ruptura_solo_Pr() / self.geo.fator_seguranca    # Reduce a pressão de ruptura dividindo-a pelo fator de segurança Ns (kgf/cm²).

    def espessura_minima_lastro_h(self) -> float:
                                                            """PASSO 8 – Qual a espessura mínima de pedra? (resultado principal)"""
        pm = self.pressao_face_inferior_dormente_Pm()       # Obtém a pressão calculada na interface entre o dormente e o lastro (Pm).
        pap = self.pressao_admissivel_plataforma_Pap()      # Obtém a pressão admissível que chega ao solo de fundação (Pap).
        if pap <= 0:                                        # Checa se a pressão admissível é nula ou negativa para evitar erros de divisão por zero.
            return 0.0                                      # Retorna 0.0 para garantir a segurança da execução e evitar exceções matemáticas.

        h_polegadas = ((16.8 * pm) / pap) ** (1 / 1.25)   # Aplica a Equação de Talbot para calcular a altura de lastro em polegadas.
        h_cm = h_polegadas * 2.54                         # Converte a altura de lastro de polegadas para centímetros (1 polegada = 2,54 cm).
        return h_cm / 100                                 # Converte a altura de lastro de centímetros para metros (1 m = 100 cm).
