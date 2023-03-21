# Projeto Interdisplicinar para Sistemas de Informação II
# Caio César Farias da Silva
# Algoritmo Genético para o Problema do Caixeiro Viajante
# Código sem comentários, e com a biblioteca time para mostrar o tempo de processamento do algoritmo. 

import tsplib95 as tspfile
import random
import time
start = time.process_time_ns()

'Numero de Gerações = 100 gerações.'
'População Inicial = 20 indivíduos'
'Seleção por Torneio'
'Taxa de Crossover = 0.8 (ou 80%)'
'Taxa de Mutação = 0.05 (ou 5%)'
'Substituição Geracional com e sem Elitismo.'
'Para ativar o elitismo, utilizar True no parametro elitismo= em def evoluir_populcao'

'Leitura do Arquivo de Entrada .tsp'
def leitura_arquivo(nome_arquivo):
    tsp = tspfile.load(nome_arquivo)
    coordenadas = []
    for i in range(1, tsp.dimension + 1):  
        coord = tsp.node_coords[i]
        coordenadas.append(tuple(coord))
    cidades = {}
    for i, coord in enumerate(coordenadas):
        info_cidades = tuple(coord) 
        cidades[str(i)] = info_cidades 
    return cidades 

'Para o AG funcionar, primeiro geramos uma única vez a população inicial, de 20 indivíduos.'
def pop_inicial(pontos, populacao_inicial=20):
    populacao = []
    n = len(pontos)
    for _ in range(populacao_inicial):
        shuffle = random.sample(pontos, n)
        populacao.append(shuffle) 
    return populacao 

'Calculando a aptidão dos indivíduos, quanto menor, melhor.'
def aptidao_individuo(cidades, populacao):
    aptidoes = []
    for rota in populacao:
        custo_rota = 0
        for i in range(len(rota) - 1):
            cidade_atual = rota[i]
            cidade_destino = rota[i+1]
            x1, y1 = cidades[cidade_atual]
            x2, y2 = cidades[cidade_destino]
            custo_rota += ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        x1, y1 = cidades[rota[-1]]
        x2, y2 = cidades[rota[0]]
        custo_rota += ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        aptidoes.append(custo_rota)
    return aptidoes

'Seleção aleatória de indivíduos para o cruzamento.'
def selecao_torneio(populacao, dicionario_cidades):
    pais_selecionados = []
    while len(pais_selecionados) < 2:
        pai1, pai2 = random.sample(populacao, 2)
        aptidao_pai1 = aptidao_individuo(dicionario_cidades, pai1)
        aptidao_pai2 = aptidao_individuo(dicionario_cidades, pai2)
        if aptidao_pai1 < aptidao_pai2:
            pais_selecionados.append(pai1)
        else:
            pais_selecionados.append(pai2)
    return pais_selecionados

'Cruzamento PMX com os vencedores do Torneio'
def crossoverpmx(pai1, pai2):
    if random.random() > 0.8:
        return [pai1, pai2]
    ponto_corte = random.randint(1, len(pai1) - 1)
    filho1 = [0] * len(pai1)
    filho2 = [0] * len(pai1)
    for i in range(ponto_corte):
        filho1[i] = pai1[i]
        filho2[i] = pai2[i]
    for i in range(ponto_corte, len(pai1)):
        if pai2[i] not in filho1:
            filho1[i] = pai2[i]
        else:
            index = pai1.index(pai2[i])
            while pai1[index] in filho1:
                index = pai1.index(pai2[index])
            filho1[i] = pai1[index]
        if pai1[i] not in filho2:
            filho2[i] = pai1[i]
        else:
            index = pai2.index(pai1[i])
            while pai2[index] in filho2:
                index = pai2.index(pai1[index])
            filho2[i] = pai2[index]
    return [filho1, filho2]

'Taxa de Mutação dos indivíduos.'
def mutation(rota):
    if random.random() < 0.05:
        index1 = random.randint(0, len(rota) - 1)
        index2 = index1
        while index2 == index1:
            index2 = random.randint(0, len(rota) - 1)
        rota[index1], rota[index2] = rota[index2], rota[index1]
    return rota

'Substituição Geracional com e sem Elitismo.'
def evoluir_populacao(population, dicionario_cidades, elitismo=True):
    nova_populacao = []
    num_replace = len(population) - int(elitismo) #20 ou 19 dependendo do Elitismo (0 ou 1) - substituições
    for _ in range(num_replace // 2):
        pais = selecao_torneio(population, dicionario_cidades)
        offspring = crossoverpmx(pais[0], pais[1])
        offspring = [mutation(individuo) for individuo in offspring]
        nova_populacao.extend(offspring)
    nova_populacao.sort(key=lambda x: aptidao_individuo(dicionario_cidades, [x])[0])
    if elitismo:
        num_elites = int(elitismo)
        elites = sorted(population, key=lambda x: aptidao_individuo(dicionario_cidades, [x])[0])[:num_elites]
        nova_populacao[-num_elites:] = elites
    else:
        nova_populacao.extend(random.sample(population, num_replace // 2))
    return nova_populacao

'Código que chama as demais funções e define o critério de parada.'
def ag(dicionario_cidades, num_geracoes=100, tamanho_populacao=20):
    populacao = pop_inicial(list(dicionario_cidades.keys()), tamanho_populacao)
    for _ in range(num_geracoes):
        populacao = evoluir_populacao(populacao, dicionario_cidades, elitismo=tamanho_populacao // 2)
    melhor_individuo = min(populacao, key=lambda x: aptidao_individuo(dicionario_cidades, [x])[0])
    melhor_custo = aptidao_individuo(dicionario_cidades, [melhor_individuo])[0]
    return melhor_individuo, melhor_custo

entrada = leitura_arquivo("wi29.tsp")
melhor_rota, melhor_custo = ag(entrada)
end = time.process_time_ns()
tempo = (end - start)
print(f"O menor trajeto foi {melhor_rota}, custando {melhor_custo} dronometros.")
print(f"O tempo em nanossegundos foi de: {tempo}.")