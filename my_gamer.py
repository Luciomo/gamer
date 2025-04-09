import random
import math

# --- Configurações ---
MAPA_LARGURA = 30
MAPA_ALTURA = 20

# --- Símbolos do Mapa ---
PAREDE = '#'
CHAO = '.'
JOGADOR = '@'

# --- Cores (para terminal ANSI - pode não funcionar em todos os terminais) ---
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

# --- Jogador ---
def encontrar_posicao_inicial(mapa):
    while True:
        x = random.randint(1, MAPA_LARGURA - 2)
        y = random.randint(1, MAPA_ALTURA - 2)
        if mapa[y][x] == CHAO:
            return x, y

# --- Funções de Jogo ---
def desenhar_mapa(mapa, jogador_x, jogador_y):
    for y in range(MAPA_ALTURA):
        linha = ""
        for x in range(MAPA_LARGURA):
            if x == jogador_x and y == jogador_y:
                linha += cores.AZUL + JOGADOR + cores.RESET
            elif mapa[y][x] == PAREDE:
                linha += cores.CINZA + PAREDE + cores.RESET
            elif mapa[y][x] == CHAO:
                linha += CHAO
        print(linha)

def pode_mover(mapa, x, y):
    return 0 <= y < MAPA_ALTURA and 0 <= x < MAPA_LARGURA and mapa[y][x] == CHAO

def obter_entrada():
    return input("Mover (wasd)? ")

def atualizar_jogo(mapa, jogador_x, jogador_y, entrada):
    novo_x, novo_y = jogador_x, jogador_y
    if entrada.lower() == 'w':
        novo_y -= 1
    elif entrada.lower() == 'a':
        novo_x -= 1
    elif entrada.lower() == 's':
        novo_y += 1
    elif entrada.lower() == 'd':
        novo_x += 1

    if pode_mover(mapa, novo_x, novo_y):
        return novo_x, novo_y
    else:
        return jogador_x, jogador_y

# --- Loop Principal do Jogo ---
if __name__ == "__main__":
    mapa = criar_mapa()
    jogador_x, jogador_y = encontrar_posicao_inicial(mapa)

    while True:
        desenhar_mapa(mapa, jogador_x, jogador_y)
        entrada = obter_entrada()
        jogador_x, jogador_y = atualizar_jogo(mapa, jogador_x, jogador_y, entrada)

        if entrada.lower() == 'q': # Adiciona uma opção para sair
            break

    print("Fim de jogo!")