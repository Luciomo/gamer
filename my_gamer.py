import random
import math
import time
import os  # Para limpar a tela do terminal

# --- Configurações ---
MAPA_LARGURA = 30
MAPA_ALTURA = 20

# --- Símbolos do Mapa ---
PAREDE = '#'
CHAO = '.'

# --- Cores (para terminal ANSI) ---
class cores:
    RESET = '\033[0m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    CINZA = '\033[90m'
    PRETO = '\033[30m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Estados do Jogo ---
ESTADO_MENU = 0
ESTADO_JOGANDO = 1
ESTADO_SAIR = 2

estado_jogo = ESTADO_MENU
musica_ligada = True
sons_ligados = True

# --- Mapa ---
def criar_mapa():
    mapa = [[PAREDE for _ in range(MAPA_LARGURA)] for _ in range(MAPA_ALTURA)]
    for y in range(1, MAPA_ALTURA - 1):
        for x in range(1, MAPA_LARGURA - 1):
            if random.random() < 0.7:
                mapa[y][x] = CHAO
    criar_sala(mapa, 5, 5, 8, 6)
    criar_sala(mapa, 15, 10, 5, 4)
    return mapa

def criar_sala(mapa, x, y, largura, altura):
    for i in range(y, y + altura):
        for j in range(x, x + largura):
            if 0 < i < MAPA_ALTURA - 1 and 0 < j < MAPA_LARGURA - 1:
                mapa[i][j] = CHAO

# --- Entidades ---
class Entidade:
    def __init__(self, x, y, sprites, cor=cores.BRANCO):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.sprite_index = 0
        self.cor = cor

    def get_sprite(self):
        return self.sprites[self.sprite_index]

    def next_frame(self):
        self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

class Jogador(Entidade):
    def __init__(self, x, y):
        sprites = ['@', '*']
        super().__init__(x, y, sprites, cores.AZUL)
        self.vida = 10

    def mover(self, dx, dy, mapa, inimigos):
        novo_x, novo_y = self.x + dx, self.y + dy
        if (0 <= novo_y < MAPA_ALTURA and
            0 <= novo_x < MAPA_LARGURA and
            mapa[novo_y][novo_x] == CHAO):
            for inimigo in inimigos:
                if inimigo.x == novo_x and inimigo.y == novo_y:
                    print(f"Você encontrou um {inimigo.get_sprite()}!")
                    self.vida -= inimigo.ataque
                    print(f"O {inimigo.get_sprite()} te ataca! Vida restante: {self.vida}")
                    return False
            self.x = novo_x
            self.y = novo_y
            return True
        return False

class Inimigo(Entidade):
    def __init__(self, x, y, nome="Goblin", vida=1, ataque=1):
        if nome == "Goblin":
            sprites = ['g', 'ğ']
            cor = cores.VERDE
            simbolo_inicial = 'G'
        elif nome == "Orc":
            sprites = ['o', 'õ']
            cor = cores.VERMELHO
            simbolo_inicial = 'O'
            vida = 2
            ataque = 2
        else:
            sprites = ['?', '!']
            cor = cores.MAGENTA
            simbolo_inicial = '?'
        super().__init__(x, y, sprites, cor)
        self.nome = nome
        self.vida = vida
        self.ataque = ataque

    def mover(self, mapa, jogador_x, jogador_y):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        novo_x, novo_y = self.x + dx, self.y + dy

        if (0 <= novo_y < MAPA_ALTURA and
            0 <= novo_x < MAPA_LARGURA and
            mapa[novo_y][novo_x] == CHAO and
            not (novo_x == jogador_x and novo_y == jogador_y)):
            self.x = novo_x
            self.y = novo_y

def encontrar_posicao_inicial(mapa):
    while True:
        x = random.randint(1, MAPA_LARGURA - 2)
        y = random.randint(1, MAPA_ALTURA - 2)
        if mapa[y][x] == CHAO:
            return x, y

def gerar_inimigos(mapa, num_inimigos):
    inimigos = []
    nomes_inimigos = ["Goblin"] * (num_inimigos // 2) + ["Orc"] * (num_inimigos - num_inimigos // 2)
    random.shuffle(nomes_inimigos)
    for nome in nomes_inimigos:
        while True:
            x = random.randint(1, MAPA_LARGURA - 2)
            y = random.randint(1, MAPA_ALTURA - 2)
            if mapa[y][x] == CHAO:
                inimigos.append(Inimigo(x, y, nome=nome))
                break
    return inimigos

# --- Funções de Jogo ---
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def desenhar_mapa(mapa, jogador, inimigos):
    for y in range(MAPA_ALTURA):
        linha = ""
        for x in range(MAPA_LARGURA):
            encontrou_entidade = False
            if x == jogador.x and y == jogador.y:
                linha += jogador.cor + jogador.get_sprite() + cores.RESET
                encontrou_entidade = True
            else:
                for inimigo in inimigos:
                    if x == inimigo.x and y == inimigo.y:
                        linha += inimigo.cor + inimigo.get_sprite() + cores.RESET
                        encontrou_entidade = True
                        break
            if not encontrou_entidade:
                if mapa[y][x] == PAREDE:
                    linha += cores.CINZA + PAREDE + cores.RESET
                elif mapa[y][x] == CHAO:
                    linha += CHAO
        print(linha)
    print(f"Vida do Jogador: {jogador.vida}")

def pode_mover(mapa, x, y):
    return 0 <= y < MAPA_ALTURA and 0 <= x < MAPA_LARGURA and mapa[y][x] == CHAO

def obter_entrada_jogo():
    return input("Mover (wasd), Atacar (j), Menu (m), Sair (q)? ")

def tentar_atacar(jogador, inimigos):
    direcao = input("Direção do ataque (wasd)? ")
    dx, dy = 0, 0
    if direcao.lower() == 'w':
        dy = -1
    elif direcao.lower() == 'a':
        dx = -1
    elif direcao.lower() == 's':
        dy = 1
    elif direcao.lower() == 'd':
        dx = 1

    alvo_x = jogador.x + dx
    alvo_y = jogador.y + dy

    for inimigo in inimigos:
        if inimigo.x == alvo_x and inimigo.y == alvo_y:
            print(f"Você ataca o {inimigo.nome}!")
            inimigo.vida -= 1
            if inimigo.vida <= 0:
                print(f"Você derrotou o {inimigo.nome}!")
                inimigos.remove(inimigo)
            return True
    print("Não há nada para atacar nessa direção.")
    return False

def atualizar_jogo(mapa, jogador, inimigos, entrada):
    dx, dy = 0, 0
    moved = False
    if entrada.lower() == 'w':
        dy = -1
        moved = jogador.mover(dx, dy, mapa, inimigos)
    elif entrada.lower() == 'a':
        dx = -1
        moved = jogador.mover(dx, dy, mapa, inimigos)
    elif entrada.lower() == 's':
        dy = 1
        moved = jogador.mover(dx, dy, mapa, inimigos)
    elif entrada.lower() == 'd':
        dx = 1
        moved = jogador.mover(dx, dy, mapa, inimigos)

    if moved:
        jogador.next_frame()

def mostrar_menu():
    limpar_tela()
    print(cores.BOLD + cores.AZUL + "=== Menu Principal ===" + cores.RESET)
    print(f"{cores.AMARELO}1.{cores.RESET} Começar o Jogo")
    print(f"{cores.AMARELO}2.{cores.RESET} Música: {'Ligada' if musica_ligada else 'Desligada'}")
    print(f"{cores.AMARELO}3.{cores.RESET} Sons: {'Ligados' if sons_ligados else 'Desligados'}")
    print(f"{cores.AMARELO}4.{cores.RESET} Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def lidar_com_menu(opcao):
    global estado_jogo, musica_ligada, sons_ligados
    if opcao == '1':
        estado_jogo = ESTADO_JOGANDO
        return True  # Indica que o jogo deve começar
    elif opcao == '2':
        musica_ligada = not musica_ligada
        return False
    elif opcao == '3':
        sons_ligados = not sons_ligados
        return False
    elif opcao == '4':
        estado_jogo = ESTADO_SAIR
        return True  # Indica que o jogo deve terminar
    else:
        print("Opção inválida.")
        time.sleep(1)
        return False

# --- Loop Principal do Jogo ---
if __name__ == "__main__":
    while estado_jogo != ESTADO_SAIR:
        if estado_jogo == ESTADO_MENU:
            if lidar_com_menu(mostrar_menu()):
                # Inicializa o jogo quando a opção "Começar o Jogo" é escolhida
                mapa = criar_mapa()
                jogador = Jogador(*encontrar_posicao_inicial(mapa))
                num_inimigos = 5
                inimigos = gerar_inimigos(mapa, num_inimigos)
                turno = 0
                ANIMATION_SPEED = 0.2
                last_animation_time = time.time()
        elif estado_jogo == ESTADO_JOGANDO:
            limpar_tela()
            desenhar_mapa(mapa, jogador, inimigos)
            entrada = obter_entrada_jogo()
            turno += 1

            if entrada.lower() == 'q':
                estado_jogo = ESTADO_MENU # Volta para o menu ao invés de sair direto
            elif entrada.lower() == 'm':
                estado_jogo = ESTADO_MENU
            elif entrada.lower() == 'j':
                tentar_atacar(jogador, inimigos)
            elif entrada.lower() in ['w', 'a', 's', 'd']:
                atualizar_jogo(mapa, jogador, inimigos, entrada)

            if jogador.vida > 0:
                for inimigo in inimigos:
                    inimigo.mover(mapa, jogador.x, jogador.y)
                    inimigo.next_frame()
                    if inimigo.x == jogador.x and inimigo.y == jogador.y:
                        print(f"O {inimigo.nome} te ataca!")
                        jogador.vida -= inimigo.ataque
                        print(f"Vida restante: {jogador.vida}")

            current_time = time.time()
            if current_time - last_animation_time > ANIMATION_SPEED:
                jogador.next_frame()
                for inimigo in inimigos:
                    inimigo.next_frame()
                last_animation_time = current_time

            if not inimigos:
                print("Você derrotou todos os inimigos!")
                estado_jogo = ESTADO_MENU # Volta para o menu após a vitória
                input("Pressione Enter para continuar...")

            if jogador.vida <= 0:
                limpar_tela()
                print(cores.VERMELHO + "Você morreu!" + cores.RESET)
                estado_jogo = ESTADO_MENU # Volta para o menu após a derrota
                input("Pressione Enter para continuar...")

    limpar_tela()
    print("Obrigado por jogar!")