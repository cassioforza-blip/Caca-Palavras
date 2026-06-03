# -*- coding: utf-8 -*-
import tkinter as tk
from src.config import COLORS, FONTS


class ResultScreen(tk.Frame):
    def __init__(self, parent, game_state, on_play_again, on_menu):
        super().__init__(parent, bg=COLORS["bg"])
        self.gs = game_state
        self.on_again = on_play_again
        self.on_menu  = on_menu
        self._build()

    def _build(self):
        total = self.gs.get("total_words", len(self.gs["words"]))
        found = len(self.gs["found_words"])
        score = self.gs.get("score", 0)
        el    = self.gs.get("time_elapsed", 0)
        tout  = self.gs.get("timeout", False)
        win   = (found == total and not tout)

        tk.Frame(self, height=40, bg=COLORS["bg"]).pack()
        tk.Frame(self, height=1, width=30, bg=COLORS["accent"]).pack()
        tk.Frame(self, height=14, bg=COLORS["bg"]).pack()
        tk.Label(self, text="Caça-Palavras", font=FONTS["hero"],
                 fg=COLORS["text_dark"], bg=COLORS["bg"]).pack()
        tk.Frame(self, height=22, bg=COLORS["bg"]).pack()

        card = tk.Frame(self, bg=COLORS["card"], highlightthickness=1,
                        highlightbackground=COLORS["card_border"])
        card.pack(padx=80, pady=(0,30), fill="x")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=36, pady=30, fill="x")

        title = "Parabéns." if win else ("Boa tentativa." if found>0 else "Tente novamente.")
        sub   = "Você encontrou todas as palavras." if win else f"Você encontrou {found} de {total} palavras."

        tk.Label(inner, text=title, font=("Georgia", 26, "bold"),
                 fg=COLORS["text_dark"], bg=COLORS["card"]).pack(anchor="w")
        tk.Frame(inner, height=4, bg=COLORS["card"]).pack()
        tk.Label(inner, text=sub, font=FONTS["subtitle"],
                 fg=COLORS["text_light"], bg=COLORS["card"]).pack(anchor="w")
        tk.Frame(inner, height=1, bg=COLORS["separator"]).pack(fill="x", pady=18)

        m,s = el//60, el%60
        sg = tk.Frame(inner, bg=COLORS["card"])
        sg.pack(fill="x")
        for i,(l,v) in enumerate([
            ("JOGADOR",self.gs["player_name"]),("TEMA",self.gs["theme"]),
            ("DIFICULDADE",self.gs["difficulty"]),
            ("PALAVRAS",f"{found}/{total}"),("TEMPO",f"{m:02d}:{s:02d}"),("PONTUAÇÃO",str(score))
        ]):
            r,c = divmod(i,3)
            b = tk.Frame(sg, bg=COLORS["card"])
            b.grid(row=r, column=c, padx=(0,36), pady=7, sticky="w")
            tk.Label(b, text=l, font=FONTS["stat_label"],
                     fg=COLORS["text_light"], bg=COLORS["card"]).pack(anchor="w")
            tk.Label(b, text=v, font=FONTS["stat_value"],
                     fg=COLORS["accent_dark"] if l=="PONTUAÇÃO" else COLORS["text_dark"],
                     bg=COLORS["card"]).pack(anchor="w")

        tk.Frame(inner, height=1, bg=COLORS["separator"]).pack(fill="x", pady=18)

        if self.gs["words"]:
            wr = tk.Frame(inner, bg=COLORS["card"])
            wr.pack(anchor="w")
            fs = set(self.gs["found_words"])
            for w in self.gs["words"]:
                ok = w in fs
                tk.Label(wr, text=w,
                         font=(FONTS["word_list"][0],FONTS["word_list"][1],"bold" if ok else "normal"),
                         fg=COLORS["found_text"] if ok else COLORS["text_light"],
                         bg=COLORS["card"]).pack(side="left", padx=(0,12))

        tk.Frame(inner, height=18, bg=COLORS["card"]).pack()
        row = tk.Frame(inner, bg=COLORS["card"])
        row.pack(anchor="w")
        self._outline(row,"Menu Principal", self.on_menu, 145, 36).pack(side="left",padx=(0,8))
        self._solid(row,  "Jogar Novamente",self.on_again,165, 36).pack(side="left")

    def _solid(self,p,t,cmd,w,h):
        f=tk.Frame(p,bg=COLORS["card"])
        c=tk.Canvas(f,width=w,height=h,bg=COLORS["card"],highlightthickness=0,cursor="hand2")
        c.pack()
        c.create_rectangle(0,0,w,h,fill=COLORS["btn_bg"],outline="",tags="r")
        c.create_text(w//2,h//2,text=t,font=FONTS["btn"],fill=COLORS["btn_text"])
        c.bind("<Button-1>",lambda e:cmd())
        c.bind("<Enter>",lambda e:c.itemconfig("r",fill="#2E2E2E"))
        c.bind("<Leave>",lambda e:c.itemconfig("r",fill=COLORS["btn_bg"]))
        return f

    def _outline(self,p,t,cmd,w,h):
        f=tk.Frame(p,bg=COLORS["card"])
        c=tk.Canvas(f,width=w,height=h,bg=COLORS["card"],highlightthickness=0,cursor="hand2")
        c.pack()
        c.create_rectangle(1,1,w-1,h-1,fill=COLORS["card"],outline=COLORS["text_dark"],width=1,tags="r")
        c.create_text(w//2,h//2,text=t,font=FONTS["btn"],fill=COLORS["text_dark"])
        c.bind("<Button-1>",lambda e:cmd())
        c.bind("<Enter>",lambda e:c.itemconfig("r",fill=COLORS["separator"]))
        c.bind("<Leave>",lambda e:c.itemconfig("r",fill=COLORS["card"]))
        return f
