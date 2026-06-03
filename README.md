# Caça-Palavras com IA

Jogo de caça-palavras em Python com palavras geradas dinamicamente pela API Claude (Anthropic). Interface gráfica elegante com 14 temas, 3 níveis de dificuldade e timer.

---

## Funcionalidades

- **3 níveis de dificuldade** — Fácil (10x10), Médio (13x13), Difícil (16x16)
- **14 temas** — Mundo, Economia, Esporte, Comida, Carros, Biologia, Astrologia, Música, Tecnologia, Cinema, Literatura, Natureza, História e Arte
- **Palavras geradas por IA** — Cada partida tem palavras únicas geradas pelo Claude
- **Timer** — Tempo limitado por dificuldade com aviso visual
- **Sistema de pontuação** — Baseado em palavras encontradas, tempo e dificuldade
- **Seleção interativa** — Clique e arraste para selecionar palavras na grade
- **Design elegante** — Interface inspirada em design editorial minimalista

---

## Requisitos

- Python 3.11 ou superior
- VS Code (recomendado)
- Chave de API da Anthropic — obtenha em [console.anthropic.com](https://console.anthropic.com)

---

## Instalação

**1. Clone ou extraia o projeto**

```bash
cd caca_palavras
```

**2. Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure a chave de API**

Crie um arquivo `.env` na raiz do projeto:

```
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
```

**5. Execute o jogo**

```bash
python main.py
```

---

## Estrutura do Projeto

```
caca_palavras/
├── main.py                    # Ponto de entrada
├── requirements.txt           # Dependências
├── .env                       # Chave de API (não versionar)
├── .env.example               # Modelo de configuração
└── src/
    ├── app.py                 # Controlador de navegação
    ├── config.py              # Cores, fontes, temas e dificuldades
    ├── grid_generator.py      # Geração da grade
    ├── word_generator.py      # Integração com API Anthropic
    ├── widgets.py             # Componentes de interface
    └── screens/
        ├── menu_screen.py     # Tela inicial
        ├── setup_screen.py    # Nome do jogador
        ├── game_screen.py     # Tela de jogo
        └── result_screen.py   # Tela de resultado
```

---

## Como Jogar

1. Na tela inicial, selecione o nível de dificuldade e o tema
2. Digite seu nome e clique em **Jogar**
3. Aguarde a geração das palavras pela IA
4. Clique e arraste sobre as letras para selecionar palavras na grade
5. Encontre todas as palavras antes do tempo acabar

### Direções por nível

| Nível   | Grade  | Palavras | Tempo | Direções                     |
|---------|--------|----------|-------|------------------------------|
| Fácil   | 10x10  | 6        | 5 min | Horizontal, vertical         |
| Médio   | 13x13  | 9        | 4 min | + diagonal                   |
| Difícil | 16x16  | 12       | 3 min | + todas invertidas           |

---

## Dependências

| Pacote         | Descrição                        |
|----------------|----------------------------------|
| anthropic      | API Claude para geração de palavras |
| python-dotenv  | Carregamento de variáveis de ambiente |
| tkinter        | Interface gráfica (incluso no Python) |

---

## Configuração no VS Code

Adicione ao `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Caca-Palavras",
            "type": "python",
            "request": "launch",
            "program": "main.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```

---

## Observações

- O arquivo `.env` não deve ser versionado — adicione ao `.gitignore`
- Caso a API esteja indisponível, o jogo utiliza palavras de fallback automaticamente
- A pontuação é calculada com base nas palavras encontradas, tempo restante e multiplicador de dificuldade

---

## API Utilizada

Este projeto utiliza a **API Claude da Anthropic** (modelo pago) para geração dinâmica de palavras temáticas em cada partida. O uso da API é cobrado por volume de tokens processados.

- Plataforma: [console.anthropic.com](https://console.anthropic.com)
- Modelo utilizado: `claude-haiku-4-5`
- Autenticação: chave de API configurada no arquivo `.env`
- Cobrança: pré-pago por tokens consumidos (geração de palavras por partida)

---

## Referência Bibliográfica

RUSSELL, Stuart J.; NORVIG, Peter. **Inteligência artificial: uma abordagem moderna**. 4. ed. Rio de Janeiro: GEN LTC, 2022.
