import cv2
import numpy as np
import threading
import queue
import dearpygui.dearpygui as dpg

class threadCamera:
    def __init__(self, fila_frame, captura=None, rodando=True, cap_largura=640, cap_altura=480):
        self.fila_frame = fila_frame
        self.captura = captura
        self.rodando = rodando
        self.cap_largura = cap_largura
        self.cap_altura = cap_altura

        # Definindo as proporções do video
        self.captura = cv2.VideoCapture(0)
        self.captura.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_largura)
        self.captura.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_altura)

        #self.captura.release()   

    def executar_thread(self):
        while self.rodando:
            verificacao, frame = self.captura.read()
            if not verificacao:
                # Se a verificação falhar, tente de novo
                continue
            
            # Espelhar imagem
            frame = cv2.flip(frame,1)
            # Converter as cores da imagem para RGBA (A interface DPG usa esse formato)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Verificação importante: se a interface não tiver consumido o frame anterior, vai descartar o novo ao invés de esperar, evita atraso na imagem
            if not self.fila_frame.full():
                self.fila_frame.put(frame)

    def atualizar_frame(self):
        try:
            # Vai tentar pegar um frame da fila sem esperar
            frame = self.fila_frame.get_nowait()
            
            # O OpenCV entrega um frame em formato (H, W, 3) com valores 0–255 (uint8).
            # O DPG espera um buffer linear (1D) de floats entre 0.0 e 1.0.
            # Então convertemos o tipo, normalizamos e achatamos os dados.
            dados = frame.astype(np.float32) / 255.0
           
            # Vai setar a textura da camera
            dpg.set_value("textura_camera", dados)

        # ESSENCIAL. Se não tiver nenhum frame na fila ele vai ignorar e segue a diante. A interface nunca fica travada esperando a câmera
        except queue.Empty:
                pass
            





