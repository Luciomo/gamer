import random
import math

from my_gamer import encontrar_posicao_inicial

# --- Configurações ---
MAPA_LARGURA = 30
MAPA_ALTURA = 20

# --- Símbolos do Mapa ---
PAREDE = '#'
CHAO = '.'
JOGADOR = '@'
INIMIGO_GOBLIN = 'G'
INIMIGO_ORC = 'O'

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
    def __init__(self, x, y, simbolo, cor=cores.BRANCO):
        self.x = x
        self.y = y
        self.simbolo = simbolo
        self.cor = cor

class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, JOGADOR, cores.AZUL)
        self.vida = 10

class Inimigo(Entidade):
    def __init__(self, x, y, simbolo, cor, vida=1, ataque=1):
        super().__init__(x, y, simbolo, cor)
        self.vida = vida
        self.ataque = ataque

def gerar_inimigos(mapa, num_inimigos):
    inimigos = []
    for _ in range(num_inimigos):
        while True:
            x = random.randint(1, MAPA_LARGURA - 2)
            y = random.randint(1, MAPA_ALTURA - 2)
            if mapa[y][x] == CHAO:
                tipo_inimigo = random.choice([INIMIGO_GOBLIN, INIMIGO_ORC])
                cor_inimigo = cores.VERDE if tipo_inimigo == INIMIGO_GOBLIN else cores.VERMELHO
                vida_inimigo = 1 if tipo_inimigo == INIMIGO_GOBLIN else 2
                ataque_inimigo = 1 if tipo_inimigo == INIMIGO_GOBLIN else 2
                inimigos.append(Inimigo(x, y, tipo_inimigo, cor_inimigo, vida_inimigo, ataque_inimigo))
                break
    return inimigos

# --- Funções de Jogo ---
def desenhar_mapa(mapa, jogador, inimigos):
    for y in range(MAPA_ALTURA):
        linha = ""
        for x in range(MAPA_LARGURA):
            encontrou_entidade = False
            if x == jogador.x and y == jogador.y:
                linha += jogador.cor + jogador.simbolo + cores.RESET
                encontrou_entidade = True
            else:
                for inimigo in inimigos:
                    if x == inimigo.x and y == inimigo.y:
                        linha += inimigo.cor + inimigo.simbolo + cores.RESET
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

def obter_entrada():
    return input("Mover (wasd), Atacar (j), Sair (q)? ")

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
            print(f"Você ataca o {inimigo.simbolo}!")
            inimigo.vida -= 1
            if inimigo.vida <= 0:
                print(f"Você derrotou o {inimigo.simbolo}!")
                inimigos.remove(inimigo)
            return True
    print("Não há nada para atacar nessa direção.")
    return False

def atualizar_jogo(mapa, jogador, inimigos, entrada):
    novo_x, novo_y = jogador.x, jogador.y
    if entrada.lower() == 'w':
        novo_y -= 1
    elif entrada.lower() == 'a':
        novo_x -= 1
    elif entrada.lower() == 's':
        novo_y += 1
    elif entrada.lower() == 'd':
        novo_x -= 1

    if pode_mover(mapa, novo_x, novo_y):
        # Verifica se há um inimigo na nova posição
        for inimigo in inimigos:
            if inimigo.x == novo_x and inimigo.y == novo_y:
                print(f"Você encontrou um {inimigo.simbolo}!")
                # Simulação de combate simples
                jogador.vida -= inimigo.ataque
                print(f"O {inimigo.simbolo} te ataca! Vida restante: {jogador.vida}")
                return jogador.x, jogador.y # Não move se encontrar um inimigo
        return novo_x, novo_y
    else:
        return jogador.x, jogador.y

# --- Loop Principal do Jogo ---
if __name__ == "__main__":
    mapa = criar_mapa()
    jogador = Jogador(*encontrar_posicao_inicial(mapa))
    num_inimigos = 5
    inimigos = gerar_inimigos(mapa, num_inimigos)

    while jogador.vida > 0:
        desenhar_mapa(mapa, jogador, inimigos)
        entrada = obter_entrada()

        if entrada.lower() == 'q':
            break
        elif entrada.lower() == 'j':
            tentar_atacar(jogador, inimigos)
        elif entrada.lower() in ['w', 'a', 's', 'd']:
            jogador.x, jogador.y = atualizar_jogo(mapa, jogador, inimigos, entrada)

        if not inimigos:
            print("Você derrotou todos os inimigos!")
            break

    if jogador.vida <= 0:
        print(cores.VERMELHO + "Você morreu!" + cores.RESET)

    print("Fim de jogo!")