"""
PARTE 4 - MÓDULO DE INTERFACE
Apresentação dos resultados (relatório no terminal).
"""

import builtins
import math
import sys
import typing
import tkinter as tk
from pathlib import Path
from tkinter import ttk

# Compatibilidade com interface.py em versões do Python < 3.14
builtins.Dict = typing.Dict
builtins.Any = typing.Any

# Localiza automaticamente a pasta src/Lcvp/ (funciona rodando da raiz ou de dentro de src/Lcvp/)
BASE_DIR = Path(__file__).resolve().parent
CANDIDATOS_SRC = [BASE_DIR / "src", BASE_DIR.parent, BASE_DIR]
for pasta in CANDIDATOS_SRC:
    pasta_lcvp = pasta / "Lcvp"
    if pasta_lcvp.is_dir():
        for caminho in (str(pasta_lcvp), str(pasta)):
            if caminho not in sys.path:
                sys.path.insert(0, caminho)
        break

from Lcvp.entrada_dados import (
    ParametrosOperacionais,
    ParametrosGeotecnicos,
    ParametrosGeometricos,
)
from Lcvp.calculos import Superestrutura
from Lcvp.modelagem_geometrica import SecaoTransversal

# Parte descoberta padronizada do dormente acima do topo do lastro (cm)
ALT_DESCOBERTA_CM = 5.0

PRESETS = {
    "estreita": {
        "peso_total": 90000.0,
        "num_rodas": 8,
        "velocidade": 70.0,
        "dist_eixos": 1.574,
        "espacamento_dormentes": 0.55,
        "cbr": 30.0,
        "fator_seguranca": 5.5,
        "comp_dormente": 2.00,
        "larg_dormente": 0.22,
        "alt_dormente": 0.16,
        "comp_soca": 0.60,
        "larg_ombro": 0.35,
        "inclinacao_talude": 1.5,
        "extensao_trecho_km": 350.0,
        "qtd_dormentes_km": 1820.0,
        "fator_majoracao_perc": 10.0,
        "arredondar_h": False,
    },
    "larga": {
        "peso_total": 119000.0,
        "num_rodas": 8,
        "velocidade": 70.0,
        "dist_eixos": 2.00,
        "espacamento_dormentes": 0.55,
        "cbr": 18.5,
        "fator_seguranca": 5.5,
        "comp_dormente": 2.80,
        "larg_dormente": 0.24,
        "alt_dormente": 0.17,
        "comp_soca": 0.80,
        "larg_ombro": 0.30,
        "inclinacao_talude": 1.5,
        "extensao_trecho_km": 200.0,
        "qtd_dormentes_km": 1820.0,
        "fator_majoracao_perc": 10.0,
        "arredondar_h": True,
    },
}

GRUPOS_ENTRADA = [
    ("Parâmetros Operacionais", [
        ("peso_total", "Peso total do vagão (kgf)"),
        ("num_rodas", "Número de rodas"),
        ("velocidade", "Velocidade (km/h)"),
        ("dist_eixos", "Distância entre eixos (m)"),
        ("espacamento_dormentes", "Espaçamento dormentes (m)"),
    ]),
    ("Parâmetros Geotécnicos", [
        ("cbr", "CBR da plataforma (%)"),
        ("fator_seguranca", "Fator de segurança (Ns)"),
    ]),
    ("Parâmetros Geométricos", [
        ("comp_dormente", "Comp. do dormente (m)"),
        ("larg_dormente", "Largura do dormente (m)"),
        ("alt_dormente", "Altura do dormente (m)"),
        ("comp_soca", "Largura soca 1 trilho (m)"),
        ("larg_ombro", "Largura do ombro (m)"),
        ("inclinacao_talude", "Inclinação do talude (1:x)"),
        ("extensao_trecho_km", "Extensão do trecho (km)"),
        ("qtd_dormentes_km", "Dormentes por km (und/km)"),
        ("fator_majoracao_perc", "Majoração (%)"),
    ]),
]


def fmt(valor: float, casas: int = 2) -> str:
    """Formata número no padrão brasileiro (ponto para milhar, vírgula para decimal)."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


class AppLcvp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lcvp — Dimensionamento de Lastro e Cubagem de Via Permanente")
        self.geometry("1260x840")
        self.minsize(1020, 680)
        self.configure(bg="#ffffff")

        self.vars: dict[str, tk.StringVar] = {}
        self.var_arredondar = tk.BooleanVar(value=False)
        self.cards: dict[str, tuple[tk.Label, tk.Label]] = {}
        self.ultimo_resultado: dict | None = None

        self._configurar_estilo()
        self._montar_cabecalho()
        self._montar_corpo()
        self.carregar_preset("estreita")

    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        fonte = ("Segoe UI", 9, "normal")
        estilo.configure(".", background="#ffffff", foreground="#111827", font=fonte)
        estilo.configure("TFrame", background="#ffffff")
        estilo.configure("TLabel", background="#ffffff", foreground="#111827", font=fonte)
        estilo.configure("TCheckbutton", background="#ffffff", foreground="#111827", font=fonte)
        estilo.configure("TNotebook", background="#ffffff", borderwidth=0)
        estilo.configure("TNotebook.Tab", background="#f3f4f6", foreground="#374151", padding=(12, 6), font=fonte)
        estilo.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#111827")])
        estilo.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#111827", rowheight=24, font=fonte)
        estilo.configure("Treeview.Heading", background="#f9fafb", foreground="#374151", font=fonte, relief="flat")

    def _montar_cabecalho(self):
        topo = tk.Frame(self, bg="#ffffff", padx=18, pady=12)
        topo.pack(fill="x")

        esq = tk.Frame(topo, bg="#ffffff")
        esq.pack(side="left", fill="x", expand=True)

        tk.Label(
            esq,
            text="Lcvp — Dimensionamento de Lastro e Cubagem de Via Permanente",
            bg="#ffffff", fg="#111827", font=("Segoe UI", 13, "normal"), anchor="w"
        ).pack(fill="x")

        tk.Label(
            esq,
            text="Projetos Integrados III (ENG01066) • UFRGS",
            bg="#ffffff", fg="#6b7280", font=("Segoe UI", 9, "normal"), anchor="w"
        ).pack(fill="x", pady=(2, 0))

        tk.Label(
            esq,
            text="Bruna Soldera Terres & Tainá Yumi Isse Sato • Orientação: Prof. Felipe Pinto da Motta Quevedo & Prof. Felipe Schaedler de Almeida • ENG01066 / UFRGS",
            bg="#ffffff", fg="#6b7280", font=("Segoe UI", 9, "normal"), anchor="w"
        ).pack(fill="x", pady=(1, 0))

        dir_btns = tk.Frame(topo, bg="#ffffff")
        dir_btns.pack(side="right", padx=(12, 0))

        for chave, texto in (
            ("estreita", "Exemplo 1: Bitola Estreita (350 km)"),
            ("larga", "Exemplo 2: Bitola Larga (200 km)"),
        ):
            tk.Button(
                dir_btns, text=texto, command=lambda c=chave: self.carregar_preset(c),
                bg="#f9fafb", fg="#111827", activebackground="#e5e7eb",
                relief="solid", bd=1, highlightthickness=0, padx=10, pady=5,
                font=("Segoe UI", 9, "normal"), cursor="hand2"
            ).pack(side="left", padx=(6, 0))

        tk.Frame(self, bg="#e5e7eb", height=1).pack(fill="x")

    def _montar_corpo(self):
        corpo = tk.Frame(self, bg="#ffffff")
        corpo.pack(fill="both", expand=True)

        # Barra lateral rolável (parâmetros de entrada)
        wrap_lat = tk.Frame(corpo, bg="#ffffff", width=310)
        wrap_lat.pack(side="left", fill="y")
        wrap_lat.pack_propagate(False)

        canvas_lat = tk.Canvas(wrap_lat, bg="#ffffff", highlightthickness=0)
        scroll_lat = ttk.Scrollbar(wrap_lat, orient="vertical", command=canvas_lat.yview)
        frame_lat = tk.Frame(canvas_lat, bg="#ffffff", padx=14, pady=12)

        frame_lat.bind("<Configure>", lambda e: canvas_lat.configure(scrollregion=canvas_lat.bbox("all")))
        canvas_lat.create_window((0, 0), window=frame_lat, anchor="nw", width=292)
        canvas_lat.configure(yscrollcommand=scroll_lat.set)

        canvas_lat.pack(side="left", fill="both", expand=True)
        scroll_lat.pack(side="right", fill="y")

        for titulo_grupo, campos in GRUPOS_ENTRADA:
            tk.Label(
                frame_lat, text=titulo_grupo, bg="#ffffff", fg="#374151",
                font=("Segoe UI", 10, "normal"), anchor="w"
            ).pack(fill="x", pady=(8, 4))
            tk.Frame(frame_lat, bg="#e5e7eb", height=1).pack(fill="x", pady=(0, 6))

            for chave, rotulo in campos:
                linha = tk.Frame(frame_lat, bg="#ffffff")
                linha.pack(fill="x", pady=2)
                tk.Label(
                    linha, text=rotulo, bg="#ffffff", fg="#374151",
                    font=("Segoe UI", 9, "normal"), anchor="w"
                ).pack(side="left")

                var = tk.StringVar()
                var.trace_add("write", lambda *_: self.atualizar())
                self.vars[chave] = var

                tk.Entry(
                    linha, textvariable=var, width=11, justify="right",
                    bg="#ffffff", fg="#111827", relief="solid", bd=1,
                    font=("Segoe UI", 9, "normal")
                ).pack(side="right")

        tk.Label(
            frame_lat, text="Opções de Projeto", bg="#ffffff", fg="#374151",
            font=("Segoe UI", 10, "normal"), anchor="w"
        ).pack(fill="x", pady=(12, 4))
        tk.Frame(frame_lat, bg="#e5e7eb", height=1).pack(fill="x", pady=(0, 6))

        ttk.Checkbutton(
            frame_lat,
            text="Arredondamento construtivo de h (cm acima)",
            variable=self.var_arredondar,
            command=self.atualizar,
        ).pack(anchor="w", pady=(2, 8))

        self.lbl_erro = tk.Label(
            frame_lat, text="", bg="#ffffff", fg="#6b7280",
            font=("Segoe UI", 8, "normal"), wraplength=260, justify="left"
        )
        self.lbl_erro.pack(fill="x", pady=(4, 0))

        tk.Frame(corpo, bg="#e5e7eb", width=1).pack(side="left", fill="y")

        # Painel principal à direita
        painel = tk.Frame(corpo, bg="#ffffff", padx=16, pady=12)
        painel.pack(side="left", fill="both", expand=True)

        # 4 cartões de resumo
        linha_cards = tk.Frame(painel, bg="#ffffff")
        linha_cards.pack(fill="x", pady=(0, 10))
        for i, (chave, titulo) in enumerate([
            ("h", "Espessura de Lastro (h)"),
            ("area", "Área da Seção Tipo"),
            ("vl", "Volume Líquido (VL)"),
            ("vl_maj", "Volume Majorado (VL_maj)"),
        ]):
            card = tk.Frame(linha_cards, bg="#ffffff", highlightbackground="#d1d5db", highlightthickness=1, padx=10, pady=8)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))
            linha_cards.columnconfigure(i, weight=1)

            tk.Label(card, text=titulo, bg="#ffffff", fg="#6b7280", font=("Segoe UI", 8, "normal"), anchor="w").pack(fill="x")
            lbl_val = tk.Label(card, text="-", bg="#ffffff", fg="#111827", font=("Segoe UI", 13, "normal"), anchor="w")
            lbl_val.pack(fill="x", pady=(2, 0))
            lbl_sub = tk.Label(card, text="", bg="#ffffff", fg="#6b7280", font=("Segoe UI", 8, "normal"), anchor="w")
            lbl_sub.pack(fill="x")
            self.cards[chave] = (lbl_val, lbl_sub)

        # Aviso normativo de kv (exibido quando kv calculado < 1.400)
        self.box_aviso_kv = tk.Frame(painel, bg="#f9fafb", highlightbackground="#d1d5db", highlightthickness=1, padx=10, pady=6)
        self.lbl_aviso_kv = tk.Label(
            self.box_aviso_kv, text="", bg="#f9fafb", fg="#374151",
            font=("Segoe UI", 9, "normal"), anchor="w"
        )
        self.lbl_aviso_kv.pack(fill="x")

        # Quadro da Representação da Seção Tipo
        self.box_svg = tk.Frame(painel, bg="#ffffff", highlightbackground="#d1d5db", highlightthickness=1, padx=10, pady=8)
        self.box_svg.pack(fill="x", pady=(0, 10))

        tk.Label(
            self.box_svg, text="Representação da Seção Tipo", bg="#ffffff", fg="#111827",
            font=("Segoe UI", 10, "normal"), anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.canvas_secao = tk.Canvas(self.box_svg, bg="#ffffff", height=250, highlightthickness=0)
        self.canvas_secao.pack(fill="x")
        self.canvas_secao.bind("<Configure>", lambda e: self._desenhar_secao())

        # Abas: Relatório Executivo e Memória de Cálculo
        abas = ttk.Notebook(painel)
        abas.pack(fill="both", expand=True)

        aba_rel = tk.Frame(abas, bg="#ffffff", pady=6)
        abas.add(aba_rel, text="Relatório Executivo")

        self.tree = ttk.Treeview(aba_rel, columns=("parametro", "valor"), show="headings")
        self.tree.heading("parametro", text="Parâmetro", anchor="w")
        self.tree.heading("valor", text="Valor", anchor="e")
        self.tree.column("parametro", anchor="w", width=520)
        self.tree.column("valor", anchor="e", width=220)
        self.tree.tag_configure("secao", background="#f3f4f6", foreground="#374151")

        scroll_tree = ttk.Scrollbar(aba_rel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_tree.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll_tree.pack(side="right", fill="y")

        aba_mem = tk.Frame(abas, bg="#ffffff", pady=6)
        abas.add(aba_mem, text="Memória de Cálculo (8 Passos de Talbot)")

        self.txt_memoria = tk.Text(
            aba_mem, bg="#ffffff", fg="#111827", relief="flat", wrap="word",
            font=("Consolas", 9, "normal"), padx=10, pady=8
        )
        scroll_mem = ttk.Scrollbar(aba_mem, orient="vertical", command=self.txt_memoria.yview)
        self.txt_memoria.configure(yscrollcommand=scroll_mem.set)
        self.txt_memoria.pack(side="left", fill="both", expand=True)
        scroll_mem.pack(side="right", fill="y")

    def carregar_preset(self, chave: str):
        dados = PRESETS[chave]
        for k, v in dados.items():
            if k == "arredondar_h":
                self.var_arredondar.set(bool(v))
            elif k in self.vars:
                self.vars[k].set(str(v))
        self.atualizar()

    def _ler_entradas(self) -> dict | None:
        try:
            valores = {k: float(v.get().replace(",", ".")) for k, v in self.vars.items()}
            valores["num_rodas"] = int(valores["num_rodas"])
            valores["arredondar_h"] = self.var_arredondar.get()
        except ValueError:
            self.lbl_erro.config(text="Preencha todos os campos com valores numéricos válidos.")
            return None

        if valores["num_rodas"] <= 0 or valores["dist_eixos"] <= 0 or valores["fator_seguranca"] <= 0:
            self.lbl_erro.config(text="Rodas, distância entre eixos e Ns devem ser maiores que zero.")
            return None

        self.lbl_erro.config(text="")
        return valores

    def atualizar(self):
        p = self._ler_entradas()
        if p is None:
            return

        # Altura enterrada do dormente descontando os 5 cm descobertos padronizados
        alt_desc_m = ALT_DESCOBERTA_CM / 100.0
        alt_enterrada_m = max(0.0, p["alt_dormente"] - alt_desc_m)

        # Instanciação direta das classes oficiais de src/Lcvp/
        op = ParametrosOperacionais(
            peso_total=p["peso_total"],
            num_rodas=p["num_rodas"],
            velocidade=p["velocidade"],
            dist_eixos=p["dist_eixos"],
            espacamento_dormentes=p["espacamento_dormentes"],
        )
        geo = ParametrosGeotecnicos(
            cbr=p["cbr"],
            fator_seguranca=p["fator_seguranca"],
        )
        geom = ParametrosGeometricos(
            comp_dormente=p["comp_dormente"],
            larg_dormente=p["larg_dormente"],
            alt_dormente=alt_enterrada_m,
            comp_soca=p["comp_soca"],
            larg_ombro=p["larg_ombro"],
            inclinacao_talude=p["inclinacao_talude"],
            extensao_trecho_m=p["extensao_trecho_km"] * 1000.0,
            extensao_trecho_km=p["extensao_trecho_km"],
            fator_majoracao_perc=p["fator_majoracao_perc"],
            qtd_dormentes_km=p["qtd_dormentes_km"],
        )

        sup = Superestrutura(op, geo, geom)
        P = sup.carga_estatica_roda_P()
        Pg = sup.carga_distribuida_dormentes_Pg()
        kv_calc = 1.0 + (4.5 * (p["velocidade"] ** 2)) / 100000.0
        kv = sup.coeficiente_dinamico_kv()
        Pv = sup.carga_de_calculo_Pv()
        Pm = sup.pressao_face_inferior_dormente_Pm()
        Pr = sup.pressao_ruptura_solo_Pr()
        Pap = sup.pressao_admissivel_plataforma_Pap()
        h_exato = sup.espessura_minima_lastro_h()

        h_projeto = (math.ceil(h_exato * 100.0) / 100.0) if p["arredondar_h"] else h_exato

        sec = SecaoTransversal(geom, op, altura_lastro=h_projeto)
        area_secao = sec.area_secao_tipo()
        vol_secao = sec.volume_secao_tipo()
        Vd = sec.volume_dormente_vd()
        qtd_dorm_km = sec.qtd_dormentes_por_km()
        Vds = sec.volume_total_dormentes_vds()
        VL = sec.volume_total_lastro_vl()
        VL_maj = sec.volume_lastro_majorado()

        b = p["comp_dormente"] + 2.0 * p["larg_ombro"]
        B = b + 2.0 * h_projeto * p["inclinacao_talude"]

        self.ultimo_resultado = {
            "p": p,
            "P": P, "Pg": Pg, "kv_calc": kv_calc, "kv": kv, "Pv": Pv, "s": geom.comp_soca,
            "Pm": Pm, "Pr": Pr, "Pap": Pap,
            "h_exato": h_exato, "h_projeto": h_projeto,
            "alt_enterrada_m": alt_enterrada_m, "alt_desc_m": alt_desc_m,
            "b": b, "B": B,
            "area_secao": area_secao, "vol_secao": vol_secao,
            "Vd": Vd, "qtd_dorm_km": qtd_dorm_km,
            "Vds": Vds, "VL": VL, "VL_maj": VL_maj,
        }

        self._atualizar_cards()
        self._atualizar_aviso_kv()
        self._atualizar_relatorio()
        self._atualizar_memoria()
        self._desenhar_secao()

    def _atualizar_aviso_kv(self):
        r = self.ultimo_resultado
        if r["kv_calc"] < 1.4:
            self.lbl_aviso_kv.config(
                text=f"[AVISO] Coeficiente dinâmico (kv) calculado foi {r['kv_calc']:.3f}. Adotado o mínimo normativo: 1.400."
            )
            if not self.box_aviso_kv.winfo_ismapped():
                self.box_aviso_kv.pack(fill="x", pady=(0, 10), before=self.box_svg)
        else:
            if self.box_aviso_kv.winfo_ismapped():
                self.box_aviso_kv.pack_forget()

    def _atualizar_cards(self):
        r = self.ultimo_resultado
        sub_h = f"Exato: {fmt(r['h_exato'] * 100, 3)} cm" if r["p"]["arredondar_h"] else f"{fmt(r['h_projeto'], 4)} m"
        self.cards["h"][0].config(text=f"{fmt(r['h_projeto'] * 100, 2)} cm")
        self.cards["h"][1].config(text=sub_h)

        self.cards["area"][0].config(text=f"{fmt(r['area_secao'], 2)} m²")
        self.cards["area"][1].config(text=f"b = {fmt(r['b'], 2)} m | B = {fmt(r['B'], 3)} m")

        self.cards["vl"][0].config(text=f"{fmt(r['VL'], 2)} m³")
        self.cards["vl"][1].config(text=f"Trecho de {fmt(r['p']['extensao_trecho_km'], 0)} km")

        self.cards["vl_maj"][0].config(text=f"{fmt(r['VL_maj'], 2)} m³")
        self.cards["vl_maj"][1].config(text=f"Majoração de +{fmt(r['p']['fator_majoracao_perc'], 0)}%")

    def _atualizar_relatorio(self):
        r = self.ultimo_resultado
        for item in self.tree.get_children():
            self.tree.delete(item)

        blocos = [
            ("[PARÂMETROS DE CARGA]", [
                ("Carga em uma roda (P)", f"{fmt(r['P'], 3)} kgf"),
                ("Carga em grupo de dormentes (Pg)", f"{fmt(r['Pg'], 3)} kgf"),
                ("Coeficiente dinâmico (kv)", f"{fmt(r['kv'], 3)}"),
                ("Carga de cálculo (Pv)", f"{fmt(r['Pv'], 3)} kgf"),
                ("Largura efetiva da soca sob um trilho (s)", f"{fmt(r['s'], 2)} m"),
            ]),
            ("[DIMENSIONAMENTO ESTRUTURAL]", [
                ("Pressão na face inferior do dormente (Pm)", f"{fmt(r['Pm'], 3)} kgf/cm²"),
                ("Pressão de ruptura do solo (Pr)", f"{fmt(r['Pr'], 3)} kgf/cm²"),
                ("Pressão admissível na Plataforma (Pap)", f"{fmt(r['Pap'], 3)} kgf/cm²"),
                ("Altura da camada de lastro (h) exata", f"> {fmt(r['h_exato'] * 100, 3)} cm"),
            ]),
            ("[QUANTITATIVOS E CUBAGEM]", [
                ("Área da Seção Tipo", f"{fmt(r['area_secao'], 2)} m²"),
                ("Volume da Seção Tipo", f"{fmt(r['vol_secao'], 2)} m³"),
                ("Volume do dormente (Vd)", f"{fmt(r['Vd'], 2)} m³"),
                ("Qtd. Dormentes por km (inserida)", f"{fmt(r['qtd_dorm_km'], 0)} und/km"),
                ("Volume total de dormentes (Vds)", f"{fmt(r['Vds'], 2)} m³"),
                ("Volume total do lastro (VL)", f"{fmt(r['VL'], 2)} m³"),
                ("Volume total do lastro Majorado", f"{fmt(r['VL_maj'], 2)} m³"),
            ]),
        ]

        for titulo, linhas in blocos:
            self.tree.insert("", "end", values=(titulo, ""), tags=("secao",))
            for nome, valor in linhas:
                self.tree.insert("", "end", values=(nome, valor))

    def _atualizar_memoria(self):
        r = self.ultimo_resultado
        p = r["p"]
        kv_calc = r["kv_calc"]
        obs_kv = " (adotado mínimo normativo 1,400)" if kv_calc < 1.4 else ""
        h_pol = (r["h_exato"] * 100.0) / 2.54

        linhas = [
            "MEMÓRIA DE CÁLCULO — 8 PASSOS DE TALBOT (src/Lcvp/calculos.py)",
            "-" * 74,
            f"1. Carga estática por roda (P) = {fmt(p['peso_total'], 0)} / {p['num_rodas']} = {fmt(r['P'], 3)} kgf",
            f"2. Carga no dormente (Pg)      = {fmt(r['P'], 3)} * ({fmt(p['espacamento_dormentes'], 2)} / {fmt(p['dist_eixos'], 3)}) = {fmt(r['Pg'], 3)} kgf",
            f"3. Coeficiente dinâmico (kv)   = 1 + (4,5 * {fmt(p['velocidade'], 1)}² / 100000) = {fmt(kv_calc, 4)} -> {fmt(r['kv'], 3)}{obs_kv}",
            f"4. Carga de cálculo (Pv)       = {fmt(r['Pg'], 3)} * {fmt(r['kv'], 3)} = {fmt(r['Pv'], 3)} kgf",
            f"5. Pressão no dormente (Pm)    = {fmt(r['Pv'], 3)} / ({fmt(p['comp_soca'], 2)} * {fmt(p['larg_dormente'], 2)} * 10000) = {fmt(r['Pm'], 3)} kgf/cm²",
            f"6. Pressão de ruptura (Pr)     = 0,7 * {fmt(p['cbr'], 1)} = {fmt(r['Pr'], 3)} kgf/cm²",
            f"7. Pressão admissível (Pap)    = {fmt(r['Pr'], 3)} / {fmt(p['fator_seguranca'], 2)} = {fmt(r['Pap'], 3)} kgf/cm²",
            f"8. Espessura Talbot (h)        = ((16,8 * {fmt(r['Pm'], 3)}) / {fmt(r['Pap'], 3)})^(1/1,25) = {fmt(h_pol, 3)} pol = {fmt(r['h_exato'] * 100, 3)} cm",
            "",
            "MODELAGEM GEOMÉTRICA E CUBAGEM (src/Lcvp/modelagem_geometrica.py)",
            "-" * 74,
            f"   Largura superior (b)        = {fmt(p['comp_dormente'], 2)} + 2 * {fmt(p['larg_ombro'], 2)} = {fmt(r['b'], 2)} m",
            f"   Base inferior (B)           = {fmt(r['b'], 2)} + 2 * {fmt(r['h_projeto'], 4)} * {fmt(p['inclinacao_talude'], 2)} = {fmt(r['B'], 3)} m",
            f"   Dormente enterrado          = {fmt(p['alt_dormente'] * 100, 1)} - {fmt(ALT_DESCOBERTA_CM, 1)} = {fmt(r['alt_enterrada_m'] * 100, 1)} cm",
            f"   Área da seção tipo          = {fmt(r['area_secao'], 2)} m²",
            f"   Volume da seção tipo        = {fmt(r['vol_secao'], 2)} m³",
            f"   Volume unitário dormente Vd = {fmt(r['Vd'], 2)} m³",
            f"   Volume total dormentes Vds  = {fmt(r['Vds'], 2)} m³",
            f"   Volume líquido lastro (VL)  = {fmt(r['VL'], 2)} m³",
            f"   Volume majorado (VL_maj)    = {fmt(r['VL_maj'], 2)} m³",
        ]

        self.txt_memoria.config(state="normal")
        self.txt_memoria.delete("1.0", "end")
        self.txt_memoria.insert("1.0", "\n".join(linhas))
        self.txt_memoria.config(state="disabled")

    def _desenhar_secao(self):
        c = self.canvas_secao
        c.delete("all")
        if not self.ultimo_resultado:
            return

        r = self.ultimo_resultado
        p = r["p"]
        w = max(c.winfo_width(), 720)
        h_cv = max(c.winfo_height(), 250)

        b, B = r["b"], r["B"]
        h_lastro = max(r["h_projeto"], 0.05)
        alt_ent = r["alt_enterrada_m"]
        alt_tot = p["alt_dormente"]
        y_topo_lastro = h_lastro + alt_ent
        y_topo_dorm = h_lastro + alt_tot

        larg_plat = B + 0.9
        escala_x = (w - 190) / max(larg_plat, 3.0)
        escala_y = (h_cv - 110) / max(y_topo_dorm + 0.25, 0.7)
        esc = min(escala_x, escala_y)

        cx = w / 2.0 - 10
        cy_base = h_cv - 54

        def px(x_m: float) -> float:
            return cx + x_m * esc

        def py(y_m: float) -> float:
            return cy_base - y_m * esc

        fonte = ("Segoe UI", 8, "normal")

        # 1. Plataforma / Sublastro (verde)
        c.create_rectangle(
            px(-larg_plat / 2), py(0), px(larg_plat / 2), py(-0.14),
            fill="#d1fae5", outline="#059669", width=1.5
        )
        c.create_line(px(-larg_plat / 2 - 0.15), py(0), px(larg_plat / 2 + 0.15), py(0), fill="#059669", width=2)
        c.create_text(
            px(0), py(-0.07),
            text=f"PLATAFORMA / SUBLASTRO (CBR = {fmt(p['cbr'], 1)}% | Pap = {fmt(r['Pap'], 2)} kgf/cm²)",
            fill="#065f46", font=fonte
        )

        # 2. Lastro (trapézio contínuo com talude em linha roxa)
        c.create_polygon(
            px(-B / 2), py(0),
            px(B / 2), py(0),
            px(b / 2), py(y_topo_lastro),
            px(-b / 2), py(y_topo_lastro),
            fill="#e2e8f0", outline="#64748b", width=1.2
        )
        c.create_line(px(-b / 2), py(y_topo_lastro), px(-B / 2), py(0), fill="#7c3aed", width=2.4)
        c.create_line(px(b / 2), py(y_topo_lastro), px(B / 2), py(0), fill="#7c3aed", width=2.4)

        # Linha tracejada na base do dormente (y = h)
        c.create_line(px(-b / 2), py(h_lastro), px(b / 2), py(h_lastro), fill="#64748b", dash=(4, 3))

        # 3. Faixas de soca sob os trilhos e trilhos
        x_trilho = min(p["comp_dormente"] * 0.25, 0.55)
        larg_soca_trilho = p["comp_soca"] / 2.0
        for sinal in (-1, 1):
            xc = sinal * x_trilho
            c.create_rectangle(
                px(xc - larg_soca_trilho / 2), py(h_lastro),
                px(xc + larg_soca_trilho / 2), py(0),
                fill="#fef08a", outline="#ca8a04", dash=(3, 2), width=1.2
            )
            c.create_rectangle(px(xc - 0.055), py(y_topo_dorm + 0.025), px(xc + 0.055), py(y_topo_dorm), fill="#64748b", outline="#334155")
            c.create_rectangle(px(xc - 0.015), py(y_topo_dorm + 0.075), px(xc + 0.015), py(y_topo_dorm + 0.025), fill="#94a3b8", outline="#334155")
            c.create_rectangle(px(xc - 0.038), py(y_topo_dorm + 0.105), px(xc + 0.038), py(y_topo_dorm + 0.075), fill="#cbd5e1", outline="#334155")

        # 4. Dormente (com 5 cm descobertos acima do topo do lastro)
        c.create_rectangle(
            px(-p["comp_dormente"] / 2), py(y_topo_dorm),
            px(p["comp_dormente"] / 2), py(h_lastro),
            fill="#92400e", outline="#78350f", width=1.6
        )

        # 5. Cotas horizontais
        def cota_h(x1: float, x2: float, y_px: float, texto: str, cor: str, acima: bool = True):
            c.create_line(x1, y_px, x2, y_px, fill=cor, arrow=tk.BOTH, width=1.2)
            dy = -10 if acima else 11
            c.create_text((x1 + x2) / 2, y_px + dy, text=texto, fill=cor, font=fonte)

        cota_h(px(-b / 2), px(b / 2), py(y_topo_dorm) - 34, f"Largura Superior b = {fmt(b, 2)} m", "#0284c7", acima=True)
        cota_h(px(-p["comp_dormente"] / 2), px(p["comp_dormente"] / 2), py(y_topo_dorm) - 16, f"Dormente = {fmt(p['comp_dormente'], 2)} m", "#b45309", acima=True)
        cota_h(px(-b / 2), px(-p["comp_dormente"] / 2), py(y_topo_lastro) - 10, f"Ombro {fmt(p['larg_ombro'] * 100, 0)} cm", "#0284c7", acima=True)
        cota_h(px(-B / 2), px(B / 2), py(-0.14) + 18, f"Base Inferior do Lastro B = {fmt(B, 3)} m", "#b45309", acima=False)

        # 6. Indicação do talude APENAS no lado esquerdo
        c.create_text(
            px((-b / 2 - B / 2) / 2) - 42, py(y_topo_lastro / 2),
            text=f"Talude 1 : {fmt(p['inclinacao_talude'], 1)}",
            fill="#7c3aed", font=fonte, anchor="e"
        )

        # 7. Cotas verticais na lateral direita (descoberto 5 cm, enterrado e h)
        x_dir = px(B / 2) + 18
        c.create_line(x_dir, py(y_topo_dorm), x_dir, py(y_topo_lastro), fill="#b45309", arrow=tk.BOTH, width=1.1)
        c.create_text(x_dir + 6, (py(y_topo_dorm) + py(y_topo_lastro)) / 2, text=f"desc. = {fmt(ALT_DESCOBERTA_CM, 0)} cm", fill="#b45309", font=fonte, anchor="w")

        c.create_line(x_dir, py(y_topo_lastro), x_dir, py(h_lastro), fill="#0284c7", arrow=tk.BOTH, width=1.1)
        c.create_text(x_dir + 6, (py(y_topo_lastro) + py(h_lastro)) / 2, text=f"ent. = {fmt(alt_ent * 100, 0)} cm", fill="#0284c7", font=fonte, anchor="w")

        c.create_line(x_dir, py(h_lastro), x_dir, py(0), fill="#7c3aed", arrow=tk.BOTH, width=1.2)
        c.create_text(x_dir + 6, (py(h_lastro) + py(0)) / 2, text=f"h = {fmt(h_lastro * 100, 2)} cm", fill="#7c3aed", font=fonte, anchor="w")


if __name__ == "__main__":
    app = AppLcvp()
    app.mainloop()
