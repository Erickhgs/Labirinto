import pygame
import numpy as np
import csv
import random
import threading

class Maze:

    '''
    O labirinto é representado por uma matriz binária em arquivo. Onde
    o valor 0 representa um quadrado da parede do labirinto, e o valor 1 representa 
    um quadrado do corredor do labirinto.
    
    O labirinto em memória é representado por uma matriz inteira, indicando para cada
    quadrado se o mesmo é uma parede, um corredor, o prêmio ou o jogador.
    '''
    
    WALL = 0
    HALL = 1
    PLAYER = 2
    PRIZE = 3
    TRAIL = 4
    
    def __init__(self):
        '''
        Inicializa a matriz de inteiros M que representa a lógica do labirinto

        '''
        self.M = None #matriz que representa o labirinto
        pygame.init()
        self.screen = None
        self.cell_size = 15
        

    
    def load_from_csv(self, file_path : str):
        '''
        Função para carregar a matriz de um arquivo CSV  

        Parameters
        ----------
        file_path : str
            Nome do arquivo contendo a matriz binária que descreve o labirinto.

        '''
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.M = np.array([list(map(int, row)) for row in reader])
            
    def init_player(self):

    #Coloca o prêmio (quadrado amarelo) e o jogador (quadrado azul)
    #em posições aleatórias no corredor do labirinto.
 
    # Escolhendo a posição aleatória do player em um corredor
     while True:
        posx = random.randint(2, 39)
        posy = random.randint(2, 39)
        if self.M[posx, posy] == Maze.HALL:
            self.init_pos_player = (posx, posy)
            self.M[posx, posy] = Maze.PLAYER  # Atualiza a matriz para refletir a posição do jogador
            break
    
    # Escolhendo a posição aleatória do premio em um corredor
     while True:
        posx = random.randint(2, 39)
        posy = random.randint(2, 39)
        if self.M[posx, posy] == Maze.HALL:
            self.M[posx, posy] = Maze.PRIZE
            break

    def find_prize(self, pos : (int, int)) -> bool:
        '''
        O tabuleiro é dividio 
        Recebe uma posição (x,y) do tabuleiro e indica se o prêmio está contido
        naquela posição.

        Parameters
        ----------
        pos : (int, int)
            Posição do quadrado na matriz do labirinto que se deseja testar se 
            foi encontrado prêmio

        Returns
        -------
        bool
            Retorna True se o quadrado do labirinto na posição 'pos' contiver o prêmio, 
            retorna False em caso contrário.

        '''
        if self.M[pos[0], pos[1]] == Maze.PRIZE:
            return True
        else:
            return False
        
    def is_free(self, pos : (int, int)) -> bool:
        '''
        Indica se a posição fornecida está livre para o jogador acessar, ou seja, 
        se for corredor ou prêmio.

        Parameters
        ----------
        pos : (int, int)
            Posição do quadrado na matriz do labirinto que se deseja testar se 
            está livre.


        Returns
        -------
        bool
            Retorna True.

        '''
        if self.M[pos[0], pos[1]] in [Maze.HALL, Maze.PRIZE]:
            return True
        else:
            return False
        
        
    def mov_player(self, pos : (int, int)) -> None:
        '''
        Move o jogador para uma nova posição do labirinto desde que ela seja uma
        posição corredor na matriz M.

        Parameters
        ----------
        pos : (int, int)
            Nova posição (x,y) no labiritno em que o jogador será movido.

        '''
        if self.is_free(pos):
            # Limpa a posição anterior do jogador
            self.M[self.init_pos_player[0], self.init_pos_player[1]] = Maze.TRAIL  # Marca a posição anterior
            self.init_pos_player = pos
            self.M[pos[0], pos[1]] = Maze.PLAYER
            self._display()
        

    def get_init_pos_player(self) -> (int, int):
        '''
        Indica a posição inicial do jogador dentro do labirinto que foi gerada 
        de forma aleatória.

        Returns
        -------
        (int, int)
            Posição inicial (x,y) do jogador no labirinto.

        '''
        return self.init_pos_player
            
    def run(self):
        '''
        Thread responsável pela atualização da visualização do labirinto.

        '''
        th = threading.Thread(target=self._display)
        th.start()

    def resolver(self):
        '''
        Resolve o labirinto utilizando backtracking com uma pilha.
        Deixa um rastro onde o jogador passa.
        '''
        pilha = []

        # Localiza a posição inicial do jogador
        posicao_inicial =self.get_init_pos_player()
        pilha.append(posicao_inicial)

        # Cria uma matriz para marcar as posições visitadas
        visited = np.zeros_like(self.M, dtype=bool)

        # Enquanto a pilha não estiver vazia
        while pilha:
            # Retire uma localização (linha, coluna) da pilha
            posicao_atual = pilha.pop()
            linha, coluna = posicao_atual

            # Se a posição tiver o prêmio
            if self.find_prize(posicao_atual):
                pygame.quit()
                return

            # Caso contrário, se este local não contiver o prêmio 
            if not visited[linha,coluna]:
                visited[linha, coluna] = True
                self.mov_player(posicao_atual)
            
            # Deixa um rastro (marca como visitado)
                if self.M[linha, coluna] != Maze.PRIZE:
                    self.M[linha, coluna] = 4
                self._display()
                pygame.time.delay(10)

            # Examine se as casas adjacentes estão livres, se sim insira sua posição na pilha
            if linha > 0 and self.is_free((linha - 1, coluna)):
                pilha.append((linha - 1, coluna))   
            if linha < self.M.shape[0] - 1 and self.is_free((linha + 1, coluna)):
                pilha.append((linha + 1, coluna))
            if coluna > 0 and self.is_free((linha, coluna - 1)):
                pilha.append((linha, coluna - 1))
            if coluna < self.M.shape[1] - 1 and self.is_free((linha, coluna + 1)):
                pilha.append((linha, coluna + 1))


    
    def _display(self, cell_size=15):
        rows, cols = self.M.shape
        width, height = cols * cell_size, rows * cell_size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Labirinto")
    
        BLACK = (0, 0, 0)
        GRAY = (192, 192, 192)
        BLUE = (0, 0, 255)
        GOLD = (255, 215, 0)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    # Captura as teclas pressionadas
                    x, y = self.init_pos_player
                    if event.key == pygame.K_UP and x > 0 and self.is_free((x - 1, y)):
                        self.mov_player((x - 1, y))
                    elif event.key == pygame.K_DOWN and x < rows - 1 and self.is_free((x + 1, y)):
                        self.mov_player((x + 1, y))
                    elif event.key == pygame.K_LEFT and y > 0 and self.is_free((x, y - 1)):
                        self.mov_player((x, y - 1))
                    elif event.key == pygame.K_RIGHT and y < cols - 1 and self.is_free((x, y + 1)):
                        self.mov_player((x, y + 1))

            screen.fill(BLACK)
    
            for y in range(rows):
                for x in range(cols):
                    if self.M[y, x] == Maze.WALL:
                        color = BLACK
                    elif self.M[y, x] == Maze.HALL:
                        color = GRAY
                    elif self.M[y, x] == Maze.PLAYER:
                        color = BLUE
                    elif self.M[y, x] == Maze.PRIZE:
                        color = GOLD
                    elif self.M[y, x] == 4:
                        color = BLUE
                       
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    
            pygame.display.flip()