import dearpygui.dearpygui as dpg
import cv2
import numpy as np
import threading
import queue
import subprocess
from camera import threadCamera

# Canal de comunicação entre as threads. Só segura 1 frame. Se tiver algum frame esperando, ele descarta o novo ao invés de acumular
fila_frame = queue.Queue(maxsize=1)

class Interface():
    def __init__(self):

        global fila_frame
        # Thread da camera
        self.camera = threadCamera(fila_frame) 

        # Inicializa o DPG
        dpg.create_context()

        # Tamanho da textura da câmera
        self.CAM_W, self.CAM_H = 640,480

        # A textura precisa existir antes da janela, por isso é criada aqui. Essa variável é uma lista de zeros que preenche a textura com preto
        self.dados_iniciais = [0.0] * (self.CAM_W * self.CAM_H * 4)

        # Gerenciador de texturas
        with dpg.texture_registry():
            
            # Cria uma textura que pode ser atualizada dinâmicamente (video)
            dpg.add_dynamic_texture(
                width=self.CAM_W,
                height=self.CAM_H,
                default_value=self.dados_iniciais, # Conteúdo inicial da textura
                tag="textura_camera" # ID da textura
            )

        # Interface gráfica:
        self._criar_janela()

        # Camera
        self._t_camera()

        while dpg.is_dearpygui_running():
            self.camera.atualizar_frame()
            dpg.render_dearpygui_frame()

    # Vai criar a janela e todos os elementos dentro dela
    def _criar_janela(self):
        # "window" é um painel flutuante. Tudo que estiver abaixo do with dele, pertence à esse painel
        with dpg.window(label="Controle-O", tag="janela_principal"):
            
            # Group é semelhante à uma DIV do HTML. É um container de widgets
            with dpg.group():

                # Vai adicionar a câmera na tela
                dpg.add_image("textura_camera", width=self.CAM_W, height=self.CAM_H)
                dpg.add_spacer(height=16)

                # O parâmetro "horizontal" serve pros widgets ficarem posicionados na horizontal, já quê, por padrão, eles ficam posicionados na vertical
                with dpg.group(horizontal=True):

                    dpg.add_button(
                        label="Aplicar Filtro",
                        callback=self._aplicar_filtro, # Vai chamar a função atribuída ao botão quando clicado
                        width=220,
                        height=44
                    )

        # Viewport é a janela do sistema operacional, que vai ser preenchida com a "window" do DPG
        dpg.create_viewport(
            title="Controle-O",
            width= self.CAM_W + 16, # Tamanho horizontal da janela
            height= self.CAM_H + 90, # Tamanho vertical da janela
            resizable= False # Vai tirar o redimensionamento da janela (Vou ativar se algum momento eu quiser adicionar responsividade ao projeto)
        )
        dpg.setup_dearpygui() # Vai processar tudo que foi criado antes de abrir a janela
        dpg.show_viewport() # Vai mostrar
        dpg.set_primary_window("janela_principal", True) # Vai setar a janela principal 

    # Inicia thread da camera
    def _t_camera(self):
        t = threading.Thread(target=self.camera.executar_thread, daemon=True) # O daemon diz pro sistema que essa thread é descartável, ou seja, não fica segurando o programa aberto caso a thread ainda não tenha terminado e você precisa fechar
        
        t.start() 

    # Vai aplicar filtro na webcam (problema pessoal, remova caso não for útil para o seu uso)
    def _aplicar_filtro(self):
        subprocess.Popen(["bash","webcam.sh"])            

app = Interface()