# -*- coding: utf-8 -*-
import tkinter as tk
from src.app import CacaPalavrasApp

def main():
    root = tk.Tk()
    root.title("Caca-Palavras")
    root.configure(bg="#F2EDE7")
    root.resizable(True, True)
    CacaPalavrasApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
