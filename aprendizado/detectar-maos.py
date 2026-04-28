import cv2
import mediapipe as mp
import subprocess


# Detectar as mãos
class DetectarMaos:
    """Classe responsável pela detecção das mãos"""
    def __init__(self, modo=False, max_maos=2, deteccao_confianca=0.5, rastreio_confianca=0.5, cor_vertices=(0,187,255), cor_arestas=(0,0,0)):
       
        """
        Função responsável por inicializar a classe.
        
        :param modo: vai dizer se vai ficar detectando as mãos a todo momento (True: Boa detecção, porém lento. False: Detecção mediana, rápido)

        :param max_maos: Vai dizer quantas mãos podem ser detectadas

        :param deteccao_confianca: Percentual da taxa de detecção. Se for menor que 0.5, a detecção não ocorre

        :param rastreio_confianca: Percentual da taxa de rastreio. Se for menor que 0.5, o rastreio não ocorre

        :param cor_vertices: cor dos pontos da mão (bolinhas)

        :param cor_arestas: cor das conexões da mão (linhas)
        """

        # Inicializar os parâmetros
        self.modo = modo
        self.max_maos = max_maos
        self.deteccao_confianca = deteccao_confianca
        self.rastreio_confianca = rastreio_confianca
        self.cor_vertices = cor_vertices
        self.cor_arestas = cor_arestas

        # Incializar os módulos de detecção das mãos (mediapipe)
        self.maos_mp = mp.solutions.hands
        self.maos = self.maos_mp.Hands(
            self.modo,
            self.max_maos,
            1, # Complexidade do modelo. 1 = complexidade padrão
            self.deteccao_confianca,
            self.rastreio_confianca
        )

        # Função para desenhar o grafo da mão
        self.desenho_mp = mp.solutions.drawing_utils

        # Configurações do desenho dos vertices
        self.desenho_config_v = self.desenho_mp.DrawingSpec(color=self.cor_vertices)

        # Configurações do desenho das arestas
        self.desenho_config_a = self.desenho_mp.DrawingSpec(color=self.cor_arestas)

    def encontrar_maos(self, imagem, desenho=True):
        """
        Função responsável por detectar as mãos

        :param imagem: Vai receber a imagem da webcam

        :param desenho: Vai desenhar o grafo da mão

        :return: Retorna a imagem desenhada
        """    

        # Converter a imagem de BGR para RGB
        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        # Passar a imagem convertida para o detector
        self.resultado = self.maos.process(imagem_rgb)

        # Verificar se alguma mão foi detectada
        if self.resultado.multi_hand_landmarks:
            for vertice in self.resultado.multi_hand_landmarks:
                # print(vertice) vai mostrar as coordenadas dos vertices (x,y,z)
                if desenho:
                    # Desenhar os grafos nas mãos detectadas 
                    self.desenho_mp.draw_landmarks(
                        imagem, # Imagem de captura
                        vertice, # Vertices das mãos
                        self.maos_mp.HAND_CONNECTIONS, # Conexão entre os vertices
                        self.desenho_config_v, # Cor dos vertices
                        self.desenho_config_a, # Cor das arestas                
                    ) 

        return imagem            

    def encontrar_vertices(self, imagem, mao_num=0, desenho=True, cor=(255,255,255), raio=7, vertice_detectado=0):
        
        """
        Função responsável por encontrar a posição dos vertices das mãos

        :param imagem: Imagem capturada pela webcam

        :param mao_num: Número da mão detectada pela função (0,1)

        :param desenho: True: O desenho aparece. False: O desenho não aparece

        :param cor: Cor do vertice

        :param raio: Tamanho do vertice

        :param vertice_detectado: Vertice a ser detectado

        :return: Lista dos vertices detectados
        """

        # Lista com os vertices detectados
        lista_v = []

        # Verificar se alguma mão foi detectada
        if self.resultado.multi_hand_landmarks:
            # Obter os vertices da mão detectada
            mao = self.resultado.multi_hand_landmarks[mao_num]

            # Obter as informações dos pontos
            for id, vertice in enumerate(mao.landmark):
                # print(id,vertice) vai mostrar o número dos vertices e suas coordenadas

                # Obter as dimensões da imagem capturada
                altura, largura, canal = imagem.shape

                # Transformar a posição do vertice de proporção para pixel
                centro_x, centro_y = int(vertice.x * largura), int(vertice.y * altura)

                # Adicionar os vertices da mão detectada na lista
                lista_v.append([id, centro_x, centro_y])

                # Colocar circulo em um vertice
                if desenho:
                    if id == vertice_detectado:
                        cv2.circle(
                            imagem, # Imagem da captura
                            (centro_x, centro_y), # Centro do circulo
                            raio, # Tamanho do circulo
                            cor, # Cor do circulo
                            cv2.FILLED # Espessura do circulo
                        )

        return lista_v        



def main():
    # Capturar a imagem da webcam
    captura = cv2.VideoCapture(0)

    # Instanciar a classe do detector
    detector = DetectarMaos()

    # Aplicar filtro na imagem
    subprocess.Popen(["bash", "webcam.sh"])

    # Realizar a captura
    while True:
        # Obter a imagem
        verificacao, imagem = captura.read()

        if not verificacao:
            print("Verificação falhou")
            break

        # Espelhar a imagem
        imagem = cv2.flip(imagem, 1)

        # Realizar a detecção das mãos
        imagem = detector.encontrar_maos(imagem, desenho=True)

        # Lista com os vertices
        lista_vertices = detector.encontrar_vertices(imagem, vertice_detectado=12)
        

        # Mostrar a imagem capturada
        cv2.imshow('Webcam', imagem)

        # Taxa de atualização
        if cv2.waitKey(1) & 0xFF == 27: # Atraso de 1ms e ESC pra sair
            break


if __name__ == "__main__":
    main()        
         