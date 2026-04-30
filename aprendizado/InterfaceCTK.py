# Descartado por perda de performance.

import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import subprocess
from detectar_maos import DetectarMaos

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Vai chamar o script que ajusta as configurações da webcam para ambientes escuros
        subprocess.Popen(["bash", "webcam.sh"])

        self.title("Controle-O")
        
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        largura_janela = max(800, min(int(largura_tela * 0.80), 1400))
        altura_janela = max(500, min(int(altura_tela * 0.80), 900))

        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2

        self.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
        self.minsize(800, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Módulo de detecção de mãos
        self.detector = DetectarMaos()

        # Vai chamar a webcam e posicional o local em que ela vai ficar
        self.captura = cv2.VideoCapture(0)
        self.moldura = ctk.CTkLabel(self, text="")
        self.moldura.grid(row=0,column=0)
        self._atualizar_frame()    

    def _atualizar_frame(self):
        verificacao, frame = self.captura.read()


        if verificacao:
        
            frame = cv2.flip(frame, 1)

            frame = self.detector.encontrar_maos(frame)

            # Converter novamente é necessário para que as cores não fiquem invertidas
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            pil_img = Image.fromarray(frame)
        
            imagem = ctk.CTkImage(light_image=pil_img, size=(pil_img.width, pil_img.height))
        
            self.moldura.configure(image=imagem)
            self.moldura.image = imagem
        
        self.after(30, self._atualizar_frame)     


if __name__ == "__main__":
    app = App()
    app.mainloop()