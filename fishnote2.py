import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import math
import os
from datetime import date

ARQUIVO = "dados.json"

# =========================
# DADOS DO JOGO
# =========================

PEIXES = {
    # ---- Comuns (12) ----
    "Sardinha 🐟": {"raridade": "Comum", "cm": (10, 25)},
    "Tilápia 🐠": {"raridade": "Comum", "cm": (20, 40)},
    "Lambari 🐟": {"raridade": "Comum", "cm": (5, 15)},
    "Piaba 🐠": {"raridade": "Comum", "cm": (4, 10)},
    "Manjuba 🐟": {"raridade": "Comum", "cm": (8, 15)},
    "Tainha 🐟": {"raridade": "Comum", "cm": (25, 50)},
    "Carpa 🎏": {"raridade": "Comum", "cm": (30, 60)},
    "Bagre 🐟": {"raridade": "Comum", "cm": (25, 55)},
    "Traíra 🐟": {"raridade": "Comum", "cm": (25, 50)},
    "Anchova 🐟": {"raridade": "Comum", "cm": (15, 35)},
    "Camarão 🦐": {"raridade": "Comum", "cm": (8, 18)},
    "Caranguejo 🦀": {"raridade": "Comum", "cm": (10, 25)},
    # ---- Raros (12) ----
    "Salmão 🐡": {"raridade": "Raro", "cm": (40, 80)},
    "Atum 🐋": {"raridade": "Raro", "cm": (60, 120)},
    "Robalo 🐟": {"raridade": "Raro", "cm": (40, 90)},
    "Dourado 🐠": {"raridade": "Raro", "cm": (50, 100)},
    "Truta 🐟": {"raridade": "Raro", "cm": (30, 60)},
    "Garoupa 🐟": {"raridade": "Raro", "cm": (50, 110)},
    "Tucunaré 🐟": {"raridade": "Raro", "cm": (35, 70)},
    "Pintado 🐟": {"raridade": "Raro", "cm": (60, 130)},
    "Lula 🦑": {"raridade": "Raro", "cm": (30, 100)},
    "Polvo 🐙": {"raridade": "Raro", "cm": (40, 120)},
    "Lagosta 🦞": {"raridade": "Raro", "cm": (25, 50)},
    "Barracuda 🐟": {"raridade": "Raro", "cm": (60, 140)},
    # ---- Épicos (7) ----
    "Peixe-Espada ⚔️🐟": {"raridade": "Épico", "cm": (100, 200)},
    "Pirarucu 🐟": {"raridade": "Épico", "cm": (150, 250)},
    "Marlim 🗡️": {"raridade": "Épico", "cm": (180, 350)},
    "Peixe-Vela ⛵": {"raridade": "Épico", "cm": (150, 300)},
    "Moreia 🐍": {"raridade": "Épico", "cm": (100, 200)},
    "Peixe-Lua 🌕": {"raridade": "Épico", "cm": (150, 300)},
    "Baiacu-Gigante 🐡": {"raridade": "Épico", "cm": (60, 130)},
    # ---- Lendários (4) ----
    "Tubarão 🦈": {"raridade": "Lendário", "cm": (200, 400)},
    "Baleia-Azul 🐳": {"raridade": "Lendário", "cm": (800, 1800)},
    "Kraken 🦑👑": {"raridade": "Lendário", "cm": (500, 1200)},
    "Leviatã 🐉": {"raridade": "Lendário", "cm": (1000, 2500)},
}

VALOR_VENDA = {"Comum": 10, "Raro": 30, "Épico": 80, "Lendário": 200}
XP_RARIDADE = {"Comum": 5, "Raro": 15, "Épico": 40, "Lendário": 100}

# pesos = chance relativa de cada raridade ao usar a isca
ISCAS = {
    "comum": {"nome": "Comum", "emoji": "🪱", "preco": 20,
              "pesos": {"Comum": 85, "Raro": 15}},
    "rara": {"nome": "Rara", "emoji": "🦋", "preco": 50,
             "pesos": {"Comum": 50, "Raro": 40, "Épico": 10}},
    "epica": {"nome": "Épica", "emoji": "🔥", "preco": 120,
              "pesos": {"Comum": 25, "Raro": 35, "Épico": 30, "Lendário": 10}},
    "lendaria": {"nome": "Lendária", "emoji": "👑", "preco": 300,
                 "pesos": {"Épico": 70, "Lendário": 30}},
}

# recompensa por concluir uma tarefa, de acordo com a prioridade
REC_TAREFA = {
    "Baixa": {"iscas": {"comum": 1}, "xp": 5, "moedas": 0},
    "Média": {"iscas": {"comum": 2}, "xp": 10, "moedas": 10},
    "Alta": {"iscas": {"comum": 1, "rara": 1}, "xp": 25, "moedas": 25},
}

# ---- tema "fundo do mar / praia" ----
C_FUNDO = "#0a2f4f"    # azul profundo
C_PAINEL = "#0f4a73"   # azul médio (painéis e tabelas)
C_ESCURO = "#06243b"   # azul bem escuro (campos de texto, trilhos)
C_TEXTO = "#eaf6ff"    # espuma
C_MUTED = "#9fc5dd"    # texto secundário
C_AREIA = "#f4d35e"    # amarelo areia / sol
C_SELECAO = "#2a7fba"  # linha selecionada

CORES = {
    "Comum": "#cfe8f7", "Raro": "#6ec6ff", "Épico": "#d7a6ff", "Lendário": "#ffb347",
    "Baixa": "#7be0a0", "Média": "#ffd166", "Alta": "#ff8a80",
}

ORDEM_PRIO = {"Alta": 0, "Média": 1, "Baixa": 2}


def misturar(c1, c2, t):
    """Mistura duas cores hex (t=0 -> c1, t=1 -> c2)."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def nome_isca(chave):
    i = ISCAS[chave]
    return f"{i['emoji']} {i['nome']}"


def texto_recompensa(prio):
    r = REC_TAREFA[prio]
    partes = [f"+{q} {ISCAS[k]['emoji']}" for k, q in r["iscas"].items()]
    partes.append(f"+{r['xp']} XP")
    if r["moedas"]:
        partes.append(f"+{r['moedas']} 💰")
    return "  ".join(partes)


def texto_chances(chave):
    pesos = ISCAS[chave]["pesos"]
    total = sum(pesos.values())
    return " · ".join(f"{r} {p * 100 / total:.0f}%" for r, p in pesos.items())


# =========================
# SALVAR / CARREGAR
# =========================

def estado_padrao():
    return {
        "iscas": {"comum": 5, "rara": 0, "epica": 0, "lendaria": 0},
        "moedas": 100,
        "xp": 0,
        "nivel": 1,
        "xp_proximo_nivel": 100,
        "total_pescas": 0,
        "total_tarefas": 0,
        "catalogo": {},   # peixe -> {"capturados": n, "maior": cm}
        "estoque": {},    # peixe -> quantidade ainda não vendida
        "tarefas": [],    # [{"texto", "prioridade"}]
        "concluidas": [], # [{"texto", "prioridade", "data"}]
    }


def _chave_isca(chave_antiga):
    """Converte chaves do save antigo ('Comum 🪱') para as novas ('comum')."""
    if chave_antiga in ISCAS:
        return chave_antiga
    primeira = chave_antiga.split()[0].lower() if chave_antiga.split() else ""
    for k, i in ISCAS.items():
        if i["nome"].lower() == primeira:
            return k
    return None


def carregar():
    e = estado_padrao()
    if not os.path.exists(ARQUIVO):
        return e
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, dict):
            raise ValueError("formato inválido")
    except (json.JSONDecodeError, OSError, ValueError):
        # arquivo corrompido: guarda uma cópia e começa do zero
        try:
            os.replace(ARQUIVO, ARQUIVO + ".bak")
        except OSError:
            pass
        return e

    for k in ("moedas", "xp", "nivel", "xp_proximo_nivel", "total_pescas", "total_tarefas"):
        if isinstance(d.get(k), int):
            e[k] = d[k]

    for chave, qt in d.get("iscas", {}).items():
        nova = _chave_isca(chave)
        if nova and isinstance(qt, int):
            e["iscas"][nova] = max(0, qt)

    estoque_antigo = {}
    for peixe, dados in d.get("catalogo", {}).items():
        if peixe not in PEIXES or not isinstance(dados, dict):
            continue
        qt_antiga = int(dados.get("quantidade", 0))
        capturados = int(dados.get("capturados", qt_antiga))
        e["catalogo"][peixe] = {"capturados": capturados, "maior": int(dados.get("maior", 0))}
        estoque_antigo[peixe] = qt_antiga

    if isinstance(d.get("estoque"), dict):
        origem = d["estoque"]
    else:
        origem = estoque_antigo  # save antigo: a "quantidade" era o estoque
    for peixe, qt in origem.items():
        if peixe in PEIXES and isinstance(qt, int) and qt > 0:
            e["estoque"][peixe] = qt

    for t in d.get("tarefas", []):
        if isinstance(t, str) and t.strip():
            e["tarefas"].append({"texto": t.strip(), "prioridade": "Baixa"})
        elif isinstance(t, dict) and t.get("texto"):
            prio = t.get("prioridade") if t.get("prioridade") in REC_TAREFA else "Média"
            e["tarefas"].append({"texto": t["texto"], "prioridade": prio})

    for t in d.get("concluidas", []):
        if isinstance(t, dict) and t.get("texto"):
            prio = t.get("prioridade") if t.get("prioridade") in REC_TAREFA else "Baixa"
            e["concluidas"].append({"texto": t["texto"], "prioridade": prio,
                                    "data": str(t.get("data", ""))})
    return e


# =========================
# APLICATIVO
# =========================

class FishNote:
    def __init__(self, root):
        self.root = root
        self.e = carregar()

        root.title("fishnote 🎣")
        root.geometry("780x620")
        root.minsize(700, 540)

        estilo = ttk.Style()
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=24)

        self.criar_menu()
        self.criar_cabecalho()

        self.status = tk.StringVar(value="Bem-vindo ao fishnote! Complete tarefas para ganhar iscas.")
        ttk.Label(root, textvariable=self.status, anchor="w", relief="sunken",
                  padding=(8, 3)).pack(side="bottom", fill="x")

        self.abas = ttk.Notebook(root)
        self.abas.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        self.criar_aba_pesca()
        self.criar_aba_tarefas()
        self.criar_aba_inventario()
        self.criar_aba_catalogo()
        self.criar_aba_loja()

        self.atualizar_tudo()
        root.protocol("WM_DELETE_WINDOW", self.fechar)

    # ---------- utilidades ----------

    def msg(self, texto):
        self.status.set(texto)

    def salvar(self):
        tmp = ARQUIVO + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.e, f, ensure_ascii=False, indent=2)
            os.replace(tmp, ARQUIVO)
        except OSError as erro:
            self.msg(f"⚠️ Não foi possível salvar: {erro}")

    def fechar(self):
        self.salvar()
        self.root.destroy()

    def criar_tree(self, pai, colunas, altura=8, selectmode="browse"):
        """colunas = [(id, titulo, largura)] -> (frame, tree)"""
        frame = ttk.Frame(pai)
        tree = ttk.Treeview(frame, columns=[c[0] for c in colunas], show="headings",
                            height=altura, selectmode=selectmode)
        for cid, titulo, larg in colunas:
            tree.heading(cid, text=titulo)
            tree.column(cid, width=larg, anchor="w")
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for nome, cor in CORES.items():
            tree.tag_configure(nome, foreground=cor)
        return frame, tree

    def repor_tree(self, tree, linhas):
        """linhas = [(iid, valores, tag)]; mantém a seleção se possível."""
        selecionados = set(tree.selection())
        tree.delete(*tree.get_children())
        for iid, valores, tag in linhas:
            tree.insert("", "end", iid=iid, values=valores, tags=(tag,) if tag else ())
        for iid in selecionados:
            if tree.exists(iid):
                tree.selection_add(iid)

    # ---------- menu e cabeçalho ----------

    def criar_menu(self):
        barra = tk.Menu(self.root)
        arquivo = tk.Menu(barra, tearoff=0)
        arquivo.add_command(label="Salvar agora", command=lambda: (self.salvar(), self.msg("💾 Progresso salvo.")))
        arquivo.add_command(label="Resetar progresso…", command=self.resetar)
        arquivo.add_separator()
        arquivo.add_command(label="Sair", command=self.fechar)
        barra.add_cascade(label="Arquivo", menu=arquivo)
        self.root.config(menu=barra)

    def criar_cabecalho(self):
        f = ttk.Frame(self.root, padding=(12, 8))
        f.pack(fill="x")
        fonte = ("Helvetica", 12, "bold")
        self.lbl_moedas = ttk.Label(f, font=fonte)
        self.lbl_nivel = ttk.Label(f, font=fonte)
        self.lbl_pescas = ttk.Label(f, font=fonte)
        self.lbl_tarefas = ttk.Label(f, font=fonte)
        for col, lbl in enumerate((self.lbl_moedas, self.lbl_nivel, self.lbl_pescas, self.lbl_tarefas)):
            lbl.grid(row=0, column=col, sticky="w", padx=(0, 12))
            f.columnconfigure(col, weight=1)
        self.barra_xp = ttk.Progressbar(f)
        self.barra_xp.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0), padx=(0, 12))
        self.lbl_xp = ttk.Label(f)
        self.lbl_xp.grid(row=1, column=3, sticky="w", pady=(6, 0))

    def resetar(self):
        if messagebox.askyesno("Resetar progresso",
                               "Isso apaga moedas, nível, peixes, iscas e tarefas.\nTem certeza?"):
            self.e = estado_padrao()
            self.salvar()
            self.txt_log.config(state="normal")
            self.txt_log.delete("1.0", "end")
            self.txt_log.config(state="disabled")
            self.lbl_resultado.config(text="Lance a linha!")
            self.atualizar_tudo()
            self.msg("Progresso resetado.")

    # ---------- XP ----------

    def ganhar_xp(self, pontos):
        e = self.e
        e["xp"] += pontos
        subidas = []
        while e["xp"] >= e["xp_proximo_nivel"]:
            e["xp"] -= e["xp_proximo_nivel"]
            e["nivel"] += 1
            e["xp_proximo_nivel"] = int(e["xp_proximo_nivel"] * 1.5)
            bonus = 50 * e["nivel"]
            e["moedas"] += bonus
            subidas.append((e["nivel"], bonus))
        return subidas

    def avisar_niveis(self, subidas):
        for nivel, bonus in subidas:
            messagebox.showinfo("LEVEL UP 🎖️", f"Subiu para o nível {nivel}!\n+{bonus} moedas!")

    # ---------- aba Pesca ----------

    def criar_aba_pesca(self):
        a = ttk.Frame(self.abas, padding=12)
        self.abas.add(a, text="🎣 Pesca")

        ttk.Label(a, text="Escolha a isca:").pack(anchor="w")
        self.combo_isca = ttk.Combobox(a, state="readonly", width=32)
        self.combo_isca.pack(anchor="w", pady=(2, 0))
        self.combo_isca.bind("<<ComboboxSelected>>", lambda ev: self.atualizar_chances())

        self.lbl_chances = ttk.Label(a, foreground="#555555")
        self.lbl_chances.pack(anchor="w", pady=4)

        ttk.Button(a, text="🎣 Pescar", command=self.pescar).pack(pady=8)

        self.lbl_resultado = ttk.Label(a, text="Lance a linha!", font=("Helvetica", 13, "bold"))
        self.lbl_resultado.pack(pady=(0, 6))

        ttk.Label(a, text="Diário de pesca").pack(anchor="w")
        self.txt_log = tk.Text(a, height=12, state="disabled", wrap="word")
        self.txt_log.pack(fill="both", expand=True)
        for r in XP_RARIDADE:
            self.txt_log.tag_configure(r, foreground=CORES[r])
        self.txt_log.tag_configure("info", foreground="#2e7d32")

    def log(self, texto, tag=None):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", texto + "\n", (tag,) if tag else ())
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def isca_selecionada(self):
        idx = self.combo_isca.current()
        return list(ISCAS)[idx if idx >= 0 else 0]

    def atualizar_chances(self):
        self.lbl_chances.config(text="Chances: " + texto_chances(self.isca_selecionada()))

    def atualizar_combo_iscas(self):
        idx = max(self.combo_isca.current(), 0)
        self.combo_isca["values"] = [f"{nome_isca(k)}  (x{self.e['iscas'][k]})" for k in ISCAS]
        self.combo_isca.current(idx)
        self.atualizar_chances()

    def pescar(self):
        e = self.e
        chave = self.isca_selecionada()
        if e["iscas"][chave] <= 0:
            messagebox.showwarning("Sem isca", "Você não tem essa isca!\nConclua tarefas ou compre na loja.")
            return
        e["iscas"][chave] -= 1

        pesos = ISCAS[chave]["pesos"]
        raridade = random.choices(list(pesos), weights=list(pesos.values()))[0]
        peixe = random.choice([p for p, i in PEIXES.items() if i["raridade"] == raridade])

        lo, hi = PEIXES[peixe]["cm"]
        bonus = e["nivel"] * 2
        tamanho = random.randint(lo + bonus, hi + bonus)

        e["total_pescas"] += 1
        cat = e["catalogo"].setdefault(peixe, {"capturados": 0, "maior": 0})
        cat["capturados"] += 1
        recorde = tamanho > cat["maior"] and cat["capturados"] > 1
        cat["maior"] = max(cat["maior"], tamanho)
        e["estoque"][peixe] = e["estoque"].get(peixe, 0) + 1

        xp_ganho = XP_RARIDADE[raridade]
        subidas = self.ganhar_xp(xp_ganho)

        self.lbl_resultado.config(text=f"{peixe}  ·  {raridade}  ·  {tamanho} cm", foreground=CORES[raridade])
        extra = "  🏆 novo recorde!" if recorde else ""
        self.log(f"{peixe} ({raridade}) {tamanho} cm  +{xp_ganho} XP{extra}", raridade)

        self.atualizar_tudo()
        self.salvar()
        self.avisar_niveis(subidas)

    # ---------- aba Tarefas ----------

    def criar_aba_tarefas(self):
        a = ttk.Frame(self.abas, padding=12)
        self.abas.add(a, text="✅ Tarefas")

        linha = ttk.Frame(a)
        linha.pack(fill="x")
        self.entry_tarefa = ttk.Entry(linha)
        self.entry_tarefa.pack(side="left", fill="x", expand=True)
        self.entry_tarefa.bind("<Return>", lambda ev: self.adicionar_tarefa())
        self.combo_prio = ttk.Combobox(linha, values=list(REC_TAREFA), state="readonly", width=8)
        self.combo_prio.set("Média")
        self.combo_prio.pack(side="left", padx=6)
        ttk.Button(linha, text="Adicionar", command=self.adicionar_tarefa).pack(side="left")

        frame, self.tree_tarefas = self.criar_tree(
            a, [("prio", "Prioridade", 90), ("texto", "Tarefa", 330), ("rec", "Recompensa", 230)],
            altura=9, selectmode="extended")
        frame.pack(fill="both", expand=True, pady=8)
        self.tree_tarefas.bind("<Double-1>", lambda ev: self.concluir_tarefa())

        botoes = ttk.Frame(a)
        botoes.pack(fill="x")
        ttk.Button(botoes, text="✔ Concluir", command=self.concluir_tarefa).pack(side="left")
        ttk.Button(botoes, text="✏️ Editar", command=self.editar_tarefa).pack(side="left", padx=6)
        ttk.Button(botoes, text="🗑 Excluir", command=self.excluir_tarefa).pack(side="left")
        ttk.Label(botoes, text="(duplo clique também conclui)", foreground="#777777").pack(side="right")

        ttk.Label(a, text="Concluídas recentemente").pack(anchor="w", pady=(10, 2))
        self.lista_hist = tk.Listbox(a, height=5)
        self.lista_hist.pack(fill="x")

    def adicionar_tarefa(self):
        texto = self.entry_tarefa.get().strip()
        if not texto:
            return
        self.e["tarefas"].append({"texto": texto[:120], "prioridade": self.combo_prio.get() or "Média"})
        self.entry_tarefa.delete(0, "end")
        self.atualizar_tarefas()
        self.salvar()
        self.msg(f"Tarefa adicionada: {texto[:60]}")

    def _indices_selecionados(self):
        return sorted(int(i) for i in self.tree_tarefas.selection())

    def concluir_tarefa(self):
        sel = self._indices_selecionados()
        if not sel:
            self.msg("Selecione uma tarefa para concluir.")
            return
        e = self.e
        subidas = []
        ganhos = {"xp": 0, "moedas": 0, "iscas": {}}
        for i in reversed(sel):
            t = e["tarefas"].pop(i)
            r = REC_TAREFA[t["prioridade"]]
            for k, q in r["iscas"].items():
                e["iscas"][k] += q
                ganhos["iscas"][k] = ganhos["iscas"].get(k, 0) + q
            e["moedas"] += r["moedas"]
            ganhos["moedas"] += r["moedas"]
            ganhos["xp"] += r["xp"]
            subidas += self.ganhar_xp(r["xp"])
            e["total_tarefas"] += 1
            e["concluidas"].append({"texto": t["texto"], "prioridade": t["prioridade"],
                                    "data": date.today().strftime("%d/%m")})
        e["concluidas"] = e["concluidas"][-50:]

        partes = [f"+{q} {ISCAS[k]['emoji']}" for k, q in ganhos["iscas"].items()]
        partes.append(f"+{ganhos['xp']} XP")
        if ganhos["moedas"]:
            partes.append(f"+{ganhos['moedas']} 💰")
        self.msg(f"✅ {len(sel)} tarefa(s) concluída(s): " + "  ".join(partes))

        self.atualizar_tudo()
        self.salvar()
        self.avisar_niveis(subidas)

    def editar_tarefa(self):
        sel = self._indices_selecionados()
        if len(sel) != 1:
            self.msg("Selecione uma única tarefa para editar.")
            return
        t = self.e["tarefas"][sel[0]]
        novo = simpledialog.askstring("Editar tarefa", "Texto da tarefa:",
                                      initialvalue=t["texto"], parent=self.root)
        if novo and novo.strip():
            t["texto"] = novo.strip()[:120]
            self.atualizar_tarefas()
            self.salvar()

    def excluir_tarefa(self):
        sel = self._indices_selecionados()
        if not sel:
            self.msg("Selecione uma tarefa para excluir.")
            return
        if messagebox.askyesno("Excluir", f"Excluir {len(sel)} tarefa(s) sem receber recompensa?"):
            for i in reversed(sel):
                self.e["tarefas"].pop(i)
            self.atualizar_tarefas()
            self.salvar()

    def atualizar_tarefas(self):
        ordem = sorted(range(len(self.e["tarefas"])),
                       key=lambda i: (ORDEM_PRIO[self.e["tarefas"][i]["prioridade"]], i))
        linhas = []
        for i in ordem:
            t = self.e["tarefas"][i]
            linhas.append((str(i), (t["prioridade"], t["texto"], texto_recompensa(t["prioridade"])), t["prioridade"]))
        self.repor_tree(self.tree_tarefas, linhas)

        self.lista_hist.delete(0, "end")
        for t in reversed(self.e["concluidas"][-5:]):
            self.lista_hist.insert("end", f"✔ {t['data']} · {t['texto']}")

    # ---------- aba Inventário ----------

    def criar_aba_inventario(self):
        a = ttk.Frame(self.abas, padding=12)
        self.abas.add(a, text="🎒 Inventário")
        a.columnconfigure(1, weight=1)
        a.rowconfigure(1, weight=1)

        ttk.Label(a, text="Iscas").grid(row=0, column=0, sticky="w")
        ttk.Label(a, text="Peixes (ainda não vendidos)").grid(row=0, column=1, sticky="w", padx=(12, 0))

        f1, self.tree_iscas = self.criar_tree(a, [("isca", "Isca", 110), ("qtd", "Qtd", 50)], altura=8)
        f1.grid(row=1, column=0, sticky="ns")
        f2, self.tree_estoque = self.criar_tree(
            a, [("peixe", "Peixe", 150), ("rar", "Raridade", 80), ("qtd", "Qtd", 45),
                ("unit", "Valor un.", 70), ("total", "Total", 70)], altura=8)
        f2.grid(row=1, column=1, sticky="nsew", padx=(12, 0))

        botoes = ttk.Frame(a)
        botoes.grid(row=2, column=1, sticky="w", padx=(12, 0), pady=8)
        ttk.Button(botoes, text="Vender 1", command=lambda: self.vender_selecionado(False)).pack(side="left")
        ttk.Button(botoes, text="Vender todos da espécie",
                   command=lambda: self.vender_selecionado(True)).pack(side="left", padx=6)
        ttk.Button(botoes, text="💰 Vender tudo", command=self.vender_tudo).pack(side="left")

        self.lbl_valor_estoque = ttk.Label(a, foreground="#555555")
        self.lbl_valor_estoque.grid(row=3, column=1, sticky="w", padx=(12, 0))

    def valor_estoque(self):
        return sum(VALOR_VENDA[PEIXES[p]["raridade"]] * q for p, q in self.e["estoque"].items() if p in PEIXES)

    def vender_selecionado(self, todos):
        sel = self.tree_estoque.selection()
        if not sel:
            self.msg("Selecione um peixe no inventário.")
            return
        peixe = list(PEIXES)[int(sel[0])]
        qt = self.e["estoque"].get(peixe, 0)
        if qt <= 0:
            return
        n = qt if todos else 1
        ganho = VALOR_VENDA[PEIXES[peixe]["raridade"]] * n
        self.e["estoque"][peixe] = qt - n
        if self.e["estoque"][peixe] <= 0:
            del self.e["estoque"][peixe]
        self.e["moedas"] += ganho
        self.msg(f"💰 Vendeu {n}x {peixe} por {ganho} moedas.")
        self.atualizar_tudo()
        self.salvar()

    def vender_tudo(self):
        total = self.valor_estoque()
        if total <= 0:
            self.msg("Você não tem peixes para vender.")
            return
        if messagebox.askyesno("Vender tudo", f"Vender todos os peixes por {total} moedas?"):
            self.e["moedas"] += total
            self.e["estoque"] = {}
            self.msg(f"💰 Você vendeu tudo e ganhou {total} moedas!")
            self.atualizar_tudo()
            self.salvar()

    def atualizar_inventario(self):
        self.repor_tree(self.tree_iscas,
                        [(k, (nome_isca(k), self.e["iscas"][k]), None) for k in ISCAS])
        linhas = []
        for idx, (peixe, info) in enumerate(PEIXES.items()):
            qt = self.e["estoque"].get(peixe, 0)
            if qt > 0:
                un = VALOR_VENDA[info["raridade"]]
                linhas.append((str(idx), (peixe, info["raridade"], qt, un, un * qt), info["raridade"]))
        self.repor_tree(self.tree_estoque, linhas)
        self.lbl_valor_estoque.config(text=f"Valor total do estoque: {self.valor_estoque()} 💰")

    # ---------- aba Catálogo ----------

    def criar_aba_catalogo(self):
        a = ttk.Frame(self.abas, padding=12)
        self.abas.add(a, text="📖 Catálogo")
        self.lbl_resumo_cat = ttk.Label(a, font=("Helvetica", 11, "bold"))
        self.lbl_resumo_cat.pack(anchor="w", pady=(0, 6))
        frame, self.tree_catalogo = self.criar_tree(
            a, [("peixe", "Peixe", 170), ("rar", "Raridade", 90), ("cap", "Capturados", 90),
                ("maior", "Maior", 80), ("valor", "Venda", 70)], altura=10)
        frame.pack(fill="both", expand=True)

    def atualizar_catalogo(self):
        cat = self.e["catalogo"]
        linhas = []
        for idx, (peixe, info) in enumerate(PEIXES.items()):
            if peixe in cat and cat[peixe]["capturados"] > 0:
                d = cat[peixe]
                linhas.append((str(idx), (peixe, info["raridade"], d["capturados"], f"{d['maior']} cm",
                                          VALOR_VENDA[info["raridade"]]), info["raridade"]))
            else:
                linhas.append((str(idx), ("❓ ???", info["raridade"], 0, "-", "-"), None))
        self.repor_tree(self.tree_catalogo, linhas)
        descobertos = sum(1 for p in PEIXES if p in cat and cat[p]["capturados"] > 0)
        self.lbl_resumo_cat.config(
            text=f"Espécies descobertas: {descobertos}/{len(PEIXES)}   ·   Total de pescas: {self.e['total_pescas']}")

    # ---------- aba Loja ----------

    def criar_aba_loja(self):
        a = ttk.Frame(self.abas, padding=12)
        self.abas.add(a, text="🛒 Loja")

        ttk.Label(a, text="Comprar iscas").pack(anchor="w")
        frame, self.tree_loja = self.criar_tree(
            a, [("isca", "Isca", 110), ("preco", "Preço", 70), ("chances", "Chances", 400), ("tem", "Você tem", 70)],
            altura=5)
        frame.pack(fill="x", pady=(2, 8))

        linha = ttk.Frame(a)
        linha.pack(fill="x")
        ttk.Label(linha, text="Quantidade:").pack(side="left")
        self.spin_qtd = ttk.Spinbox(linha, from_=1, to=99, width=5)
        self.spin_qtd.set(1)
        self.spin_qtd.pack(side="left", padx=6)
        ttk.Button(linha, text="Comprar", command=self.comprar_isca).pack(side="left")

        ttk.Separator(a).pack(fill="x", pady=14)

        ttk.Label(a, text="Vender peixes").pack(anchor="w")
        self.lbl_loja_estoque = ttk.Label(a, foreground="#555555")
        self.lbl_loja_estoque.pack(anchor="w", pady=4)
        ttk.Button(a, text="💰 Vender todos os peixes", command=self.vender_tudo).pack(anchor="w")

    def comprar_isca(self):
        sel = self.tree_loja.selection()
        if not sel:
            self.msg("Selecione uma isca na lista para comprar.")
            return
        chave = sel[0]
        try:
            qtd = int(self.spin_qtd.get())
        except ValueError:
            qtd = 0
        if qtd <= 0:
            messagebox.showwarning("Quantidade", "Informe uma quantidade válida.")
            return
        custo = ISCAS[chave]["preco"] * qtd
        if self.e["moedas"] < custo:
            messagebox.showwarning("Sem moedas", f"Você precisa de {custo} moedas (tem {self.e['moedas']}).")
            return
        self.e["moedas"] -= custo
        self.e["iscas"][chave] += qtd
        self.msg(f"🛒 Comprou {qtd}x {nome_isca(chave)} por {custo} moedas.")
        self.atualizar_tudo()
        self.salvar()

    def atualizar_loja(self):
        self.repor_tree(self.tree_loja, [
            (k, (nome_isca(k), f"{i['preco']} 💰", texto_chances(k), self.e["iscas"][k]), None)
            for k, i in ISCAS.items()])
        if not self.tree_loja.selection():
            self.tree_loja.selection_set("comum")
        total_peixes = sum(self.e["estoque"].values())
        self.lbl_loja_estoque.config(
            text=f"Você tem {total_peixes} peixe(s), valendo {self.valor_estoque()} moedas.")

    # ---------- atualização geral ----------

    def atualizar_cabecalho(self):
        e = self.e
        self.lbl_moedas.config(text=f"💰 Moedas: {e['moedas']}")
        self.lbl_nivel.config(text=f"🎖️ Nível {e['nivel']}")
        self.lbl_pescas.config(text=f"🎣 Pescas: {e['total_pescas']}")
        self.lbl_tarefas.config(text=f"✅ Tarefas: {e['total_tarefas']}")
        self.barra_xp["maximum"] = e["xp_proximo_nivel"]
        self.barra_xp["value"] = e["xp"]
        self.lbl_xp.config(text=f"XP {e['xp']}/{e['xp_proximo_nivel']}")

    def atualizar_tudo(self):
        self.atualizar_cabecalho()
        self.atualizar_combo_iscas()
        self.atualizar_tarefas()
        self.atualizar_inventario()
        self.atualizar_catalogo()
        self.atualizar_loja()


if __name__ == "__main__":
    root = tk.Tk()
    FishNote(root)
    root.mainloop()