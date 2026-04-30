import dearpygui.dearpygui as dpg
import cv2
import numpy as np
import threading
import queue
from camera import threadCamera

# Canal de comunicação entre as threads. Só segura 1 frame. Se tiver algum frame esperando, ele descarta o novo ao invés de acumular
fila_frame = queue.Queue(maxsize=1)
# Vai dizer se a câmera está capturando ou não
captura = None
# Vai indicar se as threads estão funcionando
rodando = True



