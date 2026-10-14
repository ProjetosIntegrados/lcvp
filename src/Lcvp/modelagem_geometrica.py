"""
PARTE 3 - MODELAGEM GEOMÉTRICA
Seção transversal, volumes e cubagem do lastro e dos dormentes.
"""
from entrada_dados import ParametrosGeometricos, ParametrosOperacionais


class SecaoTransversal:
    def __init__(self, geom: ParametrosGeometricos, op: ParametrosOperacionais, altura_lastro: float):
        self.geom = geom
        self.op = op
        self.h = altura_lastro

    def area_secao_tipo(self) -> float:
        # 1. Parte retangular superior (camada onde fica o dormente)
        b = self.geom.comp_dormente + (2 * self.geom.larg_ombro)
        area_retangulo = b * self.geom.alt_dormente

        # 2. Parte trapezoidal inferior (camada da espessura de lastro h)
        B = b + (2 * self.h * self.geom.inclinacao_talude)
        area_trapezio = ((B + b) * self.h) / 2

        # Arredondado para 2 casas decimais para equiparar ao cálculo manual
        area_total = area_retangulo + area_trapezio
        return round(area_total, 2)

    def volume_secao_tipo(self) -> float:
        return self.area_secao_tipo() * self.geom.extensao_trecho_m

    def volume_dormente_vd(self) -> float:
        vd_exato = self.geom.comp_dormente * self.geom.larg_dormente * self.geom.alt_dormente
        # Arredondado para 2 casas decimais para equiparar ao cálculo manual
        return round(vd_exato, 2)

    def qtd_dormentes_por_km(self) -> float:
        return self.geom.qtd_dormentes_km

    def volume_total_dormentes_vds(self) -> float:
        return self.qtd_dormentes_por_km() * self.volume_dormente_vd() * self.geom.extensao_trecho_km

    def volume_total_lastro_vl(self) -> float:
        return self.volume_secao_tipo() - self.volume_total_dormentes_vds()

    def volume_lastro_majorado(self) -> float:
        vl = self.volume_total_lastro_vl()
        return vl + (vl * (self.geom.fator_majoracao_perc / 100))