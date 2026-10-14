"""
PARTE 2 - RESOLUÇÃO DOS CÁLCULOS
Modelagem analítica da superestrutura (cargas, pressões e espessura do lastro).
"""
from entrada_dados import ParametrosOperacionais, ParametrosGeotecnicos, ParametrosGeometricos


class Superestrutura:
    def __init__(self, op: ParametrosOperacionais, geo: ParametrosGeotecnicos, geom: ParametrosGeometricos):
        self.op = op
        self.geo = geo
        self.geom = geom
        self.aviso_kv_impresso = False

    def carga_estatica_roda_P(self) -> float:
        return self.op.peso_total / self.op.num_rodas

    def carga_distribuida_dormentes_Pg(self) -> float:
        return self.carga_estatica_roda_P() * (self.op.espacamento_dormentes / self.op.dist_eixos)

    def coeficiente_dinamico_kv(self) -> float:
        kv_calculado = 1.0 + (4.5 * (self.op.velocidade ** 2) / 100000)

        if kv_calculado < 1.4:
            if not self.aviso_kv_impresso:
                print(f"\n[AVISO] O coeficiente dinâmico (kv) calculado foi {kv_calculado:.3f}. Adotando o valor mínimo: 1.400")
                self.aviso_kv_impresso = True
            return 1.4
        return kv_calculado

    def carga_de_calculo_Pv(self) -> float:
        return self.carga_distribuida_dormentes_Pg() * self.coeficiente_dinamico_kv()

    def pressao_face_inferior_dormente_Pm(self) -> float:
        area_soca = self.geom.comp_soca * self.geom.larg_dormente
        return self.carga_de_calculo_Pv() / (area_soca * 10000)

    def pressao_ruptura_solo_Pr(self) -> float:
        return self.geo.cbr * 0.7

    def pressao_admissivel_plataforma_Pap(self) -> float:
        return self.pressao_ruptura_solo_Pr() / self.geo.fator_seguranca

    def espessura_minima_lastro_h(self) -> float:
        pm = self.pressao_face_inferior_dormente_Pm()
        pap = self.pressao_admissivel_plataforma_Pap()
        if pap <= 0:
            return 0.0

        h_polegadas = ((16.8 * pm) / pap) ** (1 / 1.25)
        h_cm = h_polegadas * 2.54
        return h_cm / 100