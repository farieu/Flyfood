# Projeto Interdisplicinar para Sistemas de Informação II
# Caio César Farias da Silva
# Algoritmo de Força Bruta para o Problema do Caixeiro Viajante
# Código sem comentários, e com a biblioteca time para mostrar o tempo de processamento do algoritmo.

import time 
start = time.process_time_ns()

def leitura(nome_arquivo):
    pontos = {}
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()[1:]
        for i in range(len(linhas)):
            elementos = linhas[i].split()
            for j in range(len(elementos)):
                elemento = elementos[j]
                if elemento != '0':
                    pontos[elemento] = (i, j)
    return pontos

entrada = leitura('entrada1.txt')
print(entrada)
lista_de_pontos = list(entrada.keys())
lista_de_pontos.remove('R')

def permutacao(pontos):
    if len(pontos) <= 1:
        return [pontos]
    permutacoes = []
    for indice in range(len(pontos)):
        elem_preso = pontos[indice]
        lista_solta = pontos[:indice] + pontos[indice + 1:]
        for p in permutacao(lista_solta):
            permutacoes.append([elem_preso] + p)
    return permutacoes

perms = permutacao(lista_de_pontos)

def calculo_das_distancia(coord, rotas):
    menor_custo = 10**8 
    melhor_rota = ''
    for r in rotas:
        custo = 0
        r = ['R'] + r + ['R']
        for i in range(len(r) - 1):
            x1, y1 = coord[r[i]]
            x2, y2 = coord[r[i+1]]
            custo += abs(x1 - x2) + abs(y1 - y2)
        if custo < menor_cust:
            menor_cust = custo
            melhor_rota = ''.join(r)
    return f'O menor trajeto foi {melhor_rota}, custando {menor_custo} dronometros.'

print(calculo_das_distancia(entrada, perms))
end = time.process_time_ns()
tempo = (end - start)
print(f"O tempo em nanossegundos foi: {tempo}")