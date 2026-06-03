# -*- coding: utf-8 -*-
import tkinter as tk
from src.config import COLORS, THEMES, DIFFICULTIES
from src.screens.menu_screen   import MenuScreen
from src.screens.setup_screen  import SetupScreen
from src.screens.game_screen   import GameScreen
from src.screens.result_screen import ResultScreen


class CacaPalavrasApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=COLORS["bg"])
        self.gs = {"player_name":"","theme":"","theme_key":"","theme_prompt":"",
                   "difficulty":"","words":[],"time_elapsed":0,"found_words":[],"score":0}
        self.container = tk.Frame(root, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.cur = None
        self.show_menu()

    def _resize(self, w, h):
        sw=self.root.winfo_screenwidth(); sh=self.root.winfo_screenheight()
        x=(sw-w)//2; y=(sh-h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.update_idletasks()

    def show_menu(self):
        self._clr(); self._resize(960, 820)
        self.cur = MenuScreen(self.container, on_start=self._start)
        self.cur.pack(fill="both", expand=True)

    def _start(self, diff, theme):
        td = THEMES[theme]
        self.gs.update({"theme":theme,"theme_key":td["key"],"theme_prompt":td["prompt"],
                        "difficulty":diff,"words":[],"time_elapsed":0,"found_words":[],"score":0})
        self._clr(); self._resize(640, 500)
        self.cur = SetupScreen(self.container, game_state=self.gs,
                               on_play=self.show_game, on_back=self.show_menu)
        self.cur.pack(fill="both", expand=True)

    def show_game(self):
        self._clr()
        cfg = DIFFICULTIES[self.gs["difficulty"]]
        self._resize(cfg["win_w"], cfg["win_h"])
        self.cur = GameScreen(self.container, game_state=self.gs,
                              on_finish=self.show_result, on_exit=self.show_menu)
        self.cur.pack(fill="both", expand=True)

    def show_result(self):
        self._clr(); self._resize(800, 600)
        self.cur = ResultScreen(self.container, game_state=self.gs,
                                on_play_again=self.show_menu, on_menu=self.show_menu)
        self.cur.pack(fill="both", expand=True)

    def _clr(self):
        if self.cur: self.cur.destroy(); self.cur = None
