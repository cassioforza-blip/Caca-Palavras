# -*- coding: utf-8 -*-
import tkinter as tk
import threading, time, os, random, math
from dotenv import load_dotenv
from src.config import COLORS, FONTS, DIFFICULTIES, QUOTES
from src.grid_generator import GridGenerator
from src.word_generator import WordGeneratorService
load_dotenv()


class GameScreen(tk.Frame):
    def __init__(self, parent, game_state, on_finish, on_exit):
        super().__init__(parent, bg=COLORS["bg"])
        self.gs = game_state
        self.on_finish = on_finish
        self.on_exit   = on_exit
        self.dcfg      = DIFFICULTIES[game_state["difficulty"]]
        self.grid = []; self.wpos = {}
        self.citems = {}; self.cstates = {}
        self.found  = set(); self.wlabels = {}
        self._s0 = None; self._scells = []; self._sel = False
        self._t0 = None; self._trun = False
        self._build()
        self._load()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self):
        # Topo: título + citação
        top = tk.Frame(self, bg=COLORS["bg"])
        top.pack(fill="x")
        tk.Frame(top, height=26, bg=COLORS["bg"]).pack()
        tk.Frame(top, height=1, width=30, bg=COLORS["accent"]).pack()
        tk.Frame(top, height=12, bg=COLORS["bg"]).pack()
        tk.Label(top, text="Caça-Palavras", font=FONTS["hero"],
                 fg=COLORS["text_dark"], bg=COLORS["bg"]).pack()
        tk.Frame(top, height=8, bg=COLORS["bg"]).pack()
        q, a = random.choice(QUOTES)
        tk.Label(top, text=q, font=FONTS["quote"], fg=COLORS["text_medium"],
                 bg=COLORS["bg"], wraplength=520, justify="center").pack()
        tk.Frame(top, height=3, bg=COLORS["bg"]).pack()
        tk.Label(top, text=a.upper(), font=FONTS["author"],
                 fg=COLORS["accent_dark"], bg=COLORS["bg"]).pack()
        tk.Frame(top, height=14, bg=COLORS["bg"]).pack()

        # Card principal
        self._card = tk.Frame(self, bg=COLORS["card"],
                               highlightthickness=1,
                               highlightbackground=COLORS["card_border"])
        self._card.pack(fill="both", expand=True, padx=28, pady=(0, 22))

        self._build_header()
        tk.Frame(self._card, height=1, bg=COLORS["separator"]).pack(fill="x")

        self.main = tk.Frame(self._card, bg=COLORS["card"])
        self.main.pack(fill="both", expand=True)

    def _build_header(self):
        h = tk.Frame(self._card, bg=COLORS["card"])
        h.pack(fill="x", padx=24, pady=14)

        left = tk.Frame(h, bg=COLORS["card"])
        left.pack(side="left", fill="x", expand=True)

        for lbl, val in [
            ("JOGADOR",   self.gs["player_name"]),
            ("CATEGORIA", self.gs["theme"]),
            ("TEMPO",     None),
            ("PROGRESSO", None),
        ]:
            b = tk.Frame(left, bg=COLORS["card"])
            b.pack(side="left", padx=(0, 28))
            tk.Label(b, text=lbl, font=FONTS["stat_label"],
                     fg=COLORS["text_light"], bg=COLORS["card"]).pack(anchor="w")
            if lbl == "TEMPO":
                self.tlbl = tk.Label(b, text="00:00", font=FONTS["timer"],
                                      fg=COLORS["text_dark"], bg=COLORS["card"])
                self.tlbl.pack(anchor="w")
            elif lbl == "PROGRESSO":
                self.plbl = tk.Label(b, text="0/0", font=FONTS["stat_value"],
                                      fg=COLORS["text_dark"], bg=COLORS["card"])
                self.plbl.pack(anchor="w")
            else:
                tk.Label(b, text=val, font=FONTS["stat_value"],
                         fg=COLORS["text_dark"], bg=COLORS["card"]).pack(anchor="w")

        # Botão SAIR
        r = tk.Frame(h, bg=COLORS["card"])
        r.pack(side="right")
        c = tk.Canvas(r, width=76, height=28, bg=COLORS["card"],
                      highlightthickness=0, cursor="hand2")
        c.pack()
        c.create_rectangle(1, 1, 75, 27, fill=COLORS["card"],
                           outline=COLORS["text_dark"], width=1, tags="r")
        c.create_text(38, 14, text="SAIR", font=FONTS["btn"],
                      fill=COLORS["text_dark"])
        c.bind("<Button-1>", lambda e: self._exit())
        c.bind("<Enter>",    lambda e: c.itemconfig("r", fill=COLORS["separator"]))
        c.bind("<Leave>",    lambda e: c.itemconfig("r", fill=COLORS["card"]))

    # ── Loading ───────────────────────────────────────────────────────────────
    def _show_loading(self):
        self._clr()
        f = tk.Frame(self.main, bg=COLORS["card"])
        f.place(relx=0.5, rely=0.42, anchor="center")
        self._sc = tk.Canvas(f, width=44, height=44, bg=COLORS["card"],
                              highlightthickness=0)
        self._sc.pack()
        tk.Frame(f, height=14, bg=COLORS["card"]).pack()
        tk.Label(f, text="GERANDO PALAVRAS COM IA...", font=FONTS["loading"],
                 fg=COLORS["text_light"], bg=COLORS["card"]).pack()
        self._sang = 0
        self._spin()

    def _spin(self):
        if not self._sc.winfo_exists(): return
        self._sc.delete("all")
        cx, cy, R = 22, 22, 14
        for i in range(10):
            a = math.radians(self._sang + i*36)
            x1=cx+(R-6)*math.cos(a); y1=cy+(R-6)*math.sin(a)
            x2=cx+R*math.cos(a);     y2=cy+R*math.sin(a)
            g = 200 - int(i/10*160)
            self._sc.create_line(x1,y1,x2,y2, fill=f"#{g:02x}{g:02x}{g:02x}",
                                  width=2.5, capstyle="round")
        self._sang = (self._sang+12) % 360
        self.after(55, self._spin)

    # ── Carga ─────────────────────────────────────────────────────────────────
    def _load(self):
        self._show_loading()
        def run():
            try:
                svc   = WordGeneratorService(os.getenv("ANTHROPIC_API_KEY",""))
                words = svc.generate_words(self.gs["theme"], self.gs["theme_prompt"],
                                           self.gs["difficulty"], self.dcfg["num_words"])
                self.after(0, lambda: self._ready(words))
            except Exception as ex:
                msg = str(ex)
                self.after(0, lambda m=msg: self._err(m))
        threading.Thread(target=run, daemon=True).start()

    def _ready(self, words):
        self.gs["words"] = words
        gen = GridGenerator(self.gs["difficulty"])
        self.grid, self.wpos = gen.generate(words)
        self.cs = gen.get_cell_size()
        self._build_game()
        self._start_timer()

    def _err(self, msg):
        self._clr()
        f = tk.Frame(self.main, bg=COLORS["card"])
        f.place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(f, text="Erro ao carregar palavras", font=FONTS["title"],
                 fg=COLORS["error"], bg=COLORS["card"]).pack()
        tk.Frame(f, height=8, bg=COLORS["card"]).pack()
        tk.Label(f, text="Configure ANTHROPIC_API_KEY no arquivo .env",
                 font=FONTS["body"], fg=COLORS["text_medium"], bg=COLORS["card"]).pack()
        tk.Label(f, text=msg, font=FONTS["body"], fg=COLORS["text_light"],
                 bg=COLORS["card"], wraplength=400).pack()
        tk.Frame(f, height=16, bg=COLORS["card"]).pack()
        c = tk.Canvas(f, width=170, height=36, bg=COLORS["card"],
                      highlightthickness=0, cursor="hand2")
        c.pack()
        c.create_rectangle(0,0,170,36, fill=COLORS["btn_bg"], outline="")
        c.create_text(85,18, text="VOLTAR AO MENU", font=FONTS["btn"],
                      fill=COLORS["btn_text"])
        c.bind("<Button-1>", lambda e: self.on_exit())

    # ── Jogo ──────────────────────────────────────────────────────────────────
    def _build_game(self):
        self._clr()

        sz = self.dcfg["grid_size"]
        cs = self.cs
        self.gsz = sz

        # Container centralizado
        center = tk.Frame(self.main, bg=COLORS["card"])
        center.pack(expand=True, fill="both")

        # Frame interno que vai ser centralizado
        wrap = tk.Frame(center, bg=COLORS["card"])
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Grade
        cv = tk.Canvas(wrap, width=sz*cs, height=sz*cs,
                       bg=COLORS["card"], highlightthickness=0, cursor="crosshair")
        cv.grid(row=0, column=0, padx=(0, 40))
        self.cv = cv

        for r in range(sz):
            for c in range(sz):
                x0, y0 = c*cs, r*cs
                rect = cv.create_rectangle(x0, y0, x0+cs, y0+cs,
                    fill=COLORS["card"], outline=COLORS["grid_line"], width=0.5)
                fnt = FONTS["cell"] if cs >= 36 else FONTS["cell_sm"]
                txt = cv.create_text(x0+cs//2, y0+cs//2,
                    text=self.grid[r][c], font=fnt, fill=COLORS["text_dark"])
                self.citems[(r,c)] = (rect, txt)
                self.cstates[(r,c)] = "normal"

        cv.bind("<ButtonPress-1>",   self._press)
        cv.bind("<B1-Motion>",       self._drag)
        cv.bind("<ButtonRelease-1>", self._release)

        # Painel de palavras ao lado da grade
        side = tk.Frame(wrap, bg=COLORS["card"])
        side.grid(row=0, column=1, sticky="n", pady=4)

        tk.Label(side, text="PALAVRAS", font=FONTS["section_lbl"],
                 fg=COLORS["text_light"], bg=COLORS["card"]).pack(anchor="w")
        tk.Frame(side, height=1, bg=COLORS["separator"]).pack(fill="x", pady=8)

        for word in self.gs["words"]:
            rw = tk.Frame(side, bg=COLORS["card"])
            rw.pack(fill="x", pady=3)
            d = tk.Label(rw, text="—", font=FONTS["word_list"],
                         fg=COLORS["text_light"], bg=COLORS["card"], width=2)
            d.pack(side="left")
            l = tk.Label(rw, text=word, font=FONTS["word_list"],
                         fg=COLORS["text_medium"], bg=COLORS["card"], anchor="w")
            l.pack(side="left")
            self.wlabels[word] = (d, l)

        self.plbl.config(text=f"0/{len(self.gs['words'])}")

    # ── Seleção ───────────────────────────────────────────────────────────────
    def _cat(self, x, y):
        r, c = y//self.cs, x//self.cs
        return (r,c) if 0<=r<self.gsz and 0<=c<self.gsz else None

    def _line(self, a, b):
        if not(a and b): return [a] if a else []
        r1,c1=a; r2,c2=b; dr,dc=r2-r1,c2-c1
        if   dr==0:            st=(0, 1 if dc>0 else -1)
        elif dc==0:            st=(1 if dr>0 else -1, 0)
        elif abs(dr)==abs(dc): st=(1 if dr>0 else -1, 1 if dc>0 else -1)
        else:                  return [a]
        sr,sc=st; n=max(abs(dr),abs(dc))
        return [(r1+i*sr, c1+i*sc) for i in range(n+1)]

    def _press(self, e):
        c=self._cat(e.x,e.y)
        if c: self._sel=True; self._s0=c; self._hi([c])

    def _drag(self, e):
        if self._sel and self._s0:
            c=self._cat(e.x,e.y)
            if c: self._hi(self._line(self._s0,c))

    def _release(self, e):
        if not self._sel: return
        self._sel=False
        c=self._cat(e.x,e.y)
        if c and self._s0: self._chk(self._line(self._s0,c))
        for p in self._scells:
            if self.cstates.get(p)!="found": self._col(p,"normal")
        self._scells=[]; self._s0=None

    def _hi(self, cells):
        for p in self._scells:
            if self.cstates.get(p)!="found": self._col(p,"normal")
        self._scells=cells
        for p in cells:
            if self.cstates.get(p)!="found": self._col(p,"selected")

    def _col(self, pos, state):
        if pos not in self.citems: return
        rect,txt=self.citems[pos]
        if   state=="normal":   self.cv.itemconfig(rect,fill=COLORS["card"]);         self.cv.itemconfig(txt,fill=COLORS["text_dark"])
        elif state=="selected": self.cv.itemconfig(rect,fill=COLORS["selected_bg"]); self.cv.itemconfig(txt,fill=COLORS["accent_dark"])
        elif state=="found":    self.cv.itemconfig(rect,fill=COLORS["found_bg"]);     self.cv.itemconfig(txt,fill=COLORS["found_text"])

    def _chk(self, cells):
        if len(cells)<2: return
        sel="".join(self.grid[r][c] for r,c in cells)
        for w in self.gs["words"]:
            if w in self.found: continue
            wc=self.wpos.get(w,[])
            if cells==wc or cells==list(reversed(wc)): self._mark(w,cells); return
            if sel==w or sel==w[::-1]: self._mark(w,cells); return

    def _mark(self, word, cells):
        self.found.add(word)
        for p in cells: self.cstates[p]="found"; self._col(p,"found")
        if word in self.wlabels:
            d,l=self.wlabels[word]
            d.config(text="✓", fg=COLORS["found_text"])
            l.config(fg=COLORS["found_text"], font=FONTS["word_found"])
        n=len(self.gs["words"]); f=len(self.found)
        self.plbl.config(text=f"{f}/{n}")
        if f==n: self.after(400, self._finish)

    # ── Timer ─────────────────────────────────────────────────────────────────
    def _start_timer(self):
        self._t0=time.time(); self._trun=True; self._tick()

    def _tick(self):
        if not self._trun: return
        el=int(time.time()-self._t0)
        rm=self.dcfg["time_limit"]-el
        m,s=abs(rm)//60,abs(rm)%60
        self.tlbl.config(text=f"{m:02d}:{s:02d}",
                         fg=COLORS["error"] if rm<=30 else COLORS["text_dark"])
        self.gs["time_elapsed"]=el
        if rm<=0: self._finish(timeout=True); return
        self.after(1000,self._tick)

    def _finish(self, timeout=False):
        self._trun=False
        self.gs["found_words"]=list(self.found)
        tot=len(self.gs["words"]); fnd=len(self.found)
        el=self.gs["time_elapsed"]; tl=self.dcfg["time_limit"]
        base=fnd*100; bonus=max(0,(tl-el)*2) if not timeout else 0
        mult={"Fácil":1,"Médio":1.5,"Difícil":2}[self.gs["difficulty"]]
        self.gs.update({"score":int((base+bonus)*mult),"timeout":timeout,"total_words":tot})
        self.after(200,self.on_finish)

    def _exit(self):
        self._trun=False
        self.gs.update({"found_words":list(self.found),"score":0})
        self.on_exit()

    def _clr(self):
        for w in self.main.winfo_children(): w.destroy()

    def destroy(self):
        self._trun=False; super().destroy()
