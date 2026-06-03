# -*- coding: utf-8 -*-
import tkinter as tk
from src.config import COLORS, FONTS


class SetupScreen(tk.Frame):
    def __init__(self, parent, game_state, on_play, on_back):
        super().__init__(parent, bg=COLORS["bg"])
        self.gs = game_state
        self.on_play = on_play
        self.on_back = on_back
        self._nv = tk.StringVar(value=game_state.get("player_name",""))
        self._build()

    def _build(self):
        tk.Frame(self, height=70, bg=COLORS["bg"]).pack()
        tk.Frame(self, height=1, width=30, bg=COLORS["accent"]).pack()
        tk.Frame(self, height=16, bg=COLORS["bg"]).pack()
        tk.Label(self, text="Caça-Palavras", font=FONTS["hero"],
                 fg=COLORS["text_dark"], bg=COLORS["bg"]).pack()
        tk.Frame(self, height=28, bg=COLORS["bg"]).pack()

        card = tk.Frame(self, bg=COLORS["card"], highlightthickness=1,
                        highlightbackground=COLORS["card_border"])
        card.pack(padx=180)
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=40, pady=36)

        tk.Label(inner, text="Qual é o seu nome?", font=FONTS["title"],
                 fg=COLORS["text_dark"], bg=COLORS["card"]).pack(anchor="w")
        tk.Frame(inner, height=4, bg=COLORS["card"]).pack()
        tk.Label(inner, text="Será exibido no placar ao final da partida.",
                 font=FONTS["subtitle"], fg=COLORS["text_light"], bg=COLORS["card"]).pack(anchor="w")
        tk.Frame(inner, height=20, bg=COLORS["card"]).pack()

        ef = tk.Frame(inner, bg=COLORS["card_border"])
        ef.pack(fill="x")
        e = tk.Entry(ef, textvariable=self._nv, width=26,
                     font=("Georgia", 12), fg=COLORS["text_dark"],
                     bg=COLORS["card"], bd=0, insertbackground=COLORS["accent_dark"])
        e.pack(padx=1, pady=1, ipady=9, ipadx=12)
        e.focus_set()
        e.bind("<Return>", lambda ev: self._go())

        tk.Frame(inner, height=6, bg=COLORS["card"]).pack()
        diff  = self.gs.get("difficulty","")
        theme = self.gs.get("theme","")
        tk.Label(inner, text=f"{theme}   ·   {diff}", font=FONTS["body"],
                 fg=COLORS["text_light"], bg=COLORS["card"]).pack(anchor="w")
        tk.Frame(inner, height=24, bg=COLORS["card"]).pack()

        row = tk.Frame(inner, bg=COLORS["card"])
        row.pack(anchor="w")
        self._outline(row, "← Voltar", self.on_back, 120, 36).pack(side="left", padx=(0,8))
        self._solid(row,   "Jogar →",  self._go,     140, 36).pack(side="left")

    def _go(self):
        self.gs["player_name"] = self._nv.get().strip() or "Jogador"
        self.on_play()

    def _solid(self, p, t, cmd, w, h):
        f=tk.Frame(p,bg=COLORS["card"])
        c=tk.Canvas(f,width=w,height=h,bg=COLORS["card"],highlightthickness=0,cursor="hand2")
        c.pack()
        c.create_rectangle(0,0,w,h,fill=COLORS["btn_bg"],outline="",tags="r")
        c.create_text(w//2,h//2,text=t,font=FONTS["btn"],fill=COLORS["btn_text"])
        c.bind("<Button-1>",lambda e:cmd())
        c.bind("<Enter>",lambda e:c.itemconfig("r",fill="#2E2E2E"))
        c.bind("<Leave>",lambda e:c.itemconfig("r",fill=COLORS["btn_bg"]))
        return f

    def _outline(self, p, t, cmd, w, h):
        f=tk.Frame(p,bg=COLORS["card"])
        c=tk.Canvas(f,width=w,height=h,bg=COLORS["card"],highlightthickness=0,cursor="hand2")
        c.pack()
        c.create_rectangle(1,1,w-1,h-1,fill=COLORS["card"],outline=COLORS["text_dark"],width=1,tags="r")
        c.create_text(w//2,h//2,text=t,font=FONTS["btn"],fill=COLORS["text_dark"])
        c.bind("<Button-1>",lambda e:cmd())
        c.bind("<Enter>",lambda e:c.itemconfig("r",fill=COLORS["separator"]))
        c.bind("<Leave>",lambda e:c.itemconfig("r",fill=COLORS["card"]))
        return f
