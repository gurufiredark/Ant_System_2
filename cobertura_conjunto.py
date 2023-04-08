import random
import time

# Define o tamanho do problema
NUM_ELEMENTOS = 100
NUM_CONJUNTOS = 20
TAM_CONJUNTOS = 10

# Gera aleatoriamente os conjuntos
conjuntos = [set(random.sample(range(NUM_ELEMENTOS), TAM_CONJUNTOS)) for _ in range(NUM_CONJUNTOS)]

# Define os parâmetros do algoritmo Ant System
NUM_FORMIGAS = 50
NUM_ITERACOES = 100
PHEROMONE_INIT = 1.0
PHEROMONE_DECAY = 0.1
PHEROMONE_MIN = 0.01
ALPHA = 1.0
BETA = 2.0

# Inicializa as trilhas de feromônio
trilhas = [[PHEROMONE_INIT] * NUM_CONJUNTOS for _ in range(NUM_ELEMENTOS)]

# Define a função de avaliação
def avaliacao(sol):
    elementos_cobertos = set()
    for i, incluido in enumerate(sol):
        if incluido:
            elementos_cobertos |= conjuntos[i]
    return len(elementos_cobertos)

# Executa o algoritmo Ant System
start_time = time.time()
for it in range(NUM_ITERACOES):
    # Inicializa as soluções das formigas
    sol_formigas = [[False] * NUM_CONJUNTOS for _ in range(NUM_FORMIGAS)]
    for i in range(NUM_FORMIGAS):
        # Constrói a solução da formiga
        for j in range(NUM_CONJUNTOS):
            if random.random() < trilhas[i][j]:
                sol_formigas[i][j] = True
        # Avalia a solução da formiga
        fit_formiga = avaliacao(sol_formigas[i])
        # Atualiza as trilhas de feromônio
        for j, incluido in enumerate(sol_formigas[i]):
            if incluido:
                for k in conjuntos[j]:
                    trilhas[k][j] = max(trilhas[k][j], PHEROMONE_MIN)
                    trilhas[k][j] += (PHEROMONE_INIT - trilhas[k][j]) * ALPHA / fit_formiga
    # Atualiza as trilhas de feromônio globalmente
    for i in range(NUM_ELEMENTOS):
        for j in range(NUM_CONJUNTOS):
            trilhas[i][j] *= 1.0 - PHEROMONE_DECAY
            trilhas[i][j] = max(trilhas[i][j], PHEROMONE_MIN)
    # Seleciona a melhor solução encontrada até o momento
    melhor_sol = None
    melhor_fit = 0
    for sol in sol_formigas:
        fit = avaliacao(sol)
        if fit > melhor_fit:
            melhor_sol = sol
            melhor_fit = fit
end_time = time.time()
# Imprime a melhor solução encontrada
print('melhor solucao = ',melhor_sol)
print('melhor fit = ', melhor_fit)
print('tempo exec = ', end_time - start_time,'s')