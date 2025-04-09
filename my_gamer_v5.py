import pgzrun
import random

# --- Configurações ---
LARGURA = 800  # Aumentei para melhor jogabilidade
ALTURA = 600
TAMANHO_CELULA = 40  # Aumentei o tamanho da célula para sprites maiores
MAPA_LARGURA = LARGURA // TAMANHO_CELULA
MAPA_ALTURA = ALTURA // TAMANHO_CELULA

# --- Cores ---
COR_PAREDE = (50, 50, 50)
COR_CHAO = (150, 150, 150)
COR_JOGADOR = (0, 128, 255)
COR_GOBLIN = (0, 255, 0)
COR_ORC = (255, 0, 0)
COR_MENU_TEXTO = (255, 255, 255)
COR_MENSAGEM = (255, 255, 255)

# --- Estados do Jogo ---
ESTADO_MENU = 0
ESTADO_JOGANDO = 1
ESTADO_SAIR = 2

estado_jogo = ESTADO_MENU
musica_ligada = True
sons_ligados = True
mensagem = ""

# --- Mapa ---
mapa = [['#' for _ in range(MAPA_LARGURA)] for _ in range(MAPA_ALTURA)]

def criar_mapa():
    global mapa
    mapa = [['#' for _ in range(MAPA_LARGURA)] for _ in range(MAPA_ALTURA)]
    for y in range(1, MAPA_ALTURA - 1):
        for x in range(1, MAPA_LARGURA - 1):
            if random.random() < 0.7:
                mapa[y][x] = '.'
    criar_sala(5, 5, 8, 6)
    criar_sala(15, 10, 5, 4)

def criar_sala(x, y, largura, altura):
    for i in range(y, y + altura):
        for j in range(x, x + largura):
            if 0 < i < MAPA_ALTURA - 1 and 0 < j < MAPA_LARGURA - 1:
                mapa[i][j] = '.'

# --- Entidades ---
class Entidade(Actor):
    def __init__(self, x, y, imagem, cor):
        super().__init__(imagem)
        self.x = x * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = y * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.cor = cor
        self.vida = 1
        self.ataque = 1
        self.nome = "Entidade" # Para mensagens de ataque

    def mover(self, dx, dy):
        self.x += dx * TAMANHO_CELULA
        self.y += dy * TAMANHO_CELULA

    def tentar_mover(self, dx, dy):
        novo_x = self.x + dx * TAMANHO_CELULA
        novo_y = self.y + dy * TAMANHO_CELULA
        if 0 <= novo_x - TAMANHO_CELULA // 2 < LARGURA and 0 <= novo_y - TAMANHO_CELULA // 2 < ALTURA: # Verificação de limites
            if mapa[(novo_y - TAMANHO_CELULA // 2) // TAMANHO_CELULA][(novo_x - TAMANHO_CELULA // 2) // TAMANHO_CELULA] == '.':
                self.x = novo_x
                self.y = novo_y
                return True
        return False


class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 'jogador', COR_JOGADOR)  # 'jogador' é o nome da imagem
        self.vida = 10
        self.nome = "Jogador"

class Inimigo(Entidade):
    def __init__(self, x, y, nome):
        if nome == "Goblin":
            super().__init__(x, y, 'goblin', COR_GOBLIN)
            self.vida = 1
            self.ataque = 1
            self.nome = "Goblin"
        elif nome == "Orc":
            super().__init__(x, y, 'orc', COR_ORC)
            self.vida = 2
            self.ataque = 2
            self.nome = "Orc"

    def mover(self, jogador_x, jogador_y):
        # Segue o jogador
        if jogador_x > self.x:
            self.x += TAMANHO_CELULA
        elif jogador_x < self.x:
            self.x -= TAMANHO_CELULA
        if jogador_y > self.y:
            self.y += TAMANHO_CELULA
        elif jogador_y < self.y:
            self.y -= TAMANHO_CELULA

# --- Variáveis do jogo ---
jogador = None
inimigos = []
mapa = []
estado_jogo = ESTADO_MENU
musica_ligada = True
sons_ligados = True
turno = 0
mensagem = ""

# --- Funções de inicialização ---
def inicializar_jogo():
    global jogador, inimigos, mapa, estado_jogo
    criar_mapa()
    jogador = Jogador(*encontrar_posicao_inicial())
    inimigos = gerar_inimigos(5)
    estado_jogo = ESTADO_JOGANDO
    global turno
    turno = 0

def encontrar_posicao_inicial():
    while True:
        x = random.randint(1, MAPA_LARGURA - 2)
        y = random.randint(1, MAPA_ALTURA - 2)
        if mapa[y][x] == '.':
            return x, y

def gerar_inimigos(num_inimigos):
    inimigos = []
    nomes_inimigos = ["Goblin"] * (num_inimigos // 2) + ["Orc"] * (num_inimigos - num_inimigos // 2)
    random.shuffle(nomes_inimigos)
    for nome in nomes_inimigos:
        while True:
            x = random.randint(1, MAPA_LARGURA - 2)
            y = random.randint(1, MAPA_ALTURA - 2)
            if mapa[y][x] == '.':
                inimigos.append(Inimigo(x, y, nome=nome))
                break
    return inimigos

# --- Funções de desenho ---
def desenhar_mapa():
    for y in range(MAPA_ALTURA):
        for x in range(MAPA_LARGURA):
            if mapa[y][x] == '#':
                screen.draw.rect(Rect((x * TAMANHO_CELULA, y * TAMANHO_CELULA), (TAMANHO_CELULA, TAMANHO_CELULA)), COR_PAREDE)
            elif mapa[y][x] == '.':
                screen.draw.rect(Rect((x * TAMANHO_CELULA, y * TAMANHO_CELULA), (TAMANHO_CELULA, TAMANHO_CELULA)), COR_CHAO)

def desenhar_menu():
    screen.fill((0, 0, 0))
    screen.draw.text("=== Menu Principal ===", (LARGURA // 2, ALTURA // 4), color=COR_MENU_TEXTO, fontsize=40, center=True)
    screen.draw.text("1. Começar o Jogo", (LARGURA // 2, ALTURA // 2), color=COR_MENU_TEXTO, fontsize=30, center=True)
    screen.draw.text(f"2. Música: {'Ligada' if musica_ligada else 'Desligada'}", (LARGURA // 2, ALTURA // 2 + 40),
                     color=COR_MENU_TEXTO, fontsize=30, center=True)
    screen.draw.text(f"3. Sons: {'Ligados' if sons_ligados else 'Desligados'}",
                     (LARGURA // 2, ALTURA // 2 + 80), color=COR_MENU_TEXTO, fontsize=30, center=True)
    screen.draw.text("4. Sair", (LARGURA // 2, ALTURA // 2 + 120), color=COR_MENU_TEXTO, fontsize=30, center=True)

def desenhar_mensagem():
    screen.draw.text(mensagem, (LARGURA // 2, ALTURA - 30), color=COR_MENSAGEM, fontsize=24, center=True)

def draw():
    screen.clear()
    if estado_jogo == ESTADO_MENU:
        desenhar_menu()
    elif estado_jogo == ESTADO_JOGANDO:
        desenhar_mapa()
        jogador.draw()
        for inimigo in inimigos:
            inimigo.draw()
        desenhar_mensagem()

# --- Funções de atualização ---
def atualizar_jogo():
    global jogador, inimigos, estado_jogo, turno, mensagem
    if estado_jogo != ESTADO_JOGANDO:
        return

    turno += 1
    mensagem = ""

    # Movimento dos inimigos
    for inimigo in inimigos:
        inimigo.mover(jogador.x, jogador.y)
        if inimigo.x == jogador.x and inimigo.y == jogador.y:
            mensagem = f"O {inimigo.nome} te ataca!"
            jogador.vida -= inimigo.ataque
            if jogador.vida <= 0:
                mensagem = "Você morreu!"
                estado_jogo = ESTADO_MENU
                jogador = None
                inimigos = []
                inicializar_jogo() # Reinicia o jogo
                return

    if not inimigos:
        mensagem = "Você derrotou todos os inimigos!"
        estado_jogo = ESTADO_MENU
        jogador = None
        inimigos = []
        inicializar_jogo() # Reinicia o jogo
        return

def on_key_down(key):
    global estado_jogo, musica_ligada, sons_ligados, jogador, inimigos

    if estado_jogo == ESTADO_MENU:
        if key == keys.K_1:
            inicializar_jogo()
        elif key == keys.K_2:
            musica_ligada = not musica_ligada
        elif key == keys.K_3:
            sons_ligados = not sons_ligados
        elif key == keys.K_4:
            estado_jogo = ESTADO_SAIR

    elif estado_jogo == ESTADO_JOGANDO:
        dx = 0
        dy = 0
        if key == keys.K_w:
            dy = -1
        elif key == keys.K_a:
            dx = -1
        elif key == keys.K_s:
            dy = 1
        elif key == keys.K_d:
            dx = 1
        elif key == keys.K_j:
            tentar_atacar()
            return  # Importante: Não mover após atacar

        if jogador:
            jogador.tentar_mover(dx, dy)

        atualizar_jogo() # Atualiza o jogo após o movimento do jogador

def tentar_atacar():
    global inimigos, jogador, mensagem
    direcao = input("Direção do ataque (wasd)? ")
    dx, dy = 0, 0
    if direcao.lower() == 'w':
        dy = -TAMANHO_CELULA
    elif direcao.lower() == 'a':
        dx = -TAMANHO_CELULA
    elif direcao.lower() == 's':
        dy = TAMANHO_CELULA
    elif direcao.lower() == 'd':
        dx = TAMANHO_CELULA

    alvo_x = jogador.x + dx
    alvo_y = jogador.y + dy

    for inimigo in list(inimigos):
        if inimigo.x == alvo_x and inimigo.y == alvo_y:
            mensagem = f"Você ataca o {inimigo.nome}!"
            inimigo.vida -= 1
            if inimigo.vida <= 0:
                mensagem = f"Você derrotou o {inimigo.nome}!"
                inimigos.remove(inimigo)
            return
    mensagem = "Não há nada para atacar nessa direção."

def update():
    if estado_jogo == ESTADO_JOGANDO:
        atualizar_jogo()

def main():
    pgzrun.go()

if __name__ == '__main__':
    main()
