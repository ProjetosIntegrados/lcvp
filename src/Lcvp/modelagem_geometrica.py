"""
PARTE 3 - MODELAGEM GEOMÉTRICA
Seção transversal, volumes e cubagem do lastro e dos dormentes.
"""
from entrada_dados import ParametrosGeometricos, ParametrosOperacionais

class SecaoTransversal:
    """Calcula o tamanho da fatia (seção tipo) e a quantidade de pedra."""

    def __init__(self, geom: ParametrosGeometricos, op: ParametrosOperacionais, altura_lastro: float):
        self.geom = geom                                                      # Armazena os parâmetros geométricos no objeto da seção
        self.op = op                                                          # Armazena os parâmetros operacionais no objeto da seção
        self.h = altura_lastro                                                # Armazena a espessura do lastro calculada h (m)

    def area_secao_tipo(self) -> float:
        """Área da fatia (m²), calculada dividindo o desenho em 2 formas simples."""   # 1. Parte retangular superior (camada onde fica o dormente)
        b = self.geom.comp_dormente + (2 * self.geom.larg_ombro)                       # Calcula a largura do topo da seção somando o comprimento do dormente e duas ombreiras (m).
        area_retangulo = b * self.geom.alt_dormente                                    # Calcula a área da região retangular superior equivalente à altura do dormente (m²).
                                                                                        
                                                                           # 2. Parte trapezoidal inferior (camada da espessura de lastro h)
        B = b + (2 * self.h * self.geom.inclinacao_talude)                 # Calcula a largura da base inferior do trapézio considerando a expansão dos taludes em ambos os lados (m).
        area_trapezio = ((B + b) * self.h) / 2                             # Aplica a fórmula da área do trapézio no corpo principal da camada de lastro (m²).

        area_total = area_retangulo + area_trapezio                            # Soma a área do retângulo superior à área do trapézio inferior (m²).
        return round(area_total, 2)                                            # Retorna o valor da área total arredondado para duas casas decimais.

    def volume_secao_tipo(self) -> float:
        """Volume "bruto" da fatia ao longo de toda a ferrovia (m³)."""
        return self.area_secao_tipo() * self.geom.extensao_trecho_m            # Multiplica a área transversal da via pela sua extensão total em metros para obter o volume bruto em m³.

    def volume_dormente_vd(self) -> float:
        """Volume de UM dormente (m³) = comprimento x largura x altura."""
        vd_exato = self.geom.comp_dormente * self.geom.larg_dormente * self.geom.alt_dormente              # Multiplica comprimento, largura e altura do dormente para determinar o volume unitário em m³.
        return round(vd_exato, 2)                                                                          # Retorna o volume unitário do dormente arredondado para duas casas decimais.

    def qtd_dormentes_por_km(self) -> float:
        """Quantos dormentes há em 1 km de linha (valor informado pelo usuário)."""
        return self.geom.qtd_dormentes_km                                                                  # Retorna a densidade de dormentes especificada por quilômetro.

    def volume_total_dormentes_vds(self) -> float:
        """Volume de TODOS os dormentes do trecho (m³)."""
        return self.qtd_dormentes_por_km() * self.volume_dormente_vd() * self.geom.extensao_trecho_km      # Calcula o volume total ocupado por todos os dormentes ao longo do comprimento total em km (m³).

    def volume_total_lastro_vl(self) -> float:
        """Volume de PEDRA realmente necessário (m³)."""
        return self.volume_secao_tipo() - self.volume_total_dormentes_vds()     # Subtrai o volume ocupado pelos dormentes do volume bruto da seção para obter o volume líquido do lastro em m³.

    def volume_lastro_majorado(self) -> float:
        """Volume de pedra a COMPRAR, já com margem extra (m³)."""
        vl = self.volume_total_lastro_vl()                           # Obtém o volume líquido necessário de lastro (m³).
        return vl + (vl * (self.geom.fator_majoracao_perc / 100))    # Adiciona a porcentagem da margem de segurança/perdas ao volume líquido do lastro (m³).
