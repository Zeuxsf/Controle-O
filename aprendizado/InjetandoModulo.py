"""
Demo: Dear PyGui + OpenCV
Dependências: dearpygui opencv-python numpy
uv add dearpygui opencv-python numpy
"""
import dearpygui.dearpygui as dpg
import cv2
import numpy as np
import threading
import queue
from camera import threadCamera

# ── Estado global ─────────────────────────────────────────────────────────────
fila_frame = queue.Queue(maxsize=1)
captura = None
rodando = True

# ── Callbacks dos botões ──────────────────────────────────────────────────────
def btn_iniciar():
    dpg.set_value("status", "● Rastreamento ATIVO")
    dpg.configure_item("status", color=[0, 255, 120])

def btn_pausar():
    dpg.set_value("status", "⏸ Rastreamento PAUSADO")
    dpg.configure_item("status", color=[255, 200, 0])

def btn_sair():
    global rodando
    rodando = False
    dpg.stop_dearpygui()

# ── Thread da câmera ──────────────────────────────────────────────────────────
camera = threadCamera(fila_frame)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    dpg.create_context()

    CAM_W, CAM_H = 640, 480

    # Textura inicial preta
    dados_iniciais = [0.0] * (CAM_W * CAM_H * 4)

    with dpg.texture_registry():
        dpg.add_dynamic_texture(
            width=CAM_W,
            height=CAM_H,
            default_value=dados_iniciais,
            tag="textura_camera"
        )

    # ── Layout principal ──────────────────────────────────────────────────────
    with dpg.window(label="Controle-O", tag="janela_principal", no_close=True):

        # Título
        dpg.add_text("CONTROLE-O", color=[0, 200, 255])
        dpg.add_separator()
        dpg.add_spacer(height=4)

        # Layout horizontal: câmera | painel de controle
        with dpg.group(horizontal=True):

            # Feed da câmera
            dpg.add_image("textura_camera", width=CAM_W, height=CAM_H)

            dpg.add_spacer(width=16)

            # Painel direito
            with dpg.group():
                dpg.add_text("Controles", color=[180, 180, 180])
                dpg.add_spacer(height=8)

                dpg.add_button(
                    label="▶  Iniciar Rastreamento",
                    callback=btn_iniciar,
                    width=220,
                    height=44
                )
                dpg.add_spacer(height=6)

                dpg.add_button(
                    label="⏸  Pausar",
                    callback=btn_pausar,
                    width=220,
                    height=44
                )
                dpg.add_spacer(height=6)

                dpg.add_button(
                    label="✕  Sair",
                    callback=btn_sair,
                    width=220,
                    height=44
                )

                dpg.add_spacer(height=20)
                dpg.add_separator()
                dpg.add_spacer(height=8)

                dpg.add_text("Status:", color=[180, 180, 180])
                dpg.add_text("● Aguardando...", tag="status", color=[120, 120, 120])

                dpg.add_spacer(height=20)
                dpg.add_separator()
                dpg.add_spacer(height=8)

                dpg.add_text("Info", color=[180, 180, 180])
                dpg.add_text(f"Resolução: {CAM_W}x{CAM_H}", color=[100, 100, 100])
                dpg.add_text("Backend: CPU (MediaPipe)", color=[100, 100, 100])

    # Viewport
    dpg.create_viewport(
        title="Controle-O",
        width=CAM_W + 300,
        height=CAM_H + 60,
        resizable=False
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("janela_principal", True)

    # Inicia thread da câmera
    t = threading.Thread(target=camera.executar_thread, daemon=True)
    t.start()

    # Loop principal — atualiza frame a cada iteração
    while dpg.is_dearpygui_running():
        camera.atualizar_frame()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    main()
