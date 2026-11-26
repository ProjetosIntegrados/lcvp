"""
PARTE 4 - MÓDULO DE INTERFACE
Apresentação dos resultados (relatório no terminal).
"""
import math
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

# Configura o caminho para importar diretamente de src/Lcvp/
RAIZ_PROJETO = Path(__file__).resolve().parent
DIR_LCVP = RAIZ_PROJETO / "src" / "Lcvp"
if str(DIR_LCVP) not in sys.path:
    sys.path.insert(0, str(DIR_LCVP))
if str(RAIZ_PROJETO / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from Lcvp.calculos import Superestrutura
from Lcvp.entrada_dados import (
    ParametrosGeometricos,
    ParametrosGeotecnicos,
    ParametrosOperacionais,
)
from Lcvp.modelagem_geometrica import SecaoTransversal

# Altura descoberta do dormente padronizada em 5 cm
ALT_DESCOBERTA_CM = 5.0

PRESETS = {
    "estreita": {
        "peso_total": 90000.0,
        "num_rodas": 8,
        "velocidade": 70.0,
        "dist_eixos": 1.574,
        "espacamento_cm": 55.0,
        "cbr": 30.0,
        "fator_seguranca": 5.5,
        "comp_dormente": 2.00,
        "larg_dormente": 0.22,
        "alt_dormente_total": 0.16,
        "comp_soca": 0.60,
        "larg_ombro": 0.35,
        "inclinacao_talude": 1.5,
        "extensao_km": 350.0,
        "qtd_dormentes_km": 1820.0,
        "fator_majoracao": 10.0,
        "arredondar_h": False,
    },
    "larga": {
        "peso_total": 119000.0,
        "num_rodas": 8,
        "velocidade": 70.0,
        "dist_eixos": 2.00,
        "espacamento_cm": 55.0,
        "cbr": 18.5,
        "fator_seguranca": 5.5,
        "comp_dormente": 2.80,
        "larg_dormente": 0.24,
        "alt_dormente_total": 0.17,
        "comp_soca": 0.80,
        "larg_ombro": 0.30,
        "inclinacao_talude": 1.5,
        "extensao_km": 200.0,
        "qtd_dormentes_km": 1820.0,
        "fator_majoracao": 10.0,
        "arredondar_h": True,
    },
}

CAMPOS = [
    ("Parâmetros Operacionais", [
        ("peso_total", "Peso total do vagão (kgf)"),
        ("num_rodas", "Número de rodas"),
        ("velocidade", "Velocidade (km/h)"),
        ("dist_eixos", "Distância entre eixos (m)"),
        ("espacamento_cm", "Espaçamento dormentes (cm)"),
    ]),
    ("Parâmetros Geotécnicos", [
        ("cbr", "CBR da plataforma (%)"),
        ("fator_seguranca", "Fator de segurança (Ns)"),
    ]),
    ("Parâmetros Geométricos", [
        ("comp_dormente", "Comp. do dormente (m)"),
        ("larg_dormente", "Larg. do dormente (m)"),
        ("alt_dormente_total", "Alt. total do dormente (m)"),
        ("comp_soca", "Larg. efetiva da soca (m)"),
        ("larg_ombro", "Largura do ombro (m)"),
        ("inclinacao_talude", "Talude (1 : X)"),
        ("extensao_km", "Extensão do trecho (km)"),
        ("qtd_dormentes_km", "Dormentes por km"),
        ("fator_majoracao", "Majoração (%)"),
    ]),
]


def fmt(valor: float, casas: int = 2) -> str:
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


class AppLcvp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lcvp — Dimensionamento de Lastro e Cubagem")
        self.geometry("1220x780")
        self.configure(bg="#ffffff")

        self.fonte = ("Segoe UI", 9)
        self.fonte_peq = ("Segoe UI", 8)
        self.fonte_tit = ("Segoe UI", 10)
        self.vars: dict[str, tk.StringVar] = {}
        self.arredondar_h = tk.BooleanVar(value=False)

        self._configurar_estilo()
        self._montar_layout()
        self.carregar_preset("estreita")

    def _configurar_estilo(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background="#ffffff", foreground="#111827", font=self.fonte)
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#111827", font=self.fonte)
        style.configure("TButton", background="#f3f4f6", foreground="#111827", bordercolor="#d1d5db", padding=(10, 5))
        style.map("TButton", background=[("active", "#e5e7eb")])
        style.configure("TNotebook", background="#ffffff", borderwidth=0)
        style.configure("TNotebook.Tab", background="#f9fafb", foreground="#374151", padding=(12, 6), font=self.fonte)
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#111827")])
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#111827", rowheight=23, font=self.fonte)
        style.configure("Treeview.Heading", background="#f3f4f6", foreground="#111827", font=self.fonte)

    def _montar_layout(self):
        # Barra superior apenas com os botões dos exemplos
        topo = tk.Frame(self, bg="#ffffff", pady=8, padx=14)
        topo.pack(fill="x")
        ttk.Button(topo, text="Exemplo 1: Bitola Estreita (350 km)", command=lambda: self.carregar_preset("estreita")).pack(side="left", padx=(0, 8))
        ttk.Button(topo, text="Exemplo 2: Bitola Larga (200 km)", command=lambda: self.carregar_preset("larga")).pack(side="left")
        tk.Frame(self, bg="#e5e7eb", height=1).pack(fill="x")

        corpo = tk.Frame(self, bg="#ffffff")
        corpo.pack(fill="both", expand=True)

        # Barra lateral esquerda com rolagem
        esq_container = tk.Frame(corpo, bg="#ffffff", width=310)
        esq_container.pack(side="left", fill="y")
        esq_container.pack_propagate(False)

        canvas_esq = tk.Canvas(esq_container, bg="#ffffff", highlightthickness=0)
        scroll_esq = ttk.Scrollbar(esq_container, orient="vertical", command=canvas_esq.yview)
        self.frame_inputs = tk.Frame(canvas_esq, bg="#ffffff", padx=14, pady=10)
        self.frame_inputs.bind("<Configure>", lambda e: canvas_esq.configure(scrollregion=canvas_esq.bbox("all")))
        canvas_esq.create_window((0, 0), window=self.frame_inputs, anchor="nw", width=290)
        canvas_esq.configure(yscrollcommand=scroll_esq.set)
        canvas_esq.pack(side="left", fill="both", expand=True)
        scroll_esq.pack(side="right", fill="y")

        for titulo, lista in CAMPOS:
            tk.Label(self.frame_inputs, text=titulo, bg="#ffffff", fg="#374151", font=self.fonte_tit).pack(anchor="w", pady=(8, 4))
            for chave, rotulo in lista:
                linha = tk.Frame(self.frame_inputs, bg="#ffffff")
                linha.pack(fill="x", pady=2)
                tk.Label(linha, text=rotulo, bg="#ffffff", fg="#4b5563", font=self.fonte_peq).pack(side="left")
                var = tk.StringVar()
                var.trace_add("write", lambda *_: self.atualizar())
                self.vars[chave] = var
                ent = tk.Entry(linha, textvariable=var, width=10, justify="right", bg="#ffffff", fg="#111827", relief="solid", bd=1, font=self.fonte)
                ent.pack(side="right")

        # Opção de arredondamento construtivo
        tk.Label(self.frame_inputs, text="Opções de Projeto", bg="#ffffff", fg="#374151", font=self.fonte_tit).pack(anchor="w", pady=(10, 4))
        tk.Checkbutton(
            self.frame_inputs,
            text="Arredondar h para cm inteiro acima",
            variable=self.arredondar_h,
            command=self.atualizar,
            bg="#ffffff",
            activebackground="#ffffff",
            fg="#111827",
            font=self.fonte_peq,
        ).pack(anchor="w")

        self.lbl_erro = tk.Label(self.frame_inputs, text="", bg="#ffffff", fg="#b91c1c", font=self.fonte_peq, wraplength=260, justify="left")
        self.lbl_erro.pack(anchor="w", pady=(8, 0))

        tk.Frame(corpo, bg="#e5e7eb", width=1).pack(side="left", fill="y")

        # Área direita (cartões + desenho + abas)
        dir_frame = tk.Frame(corpo, bg="#ffffff", padx=16, pady=12)
        dir_frame.pack(side="left", fill="both", expand=True)

        # 4 cartões de resumo
        cards_frame = tk.Frame(dir_frame, bg="#ffffff")
        cards_frame.pack(fill="x", pady=(0, 10))
        self.card_vals = {}
        for i, (chave, titulo) in enumerate([
            ("h", "Espessura do Lastro (h)"),
            ("area", "Área da Seção Tipo"),
            ("vl", "Volume Líquido (VL)"),
            ("vl_maj", "Volume Majorado (VL_maj)"),
        ]):
            card = tk.Frame(cards_frame, bg="#ffffff", highlightbackground="#d1d5db", highlightthickness=1, padx=10, pady=8)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0))
            cards_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=titulo, bg="#ffffff", fg="#6b7280", font=self.fonte_peq).pack(anchor="w")
            lbl = tk.Label(card, text="—", bg="#ffffff", fg="#111827", font=("Segoe UI", 12))
            lbl.pack(anchor="w", pady=(2, 0))
            self.card_vals[chave] = lbl

        # Desenho da Seção Transversal
        sec_box = tk.Frame(dir_frame, bg="#ffffff", highlightbackground="#d1d5db", highlightthickness=1, padx=8, pady=6)
        sec_box.pack(fill="x", pady=(0, 10))
        tk.Label(sec_box, text="Representação da Seção Tipo", bg="#ffffff", fg="#374151", font=self.fonte_tit).pack(anchor="w")
        self.canvas_sec = tk.Canvas(sec_box, bg="#ffffff", height=250, highlightthickness=0)
        self.canvas_sec.pack(fill="x", pady=(4, 0))
        self.canvas_sec.bind("<Configure>", lambda e: self.atualizar())

        # Abas: Relatório Executivo e Memória de Cálculo
        abas = ttk.Notebook(dir_frame)
        abas.pack(fill="both", expand=True)

        aba_rel = ttk.Frame(abas)
        abas.add(aba_rel, text="Relatório Executivo")
        self.tree = ttk.Treeview(aba_rel, columns=("param", "valor"), show="headings")
        self.tree.heading("param", text="Parâmetro", anchor="w")
        self.tree.heading("valor", text="Valor", anchor="e")
        self.tree.column("param", anchor="w", width=420)
        self.tree.column("valor", anchor="e", width=180)
        scroll_rel = ttk.Scrollbar(aba_rel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_rel.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll_rel.pack(side="right", fill="y")

        aba_mem = ttk.Frame(abas)
        abas.add(aba_mem, text="Memória de Cálculo (8 Passos de Talbot)")
        self.txt_mem = tk.Text(aba_mem, bg="#ffffff", fg="#111827", font=("Consolas", 9), relief="flat", padx=10, pady=8)
        scroll_mem = ttk.Scrollbar(aba_mem, orient="vertical", command=self.txt_mem.yview)
        self.txt_mem.configure(yscrollcommand=scroll_mem.set)
        self.txt_mem.pack(side="left", fill="both", expand=True)
        scroll_mem.pack(side="right", fill="y")

    def carregar_preset(self, nome: str):
        dados = PRESETS[nome]
        for chave, var in self.vars.items():
            var.set(str(dados[chave]))
        self.arredondar_h.set(dados["arredondar_h"])
        self.atualizar()

    def _ler_parametros(self):
        p = {k: float(v.get().replace(",", ".")) for k, v in self.vars.items()}
        if p["num_rodas"] <= 0 or p["dist_eixos"] <= 0 or p["fator_seguranca"] <= 0 or p["comp_soca"] <= 0 or p["larg_dormente"] <= 0:
            raise ValueError("Verifique os parâmetros: valores divisores devem ser maiores que zero.")
        return p

    def atualizar(self):
        try:
            p = self._ler_parametros()
            self.lbl_erro.config(text="")
        except ValueError as err:
            self.lbl_erro.config(text=str(err))
            return

        alt_desc_m = ALT_DESCOBERTA_CM / 100.0
        alt_enterrada_m = max(0.01, p["alt_dormente_total"] - alt_desc_m)

        # Instancia as classes reais de src/Lcvp/
        op = ParametrosOperacionais(
            peso_total=p["peso_total"],
            num_rodas=int(p["num_rodas"]),
            velocidade=p["velocidade"],
            dist_eixos=p["dist_eixos"],
            espacamento_dormentes=p["espacamento_cm"] / 100.0,
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
            extensao_trecho_m=p["extensao_km"] * 1000.0,
            extensao_trecho_km=p["extensao_km"],
            fator_majoracao_perc=p["fator_majoracao"],
            qtd_dormentes_km=p["qtd_dormentes_km"],
        )

        sup = Superestrutura(op, geo, geom)
        P = sup.carga_estatica_roda_P()
        Pg = sup.carga_distribuida_dormentes_Pg()
        kv = sup.coeficiente_dinamico_kv()
        Pv = sup.carga_de_calculo_Pv()
        Pm = sup.pressao_face_inferior_dormente_Pm()
        Pr = sup.pressao_ruptura_solo_Pr()
        Pap = sup.pressao_admissivel_plataforma_Pap()
        h_exato = sup.espessura_minima_lastro_h()
        h_uso = math.ceil(h_exato * 100) / 100 if self.arredondar_h.get() and h_exato > 0 else h_exato

        sec = SecaoTransversal(geom, op, altura_lastro=h_uso)
        res = {
            "P": P, "Pg": Pg, "kv": kv, "Pv": Pv, "s": geom.comp_soca,
            "Pm": Pm, "Pr": Pr, "Pap": Pap, "h_exato": h_exato, "h_uso": h_uso,
            "area_secao": sec.area_secao_tipo(),
            "vol_secao": sec.volume_secao_tipo(),
            "Vd": sec.volume_dormente_vd(),
            "qtd_dorm_km": sec.qtd_dormentes_por_km(),
            "Vds": sec.volume_total_dormentes_vds(),
            "VL": sec.volume_total_lastro_vl(),
            "VL_maj": sec.volume_lastro_majorado(),
        }

        # Atualiza cartões
        self.card_vals["h"].config(text=f"{fmt(h_uso * 100, 2)} cm")
        self.card_vals["area"].config(text=f"{fmt(res['area_secao'], 2)} m²")
        self.card_vals["vl"].config(text=f"{fmt(res['VL'], 2)} m³")
        self.card_vals["vl_maj"].config(text=f"{fmt(res['VL_maj'], 2)} m³")

        # Atualiza tabela do Relatório Executivo
        for item in self.tree.get_children():
            self.tree.delete(item)
        linhas = [
            ("[PARÂMETROS DE CARGA]", ""),
            ("Carga em uma roda (P)", f"{fmt(res['P'], 3)} kgf"),
            ("Carga em grupo de dormentes (Pg)", f"{fmt(res['Pg'], 3)} kgf"),
            ("Coeficiente dinâmico (kv)", f"{fmt(res['kv'], 3)}"),
            ("Carga de cálculo (Pv)", f"{fmt(res['Pv'], 3)} kgf"),
            ("Largura efetiva da soca sob um trilho (s)", f"{fmt(res['s'], 2)} m"),
            ("[DIMENSIONAMENTO ESTRUTURAL]", ""),
            ("Pressão na face inferior do dormente (Pm)", f"{fmt(res['Pm'], 3)} kgf/cm²"),
            ("Pressão de ruptura do solo (Pr)", f"{fmt(res['Pr'], 3)} kgf/cm²"),
            ("Pressão admissível na Plataforma (Pap)", f"{fmt(res['Pap'], 3)} kgf/cm²"),
            ("Altura da camada de lastro (h) exata", f"> {fmt(res['h_exato'] * 100, 3)} cm"),
            ("[QUANTITATIVOS E CUBAGEM]", ""),
            ("Área da Seção Tipo", f"{fmt(res['area_secao'], 2)} m²"),
            ("Volume da Seção Tipo", f"{fmt(res['vol_secao'], 2)} m³"),
            ("Volume do dormente (Vd)", f"{fmt(res['Vd'], 2)} m³"),
            ("Qtd. Dormentes por km (inserida)", f"{fmt(res['qtd_dorm_km'], 0)} und/km"),
            ("Volume total de dormentes (Vds)", f"{fmt(res['Vds'], 2)} m³"),
            ("Volume total do lastro (VL)", f"{fmt(res['VL'], 2)} m³"),
            ("Volume total do lastro Majorado", f"{fmt(res['VL_maj'], 2)} m³"),
        ]
        for k, v in linhas:
            self.tree.insert("", "end", values=(k, v))

        # Atualiza Memória de Cálculo
        kv_calc = 1.0 + (4.5 * (p["velocidade"] ** 2) / 100000.0)
        b = p["comp_dormente"] + 2 * p["larg_ombro"]
        B = b + 2 * h_uso * p["inclinacao_talude"]
        memoria = (
            f"1. Carga por roda (P)         = {fmt(p['peso_total'], 0)} / {int(p['num_rodas'])} = {fmt(P, 3)} kgf\n"
            f"2. Carga nos dormentes (Pg)   = {fmt(P, 3)} * ({fmt(op.espacamento_dormentes, 2)} / {fmt(p['dist_eixos'], 3)}) = {fmt(Pg, 3)} kgf\n"
            f"3. Coeficiente dinâmico (kv)  = 1 + 4,5*{fmt(p['velocidade'], 1)}²/100000 = {fmt(kv_calc, 4)} -> adotado {fmt(kv, 3)}\n"
            f"4. Carga de cálculo (Pv)      = {fmt(Pg, 3)} * {fmt(kv, 3)} = {fmt(Pv, 3)} kgf\n"
            f"5. Pressão no dormente (Pm)   = {fmt(Pv, 3)} / ({fmt(p['comp_soca'], 2)} * {fmt(p['larg_dormente'], 2)} * 10000) = {fmt(Pm, 3)} kgf/cm²\n"
            f"6. Pressão de ruptura (Pr)    = 0,7 * {fmt(p['cbr'], 1)} = {fmt(Pr, 3)} kgf/cm²\n"
            f"7. Pressão admissível (Pap)   = {fmt(Pr, 3)} / {fmt(p['fator_seguranca'], 2)} = {fmt(Pap, 3)} kgf/cm²\n"
            f"8. Espessura de Talbot (h)    = ((16,8 * {fmt(Pm, 3)}) / {fmt(Pap, 3)})^0,8 * 2,54 = {fmt(h_exato * 100, 3)} cm\n"
            f"   Altura adotada na cubagem  = {fmt(h_uso * 100, 2)} cm ({fmt(h_uso, 4)} m)\n\n"
            f"GEOMETRIA E CUBAGEM (modelagem_geometrica.py):\n"
            f"   Largura superior (b)       = {fmt(b, 2)} m  |  Base inferior (B) = {fmt(B, 3)} m\n"
            f"   Dormente no lastro         = {fmt(alt_enterrada_m * 100, 1)} cm enterrados ({fmt(ALT_DESCOBERTA_CM, 0)} cm descobertos)\n"
            f"   Área da seção tipo         = {fmt(res['area_secao'], 2)} m²\n"
            f"   Volume líquido (VL)        = {fmt(res['VL'], 2)} m³\n"
            f"   Volume majorado (VL_maj)   = {fmt(res['VL_maj'], 2)} m³\n"
        )
        self.txt_mem.configure(state="normal")
        self.txt_mem.delete("1.0", "end")
        self.txt_mem.insert("1.0", memoria)
        self.txt_mem.configure(state="disabled")

        self._desenhar_secao(p, h_uso, alt_enterrada_m, alt_desc_m, Pap)

    def _desenhar_secao(self, p, h, alt_ent, alt_desc, pap):
        c = self.canvas_sec
        c.delete("all")
        w = max(c.winfo_width(), 680)
        ch = max(c.winfo_height(), 240)

        b = p["comp_dormente"] + 2 * p["larg_ombro"]
        B = b + 2 * h * p["inclinacao_talude"]
        y_ombro = h + alt_ent
        y_dorm_topo = y_ombro + alt_desc

        larg_total = max(B + 1.4, 4.2)
        alt_total = y_dorm_topo + 0.55
        escala = min((w - 140) / larg_total, (ch - 65) / alt_total)
        cx = w / 2
        cy = ch - 42

        def px(x): return cx + x * escala
        def py(y): return cy - y * escala

        # Plataforma (verde)
        plat_meio = B / 2 + 0.35
        c.create_rectangle(px(-plat_meio), py(0), px(plat_meio), py(-0.12), fill="#d1fae5", outline="#059669", width=1.5)
        c.create_text(cx, py(-0.06), text=f"PLATAFORMA / SUBLASTRO (CBR = {fmt(p['cbr'], 1)}% | Pap = {fmt(pap, 2)} kgf/cm²)", fill="#065f46", font=self.fonte_peq)

        # Lastro: trapézio contínuo com linha roxa
        pts_lastro = [px(-B / 2), py(0), px(B / 2), py(0), px(b / 2), py(y_ombro), px(-b / 2), py(y_ombro)]
        c.create_polygon(pts_lastro, fill="#e5e7eb", outline="#6b7280", width=1.2)
        c.create_line(px(-B / 2), py(0), px(-b / 2), py(y_ombro), fill="#7c3aed", width=2.4)
        c.create_line(px(B / 2), py(0), px(b / 2), py(y_ombro), fill="#7c3aed", width=2.4)

        # Linha tracejada na base do dormente
        c.create_line(px(-b / 2), py(h), px(b / 2), py(h), fill="#9ca3af", dash=(4, 3))

        # Dormente (com 5 cm descobertos acima do ombro)
        c.create_rectangle(px(-p["comp_dormente"] / 2), py(y_dorm_topo), px(p["comp_dormente"] / 2), py(h), fill="#92400e", outline="#78350f", width=1.5)

        # Trilhos apoiados no topo do dormente
        x_trilho = p["comp_dormente"] * 0.25
        for sinal in (-1, 1):
            xc = sinal * x_trilho
            c.create_rectangle(px(xc - 0.05), py(y_dorm_topo + 0.08), px(xc + 0.05), py(y_dorm_topo), fill="#475569", outline="#1e293b")

        # Cotas principais
        c.create_line(px(-b / 2), py(y_dorm_topo + 0.20), px(b / 2), py(y_dorm_topo + 0.20), fill="#0284c7", arrow="both")
        c.create_text(cx, py(y_dorm_topo + 0.28), text=f"Largura Superior b = {fmt(b, 2)} m", fill="#0369a1", font=self.fonte_peq)

        c.create_line(px(-B / 2), py(-0.20), px(B / 2), py(-0.20), fill="#d97706", arrow="both")
        c.create_text(cx, py(-0.28), text=f"Base Inferior B = {fmt(B, 3)} m", fill="#b45309", font=self.fonte_peq)

        # Cota lateral direita: h e parte descoberta
        xd = px(B / 2) + 18
        c.create_line(xd, py(0), xd, py(h), fill="#d97706", arrow="both")
        c.create_text(xd + 6, py(h / 2), text=f"h = {fmt(h * 100, 2)} cm", fill="#b45309", anchor="w", font=self.fonte_peq)
        c.create_text(xd + 6, py(y_ombro + alt_desc / 2), text=f"desc. = {fmt(ALT_DESCOBERTA_CM, 0)} cm", fill="#78350f", anchor="w", font=self.fonte_peq)

        # Talude apenas no lado esquerdo
        c.create_text(px(-B / 2) - 10, py(y_ombro / 2), text=f"Talude 1 : {fmt(p['inclinacao_talude'], 1)}", fill="#7c3aed", anchor="e", font=self.fonte_peq)


if __name__ == "__main__":
    AppLcvp().mainloop()
