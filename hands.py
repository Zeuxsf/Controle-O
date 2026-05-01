import mediapipe as mp
import cv2

class DetectarMaos:
    def __init__(self, modo=False, max_maos=2, deteccao_confianca=0.5, rastreio_confianca=0.5, cor_vertices=(0,187,255), cor_arestas=(0,0,0)):
        
        self.modo = modo
        self.max_maos = max_maos
        self.deteccao_confianca = deteccao_confianca
        self.rastreio_confianca = rastreio_confianca
        self.cor_vertices = cor_vertices
        self.cor_arestas = cor_arestas

        # Inicializando os módulos que detectam as mãos
        self.maos_mp = mp.solutions.hands
        self.maos = self.maos_mp.Hands(
            self.modo,
            self.max_maos,
            1,
            self.deteccao_confianca,
            self.rastreio_confianca
        )

        # Funções para desenhar os grafos da mão
        self.desenho_mp = mp.solutions.drawing_utils
        
        self.desenho_config_vertices = self.desenho_mp.DrawingSpec(color=self.cor_vertices)
        self.desenho_config_arestas = self.desenho_mp.DrawingSpec(color=self.cor_arestas)

    # Função para localizar as mãos na tela
    def encontrar_maos(self, imagem, desenho=True):

        # Converter a imagem recebida da camera para RGB
        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        # Passar a imagem convertida para o detector de mãos
        self.resultado = self.maos.process(imagem_rgb)

        # Verificar se alguma mão foi detectada
        if self.resultado.multi_hand_landmarks:
            for v in self.resultado.multi_hand_landmarks:
                if desenho: # Vai desenhar o grafo da mão caso ela seja detectada
                    self.desenho_mp.draw_landmarks(
                        imagem,
                        v,
                        self.maos_mp.HAND_CONNECTIONS,
                        self.desenho_config_vertices,
                        self.desenho_config_arestas
                    )
        return imagem

    # Função para selecionar vertices específicos
    def encontrar_vertices(self, imagem, mao_num=0, desenho=True, cor=(255,255,255), raio=7, vertice_detectado=0):
        
        # Inicializando uma lista pros vertices detectados ficarem
        lista_vertices = []

        # Verifica se a mão foi detectada
        if self.resultado.multi_hand_landmarks:
            # Obter os vertices da mão detectada
            mao = self.resultado.multi_hand_landmarks[mao_num]

            # Obtém as informações dos vertices
            for id, v in enumerate(mao.landmark):

                # Obtém as dimensões da imagem da webcam
                altura, largura, canal = imagem.shape

                # Transforma a posição do vertice (proporção para px)
                centro_x, centro_y = int(v.x * largura), int(v.y * altura)

                lista_vertices.append([id, centro_x, centro_y])

                if desenho: # Vai destacar os vertices selecionados
                    if id == vertice_detectado:
                        cv2.circle(
                            imagem,
                            (centro_x, centro_y),
                            raio,
                            cor,
                            cv2.FILLED
                        )

        return lista_vertices                