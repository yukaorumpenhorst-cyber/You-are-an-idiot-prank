import os
import sys

def obter_caminho_recurso(caminho_relativo):
    """ Retorna o caminho correto para arquivos externos, funcionando tanto em código puro quanto no .exe compactado """
    try:
        # O PyInstaller cria uma pasta temporária chamada _MEIPASS quando o .exe roda
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, caminho_relativo)
import customtkinter as ctk
import pygame
import threading
import time
import random

# 1. Configurações Visuais
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Frases que vão aparecer nas janelas espalhadas
FRASES = [
    "YOU ARE AN IDIOT",
    "YOU ARE AN IDIOT 🎉",
    "YOU ARE AN IDIOT",
    "YOU ARE AN IDIOT",
    "YOU ARE AN IDIOT",
    "YOU ARE AN IDIOT 🖥️"
]

class JanelaPopUp(ctk.CTkToplevel):
    """Classe que cria cada uma das pequenas janelas extras"""
    def __init__(self, texto):
        super().__init__()
        
        self.title("YOU ARE AN IDIOT")
        self.geometry("300x150")
        self.resizable(False, False)
        
        # Faz a janela ficar sempre por cima das outras
        self.attributes("-topmost", True)
        
        # Sorteia uma posição aleatória na tela para a janela surgir
        pos_x = random.randint(100, 800)
        pos_y = random.randint(100, 600)
        self.geometry(f"+{pos_x}+{pos_y}")
        
        # Conteúdo da janela
        label = ctk.CTkLabel(self, text=texto, font=("Arial", 16, "bold"), wraplength=250)
        label.pack(expand=True, pady=10)
        
        botao = ctk.CTkButton(self, text="Fechar", command=self.destroy)
        botao.pack(pady=10)

class AppPrincipal(ctk.CTk):
    """Janela principal que controla a música e o surgimento das subjanelas"""
    def __init__(self):
        super().__init__()
        
        self.title("CONGRATULATIONS YOU ARE AN IDIOT!")
        self.geometry("400x200")
        
        label = ctk.CTkLabel(self, text="Congrats, you are an idiot! 😉", font=("Arial", 18))
        label.pack(expand=True)
        
        # Iniciar a música de fundo
        self.iniciar_musica()
        
        # Iniciar a geração de janelas em uma linha de execução separada (Thread)
        # Isso impede que o programa trave enquanto cria as janelas
        self.thread_janelas = threading.Thread(target=self.gerar_janelas, daemon=True)
        self.thread_janelas.start()

    def iniciar_musica(self):
        """Inicializa o player de áudio e toca a música em loop"""
        try:
            pygame.mixer.init()
            # Lembre-se de usar o nome exato do arquivo que funcionou para você (ex: "musica.mp3")
            pygame.mixer.music.load(obter_caminho_recurso("musica.mp3"))

            pygame.mixer.music.play(-1) # O número -1 faz a música tocar em loop infinito
        except Exception as e:
            print(f"Erro ao carregar a música: {e}. Verifique se o arquivo 'musica.mp3' está na mesma pasta.")

    def gerar_janelas(self):
        """Gera várias janelas com um pequeno intervalo de tempo entre elas"""
        time.sleep(1) # Espera 1 segundo após abrir o app para começar o caos
        
        # Vamos abrir 8 janelas (você pode mudar esse número)
        for _ in range(50):
            frase_sorteada = random.choice(FRASES)
            
            # Cria a nova janela de forma segura dentro da Thread principal do Tkinter
            self.after(0, lambda f=frase_sorteada: JanelaPopUp(f))
            
            time.sleep(0.5) # Espera meio segundo antes de abrir a próxima janela

if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
