# -*- coding: utf-8 -*-
import tkinter as tk
import random
from src.config import COLORS, FONTS, QUOTES, THEMES, DIFFICULTIES


class MenuScreen(tk.Frame):
    def __init__(self, parent, on_start):
        super().__init__(parent, bg=COLORS["bg"])
        self.on_start = on_start
        self._diff  = list(DIFFICULTIES.keys())[0]
        self._theme = list(THEMES.keys())[0]
        self._diff_btns  = {}
        self._theme_btns = {}
        self._build()

    def _build(self):
        # Canvas com scroll
        cv = tk.Canvas(self, bg=COLORS["bg"], highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)

        fr = tk.Frame(cv, bg=COLORS["bg"])
        fr.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._fr_id = cv.create_window((0, 0), window=fr, anchor="nw")
        cv.bind("<Configure>", lambda e: cv.itemconfig(self._fr_id, width=e.width))

        self._fill(fr)

    def _fill(self, root):
        # Margem lateral fixa
        PAD = 120

        # ── Cabeçalho ──────────────────────────────────────────────────────
        tk.Frame(root, height=44, bg=COLORS["bg"]).pack(fill="x")
        tk.Frame(root, height=1, width=30, bg=COLORS["accent"]).pack()
        tk.Frame(root, height=16, bg=COLORS["bg"]).pack(fill="x")

        tk.Label(root, text="Caça-Palavras", font=FONTS["hero"],
                 fg=COLORS["text_dark"], bg=COLORS["bg"]).pack()

        tk.Frame(root, height=10, bg=COLORS["bg"]).pack(fill="x")

        q, a = random.choice(QUOTES)
        tk.Label(root, text=q, font=FONTS["quote"],
                 fg=COLORS["text_medium"], bg=COLORS["bg"],
                 wraplength=500, justify="center").pack()
        tk.Frame(root, height=4, bg=COLORS["bg"]).pack(fill="x")
        tk.Label(root, text=a.upper(), font=FONTS["author"],
                 fg=COLORS["accent_dark"], bg=COLORS["bg"]).pack()

        tk.Frame(root, height=34, bg=COLORS["bg"]).pack(fill="x")

        # ── Dificuldade ────────────────────────────────────────────────────
        d_outer = tk.Frame(root, bg=COLORS["bg"])
        d_outer.pack(fill="x", padx=PAD)

        tk.Label(d_outer, text="NÍVEL DE DIFICULDADE", font=FONTS["section_lbl"],
                 fg=COLORS["text_light"], bg=COLORS["bg"]).pack(anchor="w")
        tk.Frame(d_outer, height=6, bg=COLORS["bg"]).pack(fill="x")

        df = tk.Frame(d_outer, bg=COLORS["bg"])
        df.pack(fill="x")

        for diff, cfg in DIFFICULTIES.items():
            col = tk.Frame(df, bg=COLORS["bg"])
            col.pack(side="left", expand=True, fill="x", padx=(0, 6))

            card = tk.Frame(col, bg=COLORS["card"], cursor="hand2",
                            highlightthickness=1,
                            highlightbackground=COLORS["card_border"])
            card.pack(fill="both")

            ni = tk.Frame(card, bg=COLORS["card"], padx=16, pady=12)
            ni.pack(fill="x")

            nl = tk.Label(ni, text=cfg["label"], font=FONTS["diff_name"],
                          fg=COLORS["text_dark"], bg=COLORS["card"], anchor="w")
            nl.pack(fill="x")
            tk.Frame(ni, height=4, bg=COLORS["card"]).pack()
            dl = tk.Label(ni, text=cfg["description"], font=FONTS["diff_desc"],
                          fg=COLORS["text_light"], bg=COLORS["card"], anchor="w")
            dl.pack(fill="x")

            self._diff_btns[diff] = (card, ni, nl, dl)
            for w in (card, ni, nl, dl):
                w.bind("<Button-1>", lambda e, d=diff: self._sel_diff(d))

        self._sel_diff(self._diff)

        tk.Frame(root, height=24, bg=COLORS["bg"]).pack(fill="x")
        tk.Frame(root, height=1, bg=COLORS["separator"]).pack(fill="x", padx=PAD)
        tk.Frame(root, height=20, bg=COLORS["bg"]).pack(fill="x")

        # ── Tema ───────────────────────────────────────────────────────────
        t_outer = tk.Frame(root, bg=COLORS["bg"])
        t_outer.pack(fill="x", padx=PAD)

        tk.Label(t_outer, text="TEMA", font=FONTS["section_lbl"],
                 fg=COLORS["text_light"], bg=COLORS["bg"]).pack(anchor="w")
        tk.Frame(t_outer, height=6, bg=COLORS["bg"]).pack(fill="x")

        gf = tk.Frame(t_outer, bg=COLORS["bg"])
        gf.pack(fill="x")

        COLS = 5
        for i, theme in enumerate(THEMES):
            r, c = divmod(i, COLS)
            gf.columnconfigure(c, weight=1)

            card = tk.Frame(gf, bg=COLORS["card"], cursor="hand2",
                            highlightthickness=1,
                            highlightbackground=COLORS["card_border"])
            card.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

            lbl = tk.Label(card, text=theme, font=FONTS["theme_lbl"],
                           fg=COLORS["text_medium"], bg=COLORS["card"],
                           pady=9, padx=4, justify="center")
            lbl.pack(fill="both", expand=True)

            self._theme_btns[theme] = (card, lbl)
            for w in (card, lbl):
                w.bind("<Button-1>", lambda e, t=theme: self._sel_theme(t))

        self._sel_theme(self._theme)

        tk.Frame(root, height=30, bg=COLORS["bg"]).pack(fill="x")

        # ── Botão ──────────────────────────────────────────────────────────
        bf = tk.Frame(root, bg=COLORS["bg"])
        bf.pack()
        self._btn(bf, "COMEÇAR JOGO", self._go, 210, 42).pack()
        tk.Frame(root, height=50, bg=COLORS["bg"]).pack(fill="x")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _sel_diff(self, d):
        self._diff = d
        for k, (card, ni, nl, dl) in self._diff_btns.items():
            on = (k == d)
            bg = COLORS["accent_light"] if on else COLORS["card"]
            bd = COLORS["accent"]       if on else COLORS["card_border"]
            for w in (card, ni, nl, dl):
                w.config(bg=bg)
            card.config(highlightbackground=bd)

    def _sel_theme(self, t):
        self._theme = t
        for k, (card, lbl) in self._theme_btns.items():
            on  = (k == t)
            bg  = COLORS["accent_light"] if on else COLORS["card"]
            bd  = COLORS["accent"]       if on else COLORS["card_border"]
            fg  = COLORS["text_dark"]    if on else COLORS["text_medium"]
            fnt = (FONTS["theme_lbl"][0], FONTS["theme_lbl"][1], "bold") if on else FONTS["theme_lbl"]
            card.config(bg=bg, highlightbackground=bd)
            lbl.config(bg=bg, fg=fg, font=fnt)

    def _btn(self, p, text, cmd, w, h):
        f = tk.Frame(p, bg=COLORS["bg"])
        c = tk.Canvas(f, width=w, height=h, bg=COLORS["bg"],
                      highlightthickness=0, cursor="hand2")
        c.pack()
        c.create_rectangle(0, 0, w, h, fill=COLORS["btn_bg"], outline="", tags="r")
        c.create_text(w//2, h//2, text=text, font=FONTS["btn"], fill=COLORS["btn_text"])
        c.bind("<Button-1>", lambda e: cmd())
        c.bind("<Enter>",    lambda e: c.itemconfig("r", fill="#2E2E2E"))
        c.bind("<Leave>",    lambda e: c.itemconfig("r", fill=COLORS["btn_bg"]))
        return f

    def _go(self):
        self.on_start(self._diff, self._theme)
