import tkinter as tk
from tkinter import ttk
import time
import threading
import winsound

TEMPO_TRABALHO = 35 * 60
TEMPO_DESCANSO = 25 * 60

def som_trabalho():
    winsound.Beep(1000, 500)

def som_descanso():
    winsound.Beep(600, 800)

class CronometroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronômetro Pomodoro")
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        self.rodando = False
        self.pausado = False
        self.segundos_restantes = 0

        # UI
        self.label_titulo = tk.Label(root, text="Pronto", font=("Arial", 18))
        self.label_titulo.pack(pady=10)

        self.label_tempo = tk.Label(root, text="00:00", font=("Arial", 40))
        self.label_tempo.pack(pady=10)

        self.progresso = ttk.Progressbar(root, length=300, mode='determinate')
        self.progresso.pack(pady=10)

        # BOTÕES
        self.botao_iniciar = tk.Button(root, text="Iniciar", command=self.iniciar, width=15)
        self.botao_iniciar.pack(pady=5)

        self.botao_pausar = tk.Button(root, text="Pausar", command=self.pausar, width=15)
        self.botao_reset = tk.Button(root, text="Resetar", command=self.resetar, width=15)

    def atualizar_ui(self, segundos, total, titulo, cor):
        mins = segundos // 60
        secs = segundos % 60

        self.label_titulo.config(text=titulo, fg=cor)
        self.label_tempo.config(text=f"{mins:02d}:{secs:02d}")

        progresso = int((1 - segundos / total) * 100)
        self.progresso['value'] = progresso

    def contagem(self, segundos, titulo, cor, callback_som):
        total = segundos
        self.segundos_restantes = segundos

        while self.segundos_restantes >= 0 and self.rodando:
            if not self.pausado:
                self.atualizar_ui(self.segundos_restantes, total, titulo, cor)
                time.sleep(1)
                self.segundos_restantes -= 1
            else:
                time.sleep(0.1)

        if self.rodando:
            callback_som()

    def iniciar(self):
        if self.rodando:
            return

        self.rodando = True

        # esconder botão iniciar
        self.botao_iniciar.pack_forget()

        # mostrar outros botões
        self.botao_pausar.pack(pady=5)
        self.botao_reset.pack(pady=5)

        thread = threading.Thread(target=self.executar)
        thread.start()

    def executar(self):
        # Trabalho
        self.contagem(TEMPO_TRABALHO, "Exercícios", "green", som_trabalho)

        if not self.rodando:
            return

        time.sleep(2)

        # Descanso
        self.contagem(TEMPO_DESCANSO, "Descanso", "blue", som_descanso)

        self.label_titulo.config(text="Ciclo completo!", fg="black")
        self.rodando = False

    def pausar(self):
        self.pausado = not self.pausado

        if self.pausado:
            self.botao_pausar.config(text="Continuar")
        else:
            self.botao_pausar.config(text="Pausar")

    def resetar(self):
        self.rodando = False
        self.pausado = False
        self.segundos_restantes = 0

        self.label_titulo.config(text="Resetado", fg="black")
        self.label_tempo.config(text="00:00")
        self.progresso['value'] = 0

        # voltar botão iniciar
        self.botao_pausar.pack_forget()
        self.botao_reset.pack_forget()
        self.botao_iniciar.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = CronometroApp(root)
    root.mainloop()