# -*- coding: utf-8 -*-
"""
Lógica de geração e manipulação da grade do caça-palavras
"""

import random
import string
from src.config import DIFFICULTIES


class GridGenerator:
    """Gera a grade do caça-palavras com as palavras posicionadas."""

    def __init__(self, difficulty: str):
        cfg = DIFFICULTIES[difficulty]
        self.size = cfg["grid_size"]
        self.directions = cfg["directions"]
        self.grid = []
        self.word_positions = {}  # palavra -> lista de (row, col)

    # ── Direções disponíveis ───────────────────────────────────────────────────
    DIRECTION_VECTORS = {
        "H":  (0,  1),   # Horizontal →
        "HR": (0, -1),   # Horizontal invertido ←
        "V":  (1,  0),   # Vertical ↓
        "VR": (-1, 0),   # Vertical invertido ↑
        "D":  (1,  1),   # Diagonal ↘
        "DR": (-1,-1),   # Diagonal invertida ↖
        "DA": (1, -1),   # Diagonal anti ↙
        "DAR":(-1, 1),   # Diagonal anti invertida ↗
    }

    def generate(self, words: list[str]) -> tuple[list[list[str]], dict]:
        """
        Gera a grade com as palavras inseridas.
        
        Returns:
            (grid, word_positions): grade preenchida e posições de cada palavra
        """
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.word_positions = {}

        # Tenta inserir cada palavra
        placed = []
        random.shuffle(words)

        for word in words:
            if self._place_word(word):
                placed.append(word)

        # Preenche células vazias com letras aleatórias
        self._fill_random()

        return self.grid, self.word_positions

    def _place_word(self, word: str, max_attempts: int = 200) -> bool:
        """Tenta posicionar uma palavra na grade."""
        dirs = [self.DIRECTION_VECTORS[d] for d in self.directions if d in self.DIRECTION_VECTORS]

        for _ in range(max_attempts):
            direction = random.choice(dirs)
            dr, dc = direction

            # Posição inicial válida para o comprimento da palavra
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

            end_row = row + dr * (len(word) - 1)
            end_col = col + dc * (len(word) - 1)

            if not (0 <= end_row < self.size and 0 <= end_col < self.size):
                continue

            # Verifica conflitos
            can_place = True
            for i, letter in enumerate(word):
                r = row + dr * i
                c = col + dc * i
                cell = self.grid[r][c]
                if cell != '.' and cell != letter:
                    can_place = False
                    break

            if can_place:
                positions = []
                for i, letter in enumerate(word):
                    r = row + dr * i
                    c = col + dc * i
                    self.grid[r][c] = letter
                    positions.append((r, c))
                self.word_positions[word] = positions
                return True

        return False

    def _fill_random(self):
        """Preenche células vazias com letras aleatórias."""
        letters = string.ascii_uppercase
        # Evita vogais repetidas demais - mistura equilibrada
        pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2 + "AEIOU"
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == '.':
                    self.grid[r][c] = random.choice(pool)

    def get_cell_size(self) -> int:
        """Retorna tamanho ideal da célula baseado no tamanho da grade."""
        if self.size <= 10:
            return 42
        elif self.size <= 13:
            return 34
        else:
            return 28
