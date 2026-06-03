# -*- coding: utf-8 -*-

COLORS = {
    "bg":           "#F2EDE7",
    "card":         "#FDFCFB",
    "card_border":  "#E8E0D8",
    "text_dark":    "#1A1A1A",
    "text_medium":  "#6B6560",
    "text_light":   "#B0A89E",
    "accent":       "#C4A882",
    "accent_dark":  "#9E7E56",
    "accent_light": "#F0E6D6",
    "found_text":   "#4A7C59",
    "found_bg":     "#EBF4EE",
    "selected_bg":  "#F5EAD8",
    "btn_bg":       "#1A1A1A",
    "btn_text":     "#FDFCFB",
    "error":        "#A63228",
    "separator":    "#EBE5DE",
    "grid_line":    "#EDE7E0",
}

FONT_SERIF = "Georgia"
FONT_SANS  = "Segoe UI"

FONTS = {
    "hero":         (FONT_SERIF, 40, "bold"),
    "title":        (FONT_SERIF, 20, "bold"),
    "subtitle":     (FONT_SERIF, 10, "italic"),
    "stat_label":   (FONT_SANS,  7),
    "stat_value":   (FONT_SERIF, 12, "bold"),
    "timer":        (FONT_SERIF, 16, "bold"),
    "btn":          (FONT_SANS,  9),
    "cell":         (FONT_SERIF, 12, "bold"),
    "cell_sm":      (FONT_SERIF,  9, "bold"),
    "word_list":    (FONT_SANS,   9),
    "word_found":   (FONT_SANS,   9, "bold"),
    "section_lbl":  (FONT_SANS,   7),
    "body":         (FONT_SANS,   9),
    "quote":        (FONT_SERIF, 10, "italic"),
    "author":       (FONT_SANS,   7),
    "loading":      (FONT_SANS,   8),
    "diff_name":    (FONT_SERIF, 11, "bold"),
    "diff_desc":    (FONT_SANS,   8),
    "theme_lbl":    (FONT_SANS,   9),
}

DIFFICULTIES = {
    "Fácil": {
        "label": "Fácil",
        "grid_size": 10, "num_words": 6, "time_limit": 300,
        "directions": ["H", "V"],
        "description": "10 × 10   ·   6 palavras   ·   5 min",
        "win_w": 760, "win_h": 640,
    },
    "Médio": {
        "label": "Médio",
        "grid_size": 13, "num_words": 9, "time_limit": 240,
        "directions": ["H", "V", "D"],
        "description": "13 × 13   ·   9 palavras   ·   4 min",
        "win_w": 940, "win_h": 760,
    },
    "Difícil": {
        "label": "Difícil",
        "grid_size": 16, "num_words": 12, "time_limit": 180,
        "directions": ["H", "V", "D", "HR", "VR", "DR"],
        "description": "16 × 16   ·   12 palavras   ·   3 min",
        "win_w": 1100, "win_h": 880,
    },
}

THEMES = {
    "Mundo":      {"key": "mundo",      "prompt": "países, capitais, continentes, oceanos, culturas, idiomas, monumentos"},
    "Economia":   {"key": "economia",   "prompt": "finanças, mercado, investimentos, moedas, bolsa de valores, bancos, inflação"},
    "Esporte":    {"key": "esporte",    "prompt": "modalidades esportivas, atletas famosos, competições olímpicas, times, campeonatos"},
    "Comida":     {"key": "comida",     "prompt": "culinária brasileira e mundial, ingredientes, técnicas culinárias, pratos típicos"},
    "Carros":     {"key": "carros",     "prompt": "marcas de automóveis, modelos famosos, peças de carro, motorsport, tecnologia automotiva"},
    "Biologia":   {"key": "biologia",   "prompt": "seres vivos, células, genética, ecossistemas, evolução, anatomia, botânica"},
    "Astrologia": {"key": "astrologia", "prompt": "signos do zodíaco, planetas, astros, astronomia, constelações, cosmos, universo"},
    "Música":     {"key": "musica",     "prompt": "gêneros musicais, instrumentos, compositores, bandas famosas, termos musicais"},
    "Tecnologia": {"key": "tecnologia", "prompt": "programação, computadores, inteligência artificial, internet, inovações"},
    "Cinema":     {"key": "cinema",     "prompt": "filmes clássicos, diretores famosos, atores, gêneros cinematográficos, prêmios"},
    "Literatura": {"key": "literatura", "prompt": "autores clássicos, gêneros literários, obras famosas, personagens literários"},
    "Natureza":   {"key": "natureza",   "prompt": "plantas, animais, biomas, clima, fenômenos naturais, conservação, meio ambiente"},
    "História":   {"key": "historia",   "prompt": "civilizações antigas, guerras históricas, personalidades históricas, períodos"},
    "Arte":       {"key": "arte",       "prompt": "movimentos artísticos, pintores, escultores, estilos de arte, museus famosos"},
}

QUOTES = [
    ("Na natureza nada se cria, nada se perde, tudo se transforma.", "Antoine Lavoisier"),
    ("A imaginação é mais importante que o conhecimento.", "Albert Einstein"),
    ("O segredo do sucesso é começar.", "Mark Twain"),
    ("O conhecimento é poder.", "Francis Bacon"),
    ("Não é o mais forte que sobrevive, mas o mais adaptável.", "Charles Darwin"),
    ("A educação é a arma mais poderosa que você pode usar.", "Nelson Mandela"),
    ("A vida é aquilo que acontece enquanto você faz outros planos.", "John Lennon"),
]

API_MODEL = "claude-haiku-4-5-20251001"
