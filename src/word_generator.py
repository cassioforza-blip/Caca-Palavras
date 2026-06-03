# -*- coding: utf-8 -*-
"""
Serviço de geração de palavras via API Anthropic (Claude)
"""

import anthropic
import json
import re
import os
from src.config import API_MODEL


class WordGeneratorService:
    """Gera palavras temáticas usando a API Claude."""

    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY não encontrada. Configure no arquivo .env")
        self.client = anthropic.Anthropic(api_key=key)

    def generate_words(self, theme: str, theme_prompt: str, difficulty: str, num_words: int) -> list[str]:
        """
        Gera palavras para o jogo baseado no tema e dificuldade.
        
        Args:
            theme: Nome do tema (ex: "Esporte")
            theme_prompt: Descrição do tema para o prompt
            difficulty: Nível de dificuldade ("Fácil", "Médio", "Difícil")
            num_words: Número de palavras a gerar
            
        Returns:
            Lista de palavras em maiúsculas, sem acentos
        """
        # Define comprimento das palavras por dificuldade
        length_rules = {
            "Fácil": "entre 4 e 6 letras",
            "Médio": "entre 5 e 8 letras",
            "Difícil": "entre 7 e 12 letras",
        }
        length_rule = length_rules.get(difficulty, "entre 4 e 8 letras")

        prompt = f"""Você é um assistente de jogos educativos. Gere exatamente {num_words} palavras em português relacionadas ao tema: {theme}.

O tema abrange: {theme_prompt}

Regras OBRIGATÓRIAS:
1. Cada palavra deve ter {length_rule}
2. Use apenas letras do alfabeto (A-Z), SEM acentos, cedilha ou caracteres especiais
3. Substitua: Ã→A, Á→A, À→A, Â→A, É→E, Ê→E, Í→I, Ó→O, Ô→O, Õ→O, Ú→U, Ç→C
4. Palavras simples (sem espaços, sem hífens)
5. Todas em MAIÚSCULAS
6. Palavras devem ser facilmente reconhecíveis no tema "{theme}"
7. Não repita palavras

Responda APENAS com um JSON válido neste formato exato:
{{
  "palavras": ["PALAVRA1", "PALAVRA2", "PALAVRA3"]
}}

Nada além do JSON."""

        try:
            message = self.client.messages.create(
                model=API_MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )

            content = message.content[0].text.strip()

            # Extrai JSON mesmo se vier com backticks
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                data = json.loads(match.group())
                words = data.get("palavras", [])

                # Sanitiza e valida
                clean_words = []
                for w in words:
                    w = str(w).upper().strip()
                    w = self._remove_accents(w)
                    w = re.sub(r'[^A-Z]', '', w)  # Remove não-letras
                    if 3 <= len(w) <= 15:
                        clean_words.append(w)

                if len(clean_words) >= 3:
                    return clean_words[:num_words]

        except Exception as e:
            print(f"Erro na API: {e}")

        # Fallback: palavras padrão por tema
        return self._get_fallback_words(theme, num_words)

    def _remove_accents(self, text: str) -> str:
        """Remove acentos e caracteres especiais."""
        replacements = {
            'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
            'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            'Ç': 'C', 'Ñ': 'N',
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def _get_fallback_words(self, theme: str, num_words: int) -> list[str]:
        """Palavras de fallback caso a API falhe."""
        fallbacks = {
            "mundo": ["BRASIL", "EUROPA", "OCEANO", "AFRICA", "CULTURA", "CAPITAL", "IDIOMA", "PLANETA", "PAIS", "MAPA", "NORTE", "SUL"],
            "economia": ["MERCADO", "BANCO", "MOEDA", "BOLSA", "LUCRO", "IMPOSTO", "CAPITAL", "CAMBIO", "INFLACAO", "CREDITO", "DIVIDA", "RENDA"],
            "esporte": ["FUTEBOL", "OLIMPICO", "CAMPEAO", "ATLETISMO", "NADADOR", "GOLEIRO", "ESTADIO", "MEDALHA", "CORRIDA", "BASQUETE", "TENIS", "VOLEI"],
            "comida": ["FEIJAO", "CHURRASCO", "FEIJOADA", "MANDIOCA", "CAIPIRINHA", "BRIGADEIRO", "ACAI", "PIMENTA", "FARINHA", "TAPIOCA", "COXINHA", "PASTEL"],
            "carros": ["MOTOR", "VOLANTE", "FERRARI", "PNEU", "FREIO", "TURBO", "CHASSI", "CAMBIO", "PISTAO", "ESCAPE", "RADIADOR", "CILINDRO"],
            "biologia": ["CELULA", "NUCLEO", "GENE", "PROTEINA", "ENZIMA", "MITOSE", "VEGETAL", "ANIMAL", "FUNGO", "BACTERIA", "VIRUS", "EVOLUCAO"],
            "astrologia": ["SIGNO", "TOURO", "GEMEOS", "CANCER", "LEAO", "VIRGEM", "LIBRA", "ESCORPIAO", "SAGITARIO", "CAPRICORNIO", "AQUARIO", "PEIXES"],
            "musica": ["GUITARRA", "PIANO", "BATERIA", "SAMBA", "FORRO", "TECLADO", "MELODIA", "RITMO", "COMPASSO", "ACORDE", "SOLISTA", "CORAL"],
            "tecnologia": ["INTERNET", "CODIGO", "DADOS", "REDE", "SERVIDOR", "ALGORITMO", "MEMORIA", "SISTEMA", "PROGRAMA", "NUVEM", "DIGITAL", "HARDWARE"],
            "cinema": ["DIRETOR", "ROTEIRO", "CENARIO", "ATOR", "OSCAR", "FESTIVAL", "COMEDIA", "DRAMA", "FICCAO", "ANIMACAO", "PRODUCAO", "ESTUDIO"],
            "literatura": ["ROMANCE", "POESIA", "AUTOR", "CONTO", "NARRATIVA", "GENERO", "EDICAO", "VERSO", "PROSA", "CRONICA", "EPOPEIA", "TRAGEDIA"],
            "natureza": ["FLORESTA", "OCEANO", "DESERTO", "VULCAO", "BIOMA", "ESPECIE", "HABITAT", "CORAL", "SAVANA", "TUNDRA", "PANTANAL", "MANGUE"],
            "historia": ["EGIPTO", "GUERRA", "REPUBLICA", "IMPERIO", "REVOLUCAO", "MONARQUIA", "FEUDAL", "COLONIA", "TRATADO", "BATALHA", "DYNASTY", "SECULO"],
            "arte": ["PINTURA", "ESCULTURA", "MUSEU", "GALERIA", "BARROCO", "CUBISMO", "CANVAS", "RETRATO", "RELEVO", "MOSAICO", "FRESCO", "GRAVURA"],
        }

        # Identifica chave do tema
        theme_lower = theme.lower()
        for key in fallbacks:
            if key in theme_lower:
                words = fallbacks[key][:num_words]
                return words

        # Genérico
        return ["JOGO", "PALAVRA", "LETRA", "BUSCA", "GRADE", "TEMA", "NIVEL", "TEMPO", "PONTO", "VITORIA", "DESAFIO", "RECORD"][:num_words]
